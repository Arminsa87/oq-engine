Introduction
=======================================

This manual is for advanced users, i.e.  people that already know how
to use the engine.  If you have just started and the only thing you
have tried to run are the OpenQuake demos, this manual is NOT for
you. Beginners should study the `official manual
<https://www.globalquakemodel.org/single-post/OpenQuake-Engine-Manual>`_
first. This manual is for users running *large* calculations and having
troubles.

For the purposes of this manual a calculation is large if it cannot be run,
i.e. if it runs out of memory, it fails with strange errors (rabbitmq
errors, pickling errors, ...) or it just takes too long to complete.

There are various reasons why a calculation can be too large. 90% of the
times it is because the user is making some mistakes and she is trying to
run a calculation larger than she really needs. In the remaining 10% of the
times the calculation is genuinely large and the solution is to
buy a larger machine, or to ask the OpenQuake developers to optimize the
engine for the specific calculation that is giving issues.

The first things to do when you have a large calculation is to
run the command ``oq info --report job.ini``, that will tell you essential
information to estimate the size of the full calculation, in
particular the number of hazard sites, the number of ruptures, the
number of assets and the most relevant parameters you are using. If
generating the report is slow, it means that there is something wrong
with your calculation and you will never be able to run it completely
unless you reduce it.

The single most important parameter in the report is the
*number of effective ruptures*, i.e. the number of ruptures after
distance and magnitude filtering. For instance your report could
contains numbers like the following ones::

#eff_ruptures 239,556  
#tot_ruptures 8,454,592

This is an example of a computation which is potentially large - there
are over 8 millions of ruptures in the model - but that in practice will be
very fast, since 97% of the ruptures will be filtered away. The report gives a
conservative estimate, in reality even more ruptures will be discarded.

It is very common to have an unhappy combinations of parameters
in the ``job.ini`` file, like discretization parameters that are too small.
Then your source model with contains millions and millions of ruptures
and the computation will become impossibly slow or it will run out of memory.
By playing with the parameters and producing various reports, one can get
an idea of how much a calculation can be reduced even before running it.

Not it is a good time to read the section about `common mistakes`_.


.. _common mistakes: common-mistakes.html
