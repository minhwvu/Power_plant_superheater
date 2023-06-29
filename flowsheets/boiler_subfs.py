##############################################################################
# Institute for the Design of Advanced Energy Systems Process Systems
# Engineering Framework (IDAES PSE Framework) Copyright (c) 2018, by the
# software owners: The Regents of the University of California, through
# Lawrence Berkeley National Laboratory,  National Technology & Engineering
# Solutions of Sandia, LLC, Carnegie Mellon University, West Virginia
# University Research Corporation, et al. All rights reserved.
#
# Please see the files COPYRIGHT.txt and LICENSE.txt for full copyright and
# license information, respectively. Both files are also available online
# at the URL "https://github.com/IDAES/idaes".
##############################################################################
"""
Demonstration and test flowsheet for a dynamic flowsheet.

"""

# Import Pyomo libraries
import pyomo.environ as pyo
from pyomo.network import Arc

# Import IDAES core
from idaes.core.util.model_statistics import degrees_of_freedom
from idaes.core.util import copy_port_values as _set_port
import idaes.logger as idaeslog

# Import IDAES standard unit model
from idaes.generic_models.unit_models import Mixer

# Import IDAES power generation unit models
from idaes.power_generation.unit_models.helm import (
    HelmMixer,
    MomentumMixingType,
    HelmSplitter
    )
from idaes.power_generation.unit_models import (
    Drum1D,
    HeatExchangerWith3Streams,
    WaterPipe,
    HeatExchangerCrossFlow2D_Header,
    Downcomer,
    WaterwallSection,
    BoilerFireside,
    SteamHeater
    )
from flowsheets.datadictionary_escalante import data_dic

def add_unit_models(m):
    fs = m.fs_main.fs_blr
    prop_water = m.fs_main.prop_water
    prop_gas = m.fs_main.prop_gas

    # 14 waterwall zones
    fs.ww_zones = pyo.RangeSet(14)

    # boiler based on surrogate
    fs.aBoiler = BoilerFireside(default={"dynamic": False,
                               "property_package": prop_gas,
                               "calculate_PA_SA_flows": True,
                               "number_of_zones": 14,
                               "has_platen_superheater": True,
                               "has_roof_superheater": True,
                               "surrogate_dictionary": data_dic})
    fs.aDrum = Drum1D(default={"property_package": prop_water,
                               "has_holdup": True,
                               "has_heat_transfer": True,
                               "has_pressure_change": True,
                               "finite_elements": 4,
                               "drum_inner_diameter": 1.778,
                               "drum_thickness": 0.127})
    fs.blowdown_split = HelmSplitter(
        default={
            "dynamic": False,
            "property_package": prop_water,
            "outlet_list": ["FW_Downcomer", "FW_Blowdown"],
        }
    )
    # downcomer
    fs.aDowncomer = Downcomer(default={
                               "dynamic": False,
                               "property_package": prop_water,
                               "has_holdup": True,
                               "has_heat_transfer": True})

    # 14 WaterwallSection units
    fs.Waterwalls = WaterwallSection(fs.ww_zones,
                               default={
                               "has_holdup": True,
                               "property_package": prop_water,
                               "has_heat_transfer": True,
                               "has_pressure_change": True})

    # roof superheater
    fs.aRoof = SteamHeater(default={
                               "dynamic": False,
                               "property_package": prop_water,
                               "has_holdup": True,
                               "has_heat_transfer": True,
                               "has_pressure_change": True,
                               "single_side_only" : True})

    # platen superheater
    fs.aPlaten = SteamHeater(default={
                               "dynamic": False,
                               "property_package": prop_water,
                               "has_holdup": True,
                               "has_heat_transfer": True,
                               "has_pressure_change": True,
                               "single_side_only" : False})

    # 1st reheater
    fs.aRH1 = HeatExchangerCrossFlow2D_Header(default={
                               "tube_side":{"property_package": prop_water,
                                            "has_pressure_change": True},
                               "shell_side":{"property_package": prop_gas,
                                             "has_pressure_change": True},
                               "finite_elements": 4,
                               "flow_type": "counter_current",
                               "tube_arrangement": "in-line",
                               "tube_side_water_phase": "Vap",
                               "has_radiation": True,
                               "radial_elements": 5,
                               "tube_inner_diameter": 2.202*0.0254,
                               "tube_thickness": 0.149*0.0254,
                               "has_header": False})

    # 2nd reheater
    fs.aRH2 = HeatExchangerCrossFlow2D_Header(default={
                               "tube_side":{"property_package": prop_water,
                                            "has_pressure_change": True},
                               "shell_side":{"property_package": prop_gas,
                                             "has_pressure_change": True},
                               "finite_elements": 2,
                               "flow_type": "counter_current",
                               "tube_arrangement": "in-line",
                               "tube_side_water_phase": "Vap",
                               "has_radiation": True,
                               "radial_elements": 5,
                               "tube_inner_diameter": 2.217*0.0254,
                               "tube_thickness": 0.1415*0.0254,
                               "has_header": False})

    # primary superheater
    fs.aPSH = HeatExchangerCrossFlow2D_Header(default={
                               "tube_side":{"property_package": prop_water, 
                                            "has_pressure_change": True},
                               "shell_side":{"property_package": prop_gas,
                                             "has_pressure_change": True},
                               "finite_elements": 9,
                               "flow_type": "counter_current", 
                               "tube_arrangement": "in-line",
                               "tube_side_water_phase": "Vap",
                               "has_radiation": True,
                               "radial_elements": 5,
                               "tube_inner_diameter": 1.45*0.0254,
                               "tube_thickness": 0.15*0.0254,
                               "header_radial_elements": 5,
                               "header_inner_diameter": 11.376*0.0254,
                               "header_wall_thickness": 1.312*0.0254,
                               "has_header": True})

    # economizer
    fs.aECON = HeatExchangerCrossFlow2D_Header(default={
                               "tube_side":{"property_package": prop_water,
                                            "has_pressure_change": True},
                               "shell_side":{"property_package": prop_gas,
                                             "has_pressure_change": True},
                               "finite_elements": 5,
                               "flow_type": "counter_current",
                               "tube_arrangement": "in-line",
                               "tube_side_water_phase": "Liq",
                               "has_radiation": False,
                               "radial_elements": 5,
                               "tube_inner_diameter": 1.452*0.0254,
                               "tube_thickness": 0.149*0.0254,
                               "has_header": False})

    # water pipe from economizer outlet to drum
    fs.aPipe = WaterPipe(default={
                               "dynamic": False,
                               "property_package": prop_water,
                               "has_holdup": True,
                               "has_heat_transfer": False,
                               "has_pressure_change": True,
                               "water_phase": 'Liq',
                               "contraction_expansion_at_end": 'None'})

    # a mixer to mix hot primary air with tempering air
    fs.Mixer_PA = Mixer(
        default={
            "dynamic": False,
            "property_package": prop_gas,
            "momentum_mixing_type": MomentumMixingType.equality,
            "inlet_list": ["PA_inlet", "TA_inlet"],
        }
    )

    # attemperator for main steam before platen SH
    fs.Attemp = HelmMixer(
        default={
            "dynamic": False,
            "property_package": prop_water,
            "momentum_mixing_type": MomentumMixingType.equality,
            "inlet_list": ["Steam_inlet", "Water_inlet"],
        }
    )

    # air preheater as three-stream heat exchanger with heat loss to ambient,
    #     side_1: flue gas
    #     side_2:PA (priamry air?)
    #     side_3:PA (priamry air?)
    fs.aAPH = HeatExchangerWith3Streams(
        default={"dynamic": False,
            "side_1_property_package": prop_gas,
            "side_2_property_package": prop_gas,
            "side_3_property_package": prop_gas,
            "has_heat_transfer": True,
            "has_pressure_change": True,
            "has_holdup": False,
            "flow_type_side_2": "counter-current",
            "flow_type_side_3": "counter-current",
        }
    )
    return m


def set_arcs_and_constraints(m):
    # Make arc to connect streams
    fs = m.fs_main.fs_blr
    prop_gas = m.fs_main.prop_gas
    # water/steam streams
    fs.B001 = Arc(source=fs.aECON.tube_outlet,
                  destination=fs.aPipe.inlet)
    fs.B001b = Arc(source=fs.aPipe.outlet,
                   destination=fs.aDrum.feedwater_inlet)
    fs.B011 = Arc(source=fs.aDrum.liquid_outlet,
                  destination=fs.blowdown_split.inlet)
    fs.B011b = Arc(source=fs.blowdown_split.FW_Downcomer,
                  destination=fs.aDowncomer.inlet)
    fs.B007 = Arc(source=fs.aDowncomer.outlet,
                  destination=fs.Waterwalls[1].inlet)

    def ww_arc_rule(b, i):
        return (b.Waterwalls[i].outlet, b.Waterwalls[i+1].inlet)
    fs.ww_arcs = Arc(range(1,14), rule=ww_arc_rule)

    fs.B008  = Arc(source=fs.Waterwalls[14].outlet,
                   destination=fs.aDrum.water_steam_inlet)
    fs.B002 = Arc(source=fs.aDrum.steam_outlet,
                  destination=fs.aRoof.inlet)
    fs.B003 = Arc(source=fs.aRoof.outlet,
                  destination=fs.aPSH.tube_inlet)
    fs.B004 = Arc(source=fs.aPSH.tube_outlet,
                  destination=fs.Attemp.Steam_inlet)
    fs.B005 = Arc(source=fs.Attemp.outlet,
                  destination=fs.aPlaten.inlet)
    fs.B012 = Arc(source=fs.aRH1.tube_outlet,
                  destination=fs.aRH2.tube_inlet)
    fs.PA04 = Arc(source=fs.aAPH.side_2_outlet,
                  destination=fs.Mixer_PA.PA_inlet)
    fs.PA05 = Arc(source=fs.Mixer_PA.outlet,
                  destination=fs.aBoiler.primary_air_inlet)
    fs.SA03 = Arc(source=fs.aAPH.side_3_outlet,
                  destination=fs.aBoiler.secondary_air_inlet)
    fs.FG01 = Arc(source=fs.aBoiler.flue_gas_outlet,
                  destination=fs.aRH2.shell_inlet)
    fs.FG02 = Arc(source=fs.aRH2.shell_outlet,
                  destination=fs.aRH1.shell_inlet)
    fs.FG03 = Arc(source=fs.aRH1.shell_outlet,
                  destination=fs.aPSH.shell_inlet)
    fs.FG04 = Arc(source=fs.aPSH.shell_outlet,
                  destination=fs.aECON.shell_inlet)
    fs.FG05 = Arc(source=fs.aECON.shell_outlet,
                  destination=fs.aAPH.side_1_inlet)

    # According to Andrew Lee, this must be called after discretization call
    pyo.TransformationFactory("network.expand_arcs").apply_to(fs)

    #flowsheet level constraints
    # constraint for heat duty of each zone
    @fs.Constraint(fs.config.time, fs.ww_zones, doc="zone heat loss")
    def zone_heat_loss_eqn(b, t, izone):
        return 1e-6*b.aBoiler.waterwall_heat[t,izone] == 1e-6*b.Waterwalls[izone].heat_fireside[t]

    # constraint for heat duty of platen
    @fs.Constraint(fs.config.time, doc="platen SH heat loss")
    def platen_heat_loss_eqn(b, t):
        return 1e-6*b.aBoiler.platen_heat[t] == 1e-6*b.aPlaten.heat_fireside[t]

    # constraint for heat duty of roof
    @fs.Constraint(fs.config.time, doc="roof heat loss")
    def roof_heat_loss_eqn(b, t):
        return 1e-6*b.aBoiler.roof_heat[t] == 1e-6*b.aRoof.heat_fireside[t]

    # constraint for wall temperature of each zone
    @fs.Constraint(fs.config.time, fs.ww_zones, doc="zone wall temperature")
    def zone_wall_temp_eqn(b, t, izone):
        return b.aBoiler.wall_temperature_waterwall[t,izone] == b.Waterwalls[izone].temp_slag_boundary[t]

    # constraint for platen wall temperature
    @fs.Constraint(fs.config.time, doc="platen wall temperature")
    def platen_wall_temp_eqn(b, t):
        return b.aBoiler.wall_temperature_platen[t] == b.aPlaten.temp_slag_boundary[t]

    # constraint for roof wall temperature
    @fs.Constraint(fs.config.time, doc="roof wall temperature")
    def roof_wall_temp_eqn(b, t):
        return b.aBoiler.wall_temperature_roof[t] == b.aRoof.temp_slag_boundary[t]

    # set RH steam flow as 90% of main steam flow.  This constraint should be removed for entire plant flowsheet, use 92%
    @fs.Constraint(fs.config.time, doc="RH flow")
    def flow_mol_steam_rh_eqn(b, t):
        return b.aRH1.tube_inlet.flow_mol[t] == 0.91*b.aPlaten.outlet.flow_mol[t]

    # set pressure drop of APH for PA the same as that of SA since no meassured
    # pressure at PA outlet
    @fs.Constraint(fs.config.time, doc="Pressure drop of PA of APH")
    def pressure_drop_of_APH_eqn(b, t):
        return b.aAPH.deltaP_side_2[t] == b.aAPH.deltaP_side_3[t]

    # set PA before APH and TA before Mixer_PA temperature the same
    @fs.Constraint(fs.config.time, doc="Same inlet temperature for PA and SA")
    def pa_ta_temperature_identical_eqn(b, t):
        return b.aAPH.side_2_inlet.temperature[t] == b.Mixer_PA.TA_inlet.temperature[t]

    # set blowdown water flow rate at 2 percent of feed water flow
    @fs.Constraint(fs.config.time, doc="Blowdown water flow fraction")
    def blowdown_flow_fraction_eqn(b, t):
        return b.blowdown_split.FW_Blowdown.flow_mol[t] == b.aECON.tube_inlet.flow_mol[t]*0.02

    #------------- Three additional constraints for validation and optimization flowsheet -------------
    # set tempering air to total PA flow ratio as a function of coal flow rate
    @fs.Constraint(fs.config.time, prop_gas.component_list, doc="Fraction of TA as total PA flow")
    def fraction_of_ta_in_total_pa_eqn(b, t, j):
        return b.Mixer_PA.PA_inlet.flow_mol_comp[t,j] == (b.Mixer_PA.PA_inlet.flow_mol_comp[t,j] \
             + b.Mixer_PA.TA_inlet.flow_mol_comp[t,j]) * \
             (0.00041884*b.aBoiler.flowrate_coal_raw[t]**2 - 0.017505*b.aBoiler.flowrate_coal_raw[t] + 0.51429)

    # set total PA flow to coal flow ratio as a function of coal flow rate
    @fs.Constraint(fs.config.time, doc="PA to coal ratio")
    def pa_to_coal_ratio_eqn(b, t):
        return b.aBoiler.ratio_PA2coal[t] == \
            (0.0017486*b.aBoiler.flowrate_coal_raw[t]**2 - 0.12634*b.aBoiler.flowrate_coal_raw[t] + 4.5182)

    # set dry O2 percent in flue gas as a function of coal flow rate
    @fs.Constraint(fs.config.time, doc="Steady state dry O2 in flue gas")
    def dry_o2_in_flue_gas_eqn(b, t):
        return b.aBoiler.fluegas_o2_pct_dry[t] == -0.0007652*b.aBoiler.flowrate_coal_raw[t]**3 + \
            0.06744*b.aBoiler.flowrate_coal_raw[t]**2 - 1.9815*b.aBoiler.flowrate_coal_raw[t] + 22.275

    #--------------------- additional constraint for fheat_ww
    @fs.Constraint(fs.config.time, doc="Water wall heat absorption factor")
    def fheat_ww_eqn(b, t):
        return b.aBoiler.fcorrection_heat_ww[t] == 7.8431E-05*b.aBoiler.flowrate_coal_raw[t]**2 - \
                                        8.3181E-03*b.aBoiler.flowrate_coal_raw[t] + 1.1926

    # additional constraint for APH ua_side_2 (PA)
    @fs.Constraint(fs.config.time, doc="UA for APH of PA")
    def ua_side_2_eqn(b, t):
        return b.aAPH.ua_side_2[t]*1e-4 == 1e-4*(-150.1*b.aBoiler.flowrate_coal_raw[t]**2 + \
                                        9377.3*b.aBoiler.flowrate_coal_raw[t] + 63860)

    # additional constraint for APH ua_side_3 (SA), reduced by 5% based on Maojian's results
    @fs.Constraint(fs.config.time, doc="UA for APH of SA")
    def ua_side_3_eqn(b, t):
        return b.aAPH.ua_side_3[t]*1e-5 == 1e-5*(32849*b.aBoiler.flowrate_coal_raw[t] + 106022)*0.95
                                        
    # boiler efficiency based on enthalpy increase of main and RH steams
    @fs.Expression(fs.config.time, doc="boiler efficiency based on steam")
    def boiler_efficiency_steam(b, t):
        return ((b.aPlaten.outlet.flow_mol[t]-b.Attemp.Water_inlet.flow_mol[t])*(b.aPlaten.outlet.enth_mol[t]-b.aECON.tube_inlet.enth_mol[t]) + \
               b.aRH2.tube_outlet.flow_mol[t]*(b.aRH2.tube_outlet.enth_mol[t]-b.aRH1.tube_inlet.enth_mol[t]) + \
               b.Attemp.Water_inlet.flow_mol[t]*(b.aPlaten.outlet.enth_mol[t]-b.Attemp.Water_inlet.enth_mol[t])) / \
               (b.aBoiler.flowrate_coal_raw[t]*(1-b.aBoiler.mf_H2O_coal_raw[t])*b.aBoiler.hhv_coal_dry)

    # boiler efficiency based on heat absorbed
    @fs.Expression(fs.config.time, doc="boiler efficiency based on heat")
    def boiler_efficiency_heat(b, t):
        return (b.aBoiler.heat_total[t] + b.aRH2.total_heat[t] + b.aRH1.total_heat[t] + b.aPSH.total_heat[t] + b.aECON.total_heat[t]) / \
               (b.aBoiler.flowrate_coal_raw[t]*(1-b.aBoiler.mf_H2O_coal_raw[t])*b.aBoiler.hhv_coal_dry)
    return m

def set_inputs(m):
    fs = m.fs_main.fs_blr
    ############################ fix variables for geometry and design data #####################
    # Specify air composition (mole fractions)
    # based on 298.15 K and 0.5 relative humidity
    # It is defined in fire-side boiler model but used for all air inlets
    fs.aBoiler.mole_frac_air['O2'] = 0.20784
    fs.aBoiler.mole_frac_air['N2'] = 0.783994
    fs.aBoiler.mole_frac_air['CO2'] = 0.0003373
    fs.aBoiler.mole_frac_air['H2O'] = 0.0078267
    fs.aBoiler.mole_frac_air['SO2'] = 0.000001
    fs.aBoiler.mole_frac_air['NO'] = 0.000001
    # boiler
    fs.aBoiler.temperature_coal[:].fix(338.7)           # always set at 150 F
    fs.aBoiler.mf_C_coal_dry.fix(0.600245)       # fix coal ultimate analysis on dry basis
    fs.aBoiler.mf_H_coal_dry.fix(0.0456951)
    fs.aBoiler.mf_O_coal_dry.fix(0.108121)
    fs.aBoiler.mf_N_coal_dry.fix(0.0116837)
    fs.aBoiler.mf_S_coal_dry.fix(0.0138247)
    fs.aBoiler.mf_Ash_coal_dry.fix(0.220431)
    fs.aBoiler.hhv_coal_dry.fix(2.48579e+007)
    fs.aBoiler.frac_moisture_vaporized[:].fix(0.6)  # assume constant fraction of moisture vaporized in mills

    # drum
    fs.aDrum.drum_length.fix(14.3256)
    fs.aDrum.level[:].fix(0.889);
    fs.aDrum.number_downcomer.fix(8);
    fs.aDrum.downcomer_diameter.fix(0.3556);
    fs.aDrum.temperature_ambient[:].fix(300)
    fs.aDrum.insulation_thickness.fix(0.15)

    # blowdown split fraction initially set to a small value, will eventually unfixed due to a flowsheet constraint
    fs.blowdown_split.split_fraction[:,"FW_Blowdown"].fix(0.001)

    # downcomer
    fs.aDowncomer.diameter.fix(0.3556)       # 16 inch downcomer OD. assume downcomer thickness of 1 inch
    fs.aDowncomer.height.fix(43.6245)        # based on furnace height of 43.6245
    fs.aDowncomer.number_downcomers.fix(8)               # 8 downcomers
    fs.aDowncomer.heat_duty[:].fix(0.0)      # assume no heat loss

    # 14 waterwall sections
    for i in fs.ww_zones:
        # 2.5 inch OD, 0.2 inch thickness, 3 inch pitch
        fs.Waterwalls[i].tube_diameter.fix(0.05334)
        fs.Waterwalls[i].tube_thickness.fix(0.00508)
        fs.Waterwalls[i].fin_thickness.fix(0.005)
        fs.Waterwalls[i].slag_thickness[:].fix(0.001)
        fs.Waterwalls[i].fin_length.fix(0.0127)
        fs.Waterwalls[i].number_tubes.fix(558)
        fs.Waterwalls[i].fcorrection_dp.fix(1.2)

    # water wall section height
    fs.Waterwalls[1].height.fix(7.3533)
    fs.Waterwalls[2].height.fix(3.7467)
    fs.Waterwalls[3].height.fix(1.3)
    fs.Waterwalls[4].height.fix(1.3461)
    fs.Waterwalls[5].height.fix(1.2748)
    fs.Waterwalls[6].height.fix(1.2748)
    fs.Waterwalls[7].height.fix(1.1589)
    fs.Waterwalls[8].height.fix(1.2954)
    fs.Waterwalls[9].height.fix(3.25)
    fs.Waterwalls[10].height.fix(3.5)
    fs.Waterwalls[11].height.fix(3.6465)
    fs.Waterwalls[12].height.fix(3.5052)
    fs.Waterwalls[13].height.fix(5.4864)
    fs.Waterwalls[14].height.fix(5.4864)

    # water wall section projected area
    fs.Waterwalls[1].projected_area.fix(317.692)
    fs.Waterwalls[2].projected_area.fix(178.329)
    fs.Waterwalls[3].projected_area.fix(61.8753)
    fs.Waterwalls[4].projected_area.fix(64.0695)
    fs.Waterwalls[5].projected_area.fix(60.6759)
    fs.Waterwalls[6].projected_area.fix(60.6759)
    fs.Waterwalls[7].projected_area.fix(55.1595)
    fs.Waterwalls[8].projected_area.fix(61.6564)
    fs.Waterwalls[9].projected_area.fix(154.688)
    fs.Waterwalls[10].projected_area.fix(166.587)
    fs.Waterwalls[11].projected_area.fix(173.56)
    fs.Waterwalls[12].projected_area.fix(166.114)
    fs.Waterwalls[13].projected_area.fix(178.226)
    fs.Waterwalls[14].projected_area.fix(178.226)

    # roof
    fs.aRoof.diameter_in.fix(2.1*0.0254)
    fs.aRoof.tube_thickness.fix(0.2*0.0254)
    fs.aRoof.fin_thickness.fix(0.004)
    fs.aRoof.slag_thickness[:].fix(0.001)
    fs.aRoof.fin_length.fix(0.5*0.0254)
    fs.aRoof.tube_length.fix(8.2534)
    fs.aRoof.number_tubes.fix(177)
    fs.aRoof.therm_cond_slag.fix(1.3)


    # platen superheater
    fs.aPlaten.diameter_in.fix(0.04125)
    fs.aPlaten.tube_thickness.fix(0.00635)
    fs.aPlaten.fin_thickness.fix(0.004)
    fs.aPlaten.slag_thickness[:].fix(0.001)
    fs.aPlaten.fin_length.fix(0.00955)
    fs.aPlaten.tube_length.fix(45.4533)
    fs.aPlaten.number_tubes.fix(11*19)
    fs.aPlaten.therm_cond_slag.fix(1.3)


    # RH1
    fs.aRH1.pitch_x.fix(4.5*0.0254)
    fs.aRH1.pitch_y.fix(6.75*0.0254)        
    fs.aRH1.tube_length_seg.fix(300*0.0254)    # Use tube length as estimated
    fs.aRH1.tube_nseg.fix(4)
    fs.aRH1.tube_ncol.fix(78)
    fs.aRH1.tube_inlet_nrow.fix(3)
    fs.aRH1.delta_elevation.fix(0.0)
    fs.aRH1.therm_cond_wall = 43.0
    fs.aRH1.emissivity_wall.fix(0.65)
    fs.aRH1.dens_wall = 7800
    fs.aRH1.cp_wall = 470
    fs.aRH1.Young_modulus = 1.90e5
    fs.aRH1.Possion_ratio = 0.29
    fs.aRH1.coefficient_therm_expansion = 1.3e-5
    fs.aRH1.tube_r_fouling = 0.00017     #heat transfer resistance due to tube side fouling (water scales)
    fs.aRH1.shell_r_fouling = 0.00088    #heat transfer resistance due to shell side fouling (ash deposition)
    fs.aRH1.fcorrection_htc_tube.fix(0.8)  # original 0.9
    fs.aRH1.fcorrection_htc_shell.fix(0.8)  # original 0.9
    fs.aRH1.fcorrection_dp_tube.fix(5.3281932)
    fs.aRH1.fcorrection_dp_shell.fix(3.569166)
    
    # RH2
    fs.aRH2.pitch_x.fix(4.5*0.0254)
    fs.aRH2.pitch_y.fix(13.5*0.0254)
    fs.aRH2.tube_length_seg.fix(420*0.0254)    # Use tube length as estimated
    fs.aRH2.tube_nseg.fix(2)
    fs.aRH2.tube_ncol.fix(39)
    fs.aRH2.tube_inlet_nrow.fix(6)
    fs.aRH2.delta_elevation.fix(0.0)
    fs.aRH2.therm_cond_wall = 43.0
    fs.aRH2.emissivity_wall.fix(0.65)
    fs.aRH2.dens_wall = 7800
    fs.aRH2.cp_wall = 470
    fs.aRH2.Young_modulus = 1.90e5
    fs.aRH2.Possion_ratio = 0.29
    fs.aRH2.coefficient_therm_expansion = 1.3e-5
    fs.aRH2.tube_r_fouling = 0.00017     #heat transfer resistance due to tube side fouling (water scales)
    fs.aRH2.shell_r_fouling = 0.00088    #heat transfer resistance due to shell side fouling (ash deposition)   
    fs.aRH2.fcorrection_htc_tube.fix(0.8)  # original 0.9
    fs.aRH2.fcorrection_htc_shell.fix(0.8)  # original 0.9
    fs.aRH2.fcorrection_dp_tube.fix(5.3281932)
    fs.aRH2.fcorrection_dp_shell.fix(3.569166)

    # PSH
    fs.aPSH.pitch_x.fix(3.75*0.0254)
    fs.aPSH.pitch_y.fix(6.0*0.0254)
    fs.aPSH.tube_length_seg.fix(302.5*0.0254)
    fs.aPSH.tube_nseg.fix(9)
    fs.aPSH.tube_ncol.fix(88)
    fs.aPSH.tube_inlet_nrow.fix(4)
    fs.aPSH.delta_elevation.fix(5.0)
    # Update material properties (Minh)
    fs.aPSH.therm_cond_wall = 49.0      # Carbon steel SA 209 T1 
    fs.aPSH.density_wall = 7800         # kg/m3
    fs.aPSH.cp_wall = 470               # J/kg-K    
    fs.aPSH.Young_modulus = 1.90e5
    fs.aPSH.Possion_ratio = 0.29
    fs.aPSH.coefficient_therm_expansion = 1.3e-5

    fs.aPSH.tube_r_fouling = 0.00017     #heat transfer resistance due to tube side fouling (water scales)
    fs.aPSH.shell_r_fouling = 0.00088    #heat transfer resistance due to shell side fouling (ash deposition)   
    fs.aPSH.emissivity_wall.fix(0.7)
    fs.aPSH.fcorrection_htc_tube.fix(1.02)  # original 1.04
    fs.aPSH.fcorrection_htc_shell.fix(1.02)  # original 1.04
    fs.aPSH.fcorrection_dp_tube.fix(15.6)
    fs.aPSH.fcorrection_dp_shell.fix(1.252764)

    # economizer
    fs.aECON.pitch_x.fix(3.75*0.0254)
    fs.aECON.pitch_y.fix(4.0*0.0254)      
    fs.aECON.tube_length_seg.fix(302.5*0.0254)  
    fs.aECON.tube_nseg.fix(18) 
    fs.aECON.tube_ncol.fix(132)   
    fs.aECON.tube_inlet_nrow.fix(2)
    fs.aECON.delta_elevation.fix(12)
    fs.aECON.therm_cond_wall = 43.0
    fs.aECON.dens_wall = 7800
    fs.aECON.cp_wall = 470
    fs.aECON.Young_modulus = 1.90e5
    fs.aECON.Possion_ratio = 0.29
    fs.aECON.coefficient_therm_expansion = 1.3e-5
    fs.aECON.tube_r_fouling = 0.00017
    fs.aECON.shell_r_fouling = 0.00088
    fs.aECON.fcorrection_htc_tube.fix(0.849)
    fs.aECON.fcorrection_htc_shell.fix(0.849)
    fs.aECON.fcorrection_dp_tube.fix(27.322)
    fs.aECON.fcorrection_dp_shell.fix(4.4872429)

    # APH
    fs.aAPH.ua_side_2[:].fix(171103.4)
    fs.aAPH.ua_side_3[:].fix(677069.6)
    fs.aAPH.frac_heatloss.fix(0.15)
    fs.aAPH.deltaP_side_1[:].fix(-1000)
    fs.aAPH.deltaP_side_2[:].fix(-1000)
    fs.aAPH.deltaP_side_3[:].fix(-1000)

    # 132 economizer rising tubes of 2 inch O.D. assuming 1.5 inch I.D.
    fs.aPipe.diameter.fix(0.0381)
    fs.aPipe.length.fix(35)
    fs.aPipe.number_of_pipes.fix(132);
    fs.aPipe.elevation_change.fix(20)
    fs.aPipe.fcorrection_dp.fix(1)

    return m


def initialize(m):
    """Initialize unit models"""
    fs = m.fs_main.fs_blr
    prop_gas = m.fs_main.prop_gas
    outlvl = 4
    _log = idaeslog.getLogger(fs.name, outlvl, tag="unit")
    solve_log = idaeslog.getSolveLogger(fs.name, outlvl, tag="unit")
    solver = pyo.SolverFactory("ipopt")
    solver.options = {
            "tol": 1e-7,
            "linear_solver": "ma27",
            "max_iter": 50,
    }

    # set initial condition to steady-state condition
    # no need to call fix_initial_conditions('steady-state')
    # fs.fix_initial_conditions('steady-state')
    if m.dynamic==True:
        fs.aDrum.set_initial_condition()
        fs.aDowncomer.set_initial_condition()
        for i in fs.ww_zones:
            fs.Waterwalls[i].set_initial_condition()
        fs.aRoof.set_initial_condition()
        fs.aPSH.set_initial_condition()
        fs.aPlaten.set_initial_condition()
        fs.aRH1.set_initial_condition()
        fs.aRH2.set_initial_condition()
        fs.aECON.set_initial_condition()
        fs.aPipe.set_initial_condition()

    # fix operating conditions
    # aBoiler
    fs.aBoiler.mf_H2O_coal_raw[:].fix(0.156343)
    fs.aBoiler.flowrate_coal_raw[:].fix(29)
    fs.aBoiler.SR[:].fix(1.156)
    fs.aBoiler.SR_lf[:].fix(1.0)
    fs.aBoiler.ratio_PA2coal[:].fix(2.4525)
    fs.aBoiler.deltaP.fix(1000)
    fs.aBoiler.wall_temperature_waterwall[:,1].fix(641)         # initial guess of waterwall slag layer temperatures
    fs.aBoiler.wall_temperature_waterwall[:,2].fix(664)
    fs.aBoiler.wall_temperature_waterwall[:,3].fix(722)
    fs.aBoiler.wall_temperature_waterwall[:,4].fix(735)
    fs.aBoiler.wall_temperature_waterwall[:,5].fix(744)
    fs.aBoiler.wall_temperature_waterwall[:,6].fix(747)
    fs.aBoiler.wall_temperature_waterwall[:,7].fix(746)
    fs.aBoiler.wall_temperature_waterwall[:,8].fix(729)
    fs.aBoiler.wall_temperature_waterwall[:,9].fix(716)
    fs.aBoiler.wall_temperature_waterwall[:,10].fix(698)
    fs.aBoiler.wall_temperature_waterwall[:,11].fix(681)
    fs.aBoiler.wall_temperature_waterwall[:,12].fix(665)
    fs.aBoiler.wall_temperature_waterwall[:,13].fix(632)
    fs.aBoiler.wall_temperature_waterwall[:,14].fix(622)
    fs.aBoiler.wall_temperature_platen[:].fix(799)
    fs.aBoiler.wall_temperature_roof[:].fix(643)
    fs.aBoiler.fcorrection_heat_ww.fix(1.0)
    fs.aBoiler.fcorrection_heat_platen.fix(0.98)
    fs.aBoiler.primary_air_inlet.pressure[:].fix(79868.3)    # fixed as operating condition
    fs.aBoiler.secondary_air_inlet.pressure[:].fix(79868.3)    # fixed as operating condition
    fs.aBoiler.secondary_air_inlet.temperature[:].fix(634)      # initial guess, unfixed later

    # aDrum
    fs.aDrum.level[:].fix(0.889)                    # drum level, set as drum radius

    # 14 Waterwalls
    fs.Waterwalls[1].heat_fireside[:].fix(24327106)    # initial guess, unfixed later
    fs.Waterwalls[2].heat_fireside[:].fix(19275085)
    fs.Waterwalls[3].heat_fireside[:].fix(12116325)
    fs.Waterwalls[4].heat_fireside[:].fix(13680850)
    fs.Waterwalls[5].heat_fireside[:].fix(13748641)
    fs.Waterwalls[6].heat_fireside[:].fix(14064033)
    fs.Waterwalls[7].heat_fireside[:].fix(12675550)
    fs.Waterwalls[8].heat_fireside[:].fix(12638767)
    fs.Waterwalls[9].heat_fireside[:].fix(28492415)
    fs.Waterwalls[10].heat_fireside[:].fix(26241924)
    fs.Waterwalls[11].heat_fireside[:].fix(22834318)
    fs.Waterwalls[12].heat_fireside[:].fix(17924138)
    fs.Waterwalls[13].heat_fireside[:].fix(10191487)
    fs.Waterwalls[14].heat_fireside[:].fix(7578554)

    # aRoof
    fs.aRoof.heat_fireside[:].fix(6564520)            # initial guess, unfixed later

    # aPlaten
    fs.aPlaten.heat_fireside[:].fix(49796257)          # initial guess, unfixed later

    # fix economizer water inlet, to be linked with last FWH if linked with steam cycle flowsheet
    fs.aECON.tube_inlet.flow_mol[:].fix(10103)
    fs.aECON.tube_inlet.pressure[:].fix(1.35e7)
    fs.aECON.tube_inlet.enth_mol[:].fix(18335.7)
    
    # fixed RH1 inlet conditions, to be linked with steam cycle flowsheet
    fs.aRH1.tube_inlet.flow_mol[:].fix(10103*0.9)
    fs.aRH1.tube_inlet.enth_mol[:].fix(55879)
    fs.aRH1.tube_inlet.pressure[:].fix(3029886)

    fs.model_check()

    #################### Initialize Units #######################
    # since dynamic model is initialized by copy steady-state model, calling unit model's initialize() function is skiped
    # tear flue gas stream between PSH and ECON
    # Use FG molar composition to set component flow rates
    fs.aECON.shell_inlet.flow_mol_comp[:,"H2O"].value = 748
    fs.aECON.shell_inlet.flow_mol_comp[:,"CO2"].value = 1054
    fs.aECON.shell_inlet.flow_mol_comp[:,"N2"].value = 5377
    fs.aECON.shell_inlet.flow_mol_comp[:,"O2"].value = 194
    fs.aECON.shell_inlet.flow_mol_comp[:,"SO2"].value = 9
    fs.aECON.shell_inlet.flow_mol_comp[:,"NO"].value = 2.6
    fs.aECON.shell_inlet.temperature[:].value = 861.3
    fs.aECON.shell_inlet.pressure[:].value = 79686
    if m.dynamic==False or m.init_dyn==True:
        dof1 = degrees_of_freedom(fs)
        fs.aECON.initialize(outlvl=4)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("//////////////////after economizer initialization ///////////////")

    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.aPipe.inlet, fs.aECON.tube_outlet)
        dof1 = degrees_of_freedom(fs)
        fs.aPipe.initialize(outlvl=4)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("//////////////////after Pipe initialization ///////////////")

    # PA to APH
    flow_mol_pa = 1410
    for i in prop_gas.component_list:
        fs.aAPH.side_2_inlet.flow_mol_comp[:, i].fix(pyo.value(
            flow_mol_pa * fs.aBoiler.mole_frac_air[i]))
    fs.aAPH.side_2_inlet.temperature[:].fix(324.8)
    fs.aAPH.side_2_inlet.pressure[:].fix(88107.6)

    # SA to APH
    flow_mol_sa = 4716
    for i in prop_gas.component_list:
        fs.aAPH.side_3_inlet.flow_mol_comp[:, i].fix(pyo.value(
            flow_mol_sa * fs.aBoiler.mole_frac_air[i]))
    fs.aAPH.side_3_inlet.temperature[:].fix(366.2)
    fs.aAPH.side_3_inlet.pressure[:].fix(87668.4)

    flow_mol_ta = 721
    for i in prop_gas.component_list:
        fs.Mixer_PA.TA_inlet.flow_mol_comp[:, i].fix(pyo.value(
            flow_mol_ta * fs.aBoiler.mole_frac_air[i]))
    fs.Mixer_PA.TA_inlet.temperature[:].value = 324.8
    fs.Mixer_PA.TA_inlet.pressure[:].value = 88107.6

    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.aAPH.side_1_inlet, fs.aECON.shell_outlet)
        dof1 = degrees_of_freedom(fs)
        fs.aAPH.initialize(outlvl=4)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("//////////////////after aAPH initialization ///////////////")

    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.Mixer_PA.PA_inlet, fs.aAPH.side_2_outlet)
        dof1 = degrees_of_freedom(fs)
        fs.Mixer_PA.initialize(outlvl=0)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("//////////////////after Mixer_PA initialization ///////////////")
    
    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.aBoiler.primary_air_inlet, fs.Mixer_PA.outlet)
        _set_port(fs.aBoiler.secondary_air_inlet, fs.aAPH.side_3_outlet)
        dof1 = degrees_of_freedom(fs)
        fs.aBoiler.initialize(outlvl=4)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("//////////////////after Boiler initialization ///////////////")

    # tear stream from last boiler water wall section
    fs.aDrum.water_steam_inlet.flow_mol[:].value = 133444.4
    fs.aDrum.water_steam_inlet.pressure[:].value = 11469704
    fs.aDrum.water_steam_inlet.enth_mol[:].value = 27832

    fs.aDrum.water_steam_inlet.flow_mol[:].fix()
    fs.aDrum.water_steam_inlet.pressure[:].fix()
    fs.aDrum.water_steam_inlet.enth_mol[:].fix()
    
    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.aDrum.feedwater_inlet, fs.aPipe.outlet)
        '''
        fs.aDrum.feedwater_inlet.flow_mol.fix()
        fs.aDrum.feedwater_inlet.enth_mol.fix()
        fs.aDrum.feedwater_inlet.pressure.unfix()
        '''
        dof1 = degrees_of_freedom(fs)
        print('-----drum dof=', dof1)
        fs.aDrum.initialize(outlvl=4)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("//////////////////after Drum initialization ///////////////")

    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.blowdown_split.inlet, fs.aDrum.liquid_outlet)
        dof1 = degrees_of_freedom(fs)
        fs.blowdown_split.initialize()
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("//////////////////after blowdown_split initialization ///////////////")

    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.aDowncomer.inlet, fs.blowdown_split.FW_Downcomer)
        dof1 = degrees_of_freedom(fs)
        fs.aDowncomer.initialize(outlvl=4)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("//////////////////after Downcomer initialization ///////////////")

    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.Waterwalls[1].inlet, fs.aDowncomer.outlet)
        dof1 = degrees_of_freedom(fs)
        fs.Waterwalls[1].initialize(outlvl=4)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff, ' for Waterwall 1')
        print("//////////////////after Zone 1 initialization ///////////////")

    for i in fs.ww_zones:
       if (i>1):
           if m.dynamic==False or m.init_dyn==True:
               _set_port(fs.Waterwalls[i].inlet, fs.Waterwalls[i-1].outlet)
               dof1 = degrees_of_freedom(fs)
               fs.Waterwalls[i].initialize(outlvl=4)
               dof2 = degrees_of_freedom(fs)
               dof_diff = dof2 - dof1
               print('change of dof=', dof_diff, ' for Waterwall number ', i)
               print("////////////////// After all zones initialization ///////////////")

    # tear steam between RH1 and RH2
    fs.aRH2.tube_inlet.flow_mol[:].value = 7351.8
    fs.aRH2.tube_inlet.enth_mol[:].value = 61628
    fs.aRH2.tube_inlet.pressure[:].value = 2974447

    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.aRH2.shell_inlet, fs.aBoiler.flue_gas_outlet)
        # use a lower temperature to avoid convegence issue
        fs.aRH2.shell_inlet.temperature[:].value = 1350
        dof1 = degrees_of_freedom(fs)
        fs.aRH2.initialize(outlvl=4)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("////////////////// After RH2 initialization ///////////////")

    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.aRH1.shell_inlet, fs.aRH2.shell_outlet)
        # use a lower temperature to avoid convegence issue
        fs.aRH1.shell_inlet.temperature[:].value = 1200
        dof1 = degrees_of_freedom(fs)
        fs.aRH1.initialize(outlvl=4)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("////////////////// After RH1 initialization ///////////////")
    
    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.aRoof.inlet, fs.aDrum.steam_outlet)
        dof1 = degrees_of_freedom(fs)
        fs.aRoof.initialize(outlvl=4)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("////////////////// After Roof initialization ///////////////")

    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.aPSH.tube_inlet, fs.aRoof.outlet)
        _set_port(fs.aPSH.shell_inlet, fs.aRH1.shell_outlet)
        # use a lower temperature to avoid convegence issue
        fs.aPSH.shell_inlet.temperature[:].value = 1000
        dof1 = degrees_of_freedom(fs)
        fs.aPSH.initialize(outlvl=4)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("////////////////// After PSH initialization ///////////////")

    # fixed inlet conditions, to be linked with steam cycle
    fs.Attemp.Water_inlet.flow_mol[:].fix(20)
    fs.Attemp.Water_inlet.pressure[:].value = 12227274.0
    fs.Attemp.Water_inlet.enth_mol[:].fix(12767) 

    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.Attemp.Steam_inlet, fs.aPSH.tube_outlet)
        dof1 = degrees_of_freedom(fs)
        fs.Attemp.initialize(outlvl=4)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("////////////////// After Attemp initialization ///////////////")

    if m.dynamic==False or m.init_dyn==True:
        _set_port(fs.aPlaten.inlet, fs.Attemp.outlet)
        dof1 = degrees_of_freedom(fs)
        fs.aPlaten.initialize(outlvl=4)
        dof2 = degrees_of_freedom(fs)
        dof_diff = dof2 - dof1
        print('change of dof=', dof_diff)
        print("////////////////// After Platen initialization ///////////////")

    ############################# Unfix variables after initialization ###########################
    # blowdown split fraction
    fs.blowdown_split.split_fraction[:,"FW_Blowdown"].unfix()
    fs.aDrum.water_steam_inlet.unfix()
    # Waterwalls[14] heat duty
    for i in fs.ww_zones:
       fs.Waterwalls[i].heat_fireside[:].unfix()
    # heat duty to aPlaten and aRoof
    fs.aPlaten.heat_fireside[:].unfix()
    fs.aRoof.heat_fireside[:].unfix()
    # all wall temperatures
    for i in fs.aBoiler.zones:
       fs.aBoiler.wall_temperature_waterwall[:,i].unfix()
    fs.aBoiler.wall_temperature_platen[:].unfix()
    fs.aBoiler.wall_temperature_roof[:].unfix()
    # air and gas component flows
    for i in prop_gas.component_list:
        # SA at FD fan outlet and aAPH inlet
        fs.aAPH.side_2_inlet.flow_mol_comp[:,i].unfix()
        # PA at aAPH inlet
        fs.aAPH.side_3_inlet.flow_mol_comp[:,i].unfix()
        # Tempering air at Mixer_PA inlet
        fs.Mixer_PA.TA_inlet.flow_mol_comp[:, i].unfix()
    # SA pressure and temperature need to be unfixed
    fs.aBoiler.secondary_air_inlet.pressure[:].unfix()
    fs.aBoiler.secondary_air_inlet.temperature[:].unfix()
    # PA inlet pressure needs to be unfixed
    fs.aBoiler.primary_air_inlet.pressure[:].unfix()
    # inlet flow based on constraint
    fs.aRH1.tube_inlet.flow_mol[:].unfix()

    #fix feed water pressure and enthalpy but allow flow rate to change
    fs.aECON.tube_inlet.flow_mol[:].unfix()
    fs.aBoiler.SR[:].unfix()
    
    fs.aBoiler.ratio_PA2coal[:].unfix()
    # due to a constraint to set SA and PA deltP the same
    fs.aAPH.deltaP_side_2[:].unfix()
    fs.aAPH.ua_side_2.unfix()
    fs.aAPH.ua_side_3.unfix()

    fs.aBoiler.fcorrection_heat_ww.unfix()

    df = degrees_of_freedom(fs)
    print ("***************degree of freedom = ", df, "********************")
    assert df == 0

    if m.dynamic==False or m.init_dyn==True:
            fs.aBoiler.fcorrection_heat_ww.fix()
            fs.fheat_ww_eqn.deactivate()
            _log.info("//////////////////Solving boiler steady-state problem///////////////")
            with idaeslog.solver_log(solve_log, idaeslog.DEBUG) as slc:
                res = solver.solve(fs, tee=slc.tee)
            _log.info("Solving boiler steady-state problem: {}".format(idaeslog.condition(res)))
            
            fs.aBoiler.fcorrection_heat_ww.unfix()
            fs.fheat_ww_eqn.activate()
            _log.info("//////////////////Solving different fheat_ww ///////////////")
            with idaeslog.solver_log(solve_log, idaeslog.DEBUG) as slc:
                res = solver.solve(fs, tee=slc.tee)
            _log.info("Solving high coal flow rate problem: {}".format(idaeslog.condition(res)))
            print("feed water flow=", fs.aECON.tube_inlet.flow_mol[0].value)
            print('flowrate_coal_raw=', pyo.value(fs.aBoiler.flowrate_coal_raw[0]))
            print('fraction of moisture in raw coal=', pyo.value(fs.aBoiler.mf_H2O_coal_raw[0]))
            print('flowrate_fluegas=', pyo.value(fs.aBoiler.flue_gas[0].flow_mass))
            print('flowrate_PA=', pyo.value(fs.aBoiler.primary_air[0].flow_mass))
            print('flowrate_SA=', pyo.value(fs.aBoiler.secondary_air[0].flow_mass))
            print('flowrate_TCA=', pyo.value(fs.aBoiler.flow_mass_TCA[0]))
            print('ratio_PA2coal=', pyo.value(fs.aBoiler.ratio_PA2coal[0]))
            print('SR=', fs.aBoiler.SR[0].value)
            print('SR_lf=', fs.aBoiler.SR_lf[0].value)
            print('Roof slag thickness =', fs.aRoof.slag_thickness[0].value)
            print('boiler ww heat=', pyo.value(fs.aBoiler.heat_total_ww[0]))
            print('tempering air flow=', pyo.value(fs.Mixer_PA.TA_inlet_state[0].flow_mass))
    return m
