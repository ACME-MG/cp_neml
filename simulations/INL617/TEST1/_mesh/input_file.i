
BEGIN SCULPT
    
    # Dimensions
    nelx = 3
    nely = 163
    nelz = 326
    scale = 10

    # Remove cuts if any
    void_mat = 100000
    
    # Fixed mesh improvement
    smooth = 3
    defeature = 1
    pillow_curves = true
    pillow_boundaries = true
    micro_shave = true
    
    # Variable mesh improvement
    opt_threshold = 0.7
    pillow_curve_layers = 4
    pillow_curve_thresh = 0.3

    # Solver
    laplacian_iters = 5
    max_opt_iters = 50
    
    
    # Output
    input_spn = ./results/230607185336_inl_40x_10m/voxellation.spn
    exodus_file = ./results/230607185336_inl_40x_10m/mesh.e

END SCULPT
