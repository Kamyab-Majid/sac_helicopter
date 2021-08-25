# low level control of small scaled helicopter using soft actor critic method
In this reposityory, a soft actor critic method is applied to control a small scaled helicopter. 
First it is necessary to install gym-helicopter package in gym using pip install gym-helicopter.
In order to run the SAC algorithm: 
- First the optuna package is used to optimize the hyperparameters  (optuna_sac_helicopter.py)
- Then sac_helicopter.py is used to start the RL process
- The resume_sac_heli.py can be used in case of a pause during the process.
- use try_garage_policy.py to test the obtained policy.