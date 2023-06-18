"""
MAIN
"""
# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

NUM_THREADS = 32
GRAINS_FILE = "input_grainsfile.csv"
PATH_NEML   = '/home/omz/moose/neml'

import sys
sys.path.append(PATH_NEML)

# Import libaries
from _modules.material_models import cpmodel_fcc_voce
from _modules.material_models import vpmodel_macro_voce
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
EMAX   = 0.48 # Maximum strain
NSTEPS = 50 # Number of steps
ERATE  = 1.0e-4 # Strain rate
# -----------------------------------------------------------------------------------
# MATERIAL PARAMETERS
# -----------------------------------------------------------------------------------
print('------------------------------------')
print('./> MATERIAL PARAMETERS')
print('------------------------------------')
YOUNGS      = 211000    # IsotropicLinearElasticModel 211000
POISSONS    = 0.30      # IsotropicLinearElasticModel
SHEAR       = 81000.0   # E / (2 * (1 + nu)) # Shear modulus
# Asaro Inelasticity
VSH_TAU_0   = 135       # VoceSlipHardening
VSH_TAU_SAT = 760       # VoceSlipHardening
VSH_B       = 0.50      # VoceSlipHardening
AI_GAMMA0   = 0.001     # PowerLawSlipRule
AI_N        = 10        # PowerLawSlipRule
# Lattice & Slip Systems
LATTICE_A   = 1.0
SLIP_DIRECTION = [1, 1, 0]
SLIP_PLANE     = [1, 1, 1]
# -----------------------------------------------------------------------------------
VIHR_s0    = 300
VIHR_R     = 2550
VIHR_d     = 1
GPL_n      = 1
GPL_eta    = 1
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
# SIMULATION 1
# -----------------------------------------------------------------------------------
print('------------------------------------')
print('./> RUNNING SIMULATION 1 (CP_FCC_MODEL)')
print('------------------------------------')
start_time = time.time()  # simulation start time
cpmodel = cpmodel_fcc_voce(PATH_NEML, YOUNGS, POISSONS, LATTICE_A, SLIP_DIRECTION, SLIP_PLANE,
                           VSH_TAU_SAT, VSH_B, VSH_TAU_0, AI_GAMMA0, AI_N,
                           GRAIN_ORIENTATIONS, NUM_THREADS)
result1 = drivers.uniaxial_test(cpmodel, ERATE, emax=EMAX, nsteps=NSTEPS)
# -----------------------------------------------------------------------------------
elapsed_time = time.time() - start_time  # simulation end time
print('\033[92m' + '--------------------------------------' + '\033[0m')
print(f'\033[92mTHE TOTAL RAN TIME {elapsed_time:.2f} SECONDS\033[0m')
print('\033[92m' + '--------------------------------------' + '\033[0m')
print('--------------------------------------')
print('./> THE SIMULATION HAS FINISHED')
print('--------------------------------------')
# -----------------------------------------------------------------------------------
print(result1.keys())
# Save results into a csv file with column names
np.savetxt('output_result1_ccsurve.csv', np.column_stack(
    (result1['strain'], result1['stress'], result1['energy_density'],
     result1['plastic_work'])), delimiter=',', 
     header='strain, stress, energy_density, plastic_work')

# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# SIMULATION 2
# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
print('--------------------------------------')
print('./> RUNNING SIMULATION 2 (VP_MACRO_MODEL)')
print('--------------------------------------')
start_time = time.time()  # simulation start time
vpmodel = vpmodel_macro_voce(PATH_NEML, YOUNGS, POISSONS, 
                             VIHR_s0, VIHR_R, VIHR_d,
                             GPL_eta, GPL_n)
result2 = drivers.uniaxial_test(vpmodel, ERATE, emax=EMAX, nsteps=NSTEPS)
# -----------------------------------------------------------------------------------
elapsed_time = time.time() - start_time  # simulation end time
print('\033[92m' + '--------------------------------------' + '\033[0m')
print(f'\033[92mTHE TOTAL RAN TIME {elapsed_time:.2f} SECONDS\033[0m')
print('\033[92m' + '--------------------------------------' + '\033[0m')
print('--------------------------------------')
print('./> THE SIMULATION HAS FINISHED')
print('--------------------------------------')
# -----------------------------------------------------------------------------------
print(result2.keys())
# Save results into a csv file with column names
np.savetxt('output_result2_ccsurve.csv', np.column_stack(
    (result2['strain'], result2['stress'], result2['energy_density'],
     result2['plastic_work'])), delimiter=',', 
     header='strain, stress, energy_density, plastic_work')
#%% ---------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# PLOTTING SIMULATION RESULT
# -----------------------------------------------------------------------------------
print('--------------------------------------')
print('./> PLOTTING SIMULATION RESULT')
print('--------------------------------------')
fig, (ax) = plt.subplots(1, figsize=(8, 8))
# Plot experimental results
ax.plot(measure1['Strain'],      measure1['Stress'], color='gray', alpha=0.50, linewidth=4.5, label='eng_sscurve')
ax.plot(measure1['True Strain'], measure1['True Stress'], color='black', alpha=0.50, linewidth=4.5, label='true_sscurve')
# Plot simulation results 
ax.plot(result1['strain'], result1['stress'], color='tomato',    alpha=1.0, linewidth=2.5, label='cp_fcc_voce')
ax.plot(result2['strain'], result2['stress'], color='steelblue', alpha=1.0, linewidth=2.5, label='vp_macro_voce')
ax.set_title('Stress-Strain Curve', fontsize=18)
ax.set_xlabel('True Strain [mm/mm] ', fontsize=18)
ax.set_ylabel('True Stress [MPa]', fontsize=18)
ax.grid(which='major', axis='both',
        color='SlateGray', linewidth=1, linestyle=':')
ax.legend(loc='upper left', fontsize=16)
# Textbox cp_model
ax.text(0.05, 0.05, 'cp_fcc_voce' +  
        '\nt0 = ' + str(VSH_TAU_0) + ' MPa' +
        '\nts = ' + str(VSH_TAU_SAT) + ' MPa' +
        '\nb = ' + str(VSH_B) + ' MPa' +
        '\ng0 = ' + str(AI_GAMMA0) +
        '\nn = ' + str(AI_N),
        fontsize=16, bbox={'facecolor': 'tomato', 'alpha': 0.5, 'pad': 10, })
# Textbox macro_model
ax.text(0.26, 0.26, 'vp_macro_voce' + 
        '\ns0 = ' + str(VIHR_s0) + ' MPa' +
        '\nR = ' + str(VIHR_R) + ' MPa' +
        '\nd = ' + str(VIHR_d) + ' MPa' +
        '\neta = ' + str(GPL_eta) +
        '\nn = ' + str(GPL_n),
        fontsize=16, bbox={'facecolor': 'steelblue', 'alpha': 0.5, 'pad': 10, })
# Save figure
plt.savefig("output_ccsurve.png")
print('--------------------------------------')
print('./> DONE')
print('--------------------------------------')