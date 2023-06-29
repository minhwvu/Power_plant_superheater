import time as wall_clock
import pyomo.environ as pyo
from pyomo.network import Arc
from idaes.core import FlowsheetBlock
from idaes.generic_models.properties import iapws95
from idaes.core.util.model_statistics import degrees_of_freedom
import idaes.core.util.scaling as iscale
from idaes.core.util import copy_port_values
from idaes.power_generation.properties import FlueGasParameterBlock
from idaes.power_generation.control import PIDController
import flowsheets.boiler_subfs as blr
import flowsheets.steam_cycle_subfs as stc
from idaes.core.util.dyn_utils import copy_values_at_time, copy_non_time_indexed_values
import matplotlib.pyplot as plt
import idaes.core.plugins

import idaes.logger as idaeslog

_log = idaeslog.getLogger(__name__)

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
    IPOPT.solve = IPOPT._old_solve

monkey_patch_ipopt()


def set_scaling_factors(m):
    """ Set scaling factors for variables and expressions. These are used for
    variable scaling and used by the framework to scale constraints.

    Args:
        m: plant model to set scaling factors for.

    Returns:
        None
    """
    #First set boiler scaling factors
    fs = m.fs_main.fs_blr

    #iscale.set_scaling_factor(fs.flow_mol_ta, 1e-2)

    for i, ww in fs.Waterwalls.items():
        iscale.set_scaling_factor(ww.heat_fireside, 1e-7)
        if i < 4:
            iscale.set_scaling_factor(ww.heat_flux_conv, 1e-4)
        else:
            iscale.set_scaling_factor(ww.heat_flux_conv, 1e-5)
        iscale.set_scaling_factor(ww.tube_diameter, 100)
        iscale.set_scaling_factor(ww.control_volume.material_holdup, 1e-4)
        iscale.set_scaling_factor(ww.control_volume.energy_holdup, 1e-8)
        iscale.set_scaling_factor(ww.energy_holdup_slag, 1e-3)
        iscale.set_scaling_factor(ww.energy_holdup_metal, 1e-6)
        iscale.set_scaling_factor(ww.N_Re, 1e-6)
        iscale.set_scaling_factor(ww.pitch, 1e3)
        for j, c in ww.hconv_lo_eqn.items():
            iscale.constraint_scaling_transform(c, 1e-2)

    iscale.set_scaling_factor(fs.aRoof.heat_fireside, 1e-7) #old 1e-6
    iscale.set_scaling_factor(fs.aRoof.heat_flux_conv, 1e-4)
    iscale.set_scaling_factor(fs.aRoof.hconv, 1e-3)
    iscale.set_scaling_factor(fs.aRoof.deltaP, 1e-3)
    iscale.set_scaling_factor(fs.aRoof.diameter_in, 100)
    iscale.set_scaling_factor(fs.aRoof.N_Re, 1e-6)
    
    iscale.set_scaling_factor(fs.aPlaten.heat_fireside, 1e-7)
    iscale.set_scaling_factor(fs.aPlaten.heat_flux_conv, 1e-4)
    iscale.set_scaling_factor(fs.aPlaten.hconv, 1e-3)
    iscale.set_scaling_factor(fs.aPlaten.deltaP, 1e-3)
    iscale.set_scaling_factor(fs.aPlaten.diameter_in, 100) 
    iscale.set_scaling_factor(fs.aPlaten.N_Re, 1e-6)

    iscale.set_scaling_factor(fs.aDrum.control_volume.energy_holdup, 1e-10)
    iscale.set_scaling_factor(fs.aDrum.control_volume.material_holdup, 1e-5)
    if m.dynamic:
        for t, c in fs.aDrum.control_volume.energy_accumulation_disc_eq.items():
            iscale.constraint_scaling_transform(c, 1e-5)
        for t, c in fs.aDrum.heat_loss_eqn.items():
            iscale.constraint_scaling_transform(c, 1e-4)

    iscale.set_scaling_factor(fs.aDowncomer.control_volume.energy_holdup, 1e-10)
    iscale.set_scaling_factor(fs.aDowncomer.control_volume.material_holdup, 1e-5)

    iscale.set_scaling_factor(fs.aRoof.control_volume.energy_holdup, 1e-8)
    iscale.set_scaling_factor(fs.aRoof.control_volume.material_holdup, 1e-6)

    iscale.set_scaling_factor(fs.aPlaten.control_volume.energy_holdup, 1e-8)
    iscale.set_scaling_factor(fs.aPlaten.control_volume.material_holdup, 1e-6)

    iscale.set_scaling_factor(fs.aPipe.control_volume.energy_holdup, 1e-9)
    iscale.set_scaling_factor(fs.aPipe.control_volume.material_holdup, 1e-5)

    iscale.set_scaling_factor(fs.aBoiler.waterwall_heat, 1e-7)
    iscale.set_scaling_factor(fs.aBoiler.platen_heat, 1e-7)
    iscale.set_scaling_factor(fs.aBoiler.roof_heat, 1e-7)
    
    iscale.set_scaling_factor(fs.aECON.shell._enthalpy_flow, 1e-8)
    iscale.set_scaling_factor(fs.aECON.tube._enthalpy_flow, 1e-8)
    iscale.set_scaling_factor(fs.aECON.shell.enthalpy_flow_dx, 1e-7)
    iscale.set_scaling_factor(fs.aECON.tube.enthalpy_flow_dx, 1e-7)
    for t, c in fs.aECON.shell.enthalpy_flow_dx_disc_eq.items():
        iscale.constraint_scaling_transform(c, 1e-7)
    for t, c in fs.aECON.tube.enthalpy_flow_dx_disc_eq.items():
        iscale.constraint_scaling_transform(c, 1e-7)

    iscale.set_scaling_factor(fs.aPSH.shell._enthalpy_flow, 1e-8)
    iscale.set_scaling_factor(fs.aPSH.tube._enthalpy_flow, 1e-8)
    iscale.set_scaling_factor(fs.aPSH.shell.enthalpy_flow_dx, 1e-7)
    iscale.set_scaling_factor(fs.aPSH.tube.enthalpy_flow_dx, 1e-7)
    for t, c in fs.aPSH.shell.enthalpy_flow_dx_disc_eq.items():
        iscale.constraint_scaling_transform(c, 1e-7)
    for t, c in fs.aPSH.tube.enthalpy_flow_dx_disc_eq.items():
        iscale.constraint_scaling_transform(c, 1e-7)

    iscale.set_scaling_factor(fs.aRH1.shell._enthalpy_flow, 1e-8)
    iscale.set_scaling_factor(fs.aRH1.tube._enthalpy_flow, 1e-8)
    iscale.set_scaling_factor(fs.aRH1.shell.enthalpy_flow_dx, 1e-7)
    iscale.set_scaling_factor(fs.aRH1.tube.enthalpy_flow_dx, 1e-7)
    for t, c in fs.aRH1.shell.enthalpy_flow_dx_disc_eq.items():
        iscale.constraint_scaling_transform(c, 1e-7)
    for t, c in fs.aRH1.tube.enthalpy_flow_dx_disc_eq.items():
        iscale.constraint_scaling_transform(c, 1e-7)

    iscale.set_scaling_factor(fs.aRH2.shell._enthalpy_flow, 1e-8)
    iscale.set_scaling_factor(fs.aRH2.tube._enthalpy_flow, 1e-8)
    iscale.set_scaling_factor(fs.aRH2.shell.enthalpy_flow_dx, 1e-7)
    iscale.set_scaling_factor(fs.aRH2.tube.enthalpy_flow_dx, 1e-7)
    for t, c in fs.aRH2.shell.enthalpy_flow_dx_disc_eq.items():
        iscale.constraint_scaling_transform(c, 1e-7)
    for t, c in fs.aRH2.tube.enthalpy_flow_dx_disc_eq.items():
        iscale.constraint_scaling_transform(c, 1e-7)

    # Set steam cycle scale factors
    fs = m.fs_main.fs_stc

    iscale.set_scaling_factor(fs.condenser.side_1.heat, 1e-9)
    iscale.set_scaling_factor(fs.condenser.side_2.heat, 1e-9)

    iscale.set_scaling_factor(fs.aux_condenser.side_1.heat, 1e-7)
    iscale.set_scaling_factor(fs.aux_condenser.side_2.heat, 1e-7)

    iscale.set_scaling_factor(fs.hotwell_tank.control_volume.energy_holdup, 1e-9)
    iscale.set_scaling_factor(fs.hotwell_tank.control_volume.material_holdup, 1e-6)
    if m.dynamic:
        for t, c in fs.hotwell_tank.control_volume.energy_accumulation_disc_eq.items():
            iscale.constraint_scaling_transform(c, 1e-6)

    iscale.set_scaling_factor(fs.fwh1.condense.side_1.material_holdup, 1e-4)
    iscale.set_scaling_factor(fs.fwh1.condense.side_1.energy_holdup, 1e-8)
    iscale.set_scaling_factor(fs.fwh1.condense.side_2.material_holdup, 1e-4)
    iscale.set_scaling_factor(fs.fwh1.condense.side_2.energy_holdup, 1e-8)
    iscale.set_scaling_factor(fs.fwh1.condense.side_1.heat, 1e-7)
    iscale.set_scaling_factor(fs.fwh1.condense.side_2.heat, 1e-7)

    iscale.set_scaling_factor(fs.fwh2.condense.side_1.material_holdup, 1e-4)
    iscale.set_scaling_factor(fs.fwh2.condense.side_1.energy_holdup, 1e-8)
    iscale.set_scaling_factor(fs.fwh2.condense.side_2.material_holdup, 1e-4)
    iscale.set_scaling_factor(fs.fwh2.condense.side_2.energy_holdup, 1e-8)
    iscale.set_scaling_factor(fs.fwh2.condense.side_1.heat, 1e-7)
    iscale.set_scaling_factor(fs.fwh2.condense.side_2.heat, 1e-7)

    iscale.set_scaling_factor(fs.fwh3.condense.side_1.material_holdup, 1e-4)
    iscale.set_scaling_factor(fs.fwh3.condense.side_1.energy_holdup, 1e-8)
    iscale.set_scaling_factor(fs.fwh3.condense.side_2.material_holdup, 1e-4)
    iscale.set_scaling_factor(fs.fwh3.condense.side_2.energy_holdup, 1e-8)
    iscale.set_scaling_factor(fs.fwh3.condense.side_1.heat, 1e-7)
    iscale.set_scaling_factor(fs.fwh3.condense.side_2.heat, 1e-7)

    iscale.set_scaling_factor(fs.da_tank.control_volume.energy_holdup, 1e-10)
    iscale.set_scaling_factor(fs.da_tank.control_volume.material_holdup, 1e-6)
    if m.dynamic:
        for t, c in fs.da_tank.control_volume.energy_accumulation_disc_eq.items():
            iscale.constraint_scaling_transform(c, 1e-7)

    iscale.set_scaling_factor(fs.fwh5.condense.side_1.material_holdup, 1e-4)
    iscale.set_scaling_factor(fs.fwh5.condense.side_1.energy_holdup, 1e-8)
    iscale.set_scaling_factor(fs.fwh5.condense.side_2.material_holdup, 1e-4)
    iscale.set_scaling_factor(fs.fwh5.condense.side_2.energy_holdup, 1e-8)
    iscale.set_scaling_factor(fs.fwh5.condense.side_1.heat, 1e-7)
    iscale.set_scaling_factor(fs.fwh5.condense.side_2.heat, 1e-7)

    iscale.set_scaling_factor(fs.fwh6.condense.side_1.material_holdup, 1e-4)
    iscale.set_scaling_factor(fs.fwh6.condense.side_1.energy_holdup, 1e-8)
    iscale.set_scaling_factor(fs.fwh6.condense.side_2.material_holdup, 1e-4)
    iscale.set_scaling_factor(fs.fwh6.condense.side_2.energy_holdup, 1e-8)
    iscale.set_scaling_factor(fs.fwh6.condense.side_1.heat, 1e-7)
    iscale.set_scaling_factor(fs.fwh6.condense.side_2.heat, 1e-7)

    # Calculate calculated scaling factors
    iscale.calculate_scaling_factors(m)


def add_overall_performance_expressions(m):
    @m.fs_main.Expression(m.fs_main.time,
        doc="Heat input to the steam cycle (W)")
    def boiler_heat(b, t):
        return ((b.fs_stc.turb.inlet_split.mixed_state[t].flow_mol - b.fs_stc.spray_valve.outlet.flow_mol[t])
            * (b.fs_stc.turb.inlet_split.mixed_state[t].enth_mol - b.fs_stc.fwh6.desuperheat.tube.properties_out[t].enth_mol)
            + b.fs_stc.spray_valve.outlet.flow_mol[t]
            * (b.fs_stc.turb.inlet_split.mixed_state[t].enth_mol - b.fs_stc.spray_valve.outlet.enth_mol[t])
            + b.fs_stc.turb.ip_stages[1].control_volume.properties_in[t].flow_mol
            * (b.fs_stc.turb.ip_stages[1].control_volume.properties_in[t].enth_mol
            - b.fs_stc.turb.hp_split[14].outlet_1.enth_mol[t]))

    # Calculate the heat rate of the plant.  This doesn't account for
    # heat loss in the boiler, so actual plant efficiency would be lower.
    @m.fs_main.Expression(m.fs_main.time)
    def steam_cycle_eff(b, t):
        return -b.fs_stc.turb.power[t] / b.boiler_heat[t]

    # Calculate the heat rate of the plant.
    @m.fs_main.Expression(m.fs_main.time,
        doc="Heat rate based on gross power (BTU/MW)")
    def gross_heat_rate(b, t):
        return (
            -b.fs_blr.aBoiler.flowrate_coal_raw[t]
            * (1 - b.fs_blr.aBoiler.mf_H2O_coal_raw[t])
            * b.fs_blr.aBoiler.hhv_coal_dry
            * 3600 / b.fs_stc.turb.power[t]
            * 1000 / 1054)

    # Calculate the overall efficiency of the plant.
    @m.fs_main.Expression(m.fs_main.time,
        doc="Overall efficency based on gross power (%)")
    def plant_gross_efficiency(b, t):
        return (-b.fs_stc.turb.power[t] /
            (b.fs_blr.aBoiler.flowrate_coal_raw[t] * (1 - b.fs_blr.aBoiler.mf_H2O_coal_raw[t])
            * b.fs_blr.aBoiler.hhv_coal_dry))
    # Calculate the total auxillary power com
    @m.fs_main.Expression(m.fs_main.time) 
    def aux_power(b, t):
        steam_f = m.fs_main.fs_stc.turb.inlet_split.mixed_state[t].flow_mass*7.937
        #air_f = m.fs_main.fs_blr.flowrate_pa_total[t]*7.937
        air_f = m.fs_main.fs_blr.aBoiler.primary_air[t].flow_mass*7.937
        cw_f = m.fs_main.fs_stc.condenser.tube.properties_in[t].flow_mass/997*15850/1000
        steam_t = (m.fs_main.fs_blr.aPlaten.control_volume.properties_out[t].temperature - 273.15)*9/5 + 32
        steam_p = (m.fs_main.fs_blr.aPlaten.control_volume.properties_out[t].pressure - 79410)/6895
        air_p = m.fs_main.fs_blr.aAPH.side_2_inlet.pressure[t]/1000
        return (
            -7.743210e-2 * cw_f  +
            2.424004e-7 * steam_f**2 +
            1.718702e-6 * steam_f* air_f+
            5.301540e-11 * steam_f**3 +
            2.806236e-10*steam_f**2*steam_t+
            7.943112e-10*steam_f**2* air_f+
            5.106800e-10*steam_f *steam_t *air_f+
            6.356823e-10*steam_f *air_f**2+
            -2.094381e-7*steam_p *cw_f**2+
            5.849115e-10*steam_t**3+
            1.049080e-11*steam_t**2*air_f+
            1.913389e-9*steam_t*air_p**2+
            15.19445
        )*1e6


def main_steady():
    m = get_model(dynamic=False)
    return m

def input_profile(t, x0):
    #calculate the user input x as a function of time
    #x0 is the initial value
    if t<60:
       x = x0
    elif t<3060:
       x = x0*(1-(t-60)/3000*0.5)
    elif t<6660:
        x = x0*0.5
    elif t<9660:
        x = x0*(0.5+(t-6660)/3000*0.5)
    else: #hold for 1200 sec to 10860 sec
       x = x0
    return x

def main_dyn():
    start_time = wall_clock.time()
    # declare dictionary for the data to plot
    plot_data = {}
    plot_data['time'] = []
    plot_data['coal_flow'] = []
    plot_data['PA_to_APH_flow'] = []
    plot_data['PA_temp_flow'] = []
    plot_data['SA_flow'] = []
    plot_data['SR'] = []
    plot_data['dry_O2_pct_in_flue_gas'] = []
    plot_data['bfpt_opening'] = []
    plot_data['gross_power'] = []
    plot_data['ww_heat'] = []
    plot_data['fegt'] = []
    plot_data['drum_level'] = []
    plot_data['feed_water_flow_sp'] = []
    plot_data['drum_master_ctrl_op'] = []
    plot_data['feed_water_flow'] = []
    plot_data['spray_flow'] = []
    plot_data['main_steam_flow'] = []
    plot_data['rh_steam_flow'] = []
    plot_data['bfpt_flow'] = []
    plot_data['main_steam_temp'] = []
    plot_data['rh_steam_temp'] = []
    plot_data['fw_pres'] = []
    plot_data['drum_pres'] = []
    plot_data['main_steam_pres'] = []
    plot_data['rh_steam_pres'] = []
    plot_data['hw_tank_level'] = []
    plot_data['da_tank_level'] = []
    plot_data['fwh2_level'] = []
    plot_data['fwh3_level'] = []
    plot_data['fwh5_level'] = []
    plot_data['fwh6_level'] = []
    plot_data['makeup_valve_opening'] = []
    plot_data['cond_valve_opening'] = []
    plot_data['fwh2_valve_opening'] = []
    plot_data['fwh3_valve_opening'] = []
    plot_data['fwh5_valve_opening'] = []
    plot_data['fwh6_valve_opening'] = []
    plot_data['spray_valve_opening'] = []
    plot_data['tube_temp_rh2'] = []
    plot_data['temp_fg_econ_exit'] = []
    plot_data['temp_fg_aph_exit'] = []
    plot_data['throttle_opening'] = []
    plot_data['load_demand'] = []
    plot_data['sliding_pressure'] = []
    plot_data['steam_pressure_sp'] = []
    plot_data['deaerator_pressure'] = []
    plot_data['temp_econ_in'] = []
    plot_data['temp_econ_out'] = []
    plot_data['temp_econ_out_sat'] = []
    plot_data['boiler_efficiency_heat'] = []
    plot_data['boiler_efficiency_steam'] = []
    plot_data['steam_cycle_efficiency'] = []
    plot_data['plant_gross_efficiency'] = []
    plot_data['gross_heat_rate'] = []

    # Boiler health related data
    # For drum
    plot_data['drum_inner_wall_temperature'] = []
    plot_data['drum_outer_wall_temperature'] = []
    plot_data['drum_inner_theta_sigma_m'] = []
    plot_data['drum_inner_theta_sigma_t'] = []
    plot_data['drum_inner_vM_sigma'] = []
    plot_data['drum_outer_theta_sigma_m'] = []
    plot_data['drum_outer_theta_sigma_t'] = []
    plot_data['drum_outer_vM_sigma'] = []
    plot_data['drum_delta_sigma_r_theta_outer'] = []
    plot_data['drum_delta_sigma_theta_z_outer'] = []
    plot_data['drum_delta_sigma_z_r_outer'] = []
    # Stress at opening of the drum
    plot_data['drum_circumferential_P1'] = []
    plot_data['drum_circumferential_P2'] = []
    plot_data['drum_von_Mises_P1'] = []
    plot_data['drum_von_Mises_P2'] = []

    # For primary superheater
    plot_data['PSH_flue_gas_flow_disc1'] = []
    plot_data['PSH_steam_flow_disc9'] = []
    plot_data['PSH_steam_temperature_disc1'] = []
    plot_data['PSH_steam_temperature_disc2'] = []
    plot_data['PSH_steam_temperature_disc4'] = []
    plot_data['PSH_steam_temperature_disc8'] = []
    plot_data['PSH_steam_temperature_disc9'] = []
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
    plot_data['PSH_mech_circumferential_outside_disc1'] = []
    plot_data['PSH_ther_circumferential_outside_disc1'] = []
    plot_data['PSH_circumferential_outside_disc1'] = []

    # For primary superheater header
    plot_data['Header_inner_temperature'] = []
    plot_data['Header_outside_temperature'] = []
    plot_data['Header_circumferential_P1'] = []
    plot_data['Header_circumferential_P2'] = []
    plot_data['Header_circumferential_body'] = []
    plot_data['Header_von_Mises_P1'] = []
    plot_data['Header_von_Mises_P2'] = []
    plot_data['Header_rupture_time_P1'] = []
    plot_data['Header_rupture_time_P2'] = []

    # steady-state model
    m_ss = get_model(dynamic=False)
    num_step = [2, 2]
    step_size = [30, 60]
    # 1st dynamic model with smallest time step size
    m_dyn0 = get_model(dynamic=True, time_set=[0, num_step[0]*step_size[0]], nstep=num_step[0])
    # 2nd dynamic model with intermediate time step size
    #m_dyn1 = None
    m_dyn1 = get_model(dynamic=True, time_set=[0, num_step[1]*step_size[1]], nstep=num_step[1])
    # model type list, user input to specify the time duration
    itype_list = []
    for i in range(71): # to 4260
        itype_list.append(0)
    for i in range(20): # to 6660
        itype_list.append(1)
    for i in range(70): # to 10860
        itype_list.append(0)
    nperiod = len(itype_list)
    tstart = []
    model_list = []
    t = 0
    for i in range(nperiod):
        tstart.append(t)
        t += step_size[itype_list[i]]*num_step[itype_list[i]]
        if itype_list[i]==0:
            model_list.append(m_dyn0)
        else:
            model_list.append(m_dyn1)
    # start first model   
    m_dyn = model_list[0]
    copy_non_time_indexed_values(m_dyn.fs_main, m_ss.fs_main, copy_fixed=True, outlvl=idaeslog.ERROR)
    for t in m_dyn.fs_main.config.time:
        copy_values_at_time(m_dyn.fs_main, m_ss.fs_main, t, 0.0, copy_fixed=True, outlvl=idaeslog.ERROR)
    t0 = m_dyn.fs_main.config.time.first()
    # reset bias of controller to current steady-state value, this makes both error and integral error to zero
    m_dyn.fs_main.fs_stc.fwh2_ctrl.mv_ref.value = m_dyn.fs_main.fs_stc.fwh2_valve.valve_opening[t0].value
    m_dyn.fs_main.fs_stc.fwh3_ctrl.mv_ref.value = m_dyn.fs_main.fs_stc.fwh3_valve.valve_opening[t0].value
    m_dyn.fs_main.fs_stc.fwh5_ctrl.mv_ref.value = m_dyn.fs_main.fs_stc.fwh5_valve.valve_opening[t0].value
    m_dyn.fs_main.fs_stc.fwh6_ctrl.mv_ref.value = m_dyn.fs_main.fs_stc.fwh6_valve.valve_opening[t0].value
    m_dyn.fs_main.fs_stc.da_ctrl.mv_ref.value = m_dyn.fs_main.fs_stc.cond_valve.valve_opening[t0].value
    m_dyn.fs_main.fs_stc.makeup_ctrl.mv_ref.value = m_dyn.fs_main.fs_stc.makeup_valve.valve_opening[t0].value
    m_dyn.fs_main.fs_stc.spray_ctrl.mv_ref.value = m_dyn.fs_main.fs_stc.spray_valve.valve_opening[t0].value
    # two bounded ctrls require setting initial integral_of_error
    m_dyn.fs_main.fs_stc.makeup_ctrl.integral_of_error[:].value = pyo.value(m_dyn.fs_main.fs_stc.makeup_ctrl.integral_of_error_ref[t0])
    m_dyn.fs_main.fs_stc.spray_ctrl.integral_of_error[:].value = pyo.value(m_dyn.fs_main.fs_stc.spray_ctrl.integral_of_error_ref[t0])
    # drum_master_ctrl.mv_ref is always 0 (already fixed to 0)
    m_dyn.fs_main.drum_slave_ctrl.mv_ref.value = m_dyn.fs_main.fs_stc.bfp_turb_valve.valve_opening[t0].value
    m_dyn.fs_main.turbine_master_ctrl.mv_ref.value = m_ss.fs_main.fs_stc.turb.throttle_valve[1].valve_opening[t0].value
    m_dyn.fs_main.turbine_master_ctrl.setpoint[:].value = m_ss.fs_main.fs_stc.power_output[t0].value
    m_dyn.fs_main.boiler_master_ctrl.mv_ref.value = m_ss.fs_main.fs_blr.aBoiler.flowrate_coal_raw[t0].value
    m_dyn.fs_main.main_steam_pressure[:].value = m_ss.fs_main.fs_blr.aPlaten.outlet.pressure[t0].value/1e6
    m_dyn.fs_main.boiler_master_ctrl.setpoint[:].value = m_ss.fs_main.fs_blr.aPlaten.outlet.pressure[t0].value/1e6
    
    print('boiler_master_setpoint=', m_dyn.fs_main.boiler_master_ctrl.setpoint[0].value)
    print('sliding pressure=', pyo.value(m_dyn.fs_main.sliding_pressure[0]))
    solver = pyo.SolverFactory("ipopt")
    solver.options = {
            "tol": 1e-7,
            "linear_solver": "ma27",
            "max_iter": 50,
    } 
    # copy non-time-indexed variables to all dynamic models
    if itype_list[0]==0:
        if m_dyn1:
            copy_non_time_indexed_values(m_dyn1.fs_main, m_dyn.fs_main, copy_fixed=True, outlvl=idaeslog.ERROR)
    else:
        if m_dyn0:
            copy_non_time_indexed_values(m_dyn0.fs_main, m_dyn.fs_main, copy_fixed=True, outlvl=idaeslog.ERROR)
    dof = degrees_of_freedom(m_dyn)
    print('dof of full model', dof)
    # solving dynamic model at steady-state, this step could be skipped if all setup is good
    print('Solving dynamic model at steady-state...')
    results = solver.solve(m_dyn, tee=True)
    # start 1st simulation
    print("Solving for period number 0 from ", tstart[0], " sec.")
    ss_value = m_ss.fs_main.fs_stc.power_output[0].value
    run_dynamic(m_dyn, ss_value, tstart[0], plot_data, solver)
    
    # loop for remaining periods
    tlast = m_dyn.fs_main.config.time.last()
    m_prev = m_dyn
    for i in range(1,nperiod):
        m_dyn = model_list[i]
        for t in m_dyn.fs_main.config.time:
            if itype_list[i]!=itype_list[i-1] or t!=tlast:
                copy_values_at_time(m_dyn.fs_main, m_prev.fs_main, t, tlast, copy_fixed=True, outlvl=idaeslog.ERROR)
            print('windup=', m_dyn.fs_main.fs_stc.spray_ctrl.integral_of_error[t].value)
            mv_unbounded = pyo.value(
                m_dyn.fs_main.fs_stc.spray_ctrl.mv_unbounded[t])
            if mv_unbounded < pyo.value(
                    m_dyn.fs_main.fs_stc.spray_ctrl.mv_lb):
                # Reset spray control windup
                if pyo.value(m_dyn.fs_main.fs_stc.spray_ctrl.integral_of_error[t].value) > 3000:         
                    m_dyn.fs_main.fs_stc.spray_ctrl.integral_of_error[t].value = 3000
                    print('reachig lower bound and maximum windup of 3000.'
                          ' reset windup to 3000.')
            if mv_unbounded > pyo.value(
                    m_dyn.fs_main.fs_stc.spray_ctrl.mv_ub):
                # Reset spray control windup
                if pyo.value(m_dyn.fs_main.fs_stc.spray_ctrl.integral_of_error[t].value) < -10000:         
                    m_dyn.fs_main.fs_stc.spray_ctrl.integral_of_error[t].value = -10000
                    print('reachig upper bound and minimum windup of -10000.'
                          ' reset windup to -10000.')
        print("Solving for period number ", i, "from ", tstart[i], " sec.")
        run_dynamic(m_dyn, ss_value, tstart[i], plot_data, solver)
        tlast = m_dyn.fs_main.config.time.last()
        print('spray flow={}'.format(
            m_dyn.fs_main.fs_stc.spray_valve.outlet.flow_mol[tlast].value))
        m_prev = m_dyn
    end_time = wall_clock.time()
    time_used = end_time - start_time
    print("simulation time=", time_used)
    write_data_to_txt_file(plot_data)
    plot_results(plot_data)
    return m_dyn

def get_model(dynamic=True, time_set=None, nstep=None):
    m = pyo.ConcreteModel()
    m.dynamic = dynamic
    m.init_dyn = False
    if time_set is None:
        time_set = [0,20,200]
    if nstep is None:
        nstep = 5
    if m.dynamic:
        m.fs_main = FlowsheetBlock(default={"dynamic": True, "time_set": time_set, "time_units": pyo.units.s})
    else:
        m.fs_main = FlowsheetBlock(default={"dynamic": False})
    # Add property packages to flowsheet library
    m.fs_main.prop_water = iapws95.Iapws95ParameterBlock()
    m.fs_main.prop_gas = FlueGasParameterBlock()
    m.fs_main.fs_blr = FlowsheetBlock(default={"time_units": pyo.units.s})
    m.fs_main.fs_stc = FlowsheetBlock(default={"time_units": pyo.units.s})
    # Increase slope by 30% (use 0.02*1.3)
    m.fs_main.slope_pslide = pyo.Param(initialize=0.02*1.3, doc="slope of sliding pressure")
    m = blr.add_unit_models(m)
    m = stc.add_unit_models(m)
    # boiler master pv main steam pressure in MPa
    m.fs_main.main_steam_pressure = pyo.Var(
        m.fs_main.config.time,
        initialize=13,
        doc="main steam pressure in MPa for boiler master controller"
    )
    # main steam pressure in MPa
    @m.fs_main.Constraint(m.fs_main.config.time, doc="main steam pressure in MPa")
    def main_steam_pressure_eqn(b, t):
        return b.main_steam_pressure[t] == 1e-6*b.fs_blr.aPlaten.outlet.pressure[t]
    if m.dynamic:
        # extra variables required by controllers
        # master level control output, desired feed water flow rate adjustment due to level deviation
        m.fs_main.flow_level_ctrl_output = pyo.Var(
            m.fs_main.config.time,
            initialize=0,
            doc="mole flow rate of feed water demand from drum level master controller"
        )
        # PID controllers
        # master of cascading level controller
        m.fs_main.drum_master_ctrl = PIDController(default={"pv":m.fs_main.fs_blr.aDrum.level,
                                  "mv":m.fs_main.flow_level_ctrl_output,
                                  "type": 'PI'})
        # slave of cascading level controller
        m.fs_main.drum_slave_ctrl = PIDController(default={"pv":m.fs_main.fs_stc.bfp.outlet.flow_mol,
                                  "mv":m.fs_main.fs_stc.bfp_turb_valve.valve_opening,
                                  "type": 'PI',
                                  "bounded_output": False})
        # turbine master PID controller to control power output in MW by manipulating throttling valve
        m.fs_main.turbine_master_ctrl = PIDController(default={"pv":m.fs_main.fs_stc.power_output,
                                  "mv":m.fs_main.fs_stc.turb.throttle_valve[1].valve_opening,
                                  "type": 'PI'})
        # boiler master PID controller to control main steam pressure in MPa by manipulating coal feed rate
        m.fs_main.boiler_master_ctrl = PIDController(default={"pv":m.fs_main.main_steam_pressure,
                                  "mv":m.fs_main.fs_blr.aBoiler.flowrate_coal_raw,
                                  "type": 'PI'})    
    
        m.discretizer = pyo.TransformationFactory('dae.finite_difference')
        m.discretizer.apply_to(m,
                           nfe=nstep,
                           wrt=m.fs_main.config.time,
                           scheme="BACKWARD")

        # desired sliding pressure in MPa as a function of power demand in MW
        @m.fs_main.Expression(m.fs_main.config.time, doc="Sliding pressure as a function of power output")
        def sliding_pressure(b, t):
            return 12.551293+b.slope_pslide*(b.turbine_master_ctrl.setpoint[t]-250)

        # Constraint for setpoint of the slave controller of the three-element drum level controller 
        @m.fs_main.Constraint(m.fs_main.config.time, doc="Set point of drum level slave control")
        def drum_level_control_setpoint_eqn(b, t):
            return b.drum_slave_ctrl.setpoint[t] == b.flow_level_ctrl_output[t] + \
                   b.fs_blr.aPlaten.outlet.flow_mol[t] + \
                   b.fs_blr.blowdown_split.FW_Blowdown.flow_mol[t]  #revised to add steam flow only

        # Constraint for setpoint of boiler master
        @m.fs_main.Constraint(m.fs_main.config.time, doc="Set point of boiler master")
        def boiler_master_setpoint_eqn(b, t):
            return b.boiler_master_ctrl.setpoint[t] == 0.02*(b.turbine_master_ctrl.setpoint[t] - b.fs_stc.power_output[t]) + b.sliding_pressure[t]

        # Constraint for setpoint of boiler master
        @m.fs_main.Constraint(m.fs_main.config.time, doc="dry O2 in flue gas in dynamic mode")
        def dry_o2_in_flue_gas_dyn_eqn(b, t):
            return b.fs_blr.aBoiler.fluegas_o2_pct_dry[t] == 0.05*(b.fs_stc.spray_ctrl.setpoint[t] - b.fs_stc.temperature_main_steam[t]) - \
            0.0007652*b.fs_blr.aBoiler.flowrate_coal_raw[t]**3 + \
            0.06744*b.fs_blr.aBoiler.flowrate_coal_raw[t]**2 - 1.9815*b.fs_blr.aBoiler.flowrate_coal_raw[t] + 22.275

        # controller inputs
        # for master level controller
        m.fs_main.drum_master_ctrl.gain_p.fix(40000) #increased from 5000
        m.fs_main.drum_master_ctrl.gain_i.fix(100)
        m.fs_main.drum_master_ctrl.setpoint.fix(0.889)
        m.fs_main.drum_master_ctrl.mv_ref.fix(0)	#always zero regardless of load
        # for slave level controller, note the setpoint is defined by the constraint
        m.fs_main.drum_slave_ctrl.gain_p.fix(2e-2)  # increased from 1e-2
        m.fs_main.drum_slave_ctrl.gain_i.fix(2e-4)  # increased from 1e-4
        m.fs_main.drum_slave_ctrl.mv_ref.fix(0.5)
        # for turbine master controller, note the setpoint is the power demand
        m.fs_main.turbine_master_ctrl.gain_p.fix(5e-4) #changed from 2e-3
        m.fs_main.turbine_master_ctrl.gain_i.fix(5e-4) #changed from 2e-3
        m.fs_main.turbine_master_ctrl.mv_ref.fix(0.6)
        # for boiler master controller, note the setpoint is specified by the constraint
        m.fs_main.boiler_master_ctrl.gain_p.fix(10)
        m.fs_main.boiler_master_ctrl.gain_i.fix(0.25)
        m.fs_main.boiler_master_ctrl.mv_ref.fix(29.0)

        t0 = m.fs_main.config.time.first()
        m.fs_main.drum_master_ctrl.integral_of_error[t0].fix(0)
        m.fs_main.drum_slave_ctrl.integral_of_error[t0].fix(0)
        m.fs_main.turbine_master_ctrl.integral_of_error[t0].fix(0)
        m.fs_main.boiler_master_ctrl.integral_of_error[t0].fix(0)
        m.fs_main.flow_level_ctrl_output.value = 0
    else:
        @m.fs_main.Constraint(m.fs_main.config.time, doc="sliding pressure in MPa")
        def sliding_pressure_eqn(b, t):
            return b.main_steam_pressure[t] == 12.551293+b.slope_pslide*(b.fs_stc.power_output[t]-250)

    blr.set_arcs_and_constraints(m)
    blr.set_inputs(m)
    stc.set_arcs_and_constraints(m)
    stc.set_inputs(m)
    # Now that the mole is discreteized set and calculate scaling factors

    set_scaling_factors(m)
    add_overall_performance_expressions(m)

    # Add performance measures

    blr.initialize(m)
    stc.initialize(m)

    optarg={"tol":5e-7,"linear_solver":"ma27","max_iter":50}
    solver = pyo.SolverFactory("ipopt")
    solver.options = optarg

    _log.info("Bring models closer together...")
    m.fs_main.fs_blr.flow_mol_steam_rh_eqn.deactivate()
    # Hook the boiler to the steam cycle.
    m.fs_main.S001 = Arc(
        source=m.fs_main.fs_blr.aPlaten.outlet, destination=m.fs_main.fs_stc.turb.inlet_split.inlet
    )
    m.fs_main.S005 = Arc(
        source=m.fs_main.fs_stc.turb.hp_split[14].outlet_1, destination=m.fs_main.fs_blr.aRH1.tube_inlet
    )
    m.fs_main.S009 = Arc(
        source=m.fs_main.fs_blr.aRH2.tube_outlet, destination=m.fs_main.fs_stc.turb.ip_stages[1].inlet
    )
    m.fs_main.S042 = Arc(
        source=m.fs_main.fs_stc.fwh6.desuperheat.outlet_2, destination=m.fs_main.fs_blr.aECON.tube_inlet
    )
    m.fs_main.B006 = Arc(
        source=m.fs_main.fs_stc.spray_valve.outlet, destination=m.fs_main.fs_blr.Attemp.Water_inlet
    )
    pyo.TransformationFactory('network.expand_arcs').apply_to(m.fs_main)
    # unfix all connected streams
    m.fs_main.fs_stc.turb.inlet_split.inlet.unfix()
    m.fs_main.fs_stc.turb.hp_split[14].outlet_1.unfix()
    m.fs_main.fs_blr.aRH1.tube_inlet.unfix()
    m.fs_main.fs_stc.turb.ip_stages[1].inlet.unfix()
    m.fs_main.fs_blr.aECON.tube_inlet.unfix()
    m.fs_main.fs_blr.Attemp.Water_inlet.unfix()
    m.fs_main.fs_stc.spray_valve.outlet.unfix() #outlet pressure fixed on steam cycle sub-flowsheet
    # deactivate constraints on steam cycle flowsheet
    m.fs_main.fs_stc.fw_flow_constraint.deactivate()
    m.fs_main.fs_stc.turb.constraint_reheat_flow.deactivate()
    m.fs_main.fs_blr.aBoiler.flowrate_coal_raw.unfix() # steam circulation and coal flow are linked

    if m.dynamic==False:
        m.fs_main.fs_stc.spray_valve.valve_opening.unfix()
        m.fs_main.fs_stc.temperature_main_steam.fix(810)
        m.fs_main.fs_stc.turb.throttle_valve[1].valve_opening.unfix() # value is 0.75
        _log.info("Solve connected models...")
        print("Degrees of freedom = {}".format(degrees_of_freedom(m)))
        assert degrees_of_freedom(m) == 0
        res = solver.solve(m, tee=True)
        _log.info("Solved: {}".format(idaeslog.condition(res)))

        print ('fheat_ww=', pyo.value(m.fs_main.fs_blr.aBoiler.fcorrection_heat_ww[0]))
        print ('main steam enth=', pyo.value(m.fs_main.fs_stc.turb.inlet_split.inlet.enth_mol[0]))
        print ('main steam flow_mol=', pyo.value(m.fs_main.fs_stc.turb.inlet_split.inlet.flow_mol[0]))
        print ('main steam pressure=', pyo.value(m.fs_main.fs_blr.aPlaten.outlet.pressure[0]))
        print ('bfp turb steam flow=', pyo.value(m.fs_main.fs_stc.bfp_turb.inlet.flow_mol[0]))
        print ('FW pressure=', pyo.value(m.fs_main.fs_stc.bfp.outlet.pressure[0]))
        print ('HP stage 1 inlet enth_mol=', pyo.value(m.fs_main.fs_stc.turb.hp_stages[1].inlet.enth_mol[0]))
        print ('HP stage 1 inlet flow_mol=', pyo.value(m.fs_main.fs_stc.turb.hp_stages[1].inlet.flow_mol[0]))
        print ('HP stage 1 inlet pressure=', pyo.value(m.fs_main.fs_stc.turb.hp_stages[1].inlet.pressure[0]))
        print ('IP stage 1 inlet enth_mol=', pyo.value(m.fs_main.fs_stc.turb.ip_stages[1].inlet.enth_mol[0]))
        print ('IP stage 1 inlet flow_mol=', pyo.value(m.fs_main.fs_stc.turb.ip_stages[1].inlet.flow_mol[0]))
        print ('IP stage 1 inlet pressure=', pyo.value(m.fs_main.fs_stc.turb.ip_stages[1].inlet.pressure[0]))
        print ('Outlet stage enth_mol=', pyo.value(m.fs_main.fs_stc.turb.outlet_stage.outlet.enth_mol[0]))
        print ('Outlet stage flow_mol=', pyo.value(m.fs_main.fs_stc.turb.outlet_stage.outlet.flow_mol[0]))
        print ('Outlet stage pressure=', pyo.value(m.fs_main.fs_stc.turb.outlet_stage.outlet.pressure[0]))
        print ('Power output of main turbine=', pyo.value(m.fs_main.fs_stc.power_output[0]))
        print ('Power output of bfp turbine=', pyo.value(m.fs_main.fs_stc.bfp_turb.control_volume.work[0]+m.fs_main.fs_stc.bfp_turb_os.control_volume.work[0]))
        print ('FWH6 outlet enth_mol=', pyo.value(m.fs_main.fs_stc.fwh6.desuperheat.outlet_2.enth_mol[0]))
        print ('FWH6 outlet flow_mol=', pyo.value(m.fs_main.fs_stc.fwh6.desuperheat.outlet_2.flow_mol[0]))
        print ('FWH6 outlet pressure=', pyo.value(m.fs_main.fs_stc.fwh6.desuperheat.outlet_2.pressure[0]))
        print ('water makeup flow=', pyo.value(m.fs_main.fs_stc.condenser_hotwell.makeup.flow_mol[0]))
        print ('coal flow rate=', pyo.value(m.fs_main.fs_blr.aBoiler.flowrate_coal_raw[0]))
        print ('main steam temp=', pyo.value(m.fs_main.fs_blr.aPlaten.control_volume.properties_out[0].temperature))
        print ('RH2 outlet steam temp=', pyo.value(m.fs_main.fs_blr.aRH2.tube.properties[0,0].temperature))
        print ('FEGT=', pyo.value(m.fs_main.fs_blr.aBoiler.flue_gas_outlet.temperature[0]))
        print ('RH1 inlet enthalpy=', pyo.value(m.fs_main.fs_blr.aRH1.tube_inlet.enth_mol[0]))
        print ('RH1 inlet pressure=', pyo.value(m.fs_main.fs_blr.aRH1.tube_inlet.pressure[0]))
        print ('ECON outlet temperature=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 0].temperature))
        print ('ECON outlet temperature sat=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 0].temperature_sat))
        print ('ECON inlet temperature=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 1].temperature))
        print ('ECON inlet temperature sat=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 1].temperature_sat))
        print ('ECON inlet enth=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 1].enth_mol))
        print ('ECON inlet flow=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 1].flow_mol))
        print ('ECON inlet pressure=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 1].pressure))
        print ('Attemp water pressure=', pyo.value(m.fs_main.fs_blr.Attemp.Water_inlet.pressure[0]))
        print ('Attemp water enth=', pyo.value(m.fs_main.fs_blr.Attemp.Water_inlet.enth_mol[0]))
        print('Cv fwh2=', m.fs_main.fs_stc.fwh2_valve.Cv.value)
        print('Cv fwh3=', m.fs_main.fs_stc.fwh3_valve.Cv.value)
        print('Cv fwh5=', m.fs_main.fs_stc.fwh5_valve.Cv.value)
        print('Cv fwh6=', m.fs_main.fs_stc.fwh6_valve.Cv.value)
        print('Cv cond_valve=', m.fs_main.fs_stc.cond_valve.Cv.value)
        print('Cv makeup_valve=', m.fs_main.fs_stc.makeup_valve.Cv.value)
        print('Cv hotwell_rejection_valve=', m.fs_main.fs_stc.hotwell_rejection_valve.Cv.value)
        print('Cv da_rejection_valve=', m.fs_main.fs_stc.da_rejection_valve.Cv.value)
        print('Cv spray_valve=', m.fs_main.fs_stc.spray_valve.Cv.value)
        print('Cv bfp_turb_valve=', m.fs_main.fs_stc.bfp_turb_valve.Cv.value)
        print('Cv throttle valve=', m.fs_main.fs_stc.turb.throttle_valve[1].Cv.value)
        print('valve opening fwh2=', m.fs_main.fs_stc.fwh2_valve.valve_opening[0].value)
        print('valve opening fwh3=', m.fs_main.fs_stc.fwh3_valve.valve_opening[0].value)
        print('valve opening fwh5=', m.fs_main.fs_stc.fwh5_valve.valve_opening[0].value)
        print('valve opening fwh6=', m.fs_main.fs_stc.fwh6_valve.valve_opening[0].value)
        print('valve opening cond_valve=', m.fs_main.fs_stc.cond_valve.valve_opening[0].value)
        print('valve opening makeup_valve=', m.fs_main.fs_stc.makeup_valve.valve_opening[0].value)
        print('valve opening hotwell_rejection_valve=', m.fs_main.fs_stc.hotwell_rejection_valve.valve_opening[0].value)
        print('valve opening da_rejection_valve=', m.fs_main.fs_stc.da_rejection_valve.valve_opening[0].value)
        print('valve opening spray_valve=', m.fs_main.fs_stc.spray_valve.valve_opening[0].value)
        print('valve opening bfp_turb_valve=', m.fs_main.fs_stc.bfp_turb_valve.valve_opening[0].value)
        print('valve opening throttle=', m.fs_main.fs_stc.turb.throttle_valve[1].valve_opening[0].value)
        print('fwh2 level=', m.fs_main.fs_stc.fwh2.condense.level[0].value)
        print('fwh3 level=', m.fs_main.fs_stc.fwh3.condense.level[0].value)
        print('fwh5 level=', m.fs_main.fs_stc.fwh5.condense.level[0].value)
        print('fwh6 level=', m.fs_main.fs_stc.fwh6.condense.level[0].value)
        print('hotwell tank level=', m.fs_main.fs_stc.hotwell_tank.tank_level[0].value)
        print('da tank level=', m.fs_main.fs_stc.da_tank.tank_level[0].value)
        print('hotwell rejection flow=',  m.fs_main.fs_stc.hotwell_rejection_valve.outlet.flow_mol[0].value)
        print('da rejection flow=',  m.fs_main.fs_stc.da_rejection_valve.outlet.flow_mol[0].value)
        print('makeup flow=',  m.fs_main.fs_stc.makeup_valve.outlet.flow_mol[0].value)
        print('spray flow=',  m.fs_main.fs_stc.spray_valve.outlet.flow_mol[0].value)
        print('cond split fraction 1=',  m.fs_main.fs_stc.cond_split.split_fraction[0,"outlet_1"].value)
        print('cond split fraction 2=',  m.fs_main.fs_stc.cond_split.split_fraction[0,"outlet_2"].value)
        print('cond split fraction 3=',  m.fs_main.fs_stc.cond_split.split_fraction[0,"outlet_3"].value)
        print('bfp turb flow=', m.fs_main.fs_stc.bfp_turb_valve.outlet.flow_mol[0].value)
        print('bfp turb valve inlet pressure=', m.fs_main.fs_stc.bfp_turb_valve.inlet.pressure[0].value)
        print('bfp turb inlet pressure=', m.fs_main.fs_stc.bfp_turb.inlet.pressure[0].value)
        print('bfp turb outlet pressure=', m.fs_main.fs_stc.bfp_turb.outlet.pressure[0].value)
        print('bfp turb os outlet pressure=', m.fs_main.fs_stc.bfp_turb_os.outlet.pressure[0].value)
        print('bfp turb efficiency=', m.fs_main.fs_stc.bfp_turb.efficiency_isentropic[0].value)
        print('bfp turb os efficiency=', m.fs_main.fs_stc.bfp_turb_os.efficiency_isentropic[0].value)
        print('bfp turb valve open=', m.fs_main.fs_stc.bfp_turb_valve.valve_opening[0].value)
        print('bfp turb os inlet vapor frac=', pyo.value(m.fs_main.fs_stc.bfp_turb_os.control_volume.properties_in[0].vapor_frac))
        print('bfp turb os outlet vapor frac=', pyo.value(m.fs_main.fs_stc.bfp_turb_os.control_volume.properties_out[0].vapor_frac))
        print('gross heat rate=', pyo.value(m.fs_main.gross_heat_rate[0]))
        print('SA temperature=', pyo.value(m.fs_main.fs_blr.aBoiler.secondary_air_inlet.temperature[0]))
        
        # set load to 250 MW
        _log.info("Set power output is 250 MW...")
        m.fs_main.fs_stc.bfp.outlet.pressure.unfix()
        m.fs_main.fs_blr.aBoiler.flowrate_coal_raw.unfix()
        m.fs_main.fs_stc.power_output.fix(250)
        res = solver.solve(m, tee=True)

        print ('fheat_ww=', pyo.value(m.fs_main.fs_blr.aBoiler.fcorrection_heat_ww[0]))
        print ('main steam enth=', pyo.value(m.fs_main.fs_stc.turb.inlet_split.inlet.enth_mol[0]))
        print ('main steam flow_mol=', pyo.value(m.fs_main.fs_stc.turb.inlet_split.inlet.flow_mol[0]))
        print ('main steam pressure=', pyo.value(m.fs_main.fs_blr.aPlaten.outlet.pressure[0]))
        print ('bfp turb steam flow=', pyo.value(m.fs_main.fs_stc.bfp_turb.inlet.flow_mol[0]))
        print ('FW pressure=', pyo.value(m.fs_main.fs_stc.bfp.outlet.pressure[0]))
        print ('HP stage 1 inlet enth_mol=', pyo.value(m.fs_main.fs_stc.turb.hp_stages[1].inlet.enth_mol[0]))
        print ('HP stage 1 inlet flow_mol=', pyo.value(m.fs_main.fs_stc.turb.hp_stages[1].inlet.flow_mol[0]))
        print ('HP stage 1 inlet pressure=', pyo.value(m.fs_main.fs_stc.turb.hp_stages[1].inlet.pressure[0]))
        print ('IP stage 1 inlet enth_mol=', pyo.value(m.fs_main.fs_stc.turb.ip_stages[1].inlet.enth_mol[0]))
        print ('IP stage 1 inlet flow_mol=', pyo.value(m.fs_main.fs_stc.turb.ip_stages[1].inlet.flow_mol[0]))
        print ('IP stage 1 inlet pressure=', pyo.value(m.fs_main.fs_stc.turb.ip_stages[1].inlet.pressure[0]))
        print ('Outlet stage enth_mol=', pyo.value(m.fs_main.fs_stc.turb.outlet_stage.outlet.enth_mol[0]))
        print ('Outlet stage flow_mol=', pyo.value(m.fs_main.fs_stc.turb.outlet_stage.outlet.flow_mol[0]))
        print ('Outlet stage pressure=', pyo.value(m.fs_main.fs_stc.turb.outlet_stage.outlet.pressure[0]))
        print ('Power output of main turbine=', pyo.value(m.fs_main.fs_stc.power_output[0]))
        print ('Power output of bfp turbine=', pyo.value(m.fs_main.fs_stc.bfp_turb.control_volume.work[0]+m.fs_main.fs_stc.bfp_turb_os.control_volume.work[0]))
        print ('FWH6 outlet enth_mol=', pyo.value(m.fs_main.fs_stc.fwh6.desuperheat.outlet_2.enth_mol[0]))
        print ('FWH6 outlet flow_mol=', pyo.value(m.fs_main.fs_stc.fwh6.desuperheat.outlet_2.flow_mol[0]))
        print ('FWH6 outlet pressure=', pyo.value(m.fs_main.fs_stc.fwh6.desuperheat.outlet_2.pressure[0]))
        print ('water makeup flow=', pyo.value(m.fs_main.fs_stc.condenser_hotwell.makeup.flow_mol[0]))
        print ('coal flow rate=', pyo.value(m.fs_main.fs_blr.aBoiler.flowrate_coal_raw[0]))
        print ('main steam temp=', pyo.value(m.fs_main.fs_blr.aPlaten.control_volume.properties_out[0].temperature))
        print ('RH2 outlet steam temp=', pyo.value(m.fs_main.fs_blr.aRH2.tube.properties[0,0].temperature))
        print ('FEGT=', pyo.value(m.fs_main.fs_blr.aBoiler.flue_gas_outlet.temperature[0]))
        print ('RH1 inlet enthalpy=', pyo.value(m.fs_main.fs_blr.aRH1.tube_inlet.enth_mol[0]))
        print ('RH1 inlet pressure=', pyo.value(m.fs_main.fs_blr.aRH1.tube_inlet.pressure[0]))
        print ('ECON outlet temperature=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 0].temperature))
        print ('ECON outlet temperature sat=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 0].temperature_sat))
        print ('ECON inlet temperature=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 1].temperature))
        print ('ECON inlet temperature sat=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 1].temperature_sat))
        print ('ECON inlet enth=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 1].enth_mol))
        print ('ECON inlet flow=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 1].flow_mol))
        print ('ECON inlet pressure=', pyo.value(m.fs_main.fs_blr.aECON.tube.properties[0, 1].pressure))
        print ('Attemp water pressure=', pyo.value(m.fs_main.fs_blr.Attemp.Water_inlet.pressure[0]))
        print ('Attemp water enth=', pyo.value(m.fs_main.fs_blr.Attemp.Water_inlet.enth_mol[0]))
        print('Cv fwh2=', m.fs_main.fs_stc.fwh2_valve.Cv.value)
        print('Cv fwh3=', m.fs_main.fs_stc.fwh3_valve.Cv.value)
        print('Cv fwh5=', m.fs_main.fs_stc.fwh5_valve.Cv.value)
        print('Cv fwh6=', m.fs_main.fs_stc.fwh6_valve.Cv.value)
        print('Cv cond_valve=', m.fs_main.fs_stc.cond_valve.Cv.value)
        print('Cv makeup_valve=', m.fs_main.fs_stc.makeup_valve.Cv.value)
        print('Cv hotwell_rejection_valve=', m.fs_main.fs_stc.hotwell_rejection_valve.Cv.value)
        print('Cv da_rejection_valve=', m.fs_main.fs_stc.da_rejection_valve.Cv.value)
        print('Cv spray_valve=', m.fs_main.fs_stc.spray_valve.Cv.value)
        print('Cv bfp_turb_valve=', m.fs_main.fs_stc.bfp_turb_valve.Cv.value)
        print('Cv throttle valve=', m.fs_main.fs_stc.turb.throttle_valve[1].Cv.value)
        print('valve opening fwh2=', m.fs_main.fs_stc.fwh2_valve.valve_opening[0].value)
        print('valve opening fwh3=', m.fs_main.fs_stc.fwh3_valve.valve_opening[0].value)
        print('valve opening fwh5=', m.fs_main.fs_stc.fwh5_valve.valve_opening[0].value)
        print('valve opening fwh6=', m.fs_main.fs_stc.fwh6_valve.valve_opening[0].value)
        print('valve opening cond_valve=', m.fs_main.fs_stc.cond_valve.valve_opening[0].value)
        print('valve opening makeup_valve=', m.fs_main.fs_stc.makeup_valve.valve_opening[0].value)
        print('valve opening hotwell_rejection_valve=', m.fs_main.fs_stc.hotwell_rejection_valve.valve_opening[0].value)
        print('valve opening da_rejection_valve=', m.fs_main.fs_stc.da_rejection_valve.valve_opening[0].value)
        print('valve opening spray_valve=', m.fs_main.fs_stc.spray_valve.valve_opening[0].value)
        print('valve opening bfp_turb_valve=', m.fs_main.fs_stc.bfp_turb_valve.valve_opening[0].value)
        print('valve opening throttle=', m.fs_main.fs_stc.turb.throttle_valve[1].valve_opening[0].value)
        print('fwh2 level=', m.fs_main.fs_stc.fwh2.condense.level[0].value)
        print('fwh3 level=', m.fs_main.fs_stc.fwh3.condense.level[0].value)
        print('fwh5 level=', m.fs_main.fs_stc.fwh5.condense.level[0].value)
        print('fwh6 level=', m.fs_main.fs_stc.fwh6.condense.level[0].value)
        print('hotwell tank level=', m.fs_main.fs_stc.hotwell_tank.tank_level[0].value)
        print('da tank level=', m.fs_main.fs_stc.da_tank.tank_level[0].value)
        print('hotwell rejection flow=',  m.fs_main.fs_stc.hotwell_rejection_valve.outlet.flow_mol[0].value)
        print('da rejection flow=',  m.fs_main.fs_stc.da_rejection_valve.outlet.flow_mol[0].value)
        print('makeup flow=',  m.fs_main.fs_stc.makeup_valve.outlet.flow_mol[0].value)
        print('spray flow=',  m.fs_main.fs_stc.spray_valve.outlet.flow_mol[0].value)
        print('cond split fraction 1=',  m.fs_main.fs_stc.cond_split.split_fraction[0,"outlet_1"].value)
        print('cond split fraction 2=',  m.fs_main.fs_stc.cond_split.split_fraction[0,"outlet_2"].value)
        print('cond split fraction 3=',  m.fs_main.fs_stc.cond_split.split_fraction[0,"outlet_3"].value)
        print('bfp turb flow=', m.fs_main.fs_stc.bfp_turb_valve.outlet.flow_mol[0].value)
        print('bfp turb valve inlet pressure=', m.fs_main.fs_stc.bfp_turb_valve.inlet.pressure[0].value)
        print('bfp turb inlet pressure=', m.fs_main.fs_stc.bfp_turb.inlet.pressure[0].value)
        print('bfp turb outlet pressure=', m.fs_main.fs_stc.bfp_turb.outlet.pressure[0].value)
        print('bfp turb os outlet pressure=', m.fs_main.fs_stc.bfp_turb_os.outlet.pressure[0].value)
        print('bfp turb efficiency=', m.fs_main.fs_stc.bfp_turb.efficiency_isentropic[0].value)
        print('bfp turb os efficiency=', m.fs_main.fs_stc.bfp_turb_os.efficiency_isentropic[0].value)
        print('bfp turb valve open=', m.fs_main.fs_stc.bfp_turb_valve.valve_opening[0].value)
        print('bfp turb os inlet vapor frac=', pyo.value(m.fs_main.fs_stc.bfp_turb_os.control_volume.properties_in[0].vapor_frac))
        print('bfp turb os outlet vapor frac=', pyo.value(m.fs_main.fs_stc.bfp_turb_os.control_volume.properties_out[0].vapor_frac))
        print('gross heat rate=', pyo.value(m.fs_main.gross_heat_rate[0]))
        print('SA temperature=', pyo.value(m.fs_main.fs_blr.aBoiler.secondary_air_inlet.temperature[0]))
    else:
        m.fs_main.fs_blr.dry_o2_in_flue_gas_eqn.deactivate()
        t0 = m.fs_main.config.time.first()
        m.fs_main.fs_stc.fwh2.condense.level[t0].fix()
        m.fs_main.fs_stc.fwh3.condense.level[t0].fix()
        m.fs_main.fs_stc.fwh5.condense.level[t0].fix()
        m.fs_main.fs_stc.fwh6.condense.level[t0].fix()
        m.fs_main.fs_stc.hotwell_tank.tank_level[t0].fix()
        m.fs_main.fs_stc.da_tank.tank_level[t0].fix()
        m.fs_main.fs_stc.temperature_main_steam[t0].unfix()
        m.fs_main.fs_stc.spray_valve.valve_opening[t0].fix()
        m.fs_main.fs_blr.aDrum.level.unfix()
        m.fs_main.fs_blr.aDrum.level[t0].fix()
        m.fs_main.flow_level_ctrl_output.unfix()
        m.fs_main.flow_level_ctrl_output[t0].fix()
        m.fs_main.fs_stc.bfp.outlet.pressure.unfix()
        m.fs_main.fs_blr.aBoiler.flowrate_coal_raw.unfix()
        m.fs_main.fs_blr.aBoiler.flowrate_coal_raw[t0].fix()
        m.fs_main.fs_stc.turb.throttle_valve[1].valve_opening.unfix()
        m.fs_main.fs_stc.turb.throttle_valve[1].valve_opening[t0].fix()
        m.fs_main.turbine_master_ctrl.setpoint.fix()

    return m


def run_dynamic(m, x0, t0, pd, solver):
    # set input profile
    i = 0
    for t in m.fs_main.config.time:
        power_demand = input_profile(t0+t, x0)
        m.fs_main.turbine_master_ctrl.setpoint[t].value = power_demand
        print ('Point i, t, power demand=', i, t+t0, power_demand)
        i += 1
    df = degrees_of_freedom(m)
    print ("***************degree of freedom = ", df, "********************")
    '''
    solver = pyo.SolverFactory("ipopt")
    solver.options = {
            "tol": 1e-7,
            "linear_solver": "ma27",
            "max_iter": 60,
    }
    '''
    # Initialize by time element
    #initialize_by_time_element(m.fs_main, m.fs_main.config.time, solver=solver, outlvl=idaeslog.DEBUG)
    #print('dof after integrating:', degrees_of_freedom(m.fs_main))
    results = solver.solve(m, tee=True)

    # Print results
    print(results)
    print()

        
    # append results
    for t in m.fs_main.config.time:
        if t==0 and len(pd['time'])>0:
            continue
        pd['time'].append(t+t0)
        pd['coal_flow'].append(m.fs_main.fs_blr.aBoiler.flowrate_coal_raw[t].value)
        pd['PA_to_APH_flow'].append(pyo.value(m.fs_main.fs_blr.aAPH.side_2.properties_in[t].flow_mol))
        pd['PA_temp_flow'].append(pyo.value(m.fs_main.fs_blr.Mixer_PA.TA_inlet_state[t].flow_mol))
        pd['SA_flow'].append(pyo.value(m.fs_main.fs_blr.aAPH.side_3.properties_in[t].flow_mol))
        pd['SR'].append(m.fs_main.fs_blr.aBoiler.SR[t].value)
        pd['dry_O2_pct_in_flue_gas'].append(m.fs_main.fs_blr.aBoiler.fluegas_o2_pct_dry[t].value)
        pd['bfpt_opening'].append(m.fs_main.fs_stc.bfp_turb_valve.valve_opening[t].value)
        pd['gross_power'].append(pyo.value(m.fs_main.fs_stc.power_output[t]))
        pd['ww_heat'].append(pyo.value(m.fs_main.fs_blr.aBoiler.heat_total_ww[t])/1e6)
        pd['fegt'].append(m.fs_main.fs_blr.aBoiler.flue_gas_outlet.temperature[t].value)
        pd['drum_level'].append(m.fs_main.fs_blr.aDrum.level[t].value)
        pd['feed_water_flow_sp'].append(m.fs_main.drum_slave_ctrl.setpoint[t].value)
        pd['drum_master_ctrl_op'].append(m.fs_main.flow_level_ctrl_output[t].value)
        pd['feed_water_flow'].append(m.fs_main.fs_blr.aECON.tube_inlet.flow_mol[t].value)
        pd['main_steam_flow'].append(m.fs_main.fs_blr.aPlaten.outlet.flow_mol[t].value)
        pd['rh_steam_flow'].append(m.fs_main.fs_blr.aRH2.tube_outlet.flow_mol[t].value)
        pd['bfpt_flow'].append(m.fs_main.fs_stc.bfp_turb_valve.outlet.flow_mol[t].value)
        pd['spray_flow'].append(m.fs_main.fs_stc.spray_valve.outlet.flow_mol[t].value)
        pd['main_steam_temp'].append(m.fs_main.fs_stc.temperature_main_steam[t].value)
        pd['rh_steam_temp'].append(pyo.value(m.fs_main.fs_blr.aRH2.tube.properties[t,0].temperature))
        pd['fw_pres'].append(m.fs_main.fs_stc.bfp.outlet.pressure[t].value/1e6)
        pd['drum_pres'].append(m.fs_main.fs_blr.aDrum.water_steam_inlet.pressure[t].value/1e6)
        pd['main_steam_pres'].append(m.fs_main.main_steam_pressure[t].value)
        pd['rh_steam_pres'].append(m.fs_main.fs_blr.aRH2.tube_outlet.pressure[t].value/1e6)
        pd['hw_tank_level'].append(m.fs_main.fs_stc.hotwell_tank.tank_level[t].value)
        pd['da_tank_level'].append(m.fs_main.fs_stc.da_tank.tank_level[t].value)
        pd['fwh2_level'].append(m.fs_main.fs_stc.fwh2.condense.level[t].value)
        pd['fwh3_level'].append(m.fs_main.fs_stc.fwh3.condense.level[t].value)
        pd['fwh5_level'].append(m.fs_main.fs_stc.fwh5.condense.level[t].value)
        pd['fwh6_level'].append(m.fs_main.fs_stc.fwh6.condense.level[t].value)
        pd['makeup_valve_opening'].append(m.fs_main.fs_stc.makeup_valve.valve_opening[t].value)
        pd['cond_valve_opening'].append(m.fs_main.fs_stc.cond_valve.valve_opening[t].value)
        pd['fwh2_valve_opening'].append(m.fs_main.fs_stc.fwh2_valve.valve_opening[t].value)
        pd['fwh3_valve_opening'].append(m.fs_main.fs_stc.fwh3_valve.valve_opening[t].value)
        pd['fwh5_valve_opening'].append(m.fs_main.fs_stc.fwh5_valve.valve_opening[t].value)
        pd['fwh6_valve_opening'].append(m.fs_main.fs_stc.fwh6_valve.valve_opening[t].value)
        pd['spray_valve_opening'].append(m.fs_main.fs_stc.spray_valve.valve_opening[t].value)
        pd['tube_temp_rh2'].append(m.fs_main.fs_blr.aRH2.shell_wall_temperature[t,0].value)
        pd['temp_fg_econ_exit'].append(m.fs_main.fs_blr.aECON.shell_outlet.temperature[t].value)
        pd['temp_fg_aph_exit'].append(m.fs_main.fs_blr.aAPH.side_1_outlet.temperature[t].value)
        pd['throttle_opening'].append(m.fs_main.fs_stc.turb.throttle_valve[1].valve_opening[t].value)
        pd['load_demand'].append(m.fs_main.turbine_master_ctrl.setpoint[t].value)
        pd['sliding_pressure'].append(pyo.value(m.fs_main.sliding_pressure[t]))
        pd['steam_pressure_sp'].append(m.fs_main.boiler_master_ctrl.setpoint[t].value)
        pd['deaerator_pressure'].append(m.fs_main.fs_stc.da_tank.inlet.pressure[t].value/1e6)
        pd['temp_econ_in'].append(pyo.value(m.fs_main.fs_blr.aECON.tube.properties[t,1].temperature))
        pd['temp_econ_out'].append(pyo.value(m.fs_main.fs_blr.aECON.tube.properties[t,0].temperature))
        pd['temp_econ_out_sat'].append(pyo.value(m.fs_main.fs_blr.aECON.tube.properties[t,0].temperature_sat))
        pd['boiler_efficiency_heat'].append(pyo.value(m.fs_main.fs_blr.boiler_efficiency_heat[t]))
        pd['boiler_efficiency_steam'].append(pyo.value(m.fs_main.fs_blr.boiler_efficiency_steam[t]))
        pd['steam_cycle_efficiency'].append(pyo.value(m.fs_main.steam_cycle_eff[t]))
        pd['plant_gross_efficiency'].append(pyo.value(m.fs_main.plant_gross_efficiency[t]))
        pd['gross_heat_rate'].append(pyo.value(m.fs_main.gross_heat_rate[t]))
        
        # Boiler health related data
        # For drum
        pd['drum_inner_wall_temperature'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.drum_wall_temperature
                      [t, m.fs_main.fs_blr.aDrum.radial_domain.first()]))
        pd['drum_outer_wall_temperature'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.drum_wall_temperature
                      [t, m.fs_main.fs_blr.aDrum.radial_domain.last()]))
        pd['drum_inner_theta_sigma_m'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.mech_sigma_theta
                      [t, m.fs_main.fs_blr.aDrum.radial_domain.first()]))
        pd['drum_inner_theta_sigma_t'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.therm_sigma_theta
                      [t, m.fs_main.fs_blr.aDrum.radial_domain.first()]))
        pd['drum_inner_vM_sigma'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.sigma_von_Mises
                      [t, m.fs_main.fs_blr.aDrum.radial_domain.first()]))
        pd['drum_outer_theta_sigma_m'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.mech_sigma_theta
                      [t, m.fs_main.fs_blr.aDrum.radial_domain.last()]))
        pd['drum_outer_theta_sigma_t'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.therm_sigma_theta
                      [t, m.fs_main.fs_blr.aDrum.radial_domain.last()]))
        pd['drum_outer_vM_sigma'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.sigma_von_Mises
                      [t, m.fs_main.fs_blr.aDrum.radial_domain.last()]))
        pd['drum_delta_sigma_r_theta_outer'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.delta_sigma_r_theta
                      [t, m.fs_main.fs_blr.aDrum.radial_domain.last()]))
        pd['drum_delta_sigma_theta_z_outer'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.delta_sigma_theta_z
                      [t, m.fs_main.fs_blr.aDrum.radial_domain.last()]))
        pd['drum_delta_sigma_z_r_outer'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.delta_sigma_z_r
                      [t, m.fs_main.fs_blr.aDrum.radial_domain.last()]))
        pd['drum_circumferential_P1'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.sigma_theta_P1[t]))
        pd['drum_circumferential_P2'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.sigma_theta_P2[t]))
        pd['drum_von_Mises_P1'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.sigma_eff_P1[t]))
        pd['drum_von_Mises_P2'].append(
            pyo.value(m.fs_main.fs_blr.aDrum.sigma_eff_P2[t]))

        # For primary superheater
        pd['PSH_flue_gas_flow_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.shell.properties[t, 0].flow_mol))
        pd['PSH_steam_flow_disc9'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube.properties[t, 1].flow_mol))
        pd['PSH_steam_temperature_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube.properties[t, 0].temperature))
        pd['PSH_steam_temperature_disc2'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube
                      .properties[t, 0.166667].temperature))
        pd['PSH_steam_temperature_disc4'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube
                      .properties[t, 0.5].temperature))
        pd['PSH_steam_temperature_disc8'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube
                      .properties[t, 0.833333].temperature))
        pd['PSH_steam_temperature_disc9'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube.properties[t, 1].temperature))
        pd['PSH_temp_wall_tube_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube_wall_temperature
                      [t, 0, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_temp_wall_tube_disc2'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube_wall_temperature
                      [t, 0.166667, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_temp_wall_tube_disc4'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube_wall_temperature
                      [t, 0.5, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_temp_wall_tube_disc8'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube_wall_temperature
                      [t, 0.833333, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_temp_wall_tube_disc9'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube_wall_temperature
                      [t, 1, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_temp_wall_shell_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube_wall_temperature
                      [t, 0, m.fs_main.fs_blr.aPSH.r.last()]))
        pd['PSH_temp_wall_shell_disc2'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube_wall_temperature
                      [t, 0.166667, m.fs_main.fs_blr.aPSH.r.last()]))
        pd['PSH_temp_wall_shell_disc4'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube_wall_temperature
                      [t, 0.5, m.fs_main.fs_blr.aPSH.r.last()]))
        pd['PSH_temp_wall_shell_disc8'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube_wall_temperature
                      [t, 0.833333, m.fs_main.fs_blr.aPSH.r.last()]))
        pd['PSH_temp_wall_shell_disc9'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.tube_wall_temperature
                      [t, 1, m.fs_main.fs_blr.aPSH.r.last()]))
        pd['PSH_temp_wall_shell_fouling_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.shell_wall_temperature[t, 0]))
        pd['PSH_temp_wall_shell_fouling_disc2'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.shell_wall_temperature
                      [t, 0.166667]))
        pd['PSH_temp_wall_shell_fouling_disc4'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.shell_wall_temperature[t, 0.5]))
        pd['PSH_temp_wall_shell_fouling_disc8'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.shell_wall_temperature
                      [t, 0.833333]))
        pd['PSH_temp_wall_shell_fouling_disc9'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.shell_wall_temperature[t, 1]))
        pd['PSH_flue_gas_temperature_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.shell
                      .properties[t, 0].temperature))
        pd['PSH_flue_gas_temperature_disc2'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.shell
                      .properties[t, 0.166667].temperature))
        pd['PSH_flue_gas_temperature_disc4'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.shell
                      .properties[t, 0.5].temperature))
        pd['PSH_flue_gas_temperature_disc8'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.shell
                      .properties[t, 0.833333].temperature))
        pd['PSH_flue_gas_temperature_disc9'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.shell
                      .properties[t, 1].temperature))
        pd['PSH_von_Mises_inside_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.sigma_von_Mises
                      [t, 0, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_von_Mises_inside_disc2'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.sigma_von_Mises
                      [t, 0.166667, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_von_Mises_inside_disc4'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.sigma_von_Mises
                      [t, 0.5, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_von_Mises_inside_disc8'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.sigma_von_Mises
                      [t, 0.833333, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_von_Mises_inside_disc9'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.sigma_von_Mises
                      [t, 1, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_delta_s12_inside_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.delta_sigma_r_theta
                      [t, 0, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_delta_s23_inside_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.delta_sigma_theta_z
                      [t, 0, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_delta_s31_inside_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.delta_sigma_z_r
                      [t, 0, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_mech_circumferential_inside_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.mech_sigma_theta
                      [t, 0, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_ther_circumferential_inside_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.therm_sigma_theta
                      [t, 0, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_circumferential_inside_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.sigma_theta
                      [t, 0, m.fs_main.fs_blr.aPSH.r.first()]))
        pd['PSH_mech_circumferential_outside_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.mech_sigma_theta
                      [t, 0, m.fs_main.fs_blr.aPSH.r.last()]))
        pd['PSH_ther_circumferential_outside_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.therm_sigma_theta
                      [t, 0, m.fs_main.fs_blr.aPSH.r.last()]))
        pd['PSH_circumferential_outside_disc1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.sigma_theta
                      [t, 0, m.fs_main.fs_blr.aPSH.r.last()]))

        # For primary superheater header
        pd['Header_inner_temperature'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.header_wall_temperature
                      [t, m.fs_main.fs_blr.aPSH.head_r.first()]))
        pd['Header_outside_temperature'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.header_wall_temperature
                      [t, m.fs_main.fs_blr.aPSH.head_r.last()]))
        pd['Header_circumferential_P1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.sigma_theta_P1[t]))
        pd['Header_circumferential_P2'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.sigma_theta_P2[t]))
        pd['Header_circumferential_body'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.sigma_theta_header
                      [t, m.fs_main.fs_blr.aPSH.head_r.first()]))
        pd['Header_von_Mises_P1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.sigma_eff_P1[t]))
        pd['Header_von_Mises_P2'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.sigma_eff_P2[t]))
        pd['Header_rupture_time_P1'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.rupture_time_crotch_corner[t]))
        pd['Header_rupture_time_P2'].append(
            pyo.value(m.fs_main.fs_blr.aPSH.rupture_time_P2[t]))

def calculate_allowable_cycles(m,pd):
    # calculate number of allowable cycles for drum
    parser = argparse.ArgumentParser(description='Select case to simulate')
    parser.add_argument("--case",
                    choices=["drum", "header"],
                    default="drum",
                    help="Case to simulate")
    args = parser.parse_args()
    if args.case == "drum":
        # data_export = pd['drum_Tresca_equi_stress_last']
        delta_s12 = pd['drum_delta_sigma_r_theta_outer']
        delta_s23 = pd['drum_delta_sigma_theta_z_outer']
        delta_s31 = pd['drum_delta_sigma_z_r_outer']
        drum_prin_struc_radial = pd['drum_outer_sigma_r']
        drum_prin_struc_circumferential = pd['drum_outer_sigma_theta']
        drum_prin_struc_axial = pd['drum_outer_sigma_z']
        delta_sigma_D =  400             # the thermal endurance limit, Table 18.10, EN 13445, page 502
        delta_sigma_cut = 270            # the cut-off limit, Table 18.10, EN 13445, page 502
        Rm = (590+620)/2            # Tensile strength [N/mm2]
        Rp = (330+360)/2            # the yield strength of material
        T_max = 360                 # the metal temperature during the moment of the highest stress [C]
        T_min = 310                 # the metal temperature during the moment of lowest stress [C]
        K_t =  3.0                  # Thermal stress correction factor
        Rz = 50                     # the peak-to-valley height (micrometer), 50 for machine, 10 for ground, free of notches
        RO = pyo.value(m.fs_main.fs_blr.aDrum.r.last())
        RI = pyo.value(m.fs_main.fs_blr.aDrum.r.first())
        thickness = pyo.value(m.fs_main.fs_blr.aDrum.drum_thickness)
    else:
        data_export = pd['Header_von_Mises_P1']
        n = len(pd['Header_von_Mises_P1'])
        delta_sigma_D =  273             # the thermal endurance limit, Table 18.10, EN 13445, page 502
        delta_sigma_cut = 184            # the cut-off limit, Table 18.10, EN 13445, page 502
        Rm = 380                    # Tensile strength [N/mm2]
        Rp = 230                    # the yield strength of material
        T_max = (727.3282-273.15)                 # the metal temperature during the moment of the highest stress [C]
        T_min = (714.2341-273.15)                 # the metal temperature during the moment of lowest stress [C]
        K_t =  3.0                  # Thermal stress correction factor
        Rz = 50                     # the peak-to-valley height (micrometer), 50 for machine, 10 for ground, free of notches

        RO = pyo.value(m.fs_main.fs_blr.aPSH.head_ro)     # outside radius
        RI = pyo.value(m.fs_main.fs_blr.aPSH.head_ri)     # inside radius
        thickness = pyo.value(m.fs_main.fs_blr.aPSH.head_thickness) # thickness

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

    if args.case == "drum":
        # calculate max-min
        n_s12 = len(delta_s12)
        delta_s12_max = max_value_find(delta_s12,n_s12)
        delta_s12_min = min_value_find(delta_s12,n_s12)
        s12 = pyo.value(abs(delta_s12_max-delta_s12_min))

        n_s23 = len(delta_s23)
        delta_s23_max = max_value_find(delta_s23,n_s23)
        delta_s23_min = min_value_find(delta_s23,n_s23)
        s23 = pyo.value(abs(delta_s23_max-delta_s23_min))

        n_s31 = len(delta_s31)
        delta_s31_max = max_value_find(delta_s31,n_s31)
        delta_s31_min = min_value_find(delta_s31,n_s31)
        s31 = pyo.value(abs(delta_s31_max-delta_s31_min))

        Tresca = max(s12, s23, s31)
        print('Tresca equivalent stress =', pyo.value(Tresca))
        if s12 > s23 and s12 > s31:
            Ans_max = delta_s12_max
            Ans_min = delta_s12_min
            delta_sigma = Ans_max - Ans_min
            # calculate max, min for mean equivalent stress
            n_radial = len(drum_prin_struc_radial)
            n_circumferential = len(drum_prin_struc_circumferential)
            max_radial = max_value_find(drum_prin_struc_radial,n_radial)
            max_circumferential = max_value_find(drum_prin_struc_circumferential,n_circumferential)
            min_radial = min_value_find(drum_prin_struc_radial,n_radial)
            min_circumferential = min_value_find(drum_prin_struc_circumferential,n_circumferential)
            sigma_mean = pyo.value(0.5*((max_radial+max_circumferential)+(min_radial+min_circumferential)))
        elif s23 > s12 and s23 > s31:
            Ans_max = delta_s23_max
            Ans_min = delta_s23_min
            delta_sigma = Ans_max - Ans_min
            # calculate max, min for mean equivalent stress
            n_axial = len(drum_prin_struc_axial)
            n_circumferential = len(drum_prin_struc_circumferential)
            max_axial = max_value_find(drum_prin_struc_axial,n_axial)
            max_circumferential = max_value_find(drum_prin_struc_circumferential,n_circumferential)
            min_axial = min_value_find(drum_prin_struc_axial,n_axial)
            min_circumferential = min_value_find(drum_prin_struc_circumferential,n_circumferential)
            sigma_mean = pyo.value(0.5*((max_axial+max_circumferential)+(min_axial+min_circumferential)))
        elif s31 > s12 and s31 > s23:
            Ans_max = delta_s31_max
            Ans_min = delta_s31_min
            delta_sigma = Ans_max - Ans_min
            # calculate max, min for mean equivalent stress
            n_axial = len(drum_prin_struc_axial)
            n_radial = len(drum_prin_struc_radial)
            max_axial = max_value_find(drum_prin_struc_axial,n_axial)
            max_radial = max_value_find(drum_prin_struc_radial,n_radial)
            min_axial = min_value_find(drum_prin_struc_axial,n_axial)
            min_radial = min_value_find(drum_prin_struc_radial,n_radial)
            sigma_mean = pyo.value(0.5*((max_axial+max_circumferential)+(min_axial+min_circumferential)))
        else:
            raise Exception("Error occurs, check again!")
    else:
        Ans_max = max_value_find(data_export,n)
        Ans_min = min_value_find(data_export,n)
        # known parameters
        delta_sigma =  (Ans_max-Ans_min)            # equivalent structural stress range (linear distribution) [N/mm2]
        sigma_mean =  0.5*(Ans_max+Ans_min)         # mean stress
   
    # Maximum stress calculation
    sigma_max = sigma_mean + 0.5*delta_sigma

    # Calculate A0
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
    delta_sigma_eq = delta_sigma * k_e * k_v

    # Correction factors
    # Calculate temperature correction factor
    f_T = 1.03 - 1.5E-4*(0.75*T_max+0.25*T_min)-1.5E-6*(0.75*T_max+0.25*T_min)**2     # for other steels
    # f_T = 1.043 - 4.3E-4*(0.75*T_max+0.25*T_min)                                        # for austenitic steels

    #initialise N and delta_sigma_R
    delta_sigma_R = 50
    N = 10000

    Max_no_of_iterations = 100
    i = 1

    while True:
        #stopping creterion 
        if i > Max_no_of_iterations:
            break

        # calcualte effective stress concentration factor
        if N <= 2e6:
            K_f = 1+1.5*(K_t-1)/(1+0.5*max(1,(pyo.value(K_t*delta_sigma_eq/delta_sigma_D))))
        # If N > 2e6: delta_sigma_D = delta_sigma_R
        else:
            K_f = 1+1.5*(K_t-1)/(1+0.5*max(1,(pyo.value(K_t*delta_sigma_eq/delta_sigma_R))))

        # calculate effective total stress range
        delta_sigma_f = K_f * delta_sigma_eq

        # Calculate surface finish correction factor
        # polished surface withr Rz < 6: f_s = 1
        # untreated surfaces of deep drawn components and forgings: F_s = 0.25 + 0.75*(1-Rm/1500)**1.8
        if (N - 2E6) <= 0:
            f_s = (1 - 0.056*(pyo.log(Rz))**0.64 * pyo.log(Rm) + 0.289*(pyo.log(Rz))**0.53)**(0.1*(pyo.log(N))-0.465)           
        else:
            f_s = 1 - 0.056*(pyo.log(Rz))**0.64 * pyo.log(Rm) + 0.289*(pyo.log(Rz))**0.53

        # drum thickness
        e_n = thickness*1000

        # welding factor
        # if e_n < 25:
        #     f_ew = 1
        # elif (e_n<=150 and e_n>25):
        #     f_ew = (25/e_n)**0.25
        # else:
        #     f_ew = 0.6389

        # Calculate thickness correction factor
        if e_n < 25:
            f_e = 1
        elif (e_n > 25 and (N - 2E6) <= 0):  
            if (e_n <=150 and e_n>25):  
                f_e = ((25/e_n)**0.182)**(0.1*(pyo.log(N))-0.465)
            else:
                f_e = (1/6)**0.182
        elif (e_n >25 and (N-2E6)>0):
            if (e_n<=150 and e_n>25):
                f_e = (25/e_n)**0.182
            else:
                f_e = (1/6)**0.182

        #calculate reduced mean stress correction , Figure 18.6 in page 470, EN 13445
        
        if (delta_sigma <= 2*Rp and abs(sigma_max) > Rp):
            if (sigma_mean > 0):
                sigma_mean_r = Rp - 0.5*sigma_mean
            else:
                sigma_mean_r = 0.5*sigma_mean - Rp
        elif (delta_sigma <= 2*Rp and abs(sigma_max) < Rp) :
            sigma_mean_r = sigma_mean
        else:
            sigma_mean_r = 0
            f_m = 1

        # calculate mean stress sensitivity
        M = 0.00035*Rm-0.1  

        #calculat A1
        A1 = delta_sigma_R/(2*(1+M))

        # calculate full mean stress correction factor
        if N <= 2e6:
            if (-Rp <= sigma_mean_r and sigma_mean_r <= A1):
                f_m = pyo.sqrt(1-M*(2+M)/(1+M)*(2*sigma_mean_r/delta_sigma_R))
            elif (A1 < sigma_mean_r and sigma_mean_r <= Rp):
                f_m = (1+M/3)/(1+M) - M/3*(2*sigma_mean_r/delta_sigma_R)
            else:
                f_m =1
        # If N >= 2e6, replace delta_sigma_R by delta_sigma_D
        else: 
            if (-Rp <= sigma_mean_r and sigma_mean_r <= A1):
                f_m = pyo.sqrt(1-M*(2+M)/(1+M)*(2*sigma_mean_r/delta_sigma_D))
            elif (A1 < sigma_mean_r and sigma_mean_r <= Rp):
                f_m = (1+M/3)/(1+M) - M/3*(2*sigma_mean_r/delta_sigma_D)
            else:
                f_m =1

        # Calculate overall correction factor # f_u=f_T*f_s*f_e*f_m
        f_u = f_T * f_s * f_e * f_m

        # print('value f_T = {}, f_s = {}, f_e = {}, f_m = {}, f_u = {}'.format(f_T,f_s,f_e,f_m,f_u))

        # calculate delta signma R new 
        delta_sigma_R_new = delta_sigma_f/f_u

        # calculate N new
        if delta_sigma_R_new > delta_sigma_D:
            N_new = (46000/(delta_sigma_R_new-0.63*Rm + 11.5))**2
        elif delta_sigma_R_new < delta_sigma_D:
            N_new = ((2.69*Rm+89.72)/delta_sigma_R_new)**10
        elif (delta_sigma_R_new <= delta_sigma_cut):
            N_new = np.inf   

        #stopping creterion 
        if abs(N-N_new) <= 1e-7:
            break
        
        #update delta_sigma_R and N
        delta_sigma_R  = delta_sigma_R_new 
        N = N_new
        i =i+1
        print('iteration no ={},N={},delta_sigma_R={}'.format(i,N,delta_sigma_R))

    print('cycles =',int(N))
    print('stress range =', pyo.value(delta_sigma))
    print('sigma_mean =', pyo.value(sigma_mean))

    return m

def plot_results(pd):
    # ploting responses
    plt.figure(1)
    plt.plot(pd['time'], pd['coal_flow'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Coal Flow Rate [kg/s]")
    plt.show(block=False)

    plt.figure(2)
    plt.plot(pd['time'], pd['bfpt_opening'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("BFPT Valve Opening")
    plt.show(block=False)

    plt.figure(3)
    plt.plot(pd['time'], pd['gross_power'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Gross Power Output [MW]")
    plt.show(block=False)

    plt.figure(4)
    plt.plot(pd['time'], pd['ww_heat'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Waterwall Heat [MW]")
    plt.show(block=False)

    plt.figure(5)
    plt.plot(pd['time'], pd['fegt'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("FEGT [K]")
    plt.show(block=False) 
    
    plt.figure(6)
    plt.plot(pd['time'], pd['drum_level'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Drum Level [m]")
    plt.show(block=False)
    
    plt.figure(7)
    plt.plot(pd['time'], pd['feed_water_flow'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Feed Water Flow [kmol/s]")
    plt.show(block=False)
    
    plt.figure(8)
    plt.plot(pd['time'], pd['main_steam_flow'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Main Steam Flow [kmol/s]")
    plt.show(block=False) 

    plt.figure(9)
    plt.plot(pd['time'], pd['rh_steam_flow'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("RH Steam Flow [kmol/s]")
    plt.show(block=False)

    plt.figure(10)
    plt.plot(pd['time'], pd['bfpt_flow'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("BFPT Flow [mol/s]")
    plt.show(block=False)

    plt.figure(11)
    plt.plot(pd['time'], pd['spray_flow'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Water Spray Flow [mol/s]")
    plt.show(block=False)

    plt.figure(12)
    plt.plot(pd['time'], pd['main_steam_temp'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Main Steam Temperature [K]")
    plt.show(block=False)

    plt.figure(13)
    plt.plot(pd['time'], pd['rh_steam_temp'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("RH Steam Temperature [K]")
    plt.show(block=False)

    plt.figure(14)
    plt.plot(pd['time'], pd['fw_pres'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Feed Water Pressure [MPa]")
    plt.show(block=False)

    plt.figure(15)
    plt.plot(pd['time'], pd['drum_pres'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Drum Pressure [MPa]")
    plt.show(block=False)

    plt.figure(16)
    plt.plot(pd['time'], pd['main_steam_pres'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Main Steam Pressure [MPa]")
    plt.show(block=False)

    plt.figure(17)
    plt.plot(pd['time'], pd['rh_steam_pres'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("RH Steam Pressure [MPa]")
    plt.show(block=False)

    plt.figure(18)
    plt.plot(pd['time'], pd['hw_tank_level'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Hotwell Tank Level [m]")
    plt.show(block=False)

    plt.figure(19)
    plt.plot(pd['time'], pd['da_tank_level'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("DA Tank Level [m]")
    plt.show(block=False)

    plt.figure(20)
    plt.plot(pd['time'], pd['fwh2_level'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("FWH2 Level [m]")
    plt.show(block=False)

    plt.figure(21)
    plt.plot(pd['time'], pd['fwh3_level'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("FWH3 Level [m]")
    plt.show(block=False)

    plt.figure(22)
    plt.plot(pd['time'], pd['fwh5_level'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("FWH5 Level [m]")
    plt.show(block=False)

    plt.figure(23)
    plt.plot(pd['time'], pd['fwh6_level'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("FWH6 Level [m]")
    plt.show(block=False)

    plt.figure(24)
    plt.plot(pd['time'], pd['makeup_valve_opening'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Makeup Valve Opening")
    plt.show(block=False)

    plt.figure(25)
    plt.plot(pd['time'], pd['cond_valve_opening'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Condensate Valve Opening")
    plt.show(block=False)

    plt.figure(26)
    plt.plot(pd['time'], pd['fwh2_valve_opening'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("FWH2 Valve Opening")
    plt.show(block=False)

    plt.figure(27)
    plt.plot(pd['time'], pd['fwh3_valve_opening'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("FWH3 Valve Opening")
    plt.show(block=False)

    plt.figure(28)
    plt.plot(pd['time'], pd['fwh5_valve_opening'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("FWH5 Valve Opening")
    plt.show(block=False)

    plt.figure(29)
    plt.plot(pd['time'], pd['fwh6_valve_opening'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("FWH6 Valve Opening")
    plt.show(block=False)

    plt.figure(30)
    plt.plot(pd['time'], pd['spray_valve_opening'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Spray Valve Opening")
    plt.show(block=False)

    plt.figure(31)
    plt.plot(pd['time'], pd['tube_temp_rh2'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("RH Tube Temperature [K]")
    plt.show(block=False)

    plt.figure(32)
    plt.plot(pd['time'], pd['temp_fg_econ_exit'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Flue Gas T at Econ Exit [K]")
    plt.show(block=False)

    plt.figure(33)
    plt.plot(pd['time'], pd['temp_fg_aph_exit'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Flue Gas T at APH Exit [K]")
    plt.show(block=False)

    plt.figure(34)
    plt.plot(pd['time'], pd['throttle_opening'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Throttle Valve Opening")
    plt.show(block=False)
    
    plt.figure(35)
    plt.plot(pd['time'], pd['load_demand'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Load Demand [MW]")
    plt.show(block=False)

    plt.figure(36)
    plt.plot(pd['time'], pd['sliding_pressure'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Desired Sliding Pressure [MPa]")
    plt.show(block=False)

    plt.figure(37)
    plt.plot(pd['time'], pd['gross_heat_rate'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Gross Heat Rate [BTU/kW-hr]")
    plt.show(block=False)

    plt.figure(38)
    plt.plot(pd['time'], pd['deaerator_pressure'])
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("DA pressure [MPa]")
    plt.show(block=True)

def write_data_to_txt_file(plot_data):
    # write data to file
    ntime = len(plot_data['time'])
    ncount = len(plot_data)
    icount = 0
    with open("case3_1pct_result.txt","w") as fout:
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
    m_dyn = main_dyn()
    #m_ss = main_steady()