
BEGIN SCULPT
    
    # Dimensions
    nelx = 5
    nely = 88
    nelz = 113

    # Mesh Improvement
    smooth = 1
    csmooth = 4
    pillow_curves = true
    pillow_boundaries = true
    pillow_curve_layers = 4
    opt_threshold = 0.8

    # Remove cuts if any
    void_mat = 100000
    
    # Solver
    laplacian_iters = 5
    max_opt_iters = 100
    # adapt_type = 5
    # adapt_levels = 2
    
    # Output
    input_spn = ./results/230106223541/voxellation.spn
    exodus_file = ./results/230106223541/mesh.e

END SCULPT
