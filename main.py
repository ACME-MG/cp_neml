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
import psutil
import pandas as pd

from neml.math import rotations, tensors, nemlmath
from neml import elasticity, drivers

# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# FOLDER/FILE MANAGMENT
# -----------------------------------------------------------------------------------
print('------------------------------------')
print('./> FOLDER/FILE MANAGMENT')
print('------------------------------------')
# Input/Output folders
FOLDER_RUNSIM  = 'INL617/TEST1'
FOLDER_INPUT   = FOLDER_RUNSIM + '/_input'
FOLDER_MEASURE = FOLDER_RUNSIM + '/_measure'
FOLDER_OUTPUT  = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
print('------------------------------------')
print('FOLDER_RUNSIM  =', FOLDER_RUNSIM)
print('FOLDER_INPUT   =', FOLDER_INPUT)
print('FOLDER_MEASURE =', FOLDER_MEASURE)
print('FOLDER_OUTPUT  =', FOLDER_OUTPUT)
print('------------------------------------')
# Create paths
PATH_HOME    = os.getcwd() + '/simulations/'
PATH_INPUT   = PATH_HOME + FOLDER_RUNSIM + '/_input/'
PATH_MEASURE = PATH_HOME + FOLDER_RUNSIM + '/_measure/'
PATH_OUTPUT  = PATH_HOME + FOLDER_RUNSIM + '/' + FOLDER_OUTPUT
print('------------------------------------')
print('PATH_HOME   =', PATH_HOME)
print('PATH_INPUT  =', PATH_INPUT)
print('PATH_MEASURE=', PATH_MEASURE)
print('PATH_OUTPUT =', PATH_OUTPUT)
print('------------------------------------')
# -----------------------------------------------------------------------------------
# inport measured data 
measure1 = pd.read_excel(PATH_MEASURE + '/D5_TensileData_corrected.xlsx')
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
EMAX   = 0.45 # Maximum strain
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
VSH_B       = 40      # VoceSlipHardening
VSH_TAU_0   = 150     # VoceSlipHardening
AI_GAMMA0   = 0.001   # PowerLawSlipRule
AI_N        = 15      # PowerLawSlipRule
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
elapsed_time = time.time() - start_time  # simulation end time
print('\033[92m' + '--------------------------------------' + '\033[0m')
print(f'\033[92mTHE TOTAL RAN TIME {elapsed_time:.2f} SECONDS\033[0m')
print('\033[92m' + '--------------------------------------' + '\033[0m')
print('--------------------------------------')
print('./> THE SIMULATION HAS FINISHED')
print('--------------------------------------')

print(result1.keys())
# Save results into a csv file with column names
np.savetxt('output_result1_ccsurve.csv', np.column_stack(
    (result1['strain'], result1['stress'], result1['energy_density'],
     result1['plastic_work'])), delimiter=',', 
     header='strain, stress, energy_density, plastic_work')

#%%
print('--------------------------------------')
print('./> PLOTTING SIMULATION RESULT')
print('--------------------------------------')
fig, (ax) = plt.subplots(1, figsize=(8, 8))
# plot measured data Strain vs Strain set the color of the line to gray and make it transparent by setting alpha to 0.5 and linewidth of 2 
ax.plot(measure1['Strain'], measure1['Stress'], color='gray', alpha=0.50, linewidth=4.5, label='engineering')
ax.plot(measure1['True Strain'], measure1['True Stress'], color='black', alpha=0.50, linewidth=4.5, label='true')
# plot simulation data Strain vs Strain
ax.plot(result1['strain'], result1['stress'], color='tomato', alpha=1.0, linewidth=2.5, label='cp_voce')
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
