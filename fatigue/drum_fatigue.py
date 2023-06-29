from pyomo.environ import*
# ***********************************************************
# Fatigue for drum model
# Call data from excel file
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

df_data = \
pd.read_excel(r'C:\Users\minh2\OneDrive\Desktop\Header\PSH_header_simulation\plant_dyn_JM\plant_dyn_JM.xlsx',sheet_name ='case_5pct_result')


data_export = df_data['drum_von_Mises_P1'] # drum_von_Mises_P1

#----------------------------------------------------------------------------------------------------------
# Calculate number of allowable cycles

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

n= len(data_export)
Ans_max = max_value_find(data_export,n)
Ans_min = min_value_find(data_export,n)
delta_sigma =  (Ans_max-Ans_min)            # equivalent structural stress range (linear distribution) [N/mm2]
sigma_mean =  0.5*(Ans_max+Ans_min)         # mean stress

delta_sigma_D =  399             # the thermal endurance limit, Table 18.10, EN 13445, page 502
delta_sigma_cut = 270            # the cut-off limit, Table 18.10, EN 13445, page 502
Rm = (515+655)/2            # Tensile strength [N/mm2]
Rp = 275                    # the yield strength of material
T_max = 603.7249-273.15                 # the metal temperature during the moment of the highest stress [C]
T_min = 577.1474-273.15                 # the metal temperature during the moment of lowest stress [C]
K_t =  3.0                  # Thermal stress correction factor
Rz = 50                     # the peak-to-valley height (micrometer), 50 for machine, 10 for ground, free of notches

RO = (1.778+2*0.127)/2      # outside radius
RI = 1.778/2                # inside radius

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
  k_v= max(1, value(0.7/(0.5+0.4/(delta_sigma/Rp))))      
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
    K_f = 1+1.5*(K_t-1)/(1+0.5*max(1,(value(K_t*delta_sigma_eq/delta_sigma_D))))
  # If N > 2e6: delta_sigma_D = delta_sigma_R
  else:
    K_f = 1+1.5*(K_t-1)/(1+0.5*max(1,(value(K_t*delta_sigma_eq/delta_sigma_R))))

  # calculate effective total stress range
  delta_sigma_f = K_f * delta_sigma_eq

  # Calculate surface finish correction factor
  # polished surface withr Rz < 6: f_s = 1
  # untreated surfaces of deep drawn components and forgings: F_s = 0.25 + 0.75*(1-Rm/1500)**1.8
  if (N - 2E6) <= 0:
    f_s = (1 - 0.056*(log(Rz))**0.64 * log(Rm) + 0.289*(log(Rz))**0.53)**(0.1*(log(N))-0.465)           
  else:
    f_s = 1 - 0.056*(log(Rz))**0.64 * log(Rm) + 0.289*(log(Rz))**0.53


  # Drum thickness
  e_n = (RO-RI)*1000

  # Calculate thickness correction factor
  if e_n < 25:
    f_e = 1
  elif (e_n > 25 and (N - 2E6) <= 0):  
    if (e_n <=150 and e_n>25):  
      f_e = ((25/e_n)**0.182)**(0.1*(log(N))-0.465)
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

  #calculate M
  M=0.00035*Rm-0.1            
  #calculat A1
  A1 = delta_sigma_R/(2*(1+M))

  # calculate full mean stress correction factor
  if N <= 2e6:
    if (-Rp <= sigma_mean_r and sigma_mean_r <= A1):
      f_m =sqrt(1-M*(2+M)/(1+M)*(2*sigma_mean_r/delta_sigma_R))
    elif (A1 < sigma_mean_r and sigma_mean_r <= Rp):
      f_m = (1+M/3)/(1+M) - M/3*(2*sigma_mean_r/delta_sigma_R)
    else:
      f_m =1
  # If N >= 2e6, replace delta_sigma_R by delta_sigma_D
  else: 
    if (-Rp <= sigma_mean_r and sigma_mean_r <= A1):
      f_m =sqrt(1-M*(2+M)/(1+M)*(2*sigma_mean_r/delta_sigma_D))
    elif (A1 < sigma_mean_r and sigma_mean_r <= Rp):
      f_m = (1+M/3)/(1+M) - M/3*(2*sigma_mean_r/delta_sigma_D)
    else:
      f_m =1

  
  # Calculate overall correction factor # f_u=f_T*f_s*f_e*f_m
  f_u =f_T * f_s * f_e * f_m

  print('value f_T = {}, f_s = {}, f_e = {}, f_m = {}, f_u = {}'.format(f_T,f_s,f_e,f_m,f_u))

  #calulate delta signma R new and N new
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
  N =N_new
  i =i+1
  print('iteration no ={},N={},delta_sigma_R={}'.format(i,N,delta_sigma_R))

print('N =',int(N))
print('delta_sigma =', value(delta_sigma))
print('sigma_mean =', value(sigma_mean))

