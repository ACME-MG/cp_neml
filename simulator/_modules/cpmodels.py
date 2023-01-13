


from neml.cp import crystallography, slipharden, sliprules, inelasticity, kinematics, singlecrystal, polycrystal
from neml import elasticity, drivers

def cpmodel_fcc_voce(PATH_NEML, YOUNGS, POISSONS, LATTICE_A, SLIP_DIRECTION, SLIP_PLANE,
                 VSH_TAU_SAT, VSH_B, VSH_TAU_0, AI_GAMMA0, AI_N,
                 GRAIN_ORIENTATIONS, NUM_THREADS):
    import sys
    sys.path.append(PATH_NEML)

    emodel = elasticity.IsotropicLinearElasticModel(
        YOUNGS, "youngs", POISSONS, "poissons")
    # Plastic model
    strengthmodel = slipharden.VoceSlipHardening(VSH_TAU_SAT, VSH_B, VSH_TAU_0)
    slipmodel = sliprules.PowerLawSlipRule(strengthmodel, AI_GAMMA0, AI_N)
    imodel = inelasticity.AsaroInelasticity(slipmodel)
    # Elasto-Plastic model
    kmodel = kinematics.StandardKinematicModel(emodel, imodel)
    # Slip systems
    lattice = crystallography.CubicLattice(LATTICE_A)
    # Add a slip system given the Miller direction and plane.
    lattice.add_slip_system(SLIP_DIRECTION, SLIP_PLANE)
    # Combined Crystal Plasticity Model
    model = singlecrystal.SingleCrystalModel(kmodel, lattice, verbose=False)
    # Final Crystal Plasticity Model
    cpmodel = polycrystal.TaylorModel(model, GRAIN_ORIENTATIONS, nthreads=NUM_THREADS)

    return cpmodel 


def cpmodel_dmg_fcc_voce(PATH_NEML, YOUNGS, POISSONS, SHEAR, LATTICE_A, SLIP_DIRECTION, SLIP_PLANE,
                     VSH_TAU_SAT, VSH_B, VSH_TAU_0, AI_GAMMA0, AI_N,
                     GRAIN_ORIENTATIONS, NUM_THREADS):

    import sys
    sys.path.append(PATH_NEML)

    emodel = elasticity.IsotropicLinearElasticModel(
        YOUNGS, "youngs", POISSONS, "poissons")
    #emodel = elasticity.CubicLinearElasticModel(YOUNGS, POISSONS, SHEAR, "moduli")
    # Plastic model
    strengthmodel = slipharden.VoceSlipHardening(VSH_TAU_SAT, VSH_B, VSH_TAU_0)
    slipmodel = sliprules.PowerLawSlipRule(strengthmodel, AI_GAMMA0, AI_N)
    imodel = inelasticity.AsaroInelasticity(slipmodel)
    # Elasto-Plastic model
    kmodel = kinematics.StandardKinematicModel(emodel, imodel)
    # Slip systems
    lattice = crystallography.CubicLattice(LATTICE_A)
    # Add a slip system given the Miller direction and plane.
    lattice.add_slip_system(SLIP_DIRECTION, SLIP_PLANE)
    model = singlecrystal.SingleCrystalModel(kmodel, lattice, verbose=False)
    # Final Crystal Plasticity Model
    cpmodel = polycrystal.TaylorModel(
        model, GRAIN_ORIENTATIONS, nthreads=NUM_THREADS)
    
    return cpmodel
