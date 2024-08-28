// Simcenter STAR-CCM+ macro: set_alpha_neg_2_5.java
// Written by Simcenter STAR-CCM+ 19.02.009
package macro;

import java.util.*;


import star.common.*;
import star.base.neo.*;
import star.flow.*;

public class waverider_6_alpha_pos_2_5 extends StarMacro {

  String save_filename="waverider_6_alpha_pos_2_5";
  
  public void execute() {
    execute0();

  }

  private void execute0() {

    Simulation simulation_0 = 
      getActiveSimulation();

    Region region_0 = 
      simulation_0.getRegionManager().getRegion("fluid");

    Boundary boundary_0 = 
      region_0.getBoundaryManager().getBoundary("farfield");

    FlowDirectionProfile flowDirectionProfile_0 = 
      boundary_0.getValues().get(FlowDirectionProfile.class);

    Units units_0 = 
      ((Units) simulation_0.getUnitsManager().getObject(""));

    flowDirectionProfile_0.getMethod(ConstantVectorProfileMethod.class).getQuantity().setComponentsAndUnits(0.999048, 0.0436194, 0.0, units_0);

    simulation_0.saveState("C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\optimisation_new\\Stability Analysis\\alpha_pos_2_5\\setup_files\\"+save_filename+".sim");
  }

}
