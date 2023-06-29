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

    # Print results
    print(results)

    end_time_dyn = wall_clock.time()
    time_dyn_used = end_time_dyn - start_time
    print("computational time of dynamic simulation =", time_dyn_used)

    print('*******************************************************************************')
    print('Estimate number of cycles')

    # adding allowable cycles constraint
    data_sigma = []
    data_temp = []
    for t in m.fs.time:
        data_sigma.append(pyo.value(m.fs.aPSH.sigma_von_Mises[t, 0, m.fs.aPSH.r.first()]))
        data_temp.append(pyo.value(m.fs.aPSH.tube_wall_temperature[t, 0, m.fs.aPSH.r.first()]))

    n = len(data_sigma)

    def max_value_find(data_export,n):
      max = data_export[0]
      for i in range(1,n):
          if data_export[i]>max:
              max = data_export[i]
      return max

    def min_value_find(data_export,n):
      min = data_export[0]
      for i in range(1,n):
          if data_export[i]<min:
              min = data_export[i]
      return min

    Ans_max = max_value_find(data_sigma,n)
    Ans_min = min_value_find(data_sigma,n)

    # known parameters
    delta_sigma =  (Ans_max-Ans_min)            # equivalent structural stress range (linear distribution) [N/mm2]
    sigma_mean =  0.5*(Ans_max+Ans_min)         # mean stress
    delta_sigma_D =  273             # the thermal endurance limit, Table 18.10, EN 13445, page 502,  Carbon steel SA 209 T1
    Rm = 380                    # Tensile strength [N/mm2]
    Rp = 205                    # the yield strength of material
    K_t =  3.0                  # Theoretical stress correction factor
    Rz = 50                     # the peak-to-valley height (micrometer), 50 for machine, 10 for ground, free of notches

    RO = 0.5*m.fs.aPSH.tube_di.value + m.fs.aPSH.tube_thickness.value
    RI = 0.5*m.fs.aPSH.tube_di.value

    # Maximum stress calculation
    sigma_max = sigma_mean + 0.5*delta_sigma

    if Rm <= 500:
      A0 = 0.4 # for Rm <= 500 MPa and for all austenitic steels
    elif (Rm>500 and Rm <=800):
      A0 = 0.4+(Rm-500)/3000
    elif (Rm>800 and Rm <=1000):
      A0 = 0.5

    #calculate k_e
    if delta_sigma > 2*Rp:
      k_e = 1+A0*(delta_sigma/(2*Rp)-1)               # For other steels
    else:
      k_e= 1 

    # calculate kv
    if delta_sigma > 2*Rp:
      k_v= max(1, pyo.value(0.7/(0.5+0.4/(delta_sigma/Rp))))      
    else:
      k_v= 1 

    # Equivalent stress range
    """
    For any component, if the calculated pseudo-elastic structural stress range for both welded joints and unwelded
    parts exceeds twice the yield strength of the material under consideration, i.e. if Δσ eq,l > 2Rp0,2/T* , see note, it shall
    be multiplied by a plasticity correction factor. The correction factor to be applied to the stress range of mechanical
    origin is ke and to the stress range of thermal origin is kν.
    """
    delta_sigma_eq =delta_sigma * k_e * k_v

    # Correction factors
    # Calculate temperature correction factor
    @m.fs.Expression()
    def f_T(m):
        T_max = max_value_find(data_temp,n) -273.15  # (620.47-273.15)                # the metal temperature during the moment of the highest stress [C]
        T_min = min_value_find(data_temp,n) -273.15  #(594.88-273.15)                # the metal temperature during the moment of lowest stress [C]
        return 1.03 - 1.5E-4*(0.75*T_max+0.25*T_min)-1.5E-6*(0.75*T_max+0.25*T_min)**2

    # f_T = 1.03 - 1.5E-4*(0.75*T_max+0.25*T_min)-1.5E-6*(0.75*T_max+0.25*T_min)**2     # for other steels
    # f_T = 1.043 - 4.3E-4*(0.75*T_max+0.25*T_min)                                        # for austenitic steels

    #initialise N and delta_sigma_R
    delta_sigma_R = 140
    initial_cycle = 7.686e8

    m.fs.delta_sigma_R = pyo.Var(initialize=delta_sigma_R)
    m.fs.allowable_cycles = pyo.Var(initialize=initial_cycle)

    # calcualte effective stress concentration factor
    @m.fs.Expression()
    def K_f(m):  
        if pyo.value(m.allowable_cycles - 2E6) <= 0:
            return 1+1.5*(K_t-1)/(1+0.5*max(1,(pyo.value(K_t*delta_sigma_eq/delta_sigma_D))))
        # If N > 2e6: delta_sigma_D = delta_sigma_R
        else:
            return 1+1.5*(K_t-1)/(1+0.5*max(1,(pyo.value(K_t*delta_sigma_eq/m.delta_sigma_R))))

    # calculate effective total stress range
    @m.fs.Expression()
    def delta_sigma_f(m):
        return m.K_f * delta_sigma_eq

    # Calculate surface finish correction factor
    @m.fs.Expression()
    def f_s(m):
        if pyo.value(m.allowable_cycles - 2E6) <= 0:
            return (1 - 0.056*(pyo.log(Rz))**0.64 * pyo.log(Rm) + 0.289*(pyo.log(Rz))**0.53)**(0.1*(pyo.log(m.allowable_cycles))-0.465)           
        else:
            return 1 - 0.056*(pyo.log(Rz))**0.64 * pyo.log(Rm) + 0.289*(pyo.log(Rz))**0.53

    # SH thickness
    e_n = (RO-RI)*1000

    # Calculate thickness correction factor
    @m.fs.Expression()
    def f_e(m):
        if e_n < 25:
            return 1
        elif (e_n > 25 and pyo.value(m.allowable_cycles - 2E6) <= 0):  
            if (e_n <=150 and e_n>25):  
                return ((25/e_n)**0.182)**(0.1*(pyo.log(m.allowable_cycles))-0.465)
            else:
                return (1/6)**0.182
        elif (e_n >25 and pyo.value(m.allowable_cycles-2E6)>0):
            if (e_n<=150 and e_n>25):
                return (25/e_n)**0.182
            else:
                return (1/6)**0.182

    #calculate reduced mean stress correction , Figure 18.6 in page 470, EN 13445 
    @m.fs.Expression()
    def sigma_mean_r(m):
        if (delta_sigma <= 2*Rp and abs(sigma_max) > Rp):
            if (sigma_mean > 0):
                return Rp - 0.5*sigma_mean
            else:
                return 0.5*sigma_mean - Rp
        elif (delta_sigma <= 2*Rp and abs(sigma_max) < Rp) :
            return sigma_mean
        else:
            return 0

    #calculate M
    M=0.00035*Rm-0.1

    #calculat A1
    @m.fs.Expression()
    def A1(m):
        return m.delta_sigma_R/(2*(1+M))

    # calculate full mean stress correction factor
    @m.fs.Expression()
    def f_m(m):
        if pyo.value(m.allowable_cycles) <= 2e6:
            if (pyo.value(m.sigma_mean_r)>=-Rp and pyo.value(m.sigma_mean_r)<=pyo.value(m.A1)):
            # if ((value(m.sigma_mean_r)+Rp)>=0 and (value(m.sigma_mean_r)-A1<=0)):
                return pyo.sqrt(1-M*(2+M)/(1+M)*(2*m.sigma_mean_r/m.delta_sigma_R))
            elif (pyo.value(m.A1) < pyo.value(m.sigma_mean_r) and pyo.value(m.sigma_mean_r) <= Rp):
                return (1+M/3)/(1+M) - M/3*(2*m.sigma_mean_r/m.delta_sigma_R)
            else:
                return 1
        else: 
            if (pyo.value(m.sigma_mean_r)>=-Rp and pyo.value(m.sigma_mean_r)<=pyo.value(m.A1)):
                    return pyo.sqrt(1-M*(2+M)/(1+M)*(2*m.sigma_mean_r/delta_sigma_D))
            elif (pyo.value(m.A1) < pyo.value(m.sigma_mean_r) and pyo.value(m.sigma_mean_r) <= Rp):
                    return (1+M/3)/(1+M) - M/3*(2*m.sigma_mean_r/delta_sigma_D)
            else:
                return 1
    # Calculate overall correction factor # f_u=f_T*f_s*f_e*f_m
    @m.fs.Expression()
    def f_u(m):
        return m.f_T * m.f_s * m.f_e * m.f_m

    #calulate delta signma R new and N new
    @m.fs.Constraint()
    def delta_sigma_R_new(m):
        return m.delta_sigma_R == m.delta_sigma_f/m.f_u

    # calculate N new
    @m.fs.Constraint()
    def N_new(m):
        if pyo.value(m.delta_sigma_R) > delta_sigma_D:
            return m.allowable_cycles == (46000/(m.delta_sigma_R-0.63*Rm + 11.5))**2
        else:
            return m.allowable_cycles == ((2.69*Rm+89.72)/m.delta_sigma_R)**10

    results = solver.solve(m, tee=False)
    # Print results
    print(results)

    end_time_cycle = wall_clock.time()
    time_cycle_used = end_time_cycle - start_time
    print("computational time of cycle estimation =", time_cycle_used)    
    print('max allowable cycles from baseline =', pyo.value(m.fs.allowable_cycles))
    
    cycles_baseline = int(pyo.value(m.fs.allowable_cycles))

    # metal_mass = pyo.value(m.fs.aPSH.density_wall*m.fs.aPSH.area_wall_seg*m.fs.aPSH.tube_length_seg)
    # metal_mass_base = pyo.value(const.pi*m.fs.aPSH.density_wall*m.fs.aPSH.tube_thickness*(
    #     m.fs.aPSH.tube_thickness+m.fs.aPSH.tube_di)*m.fs.aPSH.tube_ncol*m.fs.aPSH.tube_inlet_nrow*m.fs.aPSH.tube_length_seg)
    
    # # record desired outlet enthalpy
    # enthalpy_desired = []
    # for t in m.fs.time:
    #     enthalpy_desired.append(pyo.value(m.fs.aPSH.tube_outlet.enth_mol[t]))
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
    # m.fs.aPSH.tube_ncol.fix(94)
    m.fs.aPSH.tube_ncol.unfix()
    m.fs.aPSH.tube_ncol.setlb(80)
    m.fs.aPSH.tube_ncol.setub(96)

    # m.fs.aPSH.tube_inlet_nrow.fix(4)
    m.fs.aPSH.tube_inlet_nrow.unfix()
    m.fs.aPSH.tube_inlet_nrow.setlb(2)
    m.fs.aPSH.tube_inlet_nrow.setub(5)
    
    # *******************************************************************
    print('provide constraints')
    #sigma_max = 78 # MPa (Referenced from NIMS data, @ 500 degree C at 200000 h
    # sigma_max = 75.95 # max stress was obtained from base case
    # vary stress constraints 70, 60 MPa to find out what would be the min bound
    # on stress, which will be the value at the current operating pressure, 
    # i.e. only due to mechanical stress - by designing these systems 
    # only thing we are trying to to lower is the thermal stress not mechanical stress
    # because mechanical stress is due to pressure that depends on the sliding pressure
    # operation of the plant

    # Revised by Jinliang
    # unfix pitch_y and adding another constraint to ensure the pitch changes when the number of tube columns changes.
    m.fs.aPSH.pitch_y.unfix()
    furnance_width = 88 * 6.0*0.0254  # obtained from the baseline, furnace_width =  tube_ncol*pitch_y
    m.fs.PSH_width = pyo.Param(default=furnance_width, mutable=False)  # m    
    m.fs.geometry_cons = pyo.Constraint(expr=m.fs.aPSH.pitch_y * m.fs.aPSH.tube_ncol == m.fs.PSH_width)

    '''
    sigma_max_base = 76.0706 # max stress was obtained from base case
    delta_sigma = 0.001
    stress_ub = sigma_max_base - delta_sigma
    m.fs.stress_ub = pyo.Param(default=stress_ub, mutable=False)  # MPa
    # define variable to calculate the maximum stress of superheater
    m.fs.tube_max_stress_cons = pyo.Var(m.fs.time, initialize=75.9498)

    @m.fs.Constraint(m.fs.time,
                              doc="maximum SH tube wall stress")
    def cum_max_stress_eqn(b, t):
        if t == m.fs.time.first():
           return 1e-5*b.tube_max_stress_cons[t] == 1e-5*b.aPSH.sigma_von_Mises[t, 1, b.aPSH.r.first()]
        else:
           t_prev = m.fs.time.prev(t)
           return 1e-5*b.tube_max_stress_cons[t] == 1e-5*smooth_max(
            b.tube_max_stress_cons[t_prev], b.aPSH.sigma_von_Mises[t, 1, b.aPSH.r.first()])

    @m.fs.Constraint(m.fs.time)
    def max_stress_cons(b, t):
        return (b.stress_ub - b.tube_max_stress_cons[t])**2  >= 0
    '''
    # outlet steam temperature constraint
    nom_temp = 700.5  # K
    disturbed_outlet_temperature = 13
    @m.fs.Constraint(m.fs.time)
    def outlet_steam_temperature_cons(b, t):
        outlet_steam_temp = b.aPSH.tube.properties[t, b.aPSH.tube.length_domain.first()].temperature
        return (outlet_steam_temp - nom_temp)**2 <= disturbed_outlet_temperature**2
        
    
    # # add another constraint for fixing outlet enthalpy of steam
    # enthalpy_outlet_error = 1e8
    # @m.fs.Constraint(m.fs.time)
    # def outlet_enthalpy_cons(b, t):
    #     j = m.fs.time_index[t].value - 1
    #     return 1e-4*(b.aPSH.tube_outlet.enth_mol[t] - enthalpy_desired[j])**2 <= 1e-4*enthalpy_outlet_error

    sigma_max_base = 76.08  #76.0706  # MPa #max stress was obtained from base case
    delta_sigma = 1.0 # MPa
    stress_ub = sigma_max_base - delta_sigma
    m.fs.stress_ub = pyo.Param(default=stress_ub, mutable=False)  # MPa
    @m.fs.Constraint(m.fs.time, m.fs.aPSH.tube.length_domain)
    def max_stress_cons(b, t, x):
        return b.stress_ub - b.aPSH.sigma_von_Mises[t, x, b.aPSH.r.first()] >= 0           
    
    # N_min_base = 768593072
    m.fs.N_min = pyo.Param(default=cycles_baseline, mutable=False)
    # set constraint for number of cycles
    m.fs.cycles_cons = pyo.Constraint(expr=m.fs.allowable_cycles - m.fs.N_min >= 0)

    # set objective function
    print("set objective function")
    
    # set objective function 1: metal mass
    metal_mass_base = 1.2e4  # kg
    obj1_f = const.pi*m.fs.aPSH.density_wall*m.fs.aPSH.tube_thickness*(
        m.fs.aPSH.tube_thickness+m.fs.aPSH.tube_di)*m.fs.aPSH.tube_ncol*m.fs.aPSH.tube_inlet_nrow*m.fs.aPSH.tube_length_seg/metal_mass_base
    
    m.fs.obj1 = pyo.Objective(expr= obj1_f, sense=pyo.minimize)

    # set objective function 2
    max_pres_drop = 9.0e5 #824949.5 # Pa 
    obj2_f = sum(
        m.fs.aPSH.tube_inlet.pressure[t] - m.fs.aPSH.tube_outlet.pressure[t] for t in m.fs.time
        )/(max_pres_drop*nstep)

    m.fs.obj2 = pyo.Objective(expr=obj2_f, sense=pyo.minimize)
    # undo patch ipopt 
    # undo_patch_ipopt()

    # # step 1
    # # run objective function 1, deactivate objective function 2
    # m.fs.obj1.activate()
    # m.fs.obj2.deactivate()

    # solver options
    print('***************************************************************')
    solver = pyo.SolverFactory("ipopt")
    solver.options['tol'] = 1e-6
    solver.options['bound_push'] = 1e-10
    solver.options['warm_start_init_point'] = 'yes'
    solver.options['warm_start_bound_push'] = 1e-10
    solver.options['warm_start_mult_bound_push'] = 1e-10
    # solver.options['mu_init'] = 1e-6
    solver.options['max_iter'] = 150

    print('***************************************************************')
    print('optimize metal mass objective function')
    m.fs.obj2.deactivate()
    results_obj1 = solver.solve(m, tee=True)
    print(results_obj1)

    end_time_opt1 = wall_clock.time()
    time_opt1_used = end_time_opt1 - start_time
    print("computational time of obj1 optimization =", time_opt1_used)

    # save optimization of objective 1 as a parameter
    obj1_opt = pyo.value(const.pi*m.fs.aPSH.density_wall*m.fs.aPSH.tube_thickness*(
        m.fs.aPSH.tube_thickness+m.fs.aPSH.tube_di)*m.fs.aPSH.tube_ncol*m.fs.aPSH.tube_inlet_nrow*m.fs.aPSH.tube_length_seg/metal_mass_base)
    m.fs.obj1_opt = pyo.Param(default=obj1_opt, mutable=False)

    print('***************************************************************')
    print('optimize pressure drop objective function')

    m.fs.obj1.deactivate()
    m.fs.obj2.activate()

    # run dynamic optimization
    results_obj2 = solver.solve(m, tee=True)
    print(results_obj2)

    end_time_opt2 = wall_clock.time()
    time_opt2_used = end_time_opt2 - start_time
    print("computational time of obj2 optimization =", time_opt2_used)

    # save optimization results of objective 2 as a parameter
    obj2_opt = pyo.value(sum(
        m.fs.aPSH.tube_inlet.pressure[t] - m.fs.aPSH.tube_outlet.pressure[t] for t in m.fs.time
        )/(max_pres_drop*nstep))
    m.fs.obj2_opt = pyo.Param(default=obj2_opt, mutable=False)

    print('***************************************************************')
    print('multi optimization with metal mass & pressure drop objective function')

    # deactivate both single objective (obj1 has been deactivated previously)
    m.fs.obj2.deactivate()

    obj1_w = 0.5
    obj2_w = 1 - obj1_w
    m.fs.omega_1 = pyo.Param(default=obj1_w, mutable=False)
    m.fs.omega_2 = pyo.Param(default=obj2_w, mutable=False)

    # multiobjective function
    multi_obj_f = pyo.sqrt(m.fs.omega_1*(obj1_f - obj1_opt)**2 + m.fs.omega_2*(obj2_f - obj2_opt)**2)
    m.fs.multi_obj = pyo.Objective(expr=multi_obj_f, sense=pyo.minimize)

    # run dynamic optimization for multiobjective
    results_multiobj = solver.solve(m, tee=True)
    print(results_multiobj)
    

    end_time_opt = wall_clock.time()
    time_opt_used = end_time_opt - start_time
    print("computational time of dynamic optimization =", time_opt_used)

    metal_mass_opt = pyo.value(const.pi*m.fs.aPSH.density_wall*m.fs.aPSH.tube_thickness*(
        m.fs.aPSH.tube_thickness+m.fs.aPSH.tube_di)*m.fs.aPSH.tube_ncol*m.fs.aPSH.tube_inlet_nrow*m.fs.aPSH.tube_length_seg)

    pressure_drop_opt = pyo.value(sum(
        m.fs.aPSH.tube_inlet.pressure[t] - m.fs.aPSH.tube_outlet.pressure[t] for t in m.fs.time
        ))

    max_allowable_cycles = pyo.value(m.fs.allowable_cycles)

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
        "pitch_y",
        # "pitch_x_to_do",
        # "pitch_y_to_do",
        # "enthalpy_desired",
        # "metal_mass_base",
        "metal_mass_opt",
        "pressure_drop_opt",
        "delta_sigma",
        "max_allowable_cycles",
        "multiobjective_value"
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
        df_val.loc[t]["pitch_y"] = pyo.value(m.fs.aPSH.pitch_y)
        # df_val.loc[t]["pitch_x_to_do"] = pyo.value(m.fs.aPSH.pitch_x_to_do)
        # df_val.loc[t]["pitch_y_to_do"] = pyo.value(m.fs.aPSH.pitch_y_to_do)
        # df_val.loc[t]["enthalpy_desired"] = pyo.value(m.fs.aPSH.tube_outlet.enth_mol[t])
        # df_val.loc[t]["metal_mass_base"] = metal_mass_base
        df_val.loc[t]["metal_mass_opt"] = metal_mass_opt
        df_val.loc[t]["pressure_drop_opt"] = pressure_drop_opt
        df_val.loc[t]["delta_sigma"] = pyo.value(delta_sigma)
        df_val.loc[t]["max_allowable_cycles"] = max_allowable_cycles
        df_val.loc[t]["multiobjective_value"] = pyo.value(multi_obj_f)
        # df_val.loc[t]["steam_outlet_temperature"] = pyo.value(m.fs.aPSH.tube.properties[t, 0].temperature)
        # df_val.loc[t]["max_stress"] = pyo.value(m.fs.tube_max_stress[t, 1])
        # df_val.loc[t]["max_stress"] = pyo.value(m.fs.aPSH.sigma_von_Mises[t, 1, m.fs.aPSH.r.first()])

        df_val.to_csv(f"SH_multiobj_stress_cons_case5.csv")

    
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
    with open("result_SH_multiobj_stress_cons_case5.txt","w") as fout:
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