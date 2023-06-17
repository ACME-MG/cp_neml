"""
MAIN
"""
# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

NUM_THREADS = 6
GRAINS_FILE = "input_grainsfile.csv"
PATH_NEML   = '/home/omux/moose/neml'

import sys
sys.path.append(PATH_NEML)

# Import libaries
from _modules.cpmodels import cpmodel_fcc_voce
import time, os, sys
import numpy as np
import matplotlib.pyplot as plt

from neml.math import rotations, tensors, nemlmath
from neml import elasticity, drivers

# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# USER FUNCTIONS
# -----------------------------------------------------------------------------------
# Check if a process is running
def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# FOLDER/FILE MANAGMENT
# -----------------------------------------------------------------------------------
print('------------------------------------')
print('./> FOLDER/FILE MANAGMENT')
print('------------------------------------')
# Input/Output folders
FOLDER_RUNSIM = 'INL617/TEST1'
FOLDER_INPUT  = FOLDER_RUNSIM + '/_input'
FOLDER_OUTPUT = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
print('------------------------------------')
print('FOLDER_RUNSIM  =', FOLDER_RUNSIM)
print('FOLDER_INPUT   =', FOLDER_INPUT)
print('FOLDER_OUTPUT  =', FOLDER_OUTPUT)
print('------------------------------------')
# Create paths
PATH_HOME    = os.getcwd() + '/simulations/'
PATH_INPUT   = PATH_HOME + FOLDER_RUNSIM + '/_input/'
PATH_OUTPUT  = PATH_HOME + FOLDER_RUNSIM + '/' + FOLDER_OUTPUT
print('------------------------------------')
print('PATH_HOME   =', PATH_HOME)
print('PATH_INPUT  =', PATH_INPUT)
print('PATH_OUTPUT =', PATH_OUTPUT)
print('------------------------------------')
# -----------------------------------------------------------------------------------
# Create an output folder
os.system('mkdir -p ' + PATH_OUTPUT)
# Copy input files into the simulation folder
os.system('cp ' + PATH_INPUT + '/* ' + PATH_OUTPUT)
# Go the output folder
os.chdir(PATH_OUTPUT)

# %% --------------------------------------------------------------------------------
# LOADING CONDITIONS
# -----------------------------------------------------------------------------------
print('------------------------------------')
print('./> LOADING CONDITIONS')
print('------------------------------------')
EMAX   = 0.10 # Maximum strain
NSTEPS = 100 # Number of steps
ERATE  = 1.0e-4 # Strain rate
# -----------------------------------------------------------------------------------
# MATERIAL PARAMETERS
# -----------------------------------------------------------------------------------
print('------------------------------------')
print('./> MATERIAL PARAMETERS')
print('------------------------------------')
YOUNGS      = 211000    # IsotropicLinearElasticModel
POISSONS    = 0.30      # IsotropicLinearElasticModel
SHEAR       = 81000.0   # E / (2 * (1 + nu)) # Shear modulus
# Asaro Inelasticity
VSH_TAU_SAT = 100     # VoceSlipHardening
VSH_B       = 5  # VoceSlipHardening
VSH_TAU_0   = 50     # VoceSlipHardening
AI_GAMMA0   = 0.001  # PowerLawSlipRule
AI_N        = 1     # PowerLawSlipRule
# Lattice & Slip Systems
LATTICE_A   = 1.0
SLIP_DIRECTION = [1, 1, 0]
SLIP_PLANE     = [1, 1, 1]
# -----------------------------------------------------------------------------------
# GRAIN ORIENTATIONS
# -----------------------------------------------------------------------------------
print('------------------------------------')
print('./> READING GRAIN ORIENTATIONS')
print('------------------------------------')
# Options for the angle units are "radians" or "degrees"
# Options for the angle convention are "bunge", "kocks", and "roe"
EULER_ANGLES_IN    = np.loadtxt('input_grainsfile.csv', delimiter=',')
GRAIN_ORIENTATIONS = [rotations.CrystalOrientation(a[0], a[1], a[2],
                                                   angle_type="degrees", convention="bunge") for a in EULER_ANGLES_IN]
print('NUMBER OF GRAINS =', len(GRAIN_ORIENTATIONS))

# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# RUN SIMULATIONS
# -----------------------------------------------------------------------------------
print('------------------------------------')
print('./> RUNNING SIMULATION 1')
print('------------------------------------')
start_time = time.time()  # simulation start time
cpmodel = cpmodel_fcc_voce(PATH_NEML, YOUNGS, POISSONS, LATTICE_A, SLIP_DIRECTION, SLIP_PLANE,
                           VSH_TAU_SAT, VSH_B, VSH_TAU_0, AI_GAMMA0, AI_N,
                           GRAIN_ORIENTATIONS, NUM_THREADS)
result1 = drivers.uniaxial_test(cpmodel, ERATE, emax=EMAX, nsteps=NSTEPS)
print(result1.keys())
# Save results into a csv file with column names
np.savetxt('output_result1_ccsurve.csv', np.column_stack(
    (result1['strain'], result1['stress'], result1['energy_density'],
     result1['plastic_work'])), delimiter=',', 
     header='strain, stress, energy_density, plastic_work')

print('--------------------------------------')
print('./> CHECK IF THE SIMULATION IS RUNNING')
print('--------------------------------------')

job_name = 'python3' # job name
time.sleep(5) # wait for 5 seconds

while is_process_running(job_name):
    elapsed_time = time.time() - start_time
    print(f"\r\033[92mTHE SIMULATION HAS BEEN RUNNING FOR {elapsed_time:.2f} SECONDS ...\033[0m", end='')
    time.sleep(10)  # Adjust the sleep interval as needed

print()  # Added this line
elapsed_time_minutes = elapsed_time / 60  # Converting the time to hours
print(f'\033[91mTHE SIMULATION TOTAL RAN TIME {elapsed_time_minutes:.2f} MINUTES\033[0m')

print('--------------------------------------')
print('./> THE SIMULATION HAS FINISHED')
print('--------------------------------------')

#%%

print('--------------------------------------')
print('./> PLOTTING SIMULATION RESULT')
print('--------------------------------------')
fig, (ax) = plt.subplots(1, figsize=(8, 8))
ax.plot(result1['strain'], result1['stress'], label='cp_voce')
ax.set_title('Stress-Strain Curve', fontsize=18)
ax.set_xlabel('True Strain [mm/mm] ', fontsize=18)
ax.set_ylabel('True Stress [MPa]', fontsize=18)
ax.grid(which='major', axis='both',
        color='SlateGray', linewidth=1, linestyle=':')
ax.legend(loc='upper left', fontsize=18)
# Textbox
ax.text(0, 0, '  tau_sat = ' + str(VSH_TAU_SAT) + ' MPa' +
        '\n  b = ' + str(VSH_B) + ' MPa' +
        '\n  tau_0 = ' + str(VSH_TAU_0) + ' MPa' +
        '\n  gamma0 = ' + str(AI_GAMMA0) +
        '\n  n = ' + str(AI_N),
        fontsize=16, bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10, })
plt.savefig("output_result1_ccsurve.png")
print('------------------------------------')
print('./> DONE')
print('------------------------------------')

# -----------------------------------------------------------------------------------
# RUN SIMULATIONS
# -----------------------------------------------------------------------------------
print('------------------------------------')
print('./> RUNNING SIMULATION 2')
print('------------------------------------')
cpmodel = cpmodel_fcc_voce(PATH_NEML, YOUNGS, POISSONS, LATTICE_A, SLIP_DIRECTION, SLIP_PLANE,
                            VSH_TAU_SAT, VSH_B, VSH_TAU_0, AI_GAMMA0, AI_N,
                            GRAIN_ORIENTATIONS, NUM_THREADS)
result2 = drivers.uniaxial_test(cpmodel, ERATE, emax=EMAX, nsteps=NSTEPS)
# Save results into a csv file with column names
np.savetxt('output_result2_ccsurve.csv', np.column_stack(
    (result2['strain'], result2['stress'], result2['energy_density'],
     result2['plastic_work'])), delimiter=',',
    header='strain, stress, energy_density, plastic_work')
print('------------------------------------')
print('./> DONE')
print('------------------------------------')

# %%

print('--------------------------------------')
print('./> PLOTTING SIMULATION RESULT')
print('--------------------------------------')
fig, (ax) = plt.subplots(1, figsize=(8, 8))
ax.plot(result2['strain'], result2['stress'], label='cp_voce')
ax.set_title('Stress-Strain Curve', fontsize=18)
ax.set_xlabel('True Strain [mm/mm] ', fontsize=18)
ax.set_ylabel('True Stress [MPa]', fontsize=18)
ax.grid(which='major', axis='both',
        color='SlateGray', linewidth=1, linestyle=':')
ax.legend(loc='upper left', fontsize=18)
# Textbox
ax.text(0, 0, '  tau_sat = ' + str(VSH_TAU_SAT) + ' MPa' +
        '\n  b = ' + str(VSH_B) + ' MPa' +
        '\n  tau_0 = ' + str(VSH_TAU_0) + ' MPa' +
        '\n  gamma0 = ' + str(AI_GAMMA0) +
        '\n  n = ' + str(AI_N),
        fontsize=16, bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10, })
plt.savefig("output_result2_ccsurve.png")
print('------------------------------------')
print('./> DONE')
print('------------------------------------')
