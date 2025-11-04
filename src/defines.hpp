#pragma once


//#define BENCHMARK // disable all extensions and setups and run benchmark setup instead
//cnd #define USE_FXFILE // get stl filename from %FXFILE% env var (or -f switch)

#ifndef BENCHMARK
//#define DEMO_CONCORDE
//#define DEMO_3D_TAYLOR_GREEN_VORTICES
//#define DEMO_NASA_COMMON_RESEARCH_MODEL
//#define DEMO_2D_TAYLOR_GREEN_VORTICES //cnd
//#define DEMO_POISEUILLE_FLOW //cnd
//#define DEMO_POISEUILLE_FLOW2D //cnd
//#define DEMO_STOKES_DRAG //cnd
//#define DEMO_CYLINDER_IN_RECTANGULAR_DUCT //cnd
//#define DEMO_TAYLOR_COUETTE_FLOW //cnd
//#define DEMO_LID_DRIVEN_CAVITY //cnd
//#define DEMO_2D_KARMAN_VORTEX_STREET //cnd
//#define DEMO_PARTICLE_TEST //cnd
//#define DEMO_DELTA_WING //cnd
//#define DEMO_BOEING_747 //cnd
//#define DEMO_CND_GLIDER //cnd
//#define DEMO_STAR_WARS_X_WING //cnd
//#define DEMO_STAR_WARS_TIE_FIGHTER //cnd
//#define DEMO_RADIAL_FAN //cnd
//#define DEMO_ELECTRIC_DUCTED_FAN //cnd
//#define DEMO_AERODYNAMIC_COW //cnd
//#define DEMO_AERODYNAMIC_COW_TEST
//#define DEMO_SPACE_SHUTTLE //cnd
//#define DEMO_STARSHIP //cnd
//#define DEMO_AHMED_BODY //cnd
//#define DEMO_CESSNA_172 //cnd
//#define DEMO_BELL_222_HELICOPTER //cnd
//#define DEMO_MERCEDES_F1_W14_CAR //cnd
//#define DEMO_HYDRAULIC_JUMP //cnd
//#define DEMO_DAM_BREAK //cnd
//#define DEMO_LIQUID_METAL_ON_A_SPEAKER //cnd
//#define DEMO_BREAKING_WAVES_ON_BEACH //cnd
//#define DEMO_RIVER //cnd
//#define DEMO_RAINDROP_IMPACT //cnd
//#define DEMO_BURSTING_BUBBLE //cnd
//#define DEMO_CUBE_WITH_CHANGING_GRAVITY //cnd
//#define DEMO_PERIODIC_FAUCET //cnd
//#define DEMO_COLLIDING_DROPLETS //cnd
//#define DEMO_RAYLEIGH_BENARD_CONVECTION //cnd
//#define DEMO_THERMAL_CONVECTION //cnd
#define DEMO_CND_WING

/*
      *	FP16S							Done
      *	FP16C							Done

      *	fpxx   (FP16S|FP16C) ? ushort : float			Done

      *	D2Q9							Done
      *	D3Q15							Done
      *	D3Q19							Done
      *	D3Q27							Done

      *	SRT							Done
      *	TRT							Done

      * VOLUME_FORCE						Done
      *	TEMPERATURE (req: VOLUME_FORCE)				Done
      *	FORCE_FIELD						Done
      *	EQUILIBRIUM_BOUNDARIES					Done
      *	MOVING_BOUNDARIES					Done
      *	SURFACE (req: UPDATE_FIELDS)				Done
      *	SUBGRID							Done
      *	PARTICLES (req: UPDATE_FIELDS)				Done
      *	UPDATE_FIELDS						Done

	GRAPHICS						Incomplete
	INTERACTIVE_GRAPHICS_ASCII (req: GRAPHICS)
	INTERACTIVE_GRAPHICS (req: GRAPHICS)

	GRAPHICS_*
	TYPE_* ?
	VIS_*

*/

#endif // BENCHMARK   || defined()



#if defined(DEMO_3D_TAYLOR_GREEN_VORTICES) || \
    defined(DEMO_2D_KARMAN_VORTEX_STREET) || \
    defined(DEMO_POISEUILLE_FLOW2D)
#define D2Q9 // choose D2Q9 velocity set for 2D; allocates 53 (FP32) or 35 (FP16) Bytes/cell
#else
//#define D3Q15 // choose D3Q15 velocity set for 3D; allocates 77 (FP32) or 47 (FP16) Bytes/cell
#define D3Q19 // choose D3Q19 velocity set for 3D; allocates 93 (FP32) or 55 (FP16) Bytes/cell; (default)
//#define D3Q27 // choose D3Q27 velocity set for 3D; allocates 125 (FP32) or 71 (FP16) Bytes/cell
#endif

#define SRT // choose single-relaxation-time LBM collision operator; (default)
//#define TRT // choose two-relaxation-time LBM collision operator

#if defined(DEMO_NASA_COMMON_RESEARCH_MODEL) || \
    defined(DEMO_RAINDROP_IMPACT) || \
    defined(DEMO_AHMED_BODY) || \
    defined(DEMO_BURSTING_BUBBLE) || \
    defined(DEMO_BELL_222_HELICOPTER)
#define FP16C
#elif defined(DEMO_RADIAL_FAN) || \
    defined(DEMO_BOEING_747) || \
    defined(DEMO_2D_KARMAN_VORTEX_STREET) || \
    defined(DEMO_CONCORDE) || \
    defined(DEMO_CND_GLIDER) || \
    defined(DEMO_STAR_WARS_X_WING) || \
    defined(DEMO_STAR_WARS_TIE_FIGHTER) || \
    defined(DEMO_ELECTRIC_DUCTED_FAN) || \
    defined(DEMO_AERODYNAMIC_COW) || \
    defined(DEMO_SPACE_SHUTTLE) || \
    defined(DEMO_STARSHIP) || \
    defined(DEMO_CESSNA_172) || \
    defined(DEMO_MERCEDES_F1_W14_CAR) || \
    defined(DEMO_HYDRAULIC_JUMP) || \
    defined(DEMO_DAM_BREAK) || \
    defined(DEMO_LIQUID_METAL_ON_A_SPEAKER) || \
    defined(DEMO_BREAKING_WAVES_ON_BEACH) || \
    defined(DEMO_RIVER) || \
    defined(DEMO_CUBE_WITH_CHANGING_GRAVITY) || \
    defined(DEMO_PERIODIC_FAUCET) || \
    defined(DEMO_COLLIDING_DROPLETS) || \
    defined(DEMO_RAYLEIGH_BENARD_CONVECTION) || \
    defined(DEMO_THERMAL_CONVECTION) || \
    defined(DEMO_DELTA_WING) 
#define FP16S // compress LBM DDFs to range-shifted IEEE-754 FP16; number conversion is done in hardware; all arithmetic is still done in FP32
#endif


#if defined(DEMO_PARTICLE_TEST) || \
    defined(DEMO_RAINDROP_IMPACT) || \
    defined(DEMO_POISEUILLE_FLOW) || \
    defined(DEMO_POISEUILLE_FLOW2D) || \
    defined(DEMO_CYLINDER_IN_RECTANGULAR_DUCT) || \
    defined(DEMO_HYDRAULIC_JUMP) || \
    defined(DEMO_LIQUID_METAL_ON_A_SPEAKER) || \
    defined(DEMO_BREAKING_WAVES_ON_BEACH) || \
    defined(DEMO_RIVER) || \
    defined(DEMO_BURSTING_BUBBLE) || \
    defined(DEMO_CUBE_WITH_CHANGING_GRAVITY) || \
    defined(DEMO_PERIODIC_FAUCET) || \
    defined(DEMO_COLLIDING_DROPLETS) || \
    defined(DEMO_RAYLEIGH_BENARD_CONVECTION) || \
    defined(DEMO_THERMAL_CONVECTION) || \
    defined(DEMO_DAM_BREAK)
#define VOLUME_FORCE // enables global force per volume in one direction (equivalent to a pressure gradient); specified in the LBM class constructor; the force can be changed on-the-fly between time steps at no performance cost
#endif

#if defined(DEMO_STOKES_DRAG) || \
    defined(DEMO_AHMED_BODY) || \
    defined(DEMO_COLLIDING_DROPLETS) || \
    defined(DEMO_PARTICLE_TEST)
#define FORCE_FIELD // enables computing the forces on solid boundaries with lbm.calculate_force_on_boundaries(); and enables setting the force for each lattice point independently (enable VOLUME_FORCE too); allocates an extra 12 Bytes/cell
#endif

#if defined(DEMO_CONCORDE) || \
    defined(DEMO_NASA_COMMON_RESEARCH_MODEL) || \
    defined(DEMO_BOEING_747) || \
    defined(DEMO_CND_GLIDER) || \
    defined(DEMO_STOKES_DRAG) || \
    defined(DEMO_DELTA_WING) || \
    defined(DEMO_ELECTRIC_DUCTED_FAN) || \
    defined(DEMO_SPACE_SHUTTLE) || \
    defined(DEMO_RAINDROP_IMPACT) || \
    defined(DEMO_CESSNA_172) || \
    defined(DEMO_2D_KARMAN_VORTEX_STREET) || \
    defined(DEMO_STAR_WARS_X_WING) || \
    defined(DEMO_STAR_WARS_TIE_FIGHTER) || \
    defined(DEMO_STARSHIP) || \
    defined(DEMO_AHMED_BODY) || \
    defined(DEMO_BELL_222_HELICOPTER) || \
    defined(DEMO_MERCEDES_F1_W14_CAR) || \
    defined(DEMO_HYDRAULIC_JUMP) || \
    defined(DEMO_BREAKING_WAVES_ON_BEACH) || \
    defined(DEMO_AERODYNAMIC_COW)
#define EQUILIBRIUM_BOUNDARIES // enables fixing the velocity/density by marking cells with TYPE_E; can be used for inflow/outflow; does not reflect shock waves
#endif

#if defined(DEMO_PARTICLE_TEST) || \
    defined(DEMO_RADIAL_FAN) || \
    defined(DEMO_ELECTRIC_DUCTED_FAN) || \
    defined(DEMO_TAYLOR_COUETTE_FLOW) || \
    defined(DEMO_LID_DRIVEN_CAVITY) || \
    defined(DEMO_BELL_222_HELICOPTER) || \
    defined(DEMO_MERCEDES_F1_W14_CAR) || \
    defined(DEMO_LIQUID_METAL_ON_A_SPEAKER) || \
    defined(DEMO_CESSNA_172)
#define MOVING_BOUNDARIES // enables moving solids: set solid cells to TYPE_S and set their velocity u unequal to zero
#endif

#if defined(DEMO_RAINDROP_IMPACT) || \
    defined(DEMO_HYDRAULIC_JUMP) || \
    defined(DEMO_LIQUID_METAL_ON_A_SPEAKER) || \
    defined(DEMO_BREAKING_WAVES_ON_BEACH) || \
    defined(DEMO_RIVER) || \
    defined(DEMO_BURSTING_BUBBLE) || \
    defined(DEMO_CUBE_WITH_CHANGING_GRAVITY) || \
    defined(DEMO_PERIODIC_FAUCET) || \
    defined(DEMO_COLLIDING_DROPLETS) || \
    defined(DEMO_DAM_BREAK)
#define SURFACE // enables free surface LBM: mark fluid cells with TYPE_F; at initialization the TYPE_I interface and TYPE_G gas domains will automatically be completed; allocates an extra 12 Bytes/cell
#endif

#if defined(DEMO_RAYLEIGH_BENARD_CONVECTION) || \
    defined(DEMO_THERMAL_CONVECTION)
#define TEMPERATURE // enables temperature extension; set fixed-temperature cells with TYPE_T (similar to EQUILIBRIUM_BOUNDARIES); allocates an extra 32 (FP32) or 18 (FP16) Bytes/cell
#endif

#if defined(DEMO_CONCORDE) || \
    defined(DEMO_NASA_COMMON_RESEARCH_MODEL) || \
    defined(DEMO_BOEING_747) || \
    defined(DEMO_CND_GLIDER) || \
    defined(DEMO_DELTA_WING) || \
    defined(DEMO_RADIAL_FAN) || \
    defined(DEMO_ELECTRIC_DUCTED_FAN) || \
    defined(DEMO_SPACE_SHUTTLE) || \
    defined(DEMO_CESSNA_172) || \
    defined(DEMO_STAR_WARS_X_WING) || \
    defined(DEMO_STAR_WARS_TIE_FIGHTER) || \
    defined(DEMO_STARSHIP) || \
    defined(DEMO_AHMED_BODY) || \
    defined(DEMO_BELL_222_HELICOPTER) || \
    defined(DEMO_MERCEDES_F1_W14_CAR) || \
    defined(DEMO_AERODYNAMIC_COW)
#define SUBGRID // enables Smagorinsky-Lilly subgrid turbulence LES model to keep simulations with very large Reynolds number stable
#endif

#if defined(DEMO_PARTICLE_TEST)
#define PARTICLES // enables particles with immersed-boundary method (for 2-way coupling also activate VOLUME_FORCE and FORCE_FIELD; only supported in single-GPU)
#endif


//#define INTERACTIVE_GRAPHICS_ASCII // enable interactive graphics in ASCII mode the console; start/pause the simulation by pressing P
//#define GRAPHICS // run FluidX3D in the console, but still enable graphics functionality for writing rendered frames to the hard drive bin/export/*png folder

#ifndef GRAPHICS
#ifndef INTERACTIVE_GRAPHICS_ASCII
#if defined(DEMO_CONCORDE) || \
    defined(DEMO_3D_TAYLOR_GREEN_VORTICES) || \
    defined(DEMO_2D_TAYLOR_GREEN_VORTICES) || \
    defined(DEMO_NASA_COMMON_RESEARCH_MODEL) || \
    defined(DEMO_BOEING_747) || \
    defined(DEMO_CND_GLIDER) || \
    defined(DEMO_PARTICLE_TEST) || \
    defined(DEMO_DELTA_WING) || \
    defined(DEMO_RADIAL_FAN) || \
    defined(DEMO_ELECTRIC_DUCTED_FAN) || \
    defined(DEMO_SPACE_SHUTTLE) || \
    defined(DEMO_RAINDROP_IMPACT) || \
    defined(DEMO_CESSNA_172) || \
    defined(DEMO_AERODYNAMIC_COW) || \
    defined(DEMO_CYLINDER_IN_RECTANGULAR_DUCT) || \
    defined(DEMO_TAYLOR_COUETTE_FLOW) || \
    defined(DEMO_LID_DRIVEN_CAVITY) || \
    defined(DEMO_2D_KARMAN_VORTEX_STREET) || \
    defined(DEMO_STAR_WARS_X_WING) || \
    defined(DEMO_STAR_WARS_TIE_FIGHTER) || \
    defined(DEMO_STARSHIP) || \
    defined(DEMO_AHMED_BODY) || \
    defined(DEMO_BELL_222_HELICOPTER) || \
    defined(DEMO_MERCEDES_F1_W14_CAR) || \
    defined(DEMO_HYDRAULIC_JUMP) || \
    defined(DEMO_LIQUID_METAL_ON_A_SPEAKER) || \
    defined(DEMO_BREAKING_WAVES_ON_BEACH) || \
    defined(DEMO_RIVER) || \
    defined(DEMO_BURSTING_BUBBLE) || \
    defined(DEMO_CUBE_WITH_CHANGING_GRAVITY) || \
    defined(DEMO_PERIODIC_FAUCET) || \
    defined(DEMO_COLLIDING_DROPLETS) || \
    defined(DEMO_RAYLEIGH_BENARD_CONVECTION) || \
    defined(DEMO_THERMAL_CONVECTION) || \
    defined(DEMO_DAM_BREAK) || \
    defined(DEMO_CND_WING)
#define INTERACTIVE_GRAPHICS // enable interactive graphics; start/pause the simulation by pressing P; either Windows or Linux X11 desktop must be available; on Linux: change to "compile on Linux with X11" command in make.sh
#endif
#endif // INTERACTIVE_GRAPHICS_ASCII
#endif // GRAPHICS

#define GRAPHICS_FULLSCREEN 1 // comment this out to get a window cnd
#define GRAPHICS_FRAME_WIDTH 1920 // set frame width if only GRAPHICS is enabled
#define GRAPHICS_FRAME_HEIGHT 1080 // set frame height if only GRAPHICS is enabled
//#define GRAPHICS_BACKGROUND_COLOR 0x000000 // set background color; black background (default) = 0x000000, white background = 0xFFFFFF
#define GRAPHICS_U_MAX 0.25f // maximum velocity for velocity coloring in units of LBM lattice speed of sound (c=1/sqrt(3)) (default: 0.25f)
#define GRAPHICS_RHO_DELTA 0.01f // coloring range for density rho will be [1.0f-GRAPHICS_RHO_DELTA, 1.0f+GRAPHICS_RHO_DELTA] (default: 0.01f)
#define GRAPHICS_T_DELTA 1.0f // coloring range for temperature T will be [1.0f-GRAPHICS_T_DELTA, 1.0f+GRAPHICS_T_DELTA] (default: 1.0f)
#define GRAPHICS_F_MAX 0.001f // maximum force in LBM units for visualization of forces on solid boundaries if VOLUME_FORCE is enabled and lbm.calculate_force_on_boundaries(); is called (default: 0.001f)
#define GRAPHICS_Q_CRITERION 0.0001f // Q-criterion value for Q-criterion isosurface visualization (default: 0.0001f)
#define GRAPHICS_STREAMLINE_SPARSE 8 // set how many streamlines there are every x lattice points
#define GRAPHICS_STREAMLINE_LENGTH 128 // set maximum length of streamlines
#define GRAPHICS_RAYTRACING_TRANSMITTANCE 0.25f // transmitted light fraction in raytracing graphics ("0.25f" = 1/4 of light is transmitted and 3/4 is absorbed along longest box side length, "1.0f" = no absorption)
#define GRAPHICS_RAYTRACING_COLOR 0x005F7F // absorption color of fluid in raytracing graphics

//#define GRAPHICS_TRANSPARENCY 0.7f // optional: comment/uncomment this line to disable/enable semi-transparent rendering (looks better but reduces framerate), number represents transparency (equal to 1-opacity) (default: 0.7f)



// #############################################################################################################

#define TYPE_S 0b00000001 // (stationary or moving) solid boundary
#define TYPE_E 0b00000010 // equilibrium boundary (inflow/outflow)
#define TYPE_T 0b00000100 // temperature boundary
#define TYPE_F 0b00001000 // fluid
#define TYPE_I 0b00010000 // interface
#define TYPE_G 0b00100000 // gas
#define TYPE_X 0b01000000 // reserved type X
#define TYPE_Y 0b10000000 // reserved type Y

#define VIS_FLAG_LATTICE  0b00000001 // lbm.graphics.visualization_modes = VIS_...|VIS_...|VIS_...;
#define VIS_FLAG_SURFACE  0b00000010
#define VIS_FIELD         0b00000100
#define VIS_STREAMLINES   0b00001000
#define VIS_Q_CRITERION   0b00010000
#define VIS_PHI_RASTERIZE 0b00100000
#define VIS_PHI_RAYTRACE  0b01000000
#define VIS_PARTICLES     0b10000000


#define fpxx16 ushort	// for FP16S and FP16C
#define fpxx float	// for FP32
/*
#if defined(FP16S) || defined(FP16C)
#define fpxx ushort
#else // FP32
#define fpxx float
#endif // FP32
*/

#ifdef BENCHMARK
#undef UPDATE_FIELDS
#undef VOLUME_FORCE
#undef FORCE_FIELD
#undef MOVING_BOUNDARIES
#undef EQUILIBRIUM_BOUNDARIES
#undef SURFACE
#undef TEMPERATURE
#undef SUBGRID
#undef PARTICLES
#undef INTERACTIVE_GRAPHICS
#undef INTERACTIVE_GRAPHICS_ASCII
#undef GRAPHICS
#endif // BENCHMARK

#ifdef SURFACE // (rho, u) need to be updated exactly every LBM step
#define UPDATE_FIELDS // update (rho, u, T) in every LBM step
#endif // SURFACE

#ifdef TEMPERATURE
#define VOLUME_FORCE
#endif // TEMPERATURE

#ifdef PARTICLES // (rho, u) need to be updated exactly every LBM step
#define UPDATE_FIELDS // update (rho, u, T) in every LBM step
#endif // PARTICLES

#if defined(INTERACTIVE_GRAPHICS) || defined(INTERACTIVE_GRAPHICS_ASCII)
#define GRAPHICS
#define UPDATE_FIELDS // to prevent flickering artifacts in interactive graphics
#endif // INTERACTIVE_GRAPHICS || INTERACTIVE_GRAPHICS_ASCII
