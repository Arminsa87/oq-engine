# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2015-2019 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.
import numpy
from numpy.testing import assert_almost_equal as aae

from openquake.qa_tests_data.scenario import (
    case_1, case_2, case_3, case_4, case_5, case_6, case_7, case_8,
    case_9, case_10)
from openquake.calculators.tests import CalculatorTestCase


def count_close(gmf_value, gmvs_site_one, gmvs_site_two, delta=0.1):
    """
    Count the number of pairs of gmf values
    within the specified range.
    See https://bugs.launchpad.net/openquake/+bug/1097646
    attached Scenario Hazard script.
    """
    lower_bound = gmf_value - delta / 2.
    upper_bound = gmf_value + delta / 2.
    return sum((lower_bound <= v1 <= upper_bound) and
               (lower_bound <= v2 <= upper_bound)
               for v1, v2 in zip(gmvs_site_one, gmvs_site_two))


class ScenarioTestCase(CalculatorTestCase):

    def frequencies(self, case, fst_value, snd_value):
        gmfa = self.execute(case.__file__, 'job.ini')
        gmvs0 = gmfa[0, :, 0]
        gmvs1 = gmfa[1, :, 0]
        realizations = float(self.calc.oqparam.number_of_ground_motion_fields)
        gmvs_within_range_fst = count_close(fst_value, gmvs0, gmvs1)
        gmvs_within_range_snd = count_close(snd_value, gmvs0, gmvs1)
        return (gmvs_within_range_fst / realizations,
                gmvs_within_range_snd / realizations)

    def medians(self, case):
        gmfa = self.execute(case.__file__, 'job.ini')
        median = {imt: [] for imt in self.calc.oqparam.imtls}
        for imti, imt in enumerate(self.calc.oqparam.imtls):
            for sid in self.calc.sitecol.sids:
                gmvs = gmfa[sid, :, imti]
                median[imt].append(numpy.median(gmvs))
        return median

    def test_case_1bis(self):
        # 2 out of 3 sites were filtered out
        out = self.run_calc(case_1.__file__, 'job.ini',
                            maximum_distance='5.0', exports='csv')
        self.assertEqualFiles(
            'BooreAtkinson2008_gmf.csv', out['gmf_data', 'csv'][0])

    def test_case_2(self):
        medians = self.medians(case_2)['PGA']
        aae(medians, [0.37412136, 0.19021782, 0.1365383], decimal=2)

    def test_case_3(self):
        medians_dict = self.medians(case_3)
        medians_pga = medians_dict['PGA']
        medians_sa = medians_dict['SA(0.1)']
        aae(medians_pga, [0.48155582, 0.21123045, 0.14484586], decimal=2)
        aae(medians_sa, [0.93913177, 0.40880148, 0.2692668], decimal=2)

    def test_case_4(self):
        medians = self.medians(case_4)['PGA']
        aae(medians, [0.41615372, 0.22797466, 0.1936226], decimal=2)

    def test_case_5(self):
        f1, f2 = self.frequencies(case_5, 0.5, 1.0)
        self.assertAlmostEqual(f1, 0.03, places=2)
        self.assertAlmostEqual(f2, 0.003, places=3)

    def test_case_6(self):
        f1, f2 = self.frequencies(case_6, 0.5, 1.0)
        self.assertAlmostEqual(f1, 0.05, places=2)
        self.assertAlmostEqual(f2, 0.006, places=3)

    def test_case_7(self):
        f1, f2 = self.frequencies(case_7, 0.5, 1.0)
        self.assertAlmostEqual(f1, 0.02, places=2)
        self.assertAlmostEqual(f2, 0.002, places=3)

    def test_case_8(self):
        # test for a GMPE requiring hypocentral depth, since it was
        # broken: https://bugs.launchpad.net/oq-engine/+bug/1334524
        # I am not really checking anything, only that it runs
        f1, f2 = self.frequencies(case_8, 0.5, 1.0)
        self.assertAlmostEqual(f1, 0)
        self.assertAlmostEqual(f2, 0)

    def test_case_9(self):
        # test for minimum_distance
        out = self.run_calc(case_9.__file__, 'job.ini', exports='csv,npz')
        f = out['gmf_data', 'csv'][0]
        self.assertEqualFiles('gmf.csv', f)

        # test the .npz export
        [fname] = out['gmf_data', 'npz']
        with numpy.load(fname) as f:
            self.assertEqual(len(f.keys()), 2)  # rlz-000 rlz-001
            data1 = f['rlz-000']
            data2 = f['rlz-001']
            self.assertEqual(data1.dtype.names, ('lon', 'lat', 'PGA'))
            self.assertEqual(data1.shape, (3,))
            self.assertEqual(data1['PGA'].shape, (3, 10))
            self.assertEqual(data1.dtype.names, data2.dtype.names)
            self.assertEqual(data1.shape, data2.shape)

    def test_case_10(self):
        # test importing an exposure with automatic gridding
        self.run_calc(case_10.__file__, 'job.ini')
        self.assertEqual(len(self.calc.datastore['sitecol']), 66)
