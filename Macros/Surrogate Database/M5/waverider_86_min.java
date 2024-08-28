// Simcenter STAR-CCM+ macro: automation_macro.java
// Written by Simcenter STAR-CCM+ 19.02.009
package macro;

import java.util.*;

import star.common.*;
import star.base.neo.*;
import star.meshing.*;
import star.resurfacer.*;
import star.realgas.*;
import star.material.*;
import star.coupledflow.*;
import star.amr.*;
import star.flow.*;
import star.energy.*;
import star.base.report.*;
import star.automation.*;
import star.metrics.*;

public class waverider_86_min extends StarMacro {

  // Set name of waverider geometry 
  String waverider_name="waverider_86";
  String cad_filename= waverider_name + ".step";
  String save_filename="waverider_86_min";

  // Define flow conditions
  double mach=5;
  double velocity=1490.0; // m/s
  double ref_pressure=2506.0; // Pa
  double static_temp=221.65; //Kelvin
  double ref_density=3.940e-2; // kg/m3

  // Define surface meshing parameters
  double surface_base_size=0.5;
  double percent_target_surface_size=100.0; // percentage of base
  double minimum_surface_size=0.01; // absolute value (meters)
  double surface_growth_rate=1.05; 
  double local_refinement_target_surface_size=0.03;

  // Define volume meshing parameters
  double volume_base_size=surface_base_size;
  double volume_growth_rate=1.05;

  // Maximum refinement level
  int max_ref_level=2;

  // AMR upper bound
  double amr_upper_bound=0.1;

  // Minimum adaptation cell size
  double min_adapt_cell_size=1e-3;

  // Max iter
  int max_iter=1000;

  // Iteration frequency for AMR
  int amr_iter_frequency=100;

  // number of refinements
  int n_refinements=2;

  // Grid sequencing CFL number
  double cfl_number_grid_sequencing=2.5;

  // Type of mesh (enhanced quality triangle or quad dominated)
  // String mesh_type="QUAD";
  String mesh_type="ENCHANCED_TRIANGLE";

  // stopping criteria settings
  int n_samples=40;
  double asymptotic_limit=1e-6;


  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation simulation_0 = 
      getActiveSimulation();

    PhysicsContinuum physicsContinuum_1 = 
      simulation_0.getContinuumManager().createContinuum(PhysicsContinuum.class);

    // PartImportManager partImportManager_0 = 
    //   simulation_0.get(PartImportManager.class);
    
    //  CAD IMPORT
    // partImportManager_0.importCadPart(resolvePath("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\GCI_new\\" +cad_filename), "SharpEdges", 30.0, 4, true, 1.0E-5, true, false, false, false, true, NeoProperty.fromString("{\'NX\': 1, \'STEP\': 1, \'SE\': 1, \'CGR\': 1, \'SW\': 1, \'RHINO\': 1, \'IFC\': 1, \'ACIS\': 1, \'JT\': 1, \'IGES\': 1, \'CATIAV5\': 1, \'CATIAV4\': 1, \'3DXML\': 1, \'CREO\': 1, \'INV\': 1}"), true, false);

    CadPart cadPart_0 = 
      ((CadPart) simulation_0.get(SimulationPartManager.class).getPart(waverider_name));

    // PartSurface partSurface_0 = 
    //   ((PartSurface) cadPart_0.getPartSurfaceManager().getPartSurface("Faces"));

    // PartCurve partCurve_0 = 
    //   ((PartCurve) cadPart_0.getPartCurveManager().getPartCurve("Edges"));

    // // Split the faces of the waverider by the curves
    // cadPart_0.getPartSurfaceManager().splitPartSurfacesByPartCurves(new ArrayList<>(Arrays.<PartSurface>asList(partSurface_0)), new ArrayList<>(Arrays.<PartCurve>asList(partCurve_0)));

    // // Assign the lower surface
    // partSurface_0.setPresentationName("lower surface");

    // PartSurface partSurface_1 = 
    //   ((PartSurface) cadPart_0.getPartSurfaceManager().getPartSurface("Faces 2"));

    // // Assign the back
    // partSurface_1.setPresentationName("back");

    // PartSurface partSurface_2 = 
    //   ((PartSurface) cadPart_0.getPartSurfaceManager().getPartSurface("Faces 3"));

    // // Assign the upper surface
    // partSurface_2.setPresentationName("upper surface");

    // SUBSTRACT WAVERIDER FROM DOMAIN
    MeshPart meshPart_0 = 
      ((MeshPart) simulation_0.get(SimulationPartManager.class).getPart("domain"));

    SubtractPartsOperation subtractPartsOperation_0 = 
      (SubtractPartsOperation) simulation_0.get(MeshOperationManager.class).createSubtractPartsOperation(new ArrayList<>(Arrays.<GeometryPart>asList(meshPart_0, cadPart_0)));

    subtractPartsOperation_0.getTargetPartManager().setQuery(null);

    subtractPartsOperation_0.getTargetPartManager().setObjects(meshPart_0);

    MeshOperationPart meshOperationPart_0 = 
      ((MeshOperationPart) simulation_0.get(SimulationPartManager.class).getPart("Subtract"));

    meshOperationPart_0.setPresentationName("remove waverider");
    // SUBTRACT BLOCK TO GET HALF OF DOMAIN
    MeshPart meshPart_1 = 
      ((MeshPart) simulation_0.get(SimulationPartManager.class).getPart("block"));

    SubtractPartsOperation subtractPartsOperation_1 = 
      (SubtractPartsOperation) simulation_0.get(MeshOperationManager.class).createSubtractPartsOperation(new ArrayList<>(Arrays.<GeometryPart>asList(meshPart_1, meshOperationPart_0)));

    subtractPartsOperation_1.getTargetPartManager().setQuery(null);

    subtractPartsOperation_1.getTargetPartManager().setObjects(meshOperationPart_0);

    MeshOperationPart meshOperationPart_1 = 
      ((MeshOperationPart) simulation_0.get(SimulationPartManager.class).getPart("Subtract 2"));

    meshOperationPart_1.setPresentationName("fluid");
    // Execute subtract operations
    subtractPartsOperation_0.execute();

    subtractPartsOperation_1.execute();

    // ASSIGN A FLUID REGION
    Region region_0 = 
      simulation_0.getRegionManager().createEmptyRegion(null);

    region_0.setPresentationName("fluid");

    Boundary boundary_0 = 
      region_0.getBoundaryManager().getBoundary("Default");

    region_0.getBoundaryManager().removeObjects(boundary_0);

    MeshOperationPart meshOperationPart_2 = 
      ((MeshOperationPart) simulation_0.get(SimulationPartManager.class).getPart("fluid"));

    simulation_0.getRegionManager().newRegionsFromParts(new ArrayList<>(Arrays.<GeometryPart>asList(meshOperationPart_2)), "OneRegion", region_0, "OneBoundaryPerPartSurface", null, RegionManager.CreateInterfaceMode.BOUNDARY, "OneEdgeBoundaryPerPart", null);

    Boundary boundary_1 = 
      region_0.getBoundaryManager().getBoundary("fluid.block.symmetry");

    boundary_1.setPresentationName("symmetry");

    Boundary boundary_2 = 
      region_0.getBoundaryManager().getBoundary("fluid.remove waverider.domain.farfield");

    boundary_2.setPresentationName("farfield");

    Boundary boundary_3 = 
      region_0.getBoundaryManager().getBoundary("fluid.remove waverider."+waverider_name+".lower surface");

    boundary_3.setPresentationName("lower surface");

    Boundary boundary_4 = 
      region_0.getBoundaryManager().getBoundary("fluid.remove waverider."+waverider_name+".upper surface");

    boundary_4.setPresentationName("upper surface");

    SymmetryBoundary symmetryBoundary_0 = 
      ((SymmetryBoundary) simulation_0.get(ConditionTypeManager.class).get(SymmetryBoundary.class));

    boundary_1.setBoundaryType(symmetryBoundary_0);

    FreeStreamBoundary freeStreamBoundary_0 = 
      ((FreeStreamBoundary) simulation_0.get(ConditionTypeManager.class).get(FreeStreamBoundary.class));

    boundary_2.setBoundaryType(freeStreamBoundary_0);

    // SURFACE MESHING
    MeshOperationPart meshOperationPart_3 = 
      ((MeshOperationPart) simulation_0.get(SimulationPartManager.class).getPart("fluid"));

    AutoMeshOperation autoMeshOperation_0 = 
      simulation_0.get(MeshOperationManager.class).createAutoMeshOperation(new StringVector(new String[] {"star.resurfacer.ResurfacerAutoMesher", "star.resurfacer.AutomaticSurfaceRepairAutoMesher"}), new ArrayList<>(Arrays.<GeometryPart>asList(meshOperationPart_3)));

    autoMeshOperation_0.setPresentationName("Automated Surface Mesh");

    ResurfacerAutoMesher resurfacerAutoMesher_0 = 
      ((ResurfacerAutoMesher) autoMeshOperation_0.getMeshers().getObject("Surface Remesher"));
    if (mesh_type=="QUAD") {
      resurfacerAutoMesher_0.getResurfacerElementTypeOption().setSelected(ResurfacerElementTypeOption.Type.QUAD);
    }
    else {
      resurfacerAutoMesher_0.getResurfacerElementTypeOption().setSelected(ResurfacerElementTypeOption.Type.ENHANCED_TRIANGLE);
    }
    
    resurfacerAutoMesher_0.setMinimumFaceQuality(0.15);

    AutomaticSurfaceRepairAutoMesher automaticSurfaceRepairAutoMesher_0 = 
      ((AutomaticSurfaceRepairAutoMesher) autoMeshOperation_0.getMeshers().getObject("Automatic Surface Repair"));

    automaticSurfaceRepairAutoMesher_0.setMinimumFaceQuality(0.15);

    Units units_0 = 
      ((Units) simulation_0.getUnitsManager().getObject("m"));

    autoMeshOperation_0.getDefaultValues().get(BaseSize.class).setValueAndUnits(surface_base_size, units_0);

    PartsMinimumSurfaceSize partsMinimumSurfaceSize_0 = 
      autoMeshOperation_0.getDefaultValues().get(PartsMinimumSurfaceSize.class);

    partsMinimumSurfaceSize_0.getRelativeOrAbsoluteOption().setSelected(RelativeOrAbsoluteOption.Type.ABSOLUTE);

    ((ScalarPhysicalQuantity) partsMinimumSurfaceSize_0.getAbsoluteSizeValue()).setValueAndUnits(minimum_surface_size, units_0);

    SurfaceGrowthRate surfaceGrowthRate_0 = 
      autoMeshOperation_0.getDefaultValues().get(SurfaceGrowthRate.class);

    surfaceGrowthRate_0.setGrowthRateOption(SurfaceGrowthRate.GrowthRateOption.USER_SPECIFIED);

    Units units_1 = 
      ((Units) simulation_0.getUnitsManager().getObject(""));

    surfaceGrowthRate_0.getGrowthRateScalar().setValueAndUnits(surface_growth_rate, units_1);
    
    // Local refinement around lower surface
    SurfaceCustomMeshControl surfaceCustomMeshControl_0 = 
      autoMeshOperation_0.getCustomMeshControls().createSurfaceControl();

    surfaceCustomMeshControl_0.setPresentationName("Lower Surface Refinement");

    surfaceCustomMeshControl_0.getGeometryObjects().setQuery(null);


    PartSurface lower_surface_part_surface = 
      ((PartSurface) meshOperationPart_3.getPartSurfaceManager().getPartSurface("remove waverider."+waverider_name+".lower surface"));

    PartSurface upper_surface_part_surface = 
      ((PartSurface) meshOperationPart_3.getPartSurfaceManager().getPartSurface("remove waverider."+waverider_name+".upper surface"));

    surfaceCustomMeshControl_0.getGeometryObjects().setObjects(lower_surface_part_surface);

    surfaceCustomMeshControl_0.getCustomConditions().get(PartsTargetSurfaceSizeOption.class).setSelected(PartsTargetSurfaceSizeOption.Type.CUSTOM);

    PartsTargetSurfaceSize partsTargetSurfaceSize_0 = 
      surfaceCustomMeshControl_0.getCustomValues().get(PartsTargetSurfaceSize.class);

    partsTargetSurfaceSize_0.getRelativeOrAbsoluteOption().setSelected(RelativeOrAbsoluteOption.Type.ABSOLUTE);


    ((ScalarPhysicalQuantity) partsTargetSurfaceSize_0.getAbsoluteSizeValue()).setValueAndUnits(local_refinement_target_surface_size, units_0);
    // Execute the surface mesh operation
    // autoMeshOperation_0.execute();

    // VOLUME MESHING
    MeshOperationPart meshOperationPart_4 = 
      ((MeshOperationPart) simulation_0.get(SimulationPartManager.class).getPart("fluid"));

    AutoMeshOperation autoMeshOperation_1 = 
      simulation_0.get(MeshOperationManager.class).createAutoMeshOperation(new StringVector(new String[] {"star.dualmesher.DualAutoMesher"}), new ArrayList<>(Arrays.<GeometryPart>asList(meshOperationPart_4)));

    autoMeshOperation_1.setPresentationName("Automated Volume Mesh");

    Units units_2 = 
      ((Units) simulation_0.getUnitsManager().getObject("m"));

    autoMeshOperation_1.getDefaultValues().get(BaseSize.class).setValueAndUnits(volume_base_size, units_2);

    // Execute the volume meshing operation
    // autoMeshOperation_1.execute();
    
    // Physics Model and Initial/Reference Values
    PhysicsContinuum physicsContinuum_0 = 
      ((PhysicsContinuum) simulation_0.getContinuumManager().getContinuum("Physics 1"));

    physicsContinuum_0.enable(ThreeDimensionalModel.class);

    physicsContinuum_0.enable(AmrModel.class);

    physicsContinuum_0.enable(SingleComponentGasModel.class);

    physicsContinuum_0.enable(CoupledFlowModel.class);

    physicsContinuum_0.enable(RealGasModel.class);

    physicsContinuum_0.enable(CoupledEnergyModel.class);

    physicsContinuum_0.enable(EquilibriumAirEosModel.class);

    physicsContinuum_0.enable(SteadyModel.class);

    physicsContinuum_0.enable(InviscidModel.class);

    // physicsContinuum_0.enable(AmrModel.class);

    AmrModel amrModel_0 = 
      physicsContinuum_0.getModelManager().getModel(AmrModel.class);

    UserDefinedAmrCriterion userDefinedAmrCriterion_0 = 
      amrModel_0.getCriterionManager().create("star.amr.UserDefinedAmrCriterion");

    userDefinedAmrCriterion_0.setMaxRefinementLevel(max_ref_level);

    AmrRequestProfile amrRequestProfile_0 = 
      userDefinedAmrCriterion_0.getAmrRequestProfile();

    UserFieldFunction userFieldFunction_0 = 
      ((UserFieldFunction) simulation_0.getFieldFunctionManager().getFunction("RefineCriterionMachNumber"));

    amrRequestProfile_0.getMethod(AmrFunctionProfileMethod.class).setFieldFunction(userFieldFunction_0);

    amrRequestProfile_0.getMethod(AmrFunctionProfileMethod.class).getRange().setArray(new DoubleVector(new double[] {0.0, amr_upper_bound}));

    amrRequestProfile_0.getMethod(AmrFunctionProfileMethod.class).setOpBelow(AmrOperation.KEEP_TAG);

    CoupledFlowModel coupledFlowModel_0 = 
      physicsContinuum_0.getModelManager().getModel(CoupledFlowModel.class);

    coupledFlowModel_0.getUpwindOption().setSelected(FlowUpwindOption.Type.MUSCL_3RD_ORDER);

    coupledFlowModel_0.setUnsteadyPreconditioningEnabled(false);

    coupledFlowModel_0.getCoupledInviscidFluxOption().setSelected(CoupledInviscidFluxOption.Type.AUSM_SCHEME);

    amrModel_0.setUseAdaptionCellSize(true);

    Units units_3 = 
      ((Units) simulation_0.getUnitsManager().getObject("m"));

    amrModel_0.getMinAdaptionCellSize().setValueAndUnits(min_adapt_cell_size, units_3);

    coupledFlowModel_0.setPositivityRate(0.05);

    Units units_4 = 
      ((Units) simulation_0.getUnitsManager().getObject("Pa"));

    physicsContinuum_0.getReferenceValues().get(MinimumAllowableAbsolutePressure.class).setValueAndUnits(1.0E-12, units_4);

    Units units_5 = 
      ((Units) simulation_0.getUnitsManager().getObject("K"));

    physicsContinuum_0.getReferenceValues().get(MaximumAllowableTemperature.class).setValueAndUnits(10000.0, units_5);

    physicsContinuum_0.getReferenceValues().get(ReferencePressure.class).setValueAndUnits(ref_pressure, units_4);

    StaticTemperatureProfile staticTemperatureProfile_0 = 
      physicsContinuum_0.getInitialConditions().get(StaticTemperatureProfile.class);

    staticTemperatureProfile_0.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValueAndUnits(static_temp, units_5);

    VelocityProfile velocityProfile_0 = 
      physicsContinuum_0.getInitialConditions().get(VelocityProfile.class);

    Units units_6 = 
      ((Units) simulation_0.getUnitsManager().getObject("m/s"));

    velocityProfile_0.getMethod(ConstantVectorProfileMethod.class).getQuantity().setComponentsAndUnits(velocity, 0.0, 0.0, units_6);

    // Region region_0 = 
    //   simulation_0.getRegionManager().getRegion("fluid");

    Boundary farfield = 
      region_0.getBoundaryManager().getBoundary("farfield");

    MachNumberProfile machNumberProfile_0 = 
      farfield.getValues().get(MachNumberProfile.class);

    Units units_7 = 
      ((Units) simulation_0.getUnitsManager().getObject(""));

    machNumberProfile_0.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValueAndUnits(mach, units_7);

    StaticTemperatureProfile staticTemperatureProfile_1 = 
      farfield.getValues().get(StaticTemperatureProfile.class);

    staticTemperatureProfile_1.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValueAndUnits(static_temp, units_5);

  // Solvers and stopping criterion

  AmrSolver amrSolver_0 = 
      ((AmrSolver) simulation_0.getSolverManager().getSolver(AmrSolver.class));

    AmrStarUpdate amrStarUpdate_0 = 
      amrSolver_0.getAmrTrigger();

    IterationUpdateFrequency iterationUpdateFrequency_0 = 
      amrStarUpdate_0.getIterationUpdateFrequency();

    IntegerValue integerValue_0 = 
      iterationUpdateFrequency_0.getIterationFrequencyQuantity();

    integerValue_0.getQuantity().setValue(amr_iter_frequency);

    iterationUpdateFrequency_0.setStopEnabled(true);

    IntegerValue integerValue_1 = 
      iterationUpdateFrequency_0.getStopIterationQuantity();

    integerValue_1.getQuantity().setValue(n_refinements*amr_iter_frequency);

    CoupledImplicitSolver coupledImplicitSolver_0 = 
      ((CoupledImplicitSolver) simulation_0.getSolverManager().getSolver(CoupledImplicitSolver.class));

    AMGLinearSolver aMGLinearSolver_0 = 
      coupledImplicitSolver_0.getAMGLinearSolver();

    aMGLinearSolver_0.getSmootherOption().setSelected(AMGSmootherOption.Type.ILU);

    coupledImplicitSolver_0.getExpertInitManager().getExpertInitOption().setSelected(ExpertInitOption.Type.GRID_SEQ_METHOD);

    GridSequencingInit gridSequencingInit_0 = 
      ((GridSequencingInit) coupledImplicitSolver_0.getExpertInitManager().getInit());

    gridSequencingInit_0.setGSCfl(cfl_number_grid_sequencing);

    StepStoppingCriterion stepStoppingCriterion_0 = 
      ((StepStoppingCriterion) simulation_0.getSolverStoppingCriterionManager().getSolverStoppingCriterion("Maximum Steps"));

    IntegerValue integerValue_2 = 
      stepStoppingCriterion_0.getMaximumNumberStepsObject();

    integerValue_2.getQuantity().setValue(max_iter);

    // Reports and monitors

    ForceReport drag_report = 
      simulation_0.getReportManager().create("star.flow.ForceReport");

    drag_report.setPresentationName("Drag");

    drag_report.getParts().setQuery(null);

    // Region region_0 = 
    //   simulation_0.getRegionManager().getRegion("fluid");

    Boundary lower_surface = 
      region_0.getBoundaryManager().getBoundary("lower surface");

    Boundary upper_surface = 
      region_0.getBoundaryManager().getBoundary("upper surface");

    drag_report.getParts().setObjects(lower_surface, upper_surface);

    ForceReport lift_report = 
      simulation_0.getReportManager().create("star.flow.ForceReport");

    lift_report.setPresentationName("Lift");

    Units units_8 = 
      ((Units) simulation_0.getUnitsManager().getObject(""));

    lift_report.getDirection().setComponentsAndUnits(0.0, 1.0, 0.0, units_8);

    lift_report.getParts().setQuery(null);

    lift_report.getParts().setObjects(lower_surface, upper_surface);

    ExpressionReport lift_to_drag_report = 
      simulation_0.getReportManager().create("star.base.report.ExpressionReport");

    lift_to_drag_report.setPresentationName("L/D");

    Units units_9 = 
      simulation_0.getUnitsManager().getPreferredUnits(Dimensions.Builder().force(1).build());

    lift_to_drag_report.setDefinition("${Lift}/${Drag}");

    simulation_0.getMonitorManager().createMonitorAndPlot(new ArrayList<>(Arrays.<Report>asList(drag_report, lift_to_drag_report, lift_report)), false, "%1$s Plot");

    ReportMonitor reportMonitor_0 = 
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("Drag Monitor"));

    MonitorPlot monitorPlot_0 = 
      simulation_0.getPlotManager().createMonitorPlot(new ArrayList<>(Arrays.<Monitor>asList(reportMonitor_0)), "Drag Monitor Plot");

    // monitorPlot_0.openInteractive();

    ReportMonitor L_D_monitor = 
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("L/D Monitor"));

    MonitorPlot monitorPlot_1 = 
      simulation_0.getPlotManager().createMonitorPlot(new ArrayList<>(Arrays.<Monitor>asList(L_D_monitor)), "L/D Monitor Plot");

    // monitorPlot_1.openInteractive();

    ReportMonitor reportMonitor_2 = 
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("Lift Monitor"));

    MonitorPlot monitorPlot_2 = 
      simulation_0.getPlotManager().createMonitorPlot(new ArrayList<>(Arrays.<Monitor>asList(reportMonitor_2)), "Lift Monitor Plot");

    // monitorPlot_2.openInteractive();

    ElementCountReport cell_count = 
      simulation_0.getReportManager().create("star.base.report.ElementCountReport");

    cell_count.setPresentationName("Cell Count");

    cell_count.getParts().setQuery(null);

    // Boundary boundary_2 = 
    //   region_0.getBoundaryManager().getBoundary("farfield");

    Boundary symmetry = 
      region_0.getBoundaryManager().getBoundary("symmetry");

    // cell_count.getParts().setObjects(region_0, farfield, upper_surface, lower_surface, symmetry);
    cell_count.getParts().setObjects(region_0);
    ReportMonitor reportMonitor_3 = 
      cell_count.createMonitor();

    // Set stopping criteria for iteration (minimum based on number of refinements) and the asymptotic of L/D
    IterationMonitor iterationMonitor_0 = 
      ((IterationMonitor) simulation_0.getMonitorManager().getMonitor("Iteration"));

    MonitorIterationStoppingCriterion monitorIterationStoppingCriterion_0 = 
      simulation_0.getSolverStoppingCriterionManager().createIterationStoppingCriterion(iterationMonitor_0);

    ((MonitorIterationStoppingCriterionOption) monitorIterationStoppingCriterion_0.getCriterionOption()).setSelected(MonitorIterationStoppingCriterionOption.Type.MAXIMUM);
    Units units_10 = 
      ((Units) simulation_0.getUnitsManager().getObject(""));

    MonitorIterationStoppingCriterionMaxLimitType monitorIterationStoppingCriterionMaxLimitType_0 = 
      ((MonitorIterationStoppingCriterionMaxLimitType) monitorIterationStoppingCriterion_0.getCriterionType());

    monitorIterationStoppingCriterion_0.getLogicalOption().setSelected(SolverStoppingCriterionLogicalOption.Type.AND);

    monitorIterationStoppingCriterionMaxLimitType_0.getLimit().setValueAndUnits(n_refinements*amr_iter_frequency, units_10);

    // ReportMonitor L_D_monitor = 
    //   ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("L/D Monitor"));

    MonitorIterationStoppingCriterion monitorIterationStoppingCriterion_1 = 
      simulation_0.getSolverStoppingCriterionManager().createIterationStoppingCriterion(L_D_monitor);

    ((MonitorIterationStoppingCriterionOption) monitorIterationStoppingCriterion_1.getCriterionOption()).setSelected(MonitorIterationStoppingCriterionOption.Type.ASYMPTOTIC);

    monitorIterationStoppingCriterion_1.getLogicalOption().setSelected(SolverStoppingCriterionLogicalOption.Type.AND);

    MonitorIterationStoppingCriterionAsymptoticType monitorIterationStoppingCriterionAsymptoticType_0 = 
      ((MonitorIterationStoppingCriterionAsymptoticType) monitorIterationStoppingCriterion_1.getCriterionType());

    monitorIterationStoppingCriterionAsymptoticType_0.setEnableSamplingRefresh(true);

    monitorIterationStoppingCriterionAsymptoticType_0.getMaxWidth().setValueAndUnits(asymptotic_limit, units_10);

    monitorIterationStoppingCriterionAsymptoticType_0.setNumberSamples(n_samples);

    // Pressure coefficient
    PressureCoefficientFunction pressureCoefficientFunction_0 = 
      ((PressureCoefficientFunction) simulation_0.getFieldFunctionManager().getFunction("PressureCoefficient"));

    Units units_11 = 
      ((Units) simulation_0.getUnitsManager().getObject("kg/m^3"));

    pressureCoefficientFunction_0.getReferenceDensity().setValueAndUnits(ref_density, units_11);

    Units units_12 = 
      ((Units) simulation_0.getUnitsManager().getObject("m/s"));

    pressureCoefficientFunction_0.getReferenceVelocity().setValueAndUnits(velocity, units_12);
  
  // set up simulation operations
    simulation_0.get(SimDriverWorkflowManager.class).createSimDriverWorkflow("Simulation Operations");

    SimDriverWorkflow simDriverWorkflow_1 = 
    ((SimDriverWorkflow) simulation_0.get(SimDriverWorkflowManager.class).getObject("Simulation Operations 1"));

    simulation_0.get(SimDriverWorkflowManager.class).setSelectedWorkflow(simDriverWorkflow_1);

    simDriverWorkflow_1.getBlocks().createBlock("star.automation.MeshAutomationBlock", "Mesh");

    simDriverWorkflow_1.getBlocks().createBlock("star.automation.InitializeSolutionAutomationBlock", "Initialize Solution");

    simDriverWorkflow_1.getBlocks().createBlock("star.common.SolvePhysics", "Solve Physics");

    SolvePhysics solvePhysics_1 = 
      ((SolvePhysics) simDriverWorkflow_1.getBlocks().getObject("Solve Physics"));

    solvePhysics_1.getSimulationObjects().setQuery(null);

    // PhysicsContinuum physicsContinuum_0 = 
    //   ((PhysicsContinuum) simulation_0.getContinuumManager().getContinuum("Physics 1"));

    solvePhysics_1.getSimulationObjects().setObjects(physicsContinuum_0);

    simulation_0.saveState("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\min_setup\\"+save_filename+".sim");
  }
}
