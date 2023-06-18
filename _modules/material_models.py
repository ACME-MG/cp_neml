
from neml.cp import crystallography, slipharden, sliprules, inelasticity, kinematics, singlecrystal, polycrystal
from neml import elasticity, drivers, surfaces, hardening, visco_flow, general_flow, models

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
    cpmodel.save('cpmodel_fcc_voce.xml', 'cpmodel')

    return cpmodel 


def vpmodel_macro_voce(PATH_NEML, YOUNGS, POISSONS, 
                       VIHR_s0, VIHR_R, VIHR_d, GPL_n, GPL_eta):

    import sys
    sys.path.append(PATH_NEML)

    emodel = elasticity.IsotropicLinearElasticModel(
        YOUNGS, "youngs", POISSONS, "poissons")
    surface_iso = surfaces.IsoJ2()
    #emodel = elasticity.CubicLinearElasticModel(YOUNGS, POISSONS, SHEAR, "moduli")
    # Plastic model
    strengthmodel = hardening.VoceIsotropicHardeningRule(VIHR_s0, VIHR_R, VIHR_d)
    gpower = visco_flow.GPowerLaw(GPL_n, GPL_eta)
    vflow  = visco_flow.PerzynaFlowRule(surface_iso, strengthmodel, gpower)
    integrator = general_flow.TVPFlowRule(emodel, vflow)
    vpmodel = models.GeneralIntegrator(emodel, integrator)
    vpmodel.save('vpmodel_macro_voce.xml', 'vpmodel')

    return vpmodel
