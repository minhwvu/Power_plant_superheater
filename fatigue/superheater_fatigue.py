from pyomo.environ import*
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------------------------------------------
# Call data from excel file
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

df_data = pd.read_excel(r'C:\Users\minh2\OneDrive - 영남대학교\West Virginia University\LTE Dynamic Health Model\Word_Excel\Excel\Full_plant_output_06232020.xlsx',sheet_name ='5%_per_min')

data_export_first = df_data['Sigma_VM_inside_x0_conv'] # (m.fs.aPSH.Von_Mises_equi_stress[t,0,m.fs.aPSH.r.first()])
data_export_last = df_data['Sigma_VM_outside_x0_conv']  # (m.fs.aPSH.Von_Mises_equi_stress[t,0,m.fs.aPSH.r.last()])


#----------------------------------------------------------------------------------------------------------

print('***************************************************************************************') 
print('Calculate allowable cycles at inside layer')
n_first= len(data_export_first)

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

Ans_max_first = max_value_find(data_export_first,n_first)
Ans_min_first = min_value_find(data_export_first,n_first)

# known parameters
delta_sigma_first =  (Ans_max_first-Ans_min_first)            # equivalent structural stress range (linear distribution) [N/mm2]
sigma_mean_first =  0.5*(Ans_max_first+Ans_min_first)         # mean stress
delta_sigma_D =  230                        # the thermal endurance limit, Carbon steel SA 210 A-1
Rm = 470                    # Tensile strength [N/mm2]
Rp = 290                    # the yield strength of material
T_max = 500                 # the metal temperature during the moment of the highest stress [C]
T_min = 400                 # the metal temperature during the moment of lowest stress [C]
K_t =  3.0                  # Thermal stress correction factor
Rz = 50                     # the peak-to-valley height (micrometer), 50 for machine, 10 for ground, free of notches

RO = (1.45*0.0254+2*0.15*0.0254)/2
RI = 1.45*0.0254/2

# Maximum stress calculation
sigma_max_first = sigma_mean_first + 0.5*delta_sigma_first

A0 = 0.4 # for Rm <= 500 MPa
# A0 = 0.4+(Rm-500)/3000  # for 500 < Rm <= 800 MPa
# A0 = 0.5 # for 800 < Rm <= 1000 MPa
#calculate k_e
if delta_sigma_first > 2*Rp:
    # k_e = 1+0.4*(delta_sigma/(2*Rp)-1)            # For austenitic steels
  k_e = 1+A0*(delta_sigma_first/(2*Rp)-1)               # For other steels
else:
  k_e= 1 

# calculate kv
if delta_sigma_first > 2*Rp:
  k_v= max(1, value(0.7/(0.5+0.4/(delta_sigma_first/Rp))))      
else:
  k_v= 1 

# Equivalent stress
delta_sigma_eq_first =delta_sigma_first * k_e * k_v

# calcualte kf
K_f_first= 1+1.5*(K_t-1)/(1+0.5*max(1,(value(K_t*delta_sigma_eq_first/delta_sigma_D))))

# calculate Delta sigma f
delta_sigma_f_first = (K_f_first * delta_sigma_eq_first)


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
  # Calculate surface finish correction factor
  if (N - 2E6) <= 0:
      f_s = (1 - 0.056*(log(Rz))**0.64 * log(Rm) + 0.289*(log(Rz))**0.53)**(0.1*(log(N))-0.465)           
  else:
      f_s = 1 - 0.056*(log(Rz))**0.64 * log(Rm) + 0.289*(log(Rz))**0.53


  # Calculate thickness correction factor
  e_n = (0.5*(RO-RI)*1000)
  if (N - 2E6) <= 0: 
      f_e = ((25/e_n)**0.182)**(0.1*(log(N))-0.465)
  else:
      f_e = (25/e_n)**0.182


  #calculate sigma_mean_r
  if (delta_sigma_first <= 2*Rp and abs(sigma_max_first) < Rp) :
      sigma_mean_r_first = sigma_mean_first
  elif (delta_sigma_first <= 2*Rp and abs(sigma_max_first) > Rp):
      if (sigma_mean_first > 0):
          sigma_mean_r_first = Rp - 0.5*sigma_mean_first
      else:
          sigma_mean_r_first = 0.5*sigma_mean_first - Rp
  else:
      sigma_mean_r_first = sigma_mean_first

  #calculate M
  M=0.00035*Rm-0.1            
  #calculat A1
  A1 = delta_sigma_R/(2*(1+M))

  # calculate Full mean stress correction factor
  if (-Rp <= sigma_mean_r_first and sigma_mean_r_first <= A1):
    # f_m =sqrt(1-M*(2+M)/(1+M)*(2*sigma_mean_r/delta_sigma_R))
    f_m =(1-M*(2+M)/(1+M)*(2*sigma_mean_r_first/delta_sigma_R))       # Book: Pressure Vessel Design_ The direct route (Zeman T.L 2006)

  elif (A1 <= sigma_mean_r_first and sigma_mean_r_first <= Rp):
    f_m = (1+M/3)/(1+M) - M/3*(2*sigma_mean_r_first/delta_sigma_R)
  else:
    f_m =1


  # Calculate overall correction factor # f_u=f_T*f_s*f_e*f_m
  f_u =f_T * f_s * f_e * f_m


  #calulate delta signma R new and N new
  delta_sigma_R_new_first = delta_sigma_f_first/f_u
  if (delta_sigma_R_new_first - delta_sigma_D) <= 0:
    N_new_first = ((2.69*Rm+89.72)/delta_sigma_R_new_first)**10
  else:
    N_new_first = (46000/(delta_sigma_R_new_first-0.63*Rm + 11.5))**2         # when delta_sigma_R >= delta_sigma_D
  # N_new = ((2.69*Rm+89.72)/delta_sigma_R_new)**10                 # when delta_sigma_R < delta_sigma_D


  #stopping creterion 
  if abs(N-N_new_first) <= 1e-5:
    break
  
  #update delta_sigma_R and N
  delta_sigma_R  =delta_sigma_R_new_first 
  N =N_new_first
  i =i+1
  print('iteration no ={},N={},delta_sigma_R={}'.format(i,N,delta_sigma_R))

print('Number of cycles at inside =',int(N))
# print('Delta sigmat at inside =', value(delta_sigma))

#----------------------------------------------------------------------------------------------------------

print('***************************************************************************************') 
print('Calculate allowable cycles at outside')
n_last= len(data_export_last)

# def max_value_find(data_export_first,n_first):
#   max = data_export_last[0]
#   for i in range(1,n_last):
#       if data_export_last[i]>max:
#           max = data_export_last[i]
#   return max

# def min_value_find(data_export_first,n_first):
#   min = data_export_last[0]
#   for i in range(1,n_last):
#       if data_export_last[i]<min:
#           min = data_export_last[i]
#   return min

Ans_max_last = max_value_find(data_export_last,n_last)
Ans_min_last = min_value_find(data_export_last,n_last)

# known parameters
delta_sigma_last =  (Ans_max_last-Ans_min_last)            # equivalent structural stress range (linear distribution) [N/mm2]
sigma_mean_last =  0.5*(Ans_max_last+Ans_min_last)         # mean stress
# delta_sigma_D =  230                        # the thermal endurance limit, Carbon steel SA 210 A-1
# Rm = 470                    # Tensile strength [N/mm2]
# Rp = 290                    # the yield strength of material
# T_max = 500                 # the metal temperature during the moment of the highest stress [C]
# T_min = 400                 # the metal temperature during the moment of lowest stress [C]
# K_t =  3.0                  # Thermal stress correction factor
# Rz = 50                     # the peak-to-valley height (micrometer), 50 for machine, 10 for ground, free of notches

# RO = value(m.fs.aPSH.r.last())
# RI = value(m.fs.aPSH.r.first())

# Maximum stress calculation
sigma_max_last = sigma_mean_last + 0.5*delta_sigma_last

A0 = 0.4 # for Rm <= 500 MPa
# A0 = 0.4+(Rm-500)/3000  # for 500 < Rm <= 800 MPa
# A0 = 0.5 # for 800 < Rm <= 1000 MPa
#calculate k_e
if delta_sigma_last > 2*Rp:
    # k_e = 1+0.4*(delta_sigma/(2*Rp)-1)            # For austenitic steels
  k_e = 1+A0*(delta_sigma_last/(2*Rp)-1)               # For other steels
else:
  k_e= 1 

# calculate kv
if delta_sigma_last > 2*Rp:
  k_v= max(1, value(0.7/(0.5+0.4/(delta_sigma_last/Rp))))      
else:
  k_v= 1 

# Equivalent stress
delta_sigma_eq_last =delta_sigma_last * k_e * k_v

# calcualte kf
K_f_last= 1+1.5*(K_t-1)/(1+0.5*max(1,(value(K_t*delta_sigma_eq_last/delta_sigma_D))))

# calculate Delta sigma f
delta_sigma_f_last = (K_f_last * delta_sigma_eq_last)


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
  # Calculate surface finish correction factor
  if (N - 2E6) <= 0:
      f_s = (1 - 0.056*(log(Rz))**0.64 * log(Rm) + 0.289*(log(Rz))**0.53)**(0.1*(log(N))-0.465)           
  else:
      f_s = 1 - 0.056*(log(Rz))**0.64 * log(Rm) + 0.289*(log(Rz))**0.53


  # Calculate thickness correction factor
  e_n = (0.5*(RO-RI)*1000)
  if (N - 2E6) <= 0: 
      f_e = ((25/e_n)**0.182)**(0.1*(log(N))-0.465)
  else:
      f_e = (25/e_n)**0.182


  #calculate sigma_mean_r
  if (delta_sigma_last <= 2*Rp and abs(sigma_max_last) < Rp) :
      sigma_mean_r_last = sigma_mean_last
  elif (delta_sigma_last <= 2*Rp and abs(sigma_max_last) > Rp):
      if (sigma_mean_last > 0):
          sigma_mean_r_last = Rp - 0.5*sigma_mean_last
      else:
          sigma_mean_r_last = 0.5*sigma_mean_last - Rp
  else:
      sigma_mean_r_last = sigma_mean_last

  #calculate M
  M=0.00035*Rm-0.1            
  #calculat A1
  A1 = delta_sigma_R/(2*(1+M))

  # calculate Full mean stress correction factor
  if (-Rp <= sigma_mean_r_last and sigma_mean_r_last <= A1):
    # f_m =sqrt(1-M*(2+M)/(1+M)*(2*sigma_mean_r/delta_sigma_R))
    f_m =(1-M*(2+M)/(1+M)*(2*sigma_mean_r_last/delta_sigma_R))       # Book: Pressure Vessel Design_ The direct route (Zeman T.L 2006)

  elif (A1 <= sigma_mean_r_last and sigma_mean_r_last <= Rp):
    f_m = (1+M/3)/(1+M) - M/3*(2*sigma_mean_r_last/delta_sigma_R)
  else:
    f_m =1


  # Calculate overall correction factor # f_u=f_T*f_s*f_e*f_m
  f_u =f_T * f_s * f_e * f_m


  #calulate delta signma R new and N new
  delta_sigma_R_new_last = delta_sigma_f_last/f_u
  if (delta_sigma_R_new_last - delta_sigma_D) <= 0:
    N_new_last = ((2.69*Rm+89.72)/delta_sigma_R_new_last)**10
  else:
    N_new_last = (46000/(delta_sigma_R_new_last-0.63*Rm + 11.5))**2         # when delta_sigma_R >= delta_sigma_D
  # N_new = ((2.69*Rm+89.72)/delta_sigma_R_new)**10                 # when delta_sigma_R < delta_sigma_D


  #stopping creterion 
  if abs(N-N_new_last) <= 1e-5:
    break
  
  #update delta_sigma_R and N
  delta_sigma_R  =delta_sigma_R_new_last 
  N =N_new_last
  i =i+1
  print('iteration no ={},N={},delta_sigma_R={}'.format(i,N,delta_sigma_R))

print('Number of cycles at outside =',int(N))
