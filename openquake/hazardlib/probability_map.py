#  -*- coding: utf-8 -*-
#  vim: tabstop=4 shiftwidth=4 softtabstop=4

#  Copyright (c) 2016, GEM Foundation

#  OpenQuake is free software: you can redistribute it and/or modify it
#  under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  OpenQuake is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.
from openquake.baselib.python3compat import zip
from openquake.hazardlib.stats import mean_quantiles
import numpy

F32 = numpy.float32


class ProbabilityCurve(object):
    """
    This class is a small wrapper over an array of PoEs associated to
    a set of intensity measure types and levels. It provides a few operators,
    including the complement operator `~`

    ~p = 1 - p

    and the inclusive or operator `|`

    p = p1 | p2 = ~(~p1 * ~p2)

    Such operators are implemented efficiently at the numpy level, by
    dispatching on the underlying array.

    Here is an example of use:

    >>> poe = ProbabilityCurve(numpy.array([0.1, 0.2, 0.3, 0, 0]))
    >>> ~(poe | poe) * .5
    <ProbabilityCurve
    [ 0.405  0.32   0.245  0.5    0.5  ]>
    """
    def __init__(self, array):
        self.array = array

    def __or__(self, other):
        if other == 0:
            return self
        else:
            return self.__class__(1. - (1. - self.array) * (1. - other.array))
    __ror__ = __or__

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.array * other.array)
        elif other == 1:
            return self
        else:
            return self.__class__(self.array * other)
    __rmul__ = __mul__

    def __invert__(self):
        return self.__class__(1. - self.array)

    def __nonzero__(self):
        return bool(self.array.any())

    def __repr__(self):
        return '<ProbabilityCurve\n%s>' % self.array


class ProbabilityMap(dict):
    """
    A dictionary site_id -> ProbabilityCurve. It defines the complement
    operator `~`, performing the complement on each curve

    ~p = 1 - p

    and the "inclusive or" operator `|`:

    m = m1 | m2 = {sid: m1[sid] | m2[sid] for sid in all_sids}

    Such operators are implemented efficiently at the numpy level, by
    dispatching on the underlying array. Moreover there is a classmethod
    .build(num_levels, num_gsims, sids, initvalue) to build initialized
    instances of ProbabilityMap.
    """
    @classmethod
    def build(cls, num_levels, num_gsims, sids, initvalue=0.):
        """
        :param num_levels: the total number of intensity measure levels
        :param num_gsims: the number of GSIMs
        :param sids: a set of site indices
        :param initvalue: the initial value of the probability (default 0)
        :returns: a ProbabilityMap dictionary
        """
        dic = cls()
        for sid in sids:
            array = numpy.empty((num_levels, num_gsims), F32)
            array.fill(initvalue)
            dic[sid] = ProbabilityCurve(array)
        return dic

    @property
    def sids(self):
        """The ordered keys of the map as a float32 array"""
        return numpy.array(sorted(self), numpy.uint32)

    @property
    def array(self):
        """
        The underlying array of shape (N, L, I)
        """
        return numpy.array([self[sid].array for sid in self.sids])

    def convert(self, imtls, nsites, idx=0):
        """
        Convert a probability map into a composite array of length `nsites`
        and dtype `imtls.imt_dt`.

        :param imtls: DictArray instance
        :param nsites: the total number of sites
        :param idx: extract the data corresponding to the given inner index
        """
        curves = numpy.zeros(nsites, imtls.imt_dt)
        for sid in self:
            for imt in imtls:
                curves[imt][sid] = self[sid].array[imtls.slicedic[imt], idx]
                # NB: curves[sid][imt] does not work on h5py 2.2
        return curves

    def filter(self, sids):
        """
        Extracs a submap of self for the given sids.
        """
        dic = self.__class__()
        for sid in sids:
            try:
                dic[sid] = self[sid]
            except KeyError:
                pass
        return dic

    def extract(self, gsim_idx):
        """
        Extracts a component of the underlying ProbabilityCurves,
        specified by the index `gsim_idx`.
        """
        out = self.__class__()
        for sid in self:
            curve = self[sid]
            array = curve.array[:, gsim_idx].reshape(-1, 1)
            out[sid] = ProbabilityCurve(array)
        return out

    def __ior__(self, other):
        self_sids = set(self)
        other_sids = set(other)
        for sid in self_sids & other_sids:
            self[sid] = self[sid] | other[sid]
        for sid in other_sids - self_sids:
            self[sid] = other[sid]
        return self

    def __or__(self, other):
        new = self.__class__(self)
        new |= other
        return new

    __ror__ = __or__

    def __mul__(self, other):
        sids = set(self) | set(other)
        return self.__class__((sid, self.get(sid, 1) * other.get(sid, 1))
                              for sid in sids)

    def __invert__(self):
        new = self.__class__()
        for sid in self:
            if (self[sid].array != 1.).any():
                new[sid] = ~self[sid]  # store only nonzero probabilities
        return new

    def __toh5__(self):
        # converts to an array of shape (num_sids, num_levels, num_gsims)
        size = len(self)
        sids = self.sids
        if size:
            shape = (size,) + self[sids[0]].array.shape
            array = numpy.zeros(shape)
            for i, sid in numpy.ndenumerate(sids):
                array[i] = self[sid].array
        else:
            array = numpy.zeros(0)
        return array, dict(sids=sids)

    def __fromh5__(self, array, attrs):
        # rebuild the map from sids and probs arrays
        for sid, prob in zip(attrs['sids'], array):
            self[sid] = ProbabilityCurve(prob)


def get_zero_pcurve(pmaps):
    """
    Return the zero ProbabilityCurve from a set of homogenous ProbabilityMaps
    """
    for pmap in pmaps:
        if pmap:
            sid = next(iter(pmap))
            break
    zero = numpy.zeros_like(pmap[sid].array)
    return ProbabilityCurve(zero)


class PmapStats(object):
    """
    A class to perform statistics on ProbabilityMaps.

    :param weights: a list of weights
    :param quantiles: a list of floats in the range 0..1

    Here is an example:

    >>> pm1 = ProbabilityMap.build(num_levels=3, num_gsims=1, sids=[0, 1],
    ...                            initvalue=1.0)
    >>> pm2 = ProbabilityMap.build(num_levels=3, num_gsims=1, sids=[0],
    ...                            initvalue=0.8)
    >>> PmapStats().mean_quantiles(sids=[0, 1], pmaps=[pm1, pm2])
    {0: <ProbabilityCurve
    [[ 0.9]
     [ 0.9]
     [ 0.9]]>, 1: <ProbabilityCurve
    [[ 0.5]
     [ 0.5]
     [ 0.5]]>}
    """
    def __init__(self, weights=None, quantiles=()):
        self.weights = weights
        self.quantiles = quantiles

    # the tests are in the engine
    def mean_quantiles(self, sids, pmaps):
        """
        :params sids: array of N site IDs
        :param pmaps: array of R simple ProbabilityMaps
        :returns: a ProbabilityMap with arrays of size (num_levels, num_stats)
        """
        if len(pmaps) == 0:
            raise ValueError('No probability maps!')
        elif len(pmaps) == 1:  # the mean is the only pmap
            assert not self.quantiles, self.quantiles
            return pmaps[0]
        zero = get_zero_pcurve(pmaps)
        nstats = len(self.quantiles) + 1
        stats = ProbabilityMap.build(len(zero.array), nstats, sids)
        for sid in sids:
            # the arrays in the entering ProbabilityMaps have shape
            # (L, 1), where L is the number of IMT levels
            data = [pmap.get(sid, zero).array for pmap in pmaps]
            mq = mean_quantiles(data, self.quantiles, self.weights)
            for i, array in enumerate(mq):
                stats[sid].array[:, i] = array[:, 0]
        return stats
