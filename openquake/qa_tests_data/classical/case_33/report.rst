Etna No Topo
============

============== ===================
checksum32     380,532,669        
date           2019-05-10T05:07:58
engine_version 3.5.0-gitbaeb4c1e35
============== ===================

num_sites = 1, num_levels = 28, num_rlzs = 1

Parameters
----------
=============================== =================
calculation_mode                'preclassical'   
number_of_logic_tree_samples    0                
maximum_distance                {'default': 50.0}
investigation_time              50.0             
ses_per_logic_tree_path         1                
truncation_level                3.0              
rupture_mesh_spacing            1.0              
complex_fault_mesh_spacing      1.0              
width_of_mfd_bin                0.1              
area_source_discretization      1.0              
ground_motion_correlation_model None             
minimum_intensity               {}               
random_seed                     23               
master_seed                     0                
ses_seed                        42               
=============================== =================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gmpe_logic_tree.xml <gmpe_logic_tree.xml>`_                
job_ini                 `job.ini <job.ini>`_                                        
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
========= ======= =============== ================
smlt_path weight  gsim_logic_tree num_realizations
========= ======= =============== ================
b1        1.00000 trivial(1)      1               
========= ======= =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ======================= ========== ========== ==========
grp_id gsims                   distances  siteparams ruptparams
====== ======================= ========== ========== ==========
0      '[TusaLanger2016Rhypo]' rhypo rrup vs30       mag       
====== ======================= ========== ========== ==========

Realizations per (GRP, GSIM)
----------------------------

::

  <RlzsAssoc(size=1, rlzs=1)
  0,'[TusaLanger2016Rhypo]': [0]>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ======== ============ ============
source_model     grp_id trt      eff_ruptures tot_ruptures
================ ====== ======== ============ ============
source_model.xml 0      Volcanic 150          150         
================ ====== ======== ============ ============

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========= ======
grp_id source_id code gidx1 gidx2 num_ruptures calc_time num_sites weight
====== ========= ==== ===== ===== ============ ========= ========= ======
0      SVF       S    0     2     150          0.00599   1.00000   150   
====== ========= ==== ===== ===== ============ ========= ========= ======

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
S    0.00599   1     
==== ========= ======

Information about the tasks
---------------------------
================== ======= ====== ======= ======= =======
operation-duration mean    stddev min     max     outputs
read_source_models 0.00549 NaN    0.00549 0.00549 1      
preclassical       0.00648 NaN    0.00648 0.00648 1      
================== ======= ====== ======= ======= =======

Data transfer
-------------
================== ===================================================== ========
task               sent                                                  received
read_source_models converter=313 B fnames=107 B                          1.76 KB 
preclassical       srcs=1.39 KB params=680 B srcfilter=219 B gsims=162 B 343 B   
================== ===================================================== ========

Slowest operations
------------------
======================== ========= ========= ======
operation                time_sec  memory_mb counts
======================== ========= ========= ======
total preclassical       0.00648   0.0       1     
total read_source_models 0.00549   0.0       1     
managing sources         0.00361   0.0       1     
store source_info        0.00224   0.0       1     
aggregate curves         1.445E-04 0.0       1     
======================== ========= ========= ======