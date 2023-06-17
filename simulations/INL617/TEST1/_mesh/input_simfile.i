
# ==================================================
# Define global parameters
# ==================================================
[GlobalParams]
  displacements = 'disp_x disp_y disp_z'
[]
# ==================================================
# Define Mesh
# ==================================================
[Mesh]
  use_displaced_mesh = false
  [./mesh_input]
    type = FileMeshGenerator
    file = "input_meshfile.e"
  [../]
  [./add_side_sets]
    input = mesh_input
    type = SideSetsFromNormalsGenerator
    normals = '0  0 -1
               0  0  1'
    fixed_normal = true
    new_boundary = 'bottom top'
  [../]
  [./back]
    input = add_side_sets
    type = SideSetsAroundSubdomainGenerator
    new_boundary = 'back'
    block = 348
    fixed_normal = true
    normal = '-1 0 0'
  [../]
  [./left]
    input = back
    type = SideSetsAroundSubdomainGenerator
    new_boundary = 'left'
    block = 348
    fixed_normal = true
    normal = '0 -1 0'
  [../]
[]
# ==================================================
# Define Initial Orientations
# ==================================================
[UserObjects]
  [./euler_angle_file]
    type = PropertyReadFile
    nprop = 3
    prop_file_name = "input_grainsfile.csv"
    read_type = block
    nblock = 348
    use_zero_based_block_indexing = false
  [../]
[]
# ==================================================
# Define Modules
# ==================================================
[Modules]
  [./TensorMechanics]
    [./Master]
      [./all]
        strain = FINITE #FINITE (for large deformation)
        add_variables = true
        new_system = true
        formulation = TOTAL
        volumetric_locking_correction = false
        generate_output = 'elastic_strain_xx elastic_strain_yy elastic_strain_zz
                           strain_xx strain_yy strain_zz
                           cauchy_stress_xx cauchy_stress_yy cauchy_stress_zz
                           mechanical_strain_xx mechanical_strain_yy mechanical_strain_zz'
      [../]
    [../]
  [../]
[]
# ==================================================
# Define Variables
# ==================================================
[AuxVariables]
  [./orientation_q1]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./orientation_q2]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./orientation_q3]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./orientation_q4]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./RGB_x]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./RGB_y]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./RGB_z]
    order = CONSTANT
    family = MONOMIAL
  [../]
[]
# ==================================================
# Define Kernels
# ==================================================
[AuxKernels]
  [q1]
    type = MaterialStdVectorAux
    property = orientation
    index = 0
    variable = orientation_q1
    execute_on = 'initial timestep_end'
    block = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50
            51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100
            101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150
            151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200
            201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250
            251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300
            301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347'
  [../]
  [q2]
    type = MaterialStdVectorAux
    property = orientation
    index = 1
    variable = orientation_q2
    execute_on = 'initial timestep_end'
    block = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50
            51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100
            101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150
            151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200
            201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250
            251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300
            301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347'
  [../]
  [q3]
    type = MaterialStdVectorAux
    property = orientation
    index = 2
    variable = orientation_q3
    execute_on = 'initial timestep_end'
    block = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50
            51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100
            101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150
            151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200
            201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250
            251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300
            301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347'
  [../]
  [q4]
    type = MaterialStdVectorAux
    property = orientation
    index = 3
    variable = orientation_q4
    execute_on = 'initial timestep_end'
    block = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50
            51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100
            101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150
            151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200
            201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250
            251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300
            301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347'
  [../]
  [RBG_x]
    type = IPFColoring
    variable = RGB_x
    q1 = orientation_q1
    q2 = orientation_q2
    q3 = orientation_q3
    q4 = orientation_q4
    sample_direction = '0.0 0.0 1.0'
    crystal_symmetry = '432'
    component = 0
    execute_on = 'initial timestep_end'
    block = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50
            51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100
            101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150
            151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200
            201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250
            251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300
            301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347'
  [../]
  [RBG_y]
    type = IPFColoring
    variable = RGB_y
    q1 = orientation_q1
    q2 = orientation_q2
    q3 = orientation_q3
    q4 = orientation_q4
    sample_direction = '0.0 0.0 1.0'
    crystal_symmetry = '432'
    component = 1
    execute_on = 'initial timestep_end'
    block = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50
            51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100
            101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150
            151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200
            201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250
            251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300
            301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347'
  [../]
  [RBG_z]
    type = IPFColoring
    variable = RGB_z
    q1 = orientation_q1
    q2 = orientation_q2
    q3 = orientation_q3
    q4 = orientation_q4
    sample_direction = '0.0 0.0 1.0'
    crystal_symmetry = '432'
    component = 2
    execute_on = 'initial timestep_end'
    block = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50
            51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100
            101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150
            151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200
            201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250
            251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300
            301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347'
  [../]
[]
# ==================================================
# Apply stress
# ==================================================
[Functions]
  [./applied_load]
    type = PiecewiseLinear
    x = '0 1'
    y = '0 489'
  [../]
[]
# ==================================================
# Boundary Conditions
# ==================================================
[BCs]
  [./x0]
    type = DirichletBC
    boundary = 'back'
    variable = disp_x
    value = 0.0
  [../]
  [./y0]
    type = DirichletBC
    boundary = 'left'
    variable = disp_y
    value = 0.0
  [../]
  [./z0]
    type = DirichletBC
    boundary = 'bottom'
    variable = disp_z
    value = 0.0
  [../]
  [./z1]
    type = FunctionDirichletBC
    boundary = 'top'
    variable = disp_z
    function = applied_load
  [../]
[]
# ==================================================
# Dampers
# ==================================================
[Dampers]
  [./damper]
    type = ReferenceElementJacobianDamper
    max_increment = 0.005 #0.002
    displacements = 'disp_x disp_y disp_z'
  [../]
[]
# ==================================================
# Define Material
# ==================================================
[Materials]
  [./stress1]
    type = NEMLCrystalPlasticity
    database = "input_matfile.xml"
    model = "CPMODEL1"
    large_kinematics = true
    euler_angle_reader = euler_angle_file
    angle_convention = "bunge"
    block = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50
            51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100
            101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150
            151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200
            201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250
            251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300
            301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347'
  [../]
  [./stress2]
    type = CauchyStressFromNEML
    database = "input_matfile.xml"
    model = "MACROMODEL1"
    large_kinematics = true
    block = 348
  [../]
[]
# ==================================================
# Define Preconditioning
# ==================================================
[Preconditioning]
  [./SMP]
    type = SMP
    full = true
  [../]
[]
# ==================================================
# Define Postprocessing (History)
# ==================================================
[VectorPostprocessors]
  [./VPEVS]
    type = ElementValueSampler
    variable = 'orientation_q1 orientation_q2 orientation_q3 orientation_q4
                cauchy_stress_xx cauchy_stress_yy cauchy_stress_zz
                strain_xx strain_yy strain_zz
                elastic_strain_xx elastic_strain_yy elastic_strain_zz
                mechanical_strain_xx mechanical_strain_yy mechanical_strain_zz'
    contains_complete_history = false
    execute_on = 'initial timestep_end'
    sort_by = id
    #outputs = VPEVS
  [../]
[]
# ==================================================
# Define Postprocessing (Model Average)
# ==================================================
[Postprocessors]
# Number of elemetts -----------------------------------------------------------
[./nelem]
  type = NumElems
[../]
# Mumber of degrees of freedom -------------------------------------------------
[./ndof]
  type = NumDOFs
[../]
# TimestepSize -----------------------------------------------------------------
  [./dt]
    type = TimestepSize
  [../]
# NumLinearIterations ----------------------------------------------------------
  [./num_lin_it]
    type = NumLinearIterations
  [../]
# NumNonlinearIterations -------------------------------------------------------
  [./num_nonlin_it]
    type = NumNonlinearIterations
  [../]
# ------------------------------------------------------------------------------
# AVERAGE FULL MODEL
# ------------------------------------------------------------------------------
# Mean: STRESS -----------------------------------------------------------------
  [./mCS_xx]
    type = ElementAverageValue
    variable = cauchy_stress_xx
  [../]
  [./mCS_yy]
    type = ElementAverageValue
    variable = cauchy_stress_yy
  [../]
  [./mCS_zz]
    type = ElementAverageValue
    variable = cauchy_stress_zz
  [../]
  # Mean: TOTAL STRAIN ---------------------------------------------------------
  [./mTE_xx]
    type = ElementAverageValue
    variable = strain_xx
  [../]
  [./mTE_yy]
    type = ElementAverageValue
    variable = strain_yy
  [../]
  [./mTE_zz]
    type = ElementAverageValue
    variable = strain_zz
  [../]
  # Mean: MECHANICAL STRAIN -----------------------------------------------------
  [./mME_xx]
    type = ElementAverageValue
    variable = mechanical_strain_xx
  [../]
  [./mME_yy]
    type = ElementAverageValue
    variable = mechanical_strain_yy
  [../]
  [./mME_zz]
    type = ElementAverageValue
    variable = mechanical_strain_zz
  [../]
  # Mean: ELASTIC STRAIN -------------------------------------------------------
  [./mEE_xx]
    type = ElementAverageValue
    variable = elastic_strain_xx
  [../]
  [./mEE_yy]
    type = ElementAverageValue
    variable = elastic_strain_yy
  [../]
  [./mEE_zz]
    type = ElementAverageValue
    variable = elastic_strain_zz
  [../]
[]
# ==================================================
# Define Simulation
# ==================================================
[Executioner]
  
  # Transient (time-dependent) problem
  type = Transient
  
  # Solver
  solve_type = NEWTON # Use Newton-Raphson, not PJFNK

  residual_and_jacobian_together = true
  
  # Options for PETSc (how to solve linear equations)
  automatic_scaling = false
  petsc_options = '-snes_converged_reason -ksp_converged_reason' 
  petsc_options_iname = '-pc_type -pc_factor_mat_solver_package -ksp_gmres_restart 
                         -pc_hypre_boomeramg_strong_threshold -pc_hypre_boomeramg_interp_type -pc_hypre_boomeramg_coarsen_type 
                         -pc_hypre_boomeramg_agg_nl -pc_hypre_boomeramg_agg_num_paths -pc_hypre_boomeramg_truncfactor'
  petsc_options_value = 'hypre boomeramg 200 0.7 ext+i PMIS 4 2 0.4'
  
  # Solver tolerances
  l_max_its = 300 
  l_tol = 1e-4 #1e-6
  nl_max_its = 15
  nl_rel_tol = 1e-6
  nl_abs_tol = 1e-6
  nl_forced_its = 1
  line_search = 'none'

  # Time variables
  start_time = 0
  end_time = 1
  dtmin = 1e-10
  dtmax = 0.1

  [./Predictor]
    type = SimplePredictor
    scale = 1.0
  [../]

  [./TimeStepper]
    type = IterationAdaptiveDT
    growth_factor = 2
    cutback_factor = 0.5
    linear_iteration_ratio = 1000
    optimal_iterations = 8 #12
    iteration_window = 1
    dt = 0.001
  [../]
[]
# ==================================================
# Define Simulation Output
# ==================================================
[Outputs]
  print_linear_residuals = false
  perf_graph = true
  checkpoint = true
    [./exodus]
    type = Exodus
    file_base = 'output'
    elemental_as_nodal = true
    interval = 1
    execute_on = 'initial timestep_end'
    #sync_only = true
    #sync_times = '0 0.5 1'
  [../]
  [./console]
    type = Console
    show = 'dt mCS_xx mCS_yy mCS_zz mTE_xx mTE_yy mTE_zz'
    output_linear = true
    print_mesh_changed_info = true
    max_rows = 5
  [../]
  [./outfile]
    type = CSV
    file_base = 'output'
    time_data = true
    delimiter = ','
    #interval = 1
    execute_on = 'initial timestep_end'
    #sync_only = true
    #sync_times = '0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0'
  [../]
[]
