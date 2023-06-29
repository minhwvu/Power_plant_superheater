import time as wall_clock
# Import Pyomo libraries
from pyomo.environ import minimize
import pyomo.environ as pyo
from pyomo.environ import units as pyunits
# from pyomo.core.expr.current import Expr_if

# Import IDAES core
from idaes.core import FlowsheetBlock
from idaes.generic_models.properties import iapws95
from idaes.power_generation.properties import FlueGasParameterBlock
from idaes.core.util.model_statistics import degrees_of_freedom
from idaes.core.util.initialization import initialize_by_time_element
from idaes.core.util.constants import Constants as const
import matplotlib.pyplot as plt
import idaes.logger as idaeslog

# from idaes.core.util.math import smooth_max, smooth_min
# from idaes.core.util.model_diagnostics import *
# from idaes.core.util.model_statistics import (large_residuals_set, number_large_residuals)

# Import non-standard aPSH models
# from aPSH_models import HeatExchangerCrossFlow2D
from boiler_heat_exchanger_2D_rev import HeatExchangerCrossFlow2D_Header

import pandas as plot_data
from pandas import ExcelWriter
from pandas import ExcelFile

import csv
import pandas as pd

def _new_solve(self, model, **kwargs):
    self.options["nlp_scaling_method"] = "user-scaling"
    self.options["linear_solver"] = "ma27"
    self.options["tol"] = 1e-6
    self.options['ma27_pivtol'] = 0.01
    self.options['ma27_pivtolmax'] = 0.6
    if kwargs["tee"]:
        print("THIS IPOPT SOLVER HAS BEEN MONKEY PATCHED FOR SCALING")
    #iscale.constraint_autoscale_large_jac(model, min_scale=1e-6)
    res = self._old_solve(model, **kwargs)
    return res

def monkey_patch_ipopt():
    from pyomo.solvers.plugins.solvers.IPOPT import IPOPT
    IPOPT._old_solve = IPOPT.solve
    IPOPT.solve = _new_solve

def undo_patch_ipopt():
	from pyomo.solvers.plugins.solvers.IPOPT import IPOPT
	IPOPT.solve = IPOPT._old_solve

# monkey_patch_ipopt()

# import data from excel
df_in10 = plot_data.read_excel(r'plant_data_10pct.xlsx',sheet_name ='full_cycle_10pct')
# df_in10 = plot_data.read_excel(r'plant_data_10pct_excel2003.xls',sheet_name ='full_cycle_10pct')
time_10pct = df_in10['time']
# print(time_10pct)

# For primary superheater
plot_data = {}
plot_data['time'] = []
plot_data['pressure_drop'] = []
plot_data['pres_fg_PSH_in'] = []
plot_data['pres_PSH_in'] = []
plot_data['PSH_flue_gas_flow_disc1'] = []
plot_data['PSH_flue_gas_flow_disc2'] = []
plot_data['PSH_flue_gas_flow_disc4'] = []
plot_data['PSH_flue_gas_flow_disc8'] = []
plot_data['PSH_flue_gas_flow_disc9'] = []
plot_data['PSH_steam_flow_disc1'] = []
plot_data['PSH_steam_flow_disc2'] = []
plot_data['PSH_steam_flow_disc4'] = []
plot_data['PSH_steam_flow_disc8'] = []
plot_data['PSH_steam_flow_disc9'] = []
plot_data['PSH_steam_temperature_disc1'] = []
plot_data['PSH_steam_temperature_disc2'] = []
plot_data['PSH_steam_temperature_disc4'] = []
plot_data['PSH_steam_temperature_disc8'] = []
plot_data['PSH_steam_temperature_disc9'] = []
plot_data['PSH_steam_pres_disc1'] = []
plot_data['PSH_steam_pres_disc2'] = []
plot_data['PSH_steam_pres_disc4'] = []
plot_data['PSH_steam_pres_disc8'] = []
plot_data['PSH_steam_pres_disc9'] = []
plot_data['PSH_temp_wall_tube_disc1'] = []
plot_data['PSH_temp_wall_tube_disc2'] = []
plot_data['PSH_temp_wall_tube_disc4'] = []
plot_data['PSH_temp_wall_tube_disc8'] = []
plot_data['PSH_temp_wall_tube_disc9'] = []
plot_data['PSH_temp_wall_shell_disc1'] = []
plot_data['PSH_temp_wall_shell_disc2'] = []
plot_data['PSH_temp_wall_shell_disc4'] = []
plot_data['PSH_temp_wall_shell_disc8'] = []
plot_data['PSH_temp_wall_shell_disc9'] = []
plot_data['PSH_temp_wall_shell_fouling_disc1'] = []
plot_data['PSH_temp_wall_shell_fouling_disc2'] = []
plot_data['PSH_temp_wall_shell_fouling_disc4'] = []
plot_data['PSH_temp_wall_shell_fouling_disc8'] = []
plot_data['PSH_temp_wall_shell_fouling_disc9'] = []
plot_data['PSH_flue_gas_temperature_disc1'] = []
plot_data['PSH_flue_gas_temperature_disc2'] = []
plot_data['PSH_flue_gas_temperature_disc4'] = []
plot_data['PSH_flue_gas_temperature_disc8'] = []
plot_data['PSH_flue_gas_temperature_disc9'] = []
plot_data['PSH_von_Mises_inside_disc1'] = []
plot_data['PSH_von_Mises_inside_disc2'] = []
plot_data['PSH_von_Mises_inside_disc4'] = []
plot_data['PSH_von_Mises_inside_disc8'] = []
plot_data['PSH_von_Mises_inside_disc9'] = []
plot_data['PSH_delta_s12_inside_disc1'] = []
plot_data['PSH_delta_s23_inside_disc1'] = []
plot_data['PSH_delta_s31_inside_disc1'] = []
plot_data['PSH_mech_circumferential_inside_disc1'] = []
plot_data['PSH_ther_circumferential_inside_disc1'] = []
plot_data['PSH_circumferential_inside_disc1'] = []
plot_data['PSH_mech_circumferential_inside_disc9'] = []
plot_data['PSH_ther_circumferential_inside_disc9'] = []
plot_data['PSH_circumferential_inside_disc9'] = []
plot_data['PSH_ther_circumferential_inside_disc2'] = []
plot_data['PSH_ther_circumferential_inside_disc4'] = []
plot_data['PSH_ther_circumferential_inside_disc8'] = []

# For primary superheater header
plot_data['PSH_header_inner_temperature'] = []
plot_data['PSH_header_outside_temperature'] = []
plot_data['PSH_header_circumferential_P1'] = []
plot_data['PSH_header_circumferential_P2'] = []
plot_data['PSH_header_circumferential_body'] = []
plot_data['PSH_header_von_Mises_P1'] = []
plot_data['PSH_header_von_Mises_P2'] = []
plot_data['PSH_header_rupture_time_P1'] = []
plot_data['PSH_header_rupture_time_P2'] = []

def max_value_find(data_export,n):
    max = data_export[0]
    for i in range(1,n):
        if data_export[i]>max:
            max = data_export[i]
    return max

def main():
    start_time = wall_clock.time()
    m = pyo.ConcreteModel()
    m.dynamic = True
    # time_set = [0,20,200]
    nstep = len(time_10pct) -1 
    # print(nstep)
    if m.dynamic:
        m.fs = FlowsheetBlock(default={"dynamic": True, "time_set": time_10pct})
    else:
        m.fs = FlowsheetBlock(default={"dynamic": False})
    # Add property packages to flowsheet library
    m.fs.prop_water = iapws95.Iapws95ParameterBlock()
    m.fs.prop_gas = FlueGasParameterBlock()
    m.fs.aPSH = HeatExchangerCrossFlow2D_Header(default={
                           "tube_side": {"property_package":
                                         m.fs.prop_water,
                                         "has_pressure_change": True},
                           "shell_side": {"property_package":
                                          m.fs.prop_gas,
                                          "has_pressure_change": True},
                           "finite_elements": 6,
                           "flow_type": "counter_current",
                           "tube_arrangement": "in-line",
                           "tube_side_water_phase": "Vap",
                           "has_radiation": True,
                           "radial_elements": 5,
                           #"tube_inner_diameter": 1.45*0.0254,
                           #"tube_thickness": 0.15*0.0254,
                           "has_header": True,
                           "header_radial_elements": 5,
                           "header_inner_diameter": 25*0.0254,
                           "header_wall_thickness": 1.312*0.0254})

    if m.dynamic:
        m.discretizer = pyo.TransformationFactory('dae.finite_difference')
        m.discretizer.apply_to(m,
                           nfe=nstep,
                           wrt=m.fs.config.time,
                           scheme='BACKWARD'
                           )

    m.fs.aPSH.pitch_x.fix(3.75*0.0254)
    m.fs.aPSH.pitch_y.fix(6.0*0.0254)
    m.fs.aPSH.tube_length_seg.fix(302.5*0.0254)
    m.fs.aPSH.tube_nseg.fix(9)
    m.fs.aPSH.tube_ncol.fix(88)
    m.fs.aPSH.tube_inlet_nrow.fix(4)
    m.fs.aPSH.delta_elevation.fix(5.0)
    m.fs.aPSH.tube_di.fix(1.45*0.0254)
    m.fs.aPSH.tube_thickness.fix(0.15*0.0254)
    m.fs.aPSH.therm_cond_wall = 49.0      # Carbon steel SA 209 T1 
    m.fs.aPSH.density_wall = 7800         # kg/m3
    m.fs.aPSH.cp_wall = 470               # J/kg-K    
    m.fs.aPSH.Young_modulus = 1.90e5
    m.fs.aPSH.Possion_ratio = 0.29
    m.fs.aPSH.coefficient_therm_expansion = 1.3e-5

    m.fs.aPSH.tube_r_fouling = 0.00017     #heat transfer resistance due to tube side fouling (water scales)
    m.fs.aPSH.shell_r_fouling = 0.00088    #heat transfer resistance due to shell side fouling (ash deposition)   
    m.fs.aPSH.emissivity_wall.fix(0.7)
    m.fs.aPSH.fcorrection_htc_tube.fix(1.02)  # original 1.04
    m.fs.aPSH.fcorrection_htc_shell.fix(1.02)  # original 1.04
    m.fs.aPSH.fcorrection_dp_tube.fix(15.6)
    m.fs.aPSH.fcorrection_dp_shell.fix(1.252764)
    m.fs.aPSH.temperature_ambient.fix(350)
    m.fs.aPSH.head_insulation_thickness.fix(0.025)
    
    # provide inputs from plantwide model
    # for t in m.fs.time:
    #     for j in range(1,len(time_10pct)):
    m.fs.aPSH.tube_inlet.flow_mol[:].value = df_in10['PSH_Steam_flow_in'][0]
    m.fs.aPSH.tube_inlet.pressure[:].value = df_in10['PSH_Steam_pres_in'][0]
    m.fs.aPSH.tube_inlet.flow_mol[:].fix()    
    m.fs.aPSH.tube_inlet.pressure[:].fix()
    m.fs.aPSH.tube_inlet.enth_mol[:].fix(pyo.value(iapws95.htpx(T= df_in10['PSH_Steam_temp_in'][0]*pyunits.K, P= df_in10['PSH_Steam_pres_in'][0]*pyunits.Pa)))

    m.fs.aPSH.shell_inlet.flow_mol_comp[:,"H2O"].value = df_in10['PSH_FG_H2O_flow_in'][0]
    m.fs.aPSH.shell_inlet.flow_mol_comp[:,"CO2"].value = df_in10['PSH_FG_CO2_flow_in'][0]
    m.fs.aPSH.shell_inlet.flow_mol_comp[:,"N2"].value = df_in10['PSH_FG_N2_flow_in'][0]
    m.fs.aPSH.shell_inlet.flow_mol_comp[:,"O2"].value = df_in10['PSH_FG_O2_flow_in'][0]
    m.fs.aPSH.shell_inlet.flow_mol_comp[:,"SO2"].value = df_in10['PSH_FG_SO2_flow_in'][0]
    m.fs.aPSH.shell_inlet.flow_mol_comp[:,"NO"].value = df_in10['PSH_FG_NO_flow_in'][0]
    m.fs.aPSH.shell_inlet.temperature[:].value = df_in10['PSH_FG_temp_in'][0]
    m.fs.aPSH.shell_inlet.pressure[:].value = df_in10['PSH_FG_pres_in'][0]
    
    m.fs.aPSH.shell_inlet.flow_mol_comp[:,"H2O"].fix()
    m.fs.aPSH.shell_inlet.flow_mol_comp[:,"CO2"].fix()
    m.fs.aPSH.shell_inlet.flow_mol_comp[:,"N2"].fix()
    m.fs.aPSH.shell_inlet.flow_mol_comp[:,"O2"].fix()
    m.fs.aPSH.shell_inlet.flow_mol_comp[:,"SO2"].fix()
    m.fs.aPSH.shell_inlet.flow_mol_comp[:,"NO"].fix()
    m.fs.aPSH.shell_inlet.temperature[:].fix()
    m.fs.aPSH.shell_inlet.pressure[:].fix()
    
    if m.dynamic:
        m.fs.aPSH.set_initial_condition()

    m.fs.aPSH.initialize(outlvl=4)
    print('dof after initialization:', degrees_of_freedom(m.fs))

    
    # Integer indexing for time domain
    m.fs.time_index = pyo.Param(m.fs.time,
                         initialize=1, mutable=True,
                         doc="Integer Indexing for Time Domain")
    for index_t, value_t in enumerate(m.fs.time, 1):
        m.fs.time_index[value_t] = index_t
    
    # for t in m.fs.time:
    #     print(t)
    #     print('value of t {} with index {}'.format(t, m.fs.time_index[t].value))
    t = 0
    # print(time_10pct)

    if m.dynamic:
        for t in m.fs.time:
            # t += 30
            # print(t)
            j = m.fs.time_index[t].value - 1
            # print('value of t {} with index {}'.format(t, m.fs.time_index[t].value))
            m.fs.aPSH.tube_inlet.flow_mol[t].value = df_in10['PSH_Steam_flow_in'][j]
            m.fs.aPSH.tube_inlet.pressure[t].value = df_in10['PSH_Steam_pres_in'][j]
            m.fs.aPSH.tube_inlet.flow_mol[t].fix()    
            m.fs.aPSH.tube_inlet.pressure[t].fix()
            m.fs.aPSH.tube_inlet.enth_mol[t].fix(
                iapws95.htpx(T= df_in10['PSH_Steam_temp_in'][j]*pyunits.K, P= df_in10['PSH_Steam_pres_in'][j]*pyunits.Pa))

            m.fs.aPSH.shell_inlet.flow_mol_comp[t,"H2O"].value = df_in10['PSH_FG_H2O_flow_in'][j]
            m.fs.aPSH.shell_inlet.flow_mol_comp[t,"CO2"].value = df_in10['PSH_FG_CO2_flow_in'][j]
            m.fs.aPSH.shell_inlet.flow_mol_comp[t,"N2"].value = df_in10['PSH_FG_N2_flow_in'][j]
            m.fs.aPSH.shell_inlet.flow_mol_comp[t,"O2"].value = df_in10['PSH_FG_O2_flow_in'][j]
            m.fs.aPSH.shell_inlet.flow_mol_comp[t,"SO2"].value = df_in10['PSH_FG_SO2_flow_in'][j]
            m.fs.aPSH.shell_inlet.flow_mol_comp[t,"NO"].value = df_in10['PSH_FG_NO_flow_in'][j]
            m.fs.aPSH.shell_inlet.temperature[t].value = df_in10['PSH_FG_temp_in'][j]
            m.fs.aPSH.shell_inlet.pressure[t].value = df_in10['PSH_FG_pres_in'][j]
            
            m.fs.aPSH.shell_inlet.flow_mol_comp[t,"H2O"].fix()
            m.fs.aPSH.shell_inlet.flow_mol_comp[t,"CO2"].fix()
            m.fs.aPSH.shell_inlet.flow_mol_comp[t,"N2"].fix()
            m.fs.aPSH.shell_inlet.flow_mol_comp[t,"O2"].fix()
            m.fs.aPSH.shell_inlet.flow_mol_comp[t,"SO2"].fix()
            m.fs.aPSH.shell_inlet.flow_mol_comp[t,"NO"].fix()
            m.fs.aPSH.shell_inlet.temperature[t].fix()
            m.fs.aPSH.shell_inlet.pressure[t].fix()

    
    solver = pyo.SolverFactory("ipopt")
    solver.options = {
            "tol": 1e-6,
            "linear_solver": "ma27",
            "max_iter": 150,
            "bound_push": 1e-10,
    }
    

    if m.dynamic:
        initialize_by_time_element(m.fs, m.fs.time, solver=solver,
                outlvl=idaeslog.INFO)
        print('dof after integrating:', degrees_of_freedom(m.fs))

    print()
    print('************************************************************')
    print('Run dynamic simulation')
    results = solver.solve(m, tee=False)

    end_time_dyn = wall_clock.time()
    time_dyn_used = end_time_dyn - start_time
    print("computational time of dynamic simulation =", time_dyn_used)

    # Print results
    print(results)

    # metal_mass = pyo.value(m.fs.aPSH.density_wall*m.fs.aPSH.area_wall_seg*m.fs.aPSH.tube_length_seg)
    # metal_mass_base = pyo.value(const.pi*m.fs.aPSH.density_wall*m.fs.aPSH.tube_thickness*(
    #     m.fs.aPSH.tube_thickness+m.fs.aPSH.tube_di)*m.fs.aPSH.tube_ncol*m.fs.aPSH.tube_inlet_nrow*m.fs.aPSH.tube_length_seg)
    
    # record desired outlet enthalpy
    enthalpy_desired = []
    for t in m.fs.time:
        enthalpy_desired.append(pyo.value(m.fs.aPSH.tube_outlet.enth_mol[t]))
    ########################################################################################################
    
    # optimization
    print()
    print('********************************************************************')
    print('Run dynamic optimization')

    # unfix variables
    # continuous decision variables
    # case 4: tube thickness + diameter + length
    # m.fs.aPSH.tube_thickness.fix(0.15*0.0254)
    m.fs.aPSH.tube_thickness.unfix()
    m.fs.aPSH.tube_thickness.setlb(0.15*0.0254*0.85)
    m.fs.aPSH.tube_thickness.setub(0.15*0.0254*1.15)

    # m.fs.aPSH.tube_di.fix(1.45*0.0254)
    m.fs.aPSH.tube_di.unfix()
    m.fs.aPSH.tube_di.setlb(1.45*0.0254*0.90)
    m.fs.aPSH.tube_di.setub(1.45*0.0254*1.10)

    # m.fs.aPSH.tube_length_seg.value = 302.5*0.0254
    m.fs.aPSH.tube_length_seg.unfix()
    m.fs.aPSH.tube_length_seg.setlb(302.5*0.0254*0.891) # reduce from 0.8 to 0.5
    m.fs.aPSH.tube_length_seg.setub(302.5*0.0254*1.109)

    # case5: continuous + discrete variables
    # m.fs.aPSH.tube_ncol.fix(88)
    m.fs.aPSH.tube_ncol.unfix()
    m.fs.aPSH.tube_ncol.setlb(80)
    m.fs.aPSH.tube_ncol.setub(96)

    # m.fs.aPSH.tube_inlet_nrow.fix(4)
    m.fs.aPSH.tube_inlet_nrow.unfix()
    m.fs.aPSH.tube_inlet_nrow.setlb(2)
    m.fs.aPSH.tube_inlet_nrow.setub(5)
    
    print('provide constraints')
    steam_outlet_sp = 700.42
    delta_t = 12.5
    temp_ub = steam_outlet_sp + delta_t
    temp_lb = steam_outlet_sp - delta_t

    #sigma_max = 78 # MPa (Referenced from NIMS data, @ 500 degree C at 200000 h
    # sigma_max = 75.95 # max stress was obtained from base case
    # vary stress constraints 70, 60 MPa to find out what would be the min bound
    # on stress, which will be the value at the current operating pressure, 
    # i.e. only due to mechanical stress - by designing these systems 
    # only thing we are trying to to lower is the thermal stress not mechanical stress
    # because mechanical stress is due to pressure that depends on the sliding pressure
    # operation of the plant
    # max stress
    sigma_max_base = 76.0706 # max stress was obtained from base case
    delta_sigma = 0.001
    stress_ub = sigma_max_base - delta_sigma

    @m.fs.Constraint(m.fs.time)
    def steam_outlet_temperature_con1(b, t):
        return 1e-2*b.aPSH.tube.properties[t, 0].temperature  <= 1e-2*temp_ub
        
    @m.fs.Constraint(m.fs.time)
    def steam_outlet_temperature_con2(b, t):
        return 1e-2*b.aPSH.tube.properties[t, 0].temperature  >= 1e-2*temp_lb

    '''
    # define variable to calculate the maximum stress of superheater
    m.fs.tube_max_stress = pyo.Var(m.fs.time, m.fs.aPSH.tube.length_domain)

    @m.fs.Constraint(m.fs.time, m.fs.aPSH.tube.length_domain,
                              doc="maximum SH tube wall stress")
    def cum_max_stress_eqn(b, t, x):
        if t == m.fs.time.first():
           return 1e-5*b.tube_max_stress[t, x] == 1e-5*b.aPSH.sigma_von_Mises[t, x, b.aPSH.r.first()]
        else:
           t_prev = m.fs.time.prev(t)
           return 1e-5*b.tube_max_stress[t, x] == 1e-5*smooth_max(
            b.tube_max_stress[t_prev, x], b.aPSH.sigma_von_Mises[t, x, b.aPSH.r.first()])

    @m.fs.Constraint(m.fs.time, m.fs.aPSH.tube.length_domain)
    def max_stress_constraint(b, t, x):
        return 1e-5*b.tube_max_stress[t, x]  <=  1e-5*stress_ub
	'''
    @m.fs.Constraint(m.fs.time, m.fs.aPSH.tube.length_domain)
    def max_stress_constraint(b, t, x):
        return 1e-5*b.aPSH.sigma_von_Mises[t, x, b.aPSH.r.first()]  <=  1e-5*stress_ub

    # add another constraint for fixing outlet enthalpy of steam   
    @m.fs.Constraint(m.fs.time)
    def outlet_enthalpy_cons(b, t):
        j = m.fs.time_index[t].value - 1
        return (b.aPSH.tube_outlet.enth_mol[t] - enthalpy_desired[j])**2 <= 1e6

    # set objective function
    # m.fs.metal_mass = m.fs.aPSH.density_wall*m.fs.aPSH.area_wall_seg*m.fs.aPSH.tube_length_seg
    # maximize delta_mass
    metal_mass_base = 10261.8
    m.obj = pyo.Objective(expr= const.pi*m.fs.aPSH.density_wall*m.fs.aPSH.tube_thickness*(
        m.fs.aPSH.tube_thickness+m.fs.aPSH.tube_di)*m.fs.aPSH.tube_ncol*m.fs.aPSH.tube_inlet_nrow*m.fs.aPSH.tube_length_seg/metal_mass_base) # minimize = +1, maximize = -1

    # undo patch ipopt 
    # undo_patch_ipopt()

    # call solver
    solver = pyo.SolverFactory("ipopt")
    solver.options['bound_push'] = 1e-10
    solver.options['warm_start_init_point'] = 'yes'
    solver.options['max_iter'] = 150
    results = solver.solve(m, tee=True)
    print(results)

    end_time_opt = wall_clock.time()
    time_opt_used = end_time_opt - start_time
    print("computational time of dynamic optimization =", time_opt_used)
    metal_mass_opt = pyo.value(const.pi*m.fs.aPSH.density_wall*m.fs.aPSH.tube_thickness*(
        m.fs.aPSH.tube_thickness+m.fs.aPSH.tube_di)*m.fs.aPSH.tube_ncol*m.fs.aPSH.tube_inlet_nrow*m.fs.aPSH.tube_length_seg)

    @m.fs.Expression(m.fs.time, doc='total pressure drop in tube side')
    def total_pressure_drop(b, t):
        return -(sum(b.aPSH.tube.deltaP[t, x] for x in b.aPSH.tube.length_domain) - b.aPSH.tube.deltaP[t, b.aPSH.tube.length_domain.last()])*(
            b.aPSH.tube_nseg * b.aPSH.tube_length_seg)/b.aPSH.config.finite_elements

    # print residuals term
    # print(number_large_residuals(m, tol=1e-6))
    # print(large_residuals_set(m, tol=1e-6))

    # # Create Degeneracy Hunter object
    # dh = DegeneracyHunter(m) 

    # # Find constraints with residuals > 0.1 
    # initial_point_constraints = dh.check_residuals(tol=1e-6)

    # # Check no constraints are near their bounds
    # solution_bounds = dh.check_variable_bounds(tol=1e-6)

    # 
    # with open('output.txt', 'w') as FILE:
    #     m.pprint(ostream=FILE)
    
    # ******************************************************************************************************
    
    col = [
        "status",
        "time",
        "tube_length_per_segment",
        "number_of_tube_columns",
        "number_of_inlet_tube_row",
        "tube_thickness",
        "tube_inside_diameter",
        # "pitch_x",
        # "pitch_y",
        # "pitch_x_to_do",
        # "pitch_y_to_do",
        # "enthalpy_desired",
        # "metal_mass_base",
        "metal_mass_opt",
        # "steam_outlet_temperature",
        # "max_stress",
    ]
    
    # Data frame to tabulate results
    df_val = pd.DataFrame(columns=col, index=m.fs.time_index)

    for t in m.fs.time:
        df_val.loc[t]["status"] = results
        df_val.loc[t]["time"] = t
        df_val.loc[t]["tube_length_per_segment"] = pyo.value(m.fs.aPSH.tube_length_seg)
        df_val.loc[t]["number_of_tube_columns"] = m.fs.aPSH.tube_ncol.value
        df_val.loc[t]["number_of_inlet_tube_row"] = m.fs.aPSH.tube_inlet_nrow.value
        df_val.loc[t]["tube_thickness"] = pyo.value(m.fs.aPSH.tube_thickness)
        df_val.loc[t]["tube_inside_diameter"] = pyo.value(m.fs.aPSH.tube_di)
        # df_val.loc[t]["pitch_x"] = pyo.value(m.fs.aPSH.pitch_x)
        # df_val.loc[t]["pitch_y"] = pyo.value(m.fs.aPSH.pitch_y)
        # df_val.loc[t]["pitch_x_to_do"] = pyo.value(m.fs.aPSH.pitch_x_to_do)
        # df_val.loc[t]["pitch_y_to_do"] = pyo.value(m.fs.aPSH.pitch_y_to_do)
        # df_val.loc[t]["enthalpy_desired"] = pyo.value(m.fs.aPSH.tube_outlet.enth_mol[t])
        # df_val.loc[t]["metal_mass_base"] = metal_mass_base
        df_val.loc[t]["metal_mass_opt"] = metal_mass_opt
        # df_val.loc[t]["steam_outlet_temperature"] = pyo.value(m.fs.aPSH.tube.properties[t, 0].temperature)
        # df_val.loc[t]["max_stress"] = pyo.value(m.fs.tube_max_stress[t, 1])
        # df_val.loc[t]["max_stress"] = pyo.value(m.fs.aPSH.sigma_von_Mises[t, 1, m.fs.aPSH.r.first()])

        df_val.to_csv(f"opt_metal_mass_case3_cycles.csv")

    
    # append data
    # For primary superheater
    for t in m.fs.time:
        if t==0 and len(plot_data['time'])>0:
            continue
        plot_data['time'].append(t)
        plot_data['pressure_drop'].append(pyo.value(m.fs.total_pressure_drop[t]))
        plot_data['pres_fg_PSH_in'].append(
            m.fs.aPSH.shell_inlet.pressure[t].value)
        plot_data['pres_PSH_in'].append(
            pyo.value(m.fs.aPSH.tube
                      .properties[t, 1].pressure))
        plot_data['PSH_flue_gas_flow_disc1'].append(
            pyo.value(m.fs.aPSH.shell.properties[t, 0].flow_mol))
        plot_data['PSH_flue_gas_flow_disc2'].append(
            pyo.value(m.fs.aPSH.shell.properties[t, 0.166667].flow_mol))
        plot_data['PSH_flue_gas_flow_disc4'].append(
            pyo.value(m.fs.aPSH.shell.properties[t, 0.5].flow_mol))
        plot_data['PSH_flue_gas_flow_disc8'].append(
            pyo.value(m.fs.aPSH.shell.properties[t, 0.666667].flow_mol))
        plot_data['PSH_flue_gas_flow_disc9'].append(
            pyo.value(m.fs.aPSH.shell.properties[t, 1].flow_mol))
        plot_data['PSH_steam_flow_disc1'].append(
            pyo.value(m.fs.aPSH.tube.properties[t, 0].flow_mol))
        plot_data['PSH_steam_flow_disc2'].append(
            pyo.value(m.fs.aPSH.tube.properties[t, 0.166667].flow_mol))
        plot_data['PSH_steam_flow_disc4'].append(
            pyo.value(m.fs.aPSH.tube.properties[t, 0.5].flow_mol))
        plot_data['PSH_steam_flow_disc8'].append(
            pyo.value(m.fs.aPSH.tube.properties[t, 0.666667].flow_mol))
        plot_data['PSH_steam_flow_disc9'].append(
            pyo.value(m.fs.aPSH.tube.properties[t, 1].flow_mol))
        plot_data['PSH_steam_temperature_disc1'].append(
            pyo.value(m.fs.aPSH.tube.properties[t, 0].temperature))
        plot_data['PSH_steam_temperature_disc2'].append(
            pyo.value(m.fs.aPSH.tube
                      .properties[t, 0.166667].temperature))
        plot_data['PSH_steam_temperature_disc4'].append(
            pyo.value(m.fs.aPSH.tube
                      .properties[t, 0.5].temperature))
        plot_data['PSH_steam_temperature_disc8'].append(
            pyo.value(m.fs.aPSH.tube
                      .properties[t, 0.833333].temperature))
        plot_data['PSH_steam_temperature_disc9'].append(
            pyo.value(m.fs.aPSH.tube.properties[t, 1].temperature))
        plot_data['PSH_steam_pres_disc1'].append(
            pyo.value(m.fs.aPSH.tube.properties[t, 0].pressure))
        plot_data['PSH_steam_pres_disc2'].append(
            pyo.value(m.fs.aPSH.tube
                      .properties[t, 0.166667].pressure))
        plot_data['PSH_steam_pres_disc4'].append(
            pyo.value(m.fs.aPSH.tube
                      .properties[t, 0.5].pressure))
        plot_data['PSH_steam_pres_disc8'].append(
            pyo.value(m.fs.aPSH.tube
                      .properties[t, 0.833333].pressure))
        plot_data['PSH_steam_pres_disc9'].append(
            pyo.value(m.fs.aPSH.tube.properties[t, 1].pressure))
        plot_data['PSH_temp_wall_tube_disc1'].append(
            pyo.value(m.fs.aPSH.tube_wall_temperature
                      [t, 0, m.fs.aPSH.r.first()]))
        plot_data['PSH_temp_wall_tube_disc2'].append(
            pyo.value(m.fs.aPSH.tube_wall_temperature
                      [t, 0.166667, m.fs.aPSH.r.first()]))
        plot_data['PSH_temp_wall_tube_disc4'].append(
            pyo.value(m.fs.aPSH.tube_wall_temperature
                      [t, 0.5, m.fs.aPSH.r.first()]))
        plot_data['PSH_temp_wall_tube_disc8'].append(
            pyo.value(m.fs.aPSH.tube_wall_temperature
                      [t, 0.833333, m.fs.aPSH.r.first()]))
        plot_data['PSH_temp_wall_tube_disc9'].append(
            pyo.value(m.fs.aPSH.tube_wall_temperature
                      [t, 1, m.fs.aPSH.r.first()]))
        plot_data['PSH_temp_wall_shell_disc1'].append(
            pyo.value(m.fs.aPSH.tube_wall_temperature
                      [t, 0, m.fs.aPSH.r.last()]))
        plot_data['PSH_temp_wall_shell_disc2'].append(
            pyo.value(m.fs.aPSH.tube_wall_temperature
                      [t, 0.166667, m.fs.aPSH.r.last()]))
        plot_data['PSH_temp_wall_shell_disc4'].append(
            pyo.value(m.fs.aPSH.tube_wall_temperature
                      [t, 0.5, m.fs.aPSH.r.last()]))
        plot_data['PSH_temp_wall_shell_disc8'].append(
            pyo.value(m.fs.aPSH.tube_wall_temperature
                      [t, 0.833333, m.fs.aPSH.r.last()]))
        plot_data['PSH_temp_wall_shell_disc9'].append(
            pyo.value(m.fs.aPSH.tube_wall_temperature
                      [t, 1, m.fs.aPSH.r.last()]))
        plot_data['PSH_temp_wall_shell_fouling_disc1'].append(
            pyo.value(m.fs.aPSH.shell_wall_temperature[t, 0]))
        plot_data['PSH_temp_wall_shell_fouling_disc2'].append(
            pyo.value(m.fs.aPSH.shell_wall_temperature
                      [t, 0.166667]))
        plot_data['PSH_temp_wall_shell_fouling_disc4'].append(
            pyo.value(m.fs.aPSH.shell_wall_temperature[t, 0.5]))
        plot_data['PSH_temp_wall_shell_fouling_disc8'].append(
            pyo.value(m.fs.aPSH.shell_wall_temperature
                      [t, 0.833333]))
        plot_data['PSH_temp_wall_shell_fouling_disc9'].append(
            pyo.value(m.fs.aPSH.shell_wall_temperature[t, 1]))
        plot_data['PSH_flue_gas_temperature_disc1'].append(
            pyo.value(m.fs.aPSH.shell
                      .properties[t, 0].temperature))
        plot_data['PSH_flue_gas_temperature_disc2'].append(
            pyo.value(m.fs.aPSH.shell
                      .properties[t, 0.166667].temperature))
        plot_data['PSH_flue_gas_temperature_disc4'].append(
            pyo.value(m.fs.aPSH.shell
                      .properties[t, 0.5].temperature))
        plot_data['PSH_flue_gas_temperature_disc8'].append(
            pyo.value(m.fs.aPSH.shell
                      .properties[t, 0.833333].temperature))
        plot_data['PSH_flue_gas_temperature_disc9'].append(
            pyo.value(m.fs.aPSH.shell
                      .properties[t, 1].temperature))
        plot_data['PSH_von_Mises_inside_disc1'].append(
            pyo.value(m.fs.aPSH.sigma_von_Mises
                      [t, 0, m.fs.aPSH.r.first()]))
        plot_data['PSH_von_Mises_inside_disc2'].append(
            pyo.value(m.fs.aPSH.sigma_von_Mises
                      [t, 0.166667, m.fs.aPSH.r.first()]))
        plot_data['PSH_von_Mises_inside_disc4'].append(
            pyo.value(m.fs.aPSH.sigma_von_Mises
                      [t, 0.5, m.fs.aPSH.r.first()]))
        plot_data['PSH_von_Mises_inside_disc8'].append(
            pyo.value(m.fs.aPSH.sigma_von_Mises
                      [t, 0.833333, m.fs.aPSH.r.first()]))
        plot_data['PSH_von_Mises_inside_disc9'].append(
            pyo.value(m.fs.aPSH.sigma_von_Mises
                      [t, 1, m.fs.aPSH.r.first()]))
        plot_data['PSH_delta_s12_inside_disc1'].append(
            pyo.value(m.fs.aPSH.delta_sigma_r_theta
                      [t, 0, m.fs.aPSH.r.first()]))
        plot_data['PSH_delta_s23_inside_disc1'].append(
            pyo.value(m.fs.aPSH.delta_sigma_theta_z
                      [t, 0, m.fs.aPSH.r.first()]))
        plot_data['PSH_delta_s31_inside_disc1'].append(
            pyo.value(m.fs.aPSH.delta_sigma_z_r
                      [t, 0, m.fs.aPSH.r.first()]))
        plot_data['PSH_mech_circumferential_inside_disc1'].append(
            pyo.value(m.fs.aPSH.mech_sigma_theta
                      [t, 0, m.fs.aPSH.r.first()]))
        plot_data['PSH_ther_circumferential_inside_disc1'].append(
            pyo.value(m.fs.aPSH.therm_sigma_theta
                      [t, 0, m.fs.aPSH.r.first()]))
        plot_data['PSH_circumferential_inside_disc1'].append(
            pyo.value(m.fs.aPSH.sigma_theta
                      [t, 0, m.fs.aPSH.r.first()]))
        plot_data['PSH_mech_circumferential_inside_disc9'].append(
            pyo.value(m.fs.aPSH.mech_sigma_theta
                      [t, 1, m.fs.aPSH.r.first()]))
        plot_data['PSH_ther_circumferential_inside_disc9'].append(
            pyo.value(m.fs.aPSH.therm_sigma_theta
                      [t, 1, m.fs.aPSH.r.first()]))
        plot_data['PSH_circumferential_inside_disc9'].append(
            pyo.value(m.fs.aPSH.sigma_theta
                      [t, 1, m.fs.aPSH.r.first()]))
        plot_data['PSH_ther_circumferential_inside_disc2'].append(
            pyo.value(m.fs.aPSH.therm_sigma_theta
                      [t, 0.166667, m.fs.aPSH.r.first()]))
        plot_data['PSH_ther_circumferential_inside_disc4'].append(
            pyo.value(m.fs.aPSH.therm_sigma_theta
                      [t, 0.5, m.fs.aPSH.r.first()]))
        plot_data['PSH_ther_circumferential_inside_disc8'].append(
            pyo.value(m.fs.aPSH.therm_sigma_theta
                      [t, 0.666667, m.fs.aPSH.r.first()]))

        # For primary superheater header
        plot_data['PSH_header_inner_temperature'].append(
            pyo.value(m.fs.aPSH.header_wall_temperature
                      [t, m.fs.aPSH.head_r.first()]))
        plot_data['PSH_header_outside_temperature'].append(
            pyo.value(m.fs.aPSH.header_wall_temperature
                      [t, m.fs.aPSH.head_r.last()]))
        plot_data['PSH_header_circumferential_P1'].append(
            pyo.value(m.fs.aPSH.sigma_theta_P1[t]))
        plot_data['PSH_header_circumferential_P2'].append(
            pyo.value(m.fs.aPSH.sigma_theta_P2[t]))
        plot_data['PSH_header_circumferential_body'].append(
            pyo.value(m.fs.aPSH.sigma_theta_header
                      [t, m.fs.aPSH.head_r.first()]))
        plot_data['PSH_header_von_Mises_P1'].append(
            pyo.value(m.fs.aPSH.sigma_eff_P1[t]))
        plot_data['PSH_header_von_Mises_P2'].append(
            pyo.value(m.fs.aPSH.sigma_eff_P2[t]))
        plot_data['PSH_header_rupture_time_P1'].append(
            pyo.value(m.fs.aPSH.rupture_time_crotch_corner[t]))
        plot_data['PSH_header_rupture_time_P2'].append(
            pyo.value(m.fs.aPSH.rupture_time_P2[t]))

    write_data_to_txt_file(plot_data)
    
    return m

def write_data_to_txt_file(plot_data):
    # write data to file
    ntime = len(plot_data['time'])
    ncount = len(plot_data)
    icount = 0
    with open("SH_opt_metal_mass_case3_cycles.txt","w") as fout:
        # write headings
        for k in plot_data:
            icount += 1
            fout.write(k)
            if icount<ncount:
                fout.write("\t")
            else:
                fout.write("\n")
        # write values
        for i in range(ntime):
            icount = 0
            for k in plot_data:
                icount += 1
                fout.write(str(plot_data[k][i]))
                if icount<ncount:
                    fout.write("\t")
                else:
                    fout.write("\n")

if __name__ == "__main__":
    m = main()