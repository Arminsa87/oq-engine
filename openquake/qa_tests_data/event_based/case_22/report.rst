Test case for the SplitSigma modified GMPE
==========================================

============== ===================
checksum32     3,396,916,014      
date           2019-05-16T13:37:03
engine_version 3.5.0-gite43b9c0a1f
============== ===================

num_sites = 624, num_levels = 40, num_rlzs = ?

Parameters
----------
=============================== ==================
calculation_mode                'event_based'     
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              50.0              
ses_per_logic_tree_path         3                 
truncation_level                3.0               
rupture_mesh_spacing            2.0               
complex_fault_mesh_spacing      2.0               
width_of_mfd_bin                0.2               
area_source_discretization      10.0              
ground_motion_correlation_model None              
minimum_intensity               {}                
random_seed                     23                
master_seed                     0                 
ses_seed                        24                
=============================== ==================

Input files
-----------
======================= ========================
Name                    File                    
======================= ========================
gsim_logic_tree         `gmmLt.xml <gmmLt.xml>`_
job_ini                 `job.ini <job.ini>`_    
source_model_logic_tree `ssmLt.xml <ssmLt.xml>`_
======================= ========================

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========= ======
grp_id source_id code gidx1 gidx2 num_ruptures calc_time num_sites weight
====== ========= ==== ===== ===== ============ ========= ========= ======
0      1         A    0     4     416          0.0       0.0       0.0   
====== ========= ==== ===== ===== ============ ========= ========= ======

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
A    0.0       1     
==== ========= ======

Information about the tasks
---------------------------
================== ======= ====== ======= ======= =======
operation-duration mean    stddev min     max     outputs
read_source_models 0.01135 NaN    0.01135 0.01135 1      
================== ======= ====== ======= ======= =======

Data transfer
-------------
================== =========================== ========
task               sent                        received
read_source_models converter=313 B fnames=79 B 2.29 KB 
================== =========================== ========

Slowest operations
------------------
======================== ======== ========= ======
operation                time_sec memory_mb counts
======================== ======== ========= ======
total read_source_models 0.01135  0.48438   1     
======================== ======== ========= ======