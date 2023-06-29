
data_dic = {
        1: '(-20468.5 * b.wall_temperature_waterwall[t, 1] \
            +7668.88 * b.wall_temperature_waterwall[t, 2] \
            +1921.7 * b.wall_temperature_waterwall[t, 3] \
            -86.992 * b.wall_temperature_waterwall[t, 4] \
            +981.208 * b.wall_temperature_waterwall[t, 5] \
            -68.5187 * b.wall_temperature_waterwall[t, 8] \
            +555.499 * b.wall_temperature_waterwall[t, 9] \
            +2248.18 * b.wall_temperature_waterwall[t, 10] \
            +132.475 * b.wall_temperature_waterwall[t, 12] \
            +246.492 * b.wall_temperature_waterwall[t, 13] \
            -353.649 * b.wall_temperature_waterwall[t, 14] \
            -291.361 * b.wall_temperature_platen[t] \
            +1.24568e+06 * b.flowrate_coal_raw[t] \
            -2.64772e+06 * b.mf_H2O_coal_raw[t] \
            +9.40752e+06 * b.SR[t] \
            -4.0975e+07 * b.SR_lf[t] \
            +12419.4 * b.secondary_air_inlet.temperature[t] \
            +3.15232e+06 * b.ratio_PA2coal[t] \
            +1.22739e+07 * log(b.wall_temperature_waterwall[t, 1]) \
            -3.60253e+06 * log(b.wall_temperature_waterwall[t, 2]) \
            +1.61347e+06 * log(b.flowrate_coal_raw[t]) \
            +140299 * log(b.mf_H2O_coal_raw[t]) \
            -8.21691e+06 * log(b.SR[t]) \
            +5.56498e+07 * log(b.SR_lf[t]) \
            -1.57741e+07 * exp(b.mf_H2O_coal_raw[t]) \
            -13350.1 * b.flowrate_coal_raw[t]**2 \
            +104.063 * b.flowrate_coal_raw[t]**3 \
            -2.9325 * b.wall_temperature_waterwall[t, 1]*b.flowrate_coal_raw[t] \
            +2113.57 * b.wall_temperature_waterwall[t, 1]*b.mf_H2O_coal_raw[t] \
            -1757.68 * b.wall_temperature_waterwall[t, 1]*b.SR_lf[t] \
            -2.56178 * b.wall_temperature_waterwall[t, 1]*b.secondary_air_inlet.temperature[t] \
            -22.6412 * b.wall_temperature_waterwall[t, 1]*b.ratio_PA2coal[t] \
            +0.0808129 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 4] \
            +0.106031 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 9] \
            -1347.41 * b.wall_temperature_waterwall[t, 2]*b.mf_H2O_coal_raw[t] \
            -153.95 * b.wall_temperature_waterwall[t, 2]*b.SR[t] \
            -1.08721 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 9] \
            -0.715745 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 10] \
            +0.65708 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 9] \
            -0.440032 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 14] \
            +0.970767 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_platen[t] \
            -9.41161 * b.wall_temperature_waterwall[t, 5]*b.flowrate_coal_raw[t] \
            -1.47402 * b.wall_temperature_waterwall[t, 5]*b.secondary_air_inlet.temperature[t] \
            +0.266019 * b.wall_temperature_waterwall[t, 6]*b.wall_temperature_waterwall[t, 7] \
            +0.100127 * b.wall_temperature_waterwall[t, 6]*b.wall_temperature_waterwall[t, 11] \
            +9.25277 * b.wall_temperature_waterwall[t, 8]*b.flowrate_coal_raw[t] \
            -10.9006 * b.wall_temperature_waterwall[t, 9]*b.ratio_PA2coal[t] \
            -881.502 * b.wall_temperature_waterwall[t, 10]*b.SR[t] \
            -162.924 * b.wall_temperature_waterwall[t, 10]*b.ratio_PA2coal[t] \
            -2.30811 * b.wall_temperature_waterwall[t, 12]*b.flowrate_coal_raw[t] \
            -12.41 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +264.662 * b.wall_temperature_waterwall[t, 14]*b.ratio_PA2coal[t] \
            -8.35253 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -755153 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -24434.5 * b.flowrate_coal_raw[t]*b.SR[t] \
            -177888 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +283.412 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -30830.4 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +4.8456e+06 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            +1.10696e+07 * b.mf_H2O_coal_raw[t]*b.SR_lf[t] \
            -13063.8 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            +334734 * b.mf_H2O_coal_raw[t]*b.ratio_PA2coal[t] \
            -4.42412e+06 * b.SR[t]*b.SR_lf[t] \
            -2.056e+06 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -1842.84 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            -2.17806 * (b.wall_temperature_waterwall[t, 9]*b.mf_H2O_coal_raw[t])**2 \
            +17955.8 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            -2566.5 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            -1645.33 * (b.flowrate_coal_raw[t]*b.SR_lf[t])**2 \
            +24.0689 * (b.flowrate_coal_raw[t]*b.SR[t])**3)',
        2: '(11226 * b.wall_temperature_waterwall[t, 1] \
            -19181.2 * b.wall_temperature_waterwall[t, 2] \
            +1375.11 * b.wall_temperature_waterwall[t, 3] \
            +63.5608 * b.wall_temperature_waterwall[t, 4] \
            +2126.95 * b.wall_temperature_waterwall[t, 5] \
            -122.416 * b.wall_temperature_waterwall[t, 8] \
            +277.16 * b.wall_temperature_waterwall[t, 9] \
            +1555.31 * b.wall_temperature_waterwall[t, 10] \
            -237.805 * b.wall_temperature_waterwall[t, 12] \
            +643.574 * b.wall_temperature_waterwall[t, 13] \
            -229.832 * b.wall_temperature_platen[t] \
            +1.09238e+06 * b.flowrate_coal_raw[t] \
            +1.56393e+07 * b.mf_H2O_coal_raw[t] \
            -9.81805e+06 * b.SR[t] \
            +6.62157e+07 * b.SR_lf[t] \
            +8604.71 * b.secondary_air_inlet.temperature[t] \
            +2.8848e+06 * b.ratio_PA2coal[t] \
            -4.88529e+06 * log(b.wall_temperature_waterwall[t, 1]) \
            +9.8727e+06 * log(b.wall_temperature_waterwall[t, 2]) \
            -608919 * log(b.wall_temperature_waterwall[t, 4]) \
            -923964 * log(b.wall_temperature_waterwall[t, 5]) \
            -440697 * log(b.wall_temperature_waterwall[t, 13]) \
            +1.52179e+06 * log(b.flowrate_coal_raw[t]) \
            -5919.2 * log(b.mf_H2O_coal_raw[t]) \
            +6.89016e+06 * log(b.SR[t]) \
            -2.45425e+07 * exp(b.mf_H2O_coal_raw[t]) \
            +1.77338e+06 * exp(b.SR[t]) \
            -1.9837e+07 * exp(b.SR_lf[t]) \
            -14309.8 * b.flowrate_coal_raw[t]**2 \
            +126.81 * b.flowrate_coal_raw[t]**3 \
            -917.773 * b.wall_temperature_waterwall[t, 1]*b.SR_lf[t] \
            -2.06667 * b.wall_temperature_waterwall[t, 1]*b.secondary_air_inlet.temperature[t] \
            -5.44227 * b.wall_temperature_waterwall[t, 1]*b.ratio_PA2coal[t] \
            +0.0596749 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 4] \
            +0.179798 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 9] \
            -6.76515 * b.wall_temperature_waterwall[t, 2]*b.flowrate_coal_raw[t] \
            -0.729652 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 9] \
            -0.56988 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 10] \
            +0.596081 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 9] \
            +0.912202 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 11] \
            -0.311133 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 14] \
            +0.749249 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_platen[t] \
            -6.59018 * b.wall_temperature_waterwall[t, 5]*b.flowrate_coal_raw[t] \
            -1.31366 * b.wall_temperature_waterwall[t, 5]*b.secondary_air_inlet.temperature[t] \
            +0.219365 * b.wall_temperature_waterwall[t, 6]*b.wall_temperature_waterwall[t, 7] \
            -0.172934 * b.wall_temperature_waterwall[t, 8]*b.wall_temperature_waterwall[t, 11] \
            +0.311788 * b.wall_temperature_waterwall[t, 8]*b.wall_temperature_waterwall[t, 14] \
            +6.39066 * b.wall_temperature_waterwall[t, 8]*b.flowrate_coal_raw[t] \
            -0.631784 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_waterwall[t, 11] \
            +0.407995 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_waterwall[t, 12] \
            -712.693 * b.wall_temperature_waterwall[t, 10]*b.SR[t] \
            -11.3242 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +1474.6 * b.wall_temperature_waterwall[t, 13]*b.mf_H2O_coal_raw[t] \
            -5.83138 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -537596 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -120688 * b.flowrate_coal_raw[t]*b.SR[t] \
            -130260 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +213.556 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -24659.7 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +2.70784e+06 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            +6.81893e+06 * b.mf_H2O_coal_raw[t]*b.SR_lf[t] \
            -10045.4 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -2.92414e+06 * b.SR[t]*b.SR_lf[t] \
            +1012.77 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            -1.91845e+06 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -1401.78 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +3.1403 * (b.wall_temperature_waterwall[t, 1]*b.mf_H2O_coal_raw[t])**2 \
            -0.0118774 * (b.wall_temperature_waterwall[t, 10]*b.ratio_PA2coal[t])**2 \
            +13365.9 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            +342.938 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            -1590.17 * (b.flowrate_coal_raw[t]*b.SR_lf[t])**2)',
        3: '(3924.61 * b.wall_temperature_waterwall[t, 1] \
            +439.568 * b.wall_temperature_waterwall[t, 2] \
            -9453.81 * b.wall_temperature_waterwall[t, 3] \
            +134.941 * b.wall_temperature_waterwall[t, 4] \
            +120.143 * b.wall_temperature_waterwall[t, 5] \
            -25.8399 * b.wall_temperature_waterwall[t, 8] \
            +1066.82 * b.wall_temperature_waterwall[t, 10] \
            +41.873 * b.wall_temperature_waterwall[t, 12] \
            -28.4594 * b.wall_temperature_waterwall[t, 13] \
            +185.728 * b.wall_temperature_platen[t] \
            +616025 * b.flowrate_coal_raw[t] \
            +7.30432e+06 * b.mf_H2O_coal_raw[t] \
            +2.68117e+06 * b.SR[t] \
            +5.59578e+06 * b.SR_lf[t] \
            +5879.89 * b.secondary_air_inlet.temperature[t] \
            +2.2435e+06 * b.ratio_PA2coal[t] \
            -1.18028e+06 * log(b.wall_temperature_waterwall[t, 1]) \
            +5.25007e+06 * log(b.wall_temperature_waterwall[t, 3]) \
            +1.06392e+06 * log(b.flowrate_coal_raw[t]) \
            +36200.8 * log(b.mf_H2O_coal_raw[t]) \
            -2.17338e+06 * log(b.SR[t]) \
            +2.14962e+07 * log(b.SR_lf[t]) \
            -117387 * log(b.secondary_air_inlet.temperature[t]) \
            -1.2551e+07 * exp(b.mf_H2O_coal_raw[t]) \
            -6.91025e+06 * exp(b.SR_lf[t]) \
            -8248.39 * b.flowrate_coal_raw[t]**2 \
            -5.70434e-05 * b.wall_temperature_waterwall[t, 14]**3 \
            +75.3371 * b.flowrate_coal_raw[t]**3 \
            +0.135016 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 14] \
            -1.74455 * b.wall_temperature_waterwall[t, 1]*b.flowrate_coal_raw[t] \
            +703.013 * b.wall_temperature_waterwall[t, 1]*b.mf_H2O_coal_raw[t] \
            -1146.84 * b.wall_temperature_waterwall[t, 1]*b.SR_lf[t] \
            -1.21497 * b.wall_temperature_waterwall[t, 1]*b.secondary_air_inlet.temperature[t] \
            -13.3324 * b.wall_temperature_waterwall[t, 1]*b.ratio_PA2coal[t] \
            -0.149176 * b.wall_temperature_waterwall[t, 2]*b.secondary_air_inlet.temperature[t] \
            -0.357391 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 10] \
            -0.0244073 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 14] \
            +0.0594707 * b.wall_temperature_waterwall[t, 6]*b.wall_temperature_waterwall[t, 11] \
            +0.0959327 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_waterwall[t, 9] \
            +3.23037 * b.wall_temperature_waterwall[t, 8]*b.flowrate_coal_raw[t] \
            -453.628 * b.wall_temperature_waterwall[t, 10]*b.SR[t] \
            -65.7458 * b.wall_temperature_waterwall[t, 10]*b.ratio_PA2coal[t] \
            -0.842008 * b.wall_temperature_waterwall[t, 12]*b.flowrate_coal_raw[t] \
            -5.48772 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +878.866 * b.wall_temperature_waterwall[t, 13]*b.mf_H2O_coal_raw[t] \
            -3.45295 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -343651 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -52137.5 * b.flowrate_coal_raw[t]*b.SR[t] \
            -52566.5 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +134.596 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -15808.1 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +1.16101e+06 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            +3.44401e+06 * b.mf_H2O_coal_raw[t]*b.SR_lf[t] \
            -6122.41 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -1.1101e+06 * b.SR[t]*b.SR_lf[t] \
            -1.55646e+06 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -921.577 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +0.831261 * (b.wall_temperature_waterwall[t, 6]*b.mf_H2O_coal_raw[t])**2 \
            +8413.53 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            +154.629 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            -1314.13 * (b.flowrate_coal_raw[t]*b.SR_lf[t])**2)',
        4: '(3141.14 * b.wall_temperature_waterwall[t, 1] \
            +172.215 * b.wall_temperature_waterwall[t, 2] \
            +847.946 * b.wall_temperature_waterwall[t, 3] \
            +30263.6 * b.wall_temperature_waterwall[t, 4] \
            +459.024 * b.wall_temperature_waterwall[t, 5] \
            -255.837 * b.wall_temperature_waterwall[t, 6] \
            -253.656 * b.wall_temperature_waterwall[t, 7] \
            -111.033 * b.wall_temperature_waterwall[t, 8] \
            -139.598 * b.wall_temperature_waterwall[t, 9] \
            +987.465 * b.wall_temperature_waterwall[t, 10] \
            -229.451 * b.wall_temperature_waterwall[t, 12] \
            +139.255 * b.wall_temperature_waterwall[t, 13] \
            -342.179 * b.wall_temperature_platen[t] \
            +808422 * b.flowrate_coal_raw[t] \
            +4.59898e+06 * b.mf_H2O_coal_raw[t] \
            +2.52239e+06 * b.SR[t] \
            -1.81024e+08 * b.SR_lf[t] \
            +5802 * b.secondary_air_inlet.temperature[t] \
            +1.79667e+06 * b.ratio_PA2coal[t] \
            -1.01439e+06 * log(b.wall_temperature_waterwall[t, 1]) \
            -9.25322e+06 * log(b.wall_temperature_waterwall[t, 4]) \
            -106900 * log(b.wall_temperature_waterwall[t, 13]) \
            -376731 * log(b.wall_temperature_platen[t]) \
            +1.08793e+06 * log(b.flowrate_coal_raw[t]) \
            +43814.2 * log(b.mf_H2O_coal_raw[t]) \
            -2.68644e+06 * log(b.SR[t]) \
            +1.10291e+08 * log(b.SR_lf[t]) \
            -1.29535e+07 * exp(b.mf_H2O_coal_raw[t]) \
            +1.51376e+08 * exp(b.SR_lf[t]) \
            -13.9677 * b.wall_temperature_waterwall[t, 4]**2 \
            -10570.2 * b.flowrate_coal_raw[t]**2 \
            -1.67364e+08 * b.SR_lf[t]**2 \
            +93.7301 * b.flowrate_coal_raw[t]**3 \
            -1.45162 * b.wall_temperature_waterwall[t, 1]*b.flowrate_coal_raw[t] \
            +958.42 * b.wall_temperature_waterwall[t, 1]*b.mf_H2O_coal_raw[t] \
            -501.786 * b.wall_temperature_waterwall[t, 1]*b.SR_lf[t] \
            -1.46924 * b.wall_temperature_waterwall[t, 1]*b.secondary_air_inlet.temperature[t] \
            -12.8843 * b.wall_temperature_waterwall[t, 1]*b.ratio_PA2coal[t] \
            +0.158379 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 4] \
            +0.186963 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 9] \
            -825.009 * b.wall_temperature_waterwall[t, 2]*b.mf_H2O_coal_raw[t] \
            -0.534193 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 9] \
            -0.459179 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 10] \
            +376.092 * b.wall_temperature_waterwall[t, 3]*b.mf_H2O_coal_raw[t] \
            +0.326125 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 9] \
            -8.35979 * b.wall_temperature_waterwall[t, 4]*b.flowrate_coal_raw[t] \
            +0.103319 * b.wall_temperature_waterwall[t, 4]*b.secondary_air_inlet.temperature[t] \
            +0.522501 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_platen[t] \
            -4.9824 * b.wall_temperature_waterwall[t, 5]*b.flowrate_coal_raw[t] \
            -1.00721 * b.wall_temperature_waterwall[t, 5]*b.secondary_air_inlet.temperature[t] \
            +0.477989 * b.wall_temperature_waterwall[t, 6]*b.wall_temperature_platen[t] \
            +0.455732 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_platen[t] \
            +3.84995 * b.wall_temperature_waterwall[t, 8]*b.flowrate_coal_raw[t] \
            +37.2828 * b.wall_temperature_waterwall[t, 8]*b.ratio_PA2coal[t] \
            +0.35644 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_waterwall[t, 12] \
            -452.508 * b.wall_temperature_waterwall[t, 10]*b.SR[t] \
            -6.23326 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +930.344 * b.wall_temperature_waterwall[t, 13]*b.mf_H2O_coal_raw[t] \
            +30.5111 * b.wall_temperature_waterwall[t, 14]*b.mf_H2O_coal_raw[t] \
            -4.00393 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -371726 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -71393.4 * b.flowrate_coal_raw[t]*b.SR[t] \
            -133621 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +151.271 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -18420.1 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +1.36928e+06 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            +6.15109e+06 * b.mf_H2O_coal_raw[t]*b.SR_lf[t] \
            -6679.38 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -1.20513e+06 * b.SR[t]*b.SR_lf[t] \
            +909.363 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            -1.17463e+06 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -1017.96 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +8948.92 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            +216.961 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            -909.761 * (b.flowrate_coal_raw[t]*b.SR_lf[t])**2)',
        5: '(1260.21 * b.wall_temperature_waterwall[t, 1] \
            +187.803 * b.wall_temperature_waterwall[t, 2] \
            +90.5357 * b.wall_temperature_waterwall[t, 3] \
            +115.405 * b.wall_temperature_waterwall[t, 4] \
            -25719.1 * b.wall_temperature_waterwall[t, 5] \
            -3.01496 * b.wall_temperature_waterwall[t, 8] \
            +227.995 * b.wall_temperature_waterwall[t, 9] \
            +1055.92 * b.wall_temperature_waterwall[t, 10] \
            +21.3607 * b.wall_temperature_waterwall[t, 12] \
            +41.0148 * b.wall_temperature_waterwall[t, 13] \
            +120.366 * b.wall_temperature_platen[t] \
            +893437 * b.flowrate_coal_raw[t] \
            +9.6191e+06 * b.mf_H2O_coal_raw[t] \
            -172486 * b.SR[t] \
            +3.5745e+07 * b.SR_lf[t] \
            +4195.57 * b.secondary_air_inlet.temperature[t] \
            +1.65447e+06 * b.ratio_PA2coal[t] \
            -705858 * log(b.wall_temperature_waterwall[t, 1]) \
            -317431 * log(b.wall_temperature_waterwall[t, 4]) \
            +3.84944e+06 * log(b.wall_temperature_waterwall[t, 5]) \
            +1.23538e+06 * log(b.flowrate_coal_raw[t]) \
            -4336.85 * log(b.mf_H2O_coal_raw[t]) \
            -1.18493e+06 * log(b.SR[t]) \
            -1.77068e+07 * exp(b.mf_H2O_coal_raw[t]) \
            +366166 * exp(b.SR[t]) \
            -1.12866e+07 * exp(b.SR_lf[t]) \
            +25.482 * b.wall_temperature_waterwall[t, 5]**2 \
            +0.548182 * b.wall_temperature_roof[t]**2 \
            -10961.7 * b.flowrate_coal_raw[t]**2 \
            -0.0120321 * b.wall_temperature_waterwall[t, 5]**3 \
            -0.000138663 * b.wall_temperature_waterwall[t, 14]**3 \
            +86.5756 * b.flowrate_coal_raw[t]**3 \
            -1.51235 * b.wall_temperature_waterwall[t, 1]*b.flowrate_coal_raw[t] \
            -21.3116 * b.wall_temperature_waterwall[t, 1]*b.SR_lf[t] \
            +12.2766 * b.wall_temperature_waterwall[t, 1]*b.ratio_PA2coal[t] \
            +0.0610504 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 4] \
            -0.441485 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 9] \
            -0.257743 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_roof[t] \
            +564.113 * b.wall_temperature_waterwall[t, 3]*b.SR_lf[t] \
            +0.480054 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 9] \
            +0.148867 * b.wall_temperature_waterwall[t, 4]*b.secondary_air_inlet.temperature[t] \
            -0.203093 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 14] \
            +0.556015 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_platen[t] \
            -13.7815 * b.wall_temperature_waterwall[t, 5]*b.flowrate_coal_raw[t] \
            +0.11546 * b.wall_temperature_waterwall[t, 6]*b.wall_temperature_waterwall[t, 7] \
            +0.0549771 * b.wall_temperature_waterwall[t, 6]*b.wall_temperature_waterwall[t, 11] \
            +3.49661 * b.wall_temperature_waterwall[t, 8]*b.flowrate_coal_raw[t] \
            -56.8992 * b.wall_temperature_waterwall[t, 9]*b.ratio_PA2coal[t] \
            -0.387365 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_roof[t] \
            -410.497 * b.wall_temperature_waterwall[t, 10]*b.SR[t] \
            -64.3265 * b.wall_temperature_waterwall[t, 10]*b.ratio_PA2coal[t] \
            -8.94896 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +969.651 * b.wall_temperature_waterwall[t, 13]*b.mf_H2O_coal_raw[t] \
            +139.144 * b.wall_temperature_waterwall[t, 14]*b.ratio_PA2coal[t] \
            -0.438688 * b.wall_temperature_platen[t]*b.wall_temperature_roof[t] \
            -3.76038 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -380005 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -94555.8 * b.flowrate_coal_raw[t]*b.SR[t] \
            -213867 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +154.784 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -18526 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +1.86237e+06 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            +6.75155e+06 * b.mf_H2O_coal_raw[t]*b.SR_lf[t] \
            -6754.36 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -1.09309e+06 * b.SR[t]*b.SR_lf[t] \
            +823.608 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            -1.03983e+06 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -1040.61 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +9386.36 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            +317.752 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            +0.00653287 * (b.wall_temperature_waterwall[t, 1]*b.mf_H2O_coal_raw[t])**3)',
        6: '(2524.13 * b.wall_temperature_waterwall[t, 1] \
            -473.39 * b.wall_temperature_waterwall[t, 2] \
            -611.819 * b.wall_temperature_waterwall[t, 3] \
            -327.538 * b.wall_temperature_waterwall[t, 4] \
            +23715.9 * b.wall_temperature_waterwall[t, 5] \
            -69507.5 * b.wall_temperature_waterwall[t, 6] \
            -277.542 * b.wall_temperature_waterwall[t, 7] \
            +75.8839 * b.wall_temperature_waterwall[t, 8] \
            -382.351 * b.wall_temperature_waterwall[t, 9] \
            +1063.19 * b.wall_temperature_waterwall[t, 10] \
            +1804.61 * b.wall_temperature_waterwall[t, 11] \
            -361.396 * b.wall_temperature_waterwall[t, 12] \
            +168.069 * b.wall_temperature_waterwall[t, 13] \
            -16.2907 * b.wall_temperature_platen[t] \
            +940653 * b.flowrate_coal_raw[t] \
            +4.23171e+06 * b.mf_H2O_coal_raw[t] \
            +2.28657e+06 * b.SR[t] \
            +3.45724e+07 * b.SR_lf[t] \
            +5518.2 * b.secondary_air_inlet.temperature[t] \
            +1.71137e+06 * b.ratio_PA2coal[t] \
            -893878 * log(b.wall_temperature_waterwall[t, 1]) \
            -149762 * log(b.wall_temperature_waterwall[t, 4]) \
            -8.86277e+06 * log(b.wall_temperature_waterwall[t, 5]) \
            +1.25918e+07 * log(b.wall_temperature_waterwall[t, 6]) \
            +1.11622e+06 * log(b.flowrate_coal_raw[t]) \
            +49611.9 * log(b.mf_H2O_coal_raw[t]) \
            -4.8279e+06 * log(b.SR[t]) \
            -1.32067e+07 * exp(b.mf_H2O_coal_raw[t]) \
            -1.13998e+07 * exp(b.SR_lf[t]) \
            -7.92713 * b.wall_temperature_waterwall[t, 5]**2 \
            +61.0611 * b.wall_temperature_waterwall[t, 6]**2 \
            -0.1904 * b.wall_temperature_waterwall[t, 14]**2 \
            -11705.1 * b.flowrate_coal_raw[t]**2 \
            -0.0247076 * b.wall_temperature_waterwall[t, 6]**3 \
            +92.3209 * b.flowrate_coal_raw[t]**3 \
            -0.310677 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 13] \
            +0.172257 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 14] \
            -1.44116 * b.wall_temperature_waterwall[t, 1]*b.secondary_air_inlet.temperature[t] \
            -19.4625 * b.wall_temperature_waterwall[t, 1]*b.ratio_PA2coal[t] \
            +0.684303 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 3] \
            +0.238784 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 4] \
            -0.391165 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 10] \
            +541.242 * b.wall_temperature_waterwall[t, 3]*b.SR_lf[t] \
            +0.437355 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 9] \
            +0.28436 * b.wall_temperature_waterwall[t, 4]*b.secondary_air_inlet.temperature[t] \
            +0.350263 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 9] \
            -0.632562 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 11] \
            +0.536186 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 12] \
            -0.318697 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 14] \
            +0.480491 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_platen[t] \
            -5.50346 * b.wall_temperature_waterwall[t, 5]*b.flowrate_coal_raw[t] \
            +0.460134 * b.wall_temperature_waterwall[t, 6]*b.wall_temperature_platen[t] \
            -11.674 * b.wall_temperature_waterwall[t, 6]*b.flowrate_coal_raw[t] \
            +298.115 * b.wall_temperature_waterwall[t, 7]*b.SR[t] \
            -17.6983 * b.wall_temperature_waterwall[t, 9]*b.ratio_PA2coal[t] \
            -542.341 * b.wall_temperature_waterwall[t, 10]*b.SR[t] \
            -0.637401 * b.wall_temperature_waterwall[t, 11]*b.wall_temperature_platen[t] \
            -1.31338 * b.wall_temperature_waterwall[t, 11]*b.secondary_air_inlet.temperature[t] \
            -8.51399 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +1398.38 * b.wall_temperature_waterwall[t, 13]*b.mf_H2O_coal_raw[t] \
            -60.938 * b.wall_temperature_waterwall[t, 14]*b.mf_H2O_coal_raw[t] \
            +150.91 * b.wall_temperature_waterwall[t, 14]*b.ratio_PA2coal[t] \
            -4.01606 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -378070 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -128539 * b.flowrate_coal_raw[t]*b.SR[t] \
            -188207 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +160.627 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -18193.8 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +2.45023e+06 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            +5.92299e+06 * b.mf_H2O_coal_raw[t]*b.SR_lf[t] \
            -7319.98 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            +1379.5 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            -1.15268e+06 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -1055.24 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +8780.41 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            +420.738 * (b.flowrate_coal_raw[t]*b.SR[t])**2)',
        7: '(474.27 * b.wall_temperature_waterwall[t, 1] \
            +45.9059 * b.wall_temperature_waterwall[t, 2] \
            +320.83 * b.wall_temperature_waterwall[t, 3] \
            -280.775 * b.wall_temperature_waterwall[t, 4] \
            +1072.55 * b.wall_temperature_waterwall[t, 5] \
            +142.021 * b.wall_temperature_waterwall[t, 6] \
            -9016.5 * b.wall_temperature_waterwall[t, 7] \
            +20.6564 * b.wall_temperature_waterwall[t, 8] \
            -137.75 * b.wall_temperature_waterwall[t, 9] \
            +1141.63 * b.wall_temperature_waterwall[t, 10] \
            +976.004 * b.wall_temperature_waterwall[t, 11] \
            +26.7798 * b.wall_temperature_waterwall[t, 12] \
            -86.7844 * b.wall_temperature_waterwall[t, 13] \
            -632.481 * b.wall_temperature_waterwall[t, 14] \
            +386.622 * b.wall_temperature_platen[t] \
            +798165 * b.flowrate_coal_raw[t] \
            -8.86116e+06 * b.mf_H2O_coal_raw[t] \
            +2.67217e+06 * b.SR[t] \
            -2.23579e+07 * b.SR_lf[t] \
            +4616.63 * b.secondary_air_inlet.temperature[t] \
            +1.26689e+06 * b.ratio_PA2coal[t] \
            -457474 * log(b.wall_temperature_waterwall[t, 1]) \
            -456908 * log(b.wall_temperature_waterwall[t, 5]) \
            +4.97543e+06 * log(b.wall_temperature_waterwall[t, 7]) \
            -324054 * log(b.wall_temperature_platen[t]) \
            +859905 * log(b.flowrate_coal_raw[t]) \
            +51982.4 * log(b.mf_H2O_coal_raw[t]) \
            -6.09034e+06 * log(b.SR[t]) \
            +2.51526e+07 * log(b.SR_lf[t]) \
            -2.00793e+06 * exp(b.mf_H2O_coal_raw[t]) \
            -8569.95 * b.flowrate_coal_raw[t]**2 \
            +58.8983 * b.flowrate_coal_raw[t]**3 \
            +693.438 * b.wall_temperature_waterwall[t, 1]*b.mf_H2O_coal_raw[t] \
            +238.611 * b.wall_temperature_waterwall[t, 1]*b.SR_lf[t] \
            -5.93448 * b.wall_temperature_waterwall[t, 1]*b.ratio_PA2coal[t] \
            +0.301957 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 9] \
            -709.971 * b.wall_temperature_waterwall[t, 2]*b.mf_H2O_coal_raw[t] \
            -0.527198 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 9] \
            -0.286885 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 10] \
            +541.712 * b.wall_temperature_waterwall[t, 3]*b.mf_H2O_coal_raw[t] \
            -9.71413 * b.wall_temperature_waterwall[t, 3]*b.SR[t] \
            +301.185 * b.wall_temperature_waterwall[t, 3]*b.SR_lf[t] \
            +0.27972 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 9] \
            -2.08875 * b.wall_temperature_waterwall[t, 4]*b.SR[t] \
            +0.29136 * b.wall_temperature_waterwall[t, 4]*b.secondary_air_inlet.temperature[t] \
            +0.214989 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 9] \
            -0.259724 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 14] \
            +0.490069 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_platen[t] \
            -4.44612 * b.wall_temperature_waterwall[t, 5]*b.flowrate_coal_raw[t] \
            -0.947716 * b.wall_temperature_waterwall[t, 5]*b.secondary_air_inlet.temperature[t] \
            -13.9317 * b.wall_temperature_waterwall[t, 7]*b.flowrate_coal_raw[t] \
            +3.06822 * b.wall_temperature_waterwall[t, 8]*b.flowrate_coal_raw[t] \
            +0.168198 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_platen[t] \
            -1.26534 * b.wall_temperature_waterwall[t, 9]*b.flowrate_coal_raw[t] \
            -458.871 * b.wall_temperature_waterwall[t, 10]*b.SR[t] \
            -84.5202 * b.wall_temperature_waterwall[t, 10]*b.ratio_PA2coal[t] \
            -0.313148 * b.wall_temperature_waterwall[t, 11]*b.wall_temperature_platen[t] \
            -1.13435 * b.wall_temperature_waterwall[t, 11]*b.secondary_air_inlet.temperature[t] \
            +0.353432 * b.wall_temperature_waterwall[t, 13]*b.wall_temperature_waterwall[t, 14] \
            -7.75573 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +4286.46 * b.wall_temperature_waterwall[t, 14]*b.mf_H2O_coal_raw[t] \
            +116.804 * b.wall_temperature_waterwall[t, 14]*b.ratio_PA2coal[t] \
            -4.25261 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -331508 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -89127.3 * b.flowrate_coal_raw[t]*b.SR[t] \
            -149368 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +150.79 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -15081.2 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +2.98611e+06 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            +4.35995e+06 * b.mf_H2O_coal_raw[t]*b.SR_lf[t] \
            -6541.34 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            +1362.51 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            +93589.9 * b.SR[t]*b.ratio_PA2coal[t] \
            -821249 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -970.474 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            -9.97514 * (b.wall_temperature_waterwall[t, 14]*b.mf_H2O_coal_raw[t])**2 \
            +7495.68 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            -853.77 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            +11.0189 * (b.flowrate_coal_raw[t]*b.SR[t])**3)',
        8: '(1203.05 * b.wall_temperature_waterwall[t, 1] \
            -344.597 * b.wall_temperature_waterwall[t, 2] \
            +19.5032 * b.wall_temperature_waterwall[t, 3] \
            -510.784 * b.wall_temperature_waterwall[t, 4] \
            +43.0538 * b.wall_temperature_waterwall[t, 5] \
            -16414.7 * b.wall_temperature_waterwall[t, 6] \
            -166.079 * b.wall_temperature_waterwall[t, 7] \
            +5262.84 * b.wall_temperature_waterwall[t, 8] \
            +951.118 * b.wall_temperature_waterwall[t, 9] \
            +1944.21 * b.wall_temperature_waterwall[t, 10] \
            -524.099 * b.wall_temperature_waterwall[t, 11] \
            +286.689 * b.wall_temperature_waterwall[t, 12] \
            +376.151 * b.wall_temperature_waterwall[t, 13] \
            -311.631 * b.wall_temperature_waterwall[t, 14] \
            +94.5494 * b.wall_temperature_platen[t] \
            +403.623 * b.wall_temperature_roof[t] \
            +729460 * b.flowrate_coal_raw[t] \
            -8.10765e+06 * b.mf_H2O_coal_raw[t] \
            +5.12163e+06 * b.SR[t] \
            +340605 * b.SR_lf[t] \
            +10439.8 * b.secondary_air_inlet.temperature[t] \
            +377793 * b.ratio_PA2coal[t] \
            -597041 * log(b.wall_temperature_waterwall[t, 1]) \
            -455726 * log(b.wall_temperature_waterwall[t, 9]) \
            +715043 * log(b.flowrate_coal_raw[t]) \
            -1.31066e+07 * log(b.SR[t]) \
            +23.7108 * b.wall_temperature_waterwall[t, 6]**2 \
            -5.33194 * b.wall_temperature_waterwall[t, 8]**2 \
            +0.642661 * b.wall_temperature_waterwall[t, 11]**2 \
            +0.66995 * b.wall_temperature_roof[t]**2 \
            -7235.52 * b.flowrate_coal_raw[t]**2 \
            -9.50943e+06 * b.mf_H2O_coal_raw[t]**2 \
            -0.0109567 * b.wall_temperature_waterwall[t, 6]**3 \
            -7.59659e-05 * b.wall_temperature_waterwall[t, 14]**3 \
            +43.2711 * b.flowrate_coal_raw[t]**3 \
            +5.74405e+06 * b.mf_H2O_coal_raw[t]**3 \
            -0.319511 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 13] \
            +0.647747 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 3] \
            +0.0386179 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 9] \
            -0.00978949 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 10] \
            -0.289837 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 11] \
            +3.11788 * b.wall_temperature_waterwall[t, 3]*b.flowrate_coal_raw[t] \
            -188.549 * b.wall_temperature_waterwall[t, 3]*b.SR[t] \
            +0.180779 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 11] \
            +0.421665 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_platen[t] \
            +0.556927 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_roof[t] \
            -179.362 * b.wall_temperature_waterwall[t, 4]*b.SR[t] \
            +0.489665 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 12] \
            +0.525549 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_platen[t] \
            -1.11894 * b.wall_temperature_waterwall[t, 5]*b.secondary_air_inlet.temperature[t] \
            -0.651636 * b.wall_temperature_waterwall[t, 6]*b.wall_temperature_waterwall[t, 12] \
            +0.26951 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_waterwall[t, 14] \
            +91.4022 * b.wall_temperature_waterwall[t, 7]*b.SR[t] \
            -0.337552 * b.wall_temperature_waterwall[t, 8]*b.wall_temperature_waterwall[t, 11] \
            -13.1205 * b.wall_temperature_waterwall[t, 8]*b.flowrate_coal_raw[t] \
            +625.447 * b.wall_temperature_waterwall[t, 8]*b.mf_H2O_coal_raw[t] \
            +111.871 * b.wall_temperature_waterwall[t, 8]*b.SR[t] \
            -0.143315 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_roof[t] \
            -1.43078 * b.wall_temperature_waterwall[t, 9]*b.flowrate_coal_raw[t] \
            -0.437508 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 11] \
            -392.538 * b.wall_temperature_waterwall[t, 10]*b.SR[t] \
            -1.03531 * b.wall_temperature_waterwall[t, 10]*b.secondary_air_inlet.temperature[t] \
            -132.023 * b.wall_temperature_waterwall[t, 10]*b.ratio_PA2coal[t] \
            -0.366015 * b.wall_temperature_waterwall[t, 11]*b.wall_temperature_platen[t] \
            +454.417 * b.wall_temperature_waterwall[t, 11]*b.SR[t] \
            -0.0654458 * b.wall_temperature_waterwall[t, 12]*b.wall_temperature_waterwall[t, 13] \
            -80.8874 * b.wall_temperature_waterwall[t, 12]*b.SR[t] \
            -9.01814 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +0.0887393 * b.wall_temperature_waterwall[t, 14]*b.secondary_air_inlet.temperature[t] \
            +69.5916 * b.wall_temperature_waterwall[t, 14]*b.ratio_PA2coal[t] \
            -0.507975 * b.wall_temperature_platen[t]*b.wall_temperature_roof[t] \
            -12.9206 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -166.031 * b.wall_temperature_platen[t]*b.SR[t] \
            +343.605 * b.wall_temperature_platen[t]*b.SR_lf[t] \
            -351.38 * b.wall_temperature_roof[t]*b.SR[t] \
            -939.183 * b.wall_temperature_roof[t]*b.SR_lf[t] \
            +36.4681 * b.wall_temperature_roof[t]*b.ratio_PA2coal[t] \
            -276870 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -323281 * b.flowrate_coal_raw[t]*b.SR[t] \
            +146293 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +186.683 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -6502.59 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +7.74397e+06 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            -7126.9 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            +1.75851e+06 * b.SR[t]*b.SR_lf[t] \
            -953.168 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            +207351 * b.SR[t]*b.ratio_PA2coal[t] \
            -4595.65 * b.SR_lf[t]*b.secondary_air_inlet.temperature[t] \
            -1113.66 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +2.11788 * (b.wall_temperature_waterwall[t, 13]*b.mf_H2O_coal_raw[t])**2 \
            +0.00013867 * (b.wall_temperature_platen[t]*b.flowrate_coal_raw[t])**2 \
            +5802.79 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            -282.498 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            -1510.03 * (b.flowrate_coal_raw[t]*b.SR_lf[t])**2 \
            +1.34 * (b.SR[t]*b.secondary_air_inlet.temperature[t])**2 \
            +14.3624 * (b.flowrate_coal_raw[t]*b.SR[t])**3)',
        9: '(1836.1 * b.wall_temperature_waterwall[t, 1] \
            +462.437 * b.wall_temperature_waterwall[t, 2] \
            +700.405 * b.wall_temperature_waterwall[t, 3] \
            -1498.3 * b.wall_temperature_waterwall[t, 4] \
            +1209.82 * b.wall_temperature_waterwall[t, 5] \
            -38993.2 * b.wall_temperature_waterwall[t, 6] \
            +19929.9 * b.wall_temperature_waterwall[t, 7] \
            +542.635 * b.wall_temperature_waterwall[t, 8] \
            -19440.9 * b.wall_temperature_waterwall[t, 9] \
            +5496.56 * b.wall_temperature_waterwall[t, 10] \
            +1289.79 * b.wall_temperature_waterwall[t, 11] \
            -851.372 * b.wall_temperature_waterwall[t, 12] \
            -799.691 * b.wall_temperature_waterwall[t, 13] \
            +383.718 * b.wall_temperature_waterwall[t, 14] \
            +1749 * b.wall_temperature_platen[t] \
            +3770.54 * b.wall_temperature_roof[t] \
            +1.70303e+06 * b.flowrate_coal_raw[t] \
            +934596 * b.mf_H2O_coal_raw[t] \
            +1.37643e+07 * b.SR[t] \
            -1.30096e+07 * b.SR_lf[t] \
            +16055.5 * b.secondary_air_inlet.temperature[t] \
            +201380 * b.ratio_PA2coal[t] \
            -1.07631e+06 * log(b.wall_temperature_waterwall[t, 1]) \
            -450288 * log(b.wall_temperature_waterwall[t, 4]) \
            +1.08255e+07 * log(b.wall_temperature_waterwall[t, 9]) \
            -1.17544e+06 * log(b.wall_temperature_waterwall[t, 10]) \
            -1.53803e+06 * log(b.wall_temperature_waterwall[t, 11]) \
            -177549 * log(b.wall_temperature_waterwall[t, 12]) \
            +39948.2 * log(b.wall_temperature_platen[t]) \
            -2.20703e+06 * log(b.wall_temperature_roof[t]) \
            +992927 * log(b.flowrate_coal_raw[t]) \
            -1.86841e+07 * log(b.SR[t]) \
            -2.31856e+07 * exp(b.mf_H2O_coal_raw[t]) \
            +54.2939 * b.wall_temperature_waterwall[t, 6]**2 \
            -8.06834 * b.wall_temperature_waterwall[t, 7]**2 \
            -12035.4 * b.flowrate_coal_raw[t]**2 \
            +6.59153e+06 * b.SR_lf[t]**2 \
            -0.024925 * b.wall_temperature_waterwall[t, 6]**3 \
            -0.000354734 * b.wall_temperature_waterwall[t, 14]**3 \
            +41.1893 * b.flowrate_coal_raw[t]**3 \
            -0.103124 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 13] \
            -0.211392 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 9] \
            +1.2001 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 4] \
            -1.26509 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 11] \
            +0.00199659 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_roof[t] \
            -390.09 * b.wall_temperature_waterwall[t, 3]*b.SR[t] \
            +0.0340134 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 8] \
            -0.0875401 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 11] \
            +0.921992 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_platen[t] \
            +1.14569 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_roof[t] \
            -201.086 * b.wall_temperature_waterwall[t, 4]*b.SR[t] \
            +0.358484 * b.wall_temperature_waterwall[t, 4]*b.secondary_air_inlet.temperature[t] \
            +1.2154 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 12] \
            -3.04479 * b.wall_temperature_waterwall[t, 5]*b.secondary_air_inlet.temperature[t] \
            +494.397 * b.wall_temperature_waterwall[t, 6]*b.mf_H2O_coal_raw[t] \
            +0.851817 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_waterwall[t, 12] \
            +0.936564 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_waterwall[t, 14] \
            +566.986 * b.wall_temperature_waterwall[t, 7]*b.mf_H2O_coal_raw[t] \
            -14307 * b.wall_temperature_waterwall[t, 7]*b.SR[t] \
            -0.0178573 * b.wall_temperature_waterwall[t, 8]*b.wall_temperature_platen[t] \
            -258.651 * b.wall_temperature_waterwall[t, 8]*b.SR_lf[t] \
            -0.14334 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_platen[t] \
            -0.425254 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_roof[t] \
            -43.2167 * b.wall_temperature_waterwall[t, 9]*b.flowrate_coal_raw[t] \
            -1.90981 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 14] \
            -1062.96 * b.wall_temperature_waterwall[t, 10]*b.SR[t] \
            -235.592 * b.wall_temperature_waterwall[t, 10]*b.ratio_PA2coal[t] \
            +1.84247 * b.wall_temperature_waterwall[t, 11]*b.wall_temperature_waterwall[t, 13] \
            -1.02394 * b.wall_temperature_waterwall[t, 11]*b.wall_temperature_platen[t] \
            +1212.52 * b.wall_temperature_waterwall[t, 11]*b.SR[t] \
            -217.572 * b.wall_temperature_waterwall[t, 12]*b.SR[t] \
            -20.4304 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +1.06493 * b.wall_temperature_waterwall[t, 14]*b.secondary_air_inlet.temperature[t] \
            -1.12386 * b.wall_temperature_platen[t]*b.wall_temperature_roof[t] \
            -45.3926 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            +74.1654 * b.wall_temperature_roof[t]*b.ratio_PA2coal[t] \
            -655976 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -639368 * b.flowrate_coal_raw[t]*b.SR[t] \
            +256375 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +444.669 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -13228.3 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +1.97974e+07 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            -15073.3 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -3797.82 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            +358253 * b.SR[t]*b.ratio_PA2coal[t] \
            -6507.56 * b.SR_lf[t]*b.secondary_air_inlet.temperature[t] \
            +621411 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -2266.27 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +3.79183 * (b.wall_temperature_waterwall[t, 7]*b.SR[t])**2 \
            -0.214096 * (b.wall_temperature_waterwall[t, 9]*b.SR[t])**2 \
            +0.0246641 * (b.wall_temperature_waterwall[t, 14]*b.ratio_PA2coal[t])**2 \
            +0.000570728 * (b.wall_temperature_platen[t]*b.flowrate_coal_raw[t])**2 \
            -0.240504 * (b.wall_temperature_roof[t]*b.SR[t])**2 \
            +13497.1 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            -3995.29 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            -2167.38 * (b.flowrate_coal_raw[t]*b.SR_lf[t])**2 \
            +3.74466 * (b.SR[t]*b.secondary_air_inlet.temperature[t])**2 \
            +54.9147 * (b.flowrate_coal_raw[t]*b.SR[t])**3)',
        10: '(1625.59 * b.wall_temperature_waterwall[t, 1] \
            -48971 * b.wall_temperature_waterwall[t, 2] \
            +1099.29 * b.wall_temperature_waterwall[t, 3] \
            -1530.47 * b.wall_temperature_waterwall[t, 4] \
            +1344.08 * b.wall_temperature_waterwall[t, 5] \
            +49046.3 * b.wall_temperature_waterwall[t, 6] \
            -3856.09 * b.wall_temperature_waterwall[t, 7] \
            -433.777 * b.wall_temperature_waterwall[t, 8] \
            +3144.18 * b.wall_temperature_waterwall[t, 9] \
            +23674 * b.wall_temperature_waterwall[t, 10] \
            +2410.01 * b.wall_temperature_waterwall[t, 11] \
            -840.61 * b.wall_temperature_waterwall[t, 12] \
            +45.6992 * b.wall_temperature_waterwall[t, 13] \
            +232.693 * b.wall_temperature_waterwall[t, 14] \
            +2993.11 * b.wall_temperature_platen[t] \
            +3534.78 * b.wall_temperature_roof[t] \
            +1.65729e+06 * b.flowrate_coal_raw[t] \
            -3.16276e+07 * b.mf_H2O_coal_raw[t] \
            +4.18764e+06 * b.SR[t] \
            -2.68781e+07 * b.SR_lf[t] \
            -459.342 * b.secondary_air_inlet.temperature[t] \
            -300318 * b.ratio_PA2coal[t] \
            -1.06227e+06 * log(b.wall_temperature_waterwall[t, 1]) \
            +2.24874e+07 * log(b.wall_temperature_waterwall[t, 2]) \
            +402203 * log(b.wall_temperature_waterwall[t, 4]) \
            -2.3312e+07 * log(b.wall_temperature_waterwall[t, 6]) \
            +1.08194e+07 * log(b.wall_temperature_waterwall[t, 7]) \
            -1.39558e+06 * log(b.wall_temperature_waterwall[t, 9]) \
            -7.72647e+06 * log(b.wall_temperature_waterwall[t, 10]) \
            -247038 * log(b.wall_temperature_waterwall[t, 12]) \
            +1.0317e+06 * log(b.wall_temperature_waterwall[t, 14]) \
            -362815 * log(b.wall_temperature_platen[t]) \
            -1.6513e+06 * log(b.wall_temperature_roof[t]) \
            -62425.8 * log(b.flowrate_coal_raw[t]) \
            +360156 * log(b.mf_H2O_coal_raw[t]) \
            -1.04043e+07 * log(b.SR[t]) \
            +628079 * exp(b.SR[t]) \
            +8.19933e+06 * exp(b.SR_lf[t]) \
            -8564.38 * b.flowrate_coal_raw[t]**2 \
            +0.0113407 * b.wall_temperature_waterwall[t, 2]**3 \
            -0.0103721 * b.wall_temperature_waterwall[t, 6]**3 \
            -0.0091608 * b.wall_temperature_waterwall[t, 10]**3 \
            -0.955465 * b.flowrate_coal_raw[t]**3 \
            -0.269058 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 5] \
            +0.942715 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 8] \
            -0.599579 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 13] \
            +0.479366 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 9] \
            -0.158162 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_platen[t] \
            -1.09217 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 11] \
            +4.91327 * b.wall_temperature_waterwall[t, 3]*b.flowrate_coal_raw[t] \
            -224.355 * b.wall_temperature_waterwall[t, 3]*b.SR[t] \
            +1.22198 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_roof[t] \
            +184.763 * b.wall_temperature_waterwall[t, 4]*b.SR[t] \
            +1.23891 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 12] \
            -3.08247 * b.wall_temperature_waterwall[t, 5]*b.secondary_air_inlet.temperature[t] \
            +1.09686 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_waterwall[t, 12] \
            +1232.56 * b.wall_temperature_waterwall[t, 7]*b.mf_H2O_coal_raw[t] \
            -18397.5 * b.wall_temperature_waterwall[t, 7]*b.SR[t] \
            +1489.57 * b.wall_temperature_waterwall[t, 8]*b.mf_H2O_coal_raw[t] \
            -187.361 * b.wall_temperature_waterwall[t, 8]*b.SR_lf[t] \
            +0.0815017 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_waterwall[t, 14] \
            -0.230493 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_platen[t] \
            -0.67902 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_roof[t] \
            -9.33015 * b.wall_temperature_waterwall[t, 9]*b.flowrate_coal_raw[t] \
            -1.12153 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 11] \
            -0.176876 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 12] \
            -1.88087 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 14] \
            -37.1044 * b.wall_temperature_waterwall[t, 10]*b.flowrate_coal_raw[t] \
            -1188.3 * b.wall_temperature_waterwall[t, 10]*b.SR[t] \
            -257.4 * b.wall_temperature_waterwall[t, 10]*b.ratio_PA2coal[t] \
            -2.17159 * b.wall_temperature_waterwall[t, 11]*b.wall_temperature_waterwall[t, 14] \
            -0.784482 * b.wall_temperature_waterwall[t, 11]*b.wall_temperature_platen[t] \
            +1274.39 * b.wall_temperature_waterwall[t, 11]*b.SR[t] \
            +0.136902 * b.wall_temperature_waterwall[t, 12]*b.wall_temperature_waterwall[t, 13] \
            -188.324 * b.wall_temperature_waterwall[t, 12]*b.SR[t] \
            +1.0627 * b.wall_temperature_waterwall[t, 13]*b.wall_temperature_waterwall[t, 14] \
            -19.5148 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +0.653504 * b.wall_temperature_waterwall[t, 14]*b.secondary_air_inlet.temperature[t] \
            -37.4635 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -560.229 * b.wall_temperature_platen[t]*b.SR[t] \
            -10.567 * b.wall_temperature_roof[t]*b.flowrate_coal_raw[t] \
            -1082.38 * b.wall_temperature_roof[t]*b.SR[t] \
            -601636 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -470098 * b.flowrate_coal_raw[t]*b.SR[t] \
            +124754 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +430.837 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -9270.15 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +2.08162e+07 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            -12796 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            +8170.38 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            +225163 * b.SR[t]*b.ratio_PA2coal[t] \
            +1.12393e+06 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -1763.29 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +4.89596 * (b.wall_temperature_waterwall[t, 7]*b.SR[t])**2 \
            +0.000433641 * (b.wall_temperature_platen[t]*b.flowrate_coal_raw[t])**2 \
            +9195.08 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            -7066.47 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            +72.3083 * (b.flowrate_coal_raw[t]*b.SR[t])**3)',
        11: '(1149.96 * b.wall_temperature_waterwall[t, 1] \
            +486.815 * b.wall_temperature_waterwall[t, 2] \
            +985.013 * b.wall_temperature_waterwall[t, 3] \
            -1168.2 * b.wall_temperature_waterwall[t, 4] \
            +1424.95 * b.wall_temperature_waterwall[t, 5] \
            +191.148 * b.wall_temperature_waterwall[t, 6] \
            +23467.9 * b.wall_temperature_waterwall[t, 7] \
            -382.945 * b.wall_temperature_waterwall[t, 8] \
            +3211.32 * b.wall_temperature_waterwall[t, 9] \
            +4291.96 * b.wall_temperature_waterwall[t, 10] \
            -19488.8 * b.wall_temperature_waterwall[t, 11] \
            +2120.76 * b.wall_temperature_waterwall[t, 12] \
            +39.2439 * b.wall_temperature_waterwall[t, 13] \
            -1725.39 * b.wall_temperature_waterwall[t, 14] \
            +4715.43 * b.wall_temperature_platen[t] \
            +7808.52 * b.wall_temperature_roof[t] \
            +1.2977e+06 * b.flowrate_coal_raw[t] \
            -7.18061e+06 * b.mf_H2O_coal_raw[t] \
            +6.93565e+06 * b.SR[t] \
            -2.37482e+07 * b.SR_lf[t] \
            -2853.01 * b.secondary_air_inlet.temperature[t] \
            -268510 * b.ratio_PA2coal[t] \
            -892091 * log(b.wall_temperature_waterwall[t, 1]) \
            -1.66828e+06 * log(b.wall_temperature_waterwall[t, 9]) \
            -1.82491e+06 * log(b.wall_temperature_waterwall[t, 10]) \
            +1.05208e+07 * log(b.wall_temperature_waterwall[t, 11]) \
            -967600 * log(b.wall_temperature_waterwall[t, 12]) \
            +235346 * log(b.wall_temperature_waterwall[t, 14]) \
            -1.48537e+06 * log(b.wall_temperature_platen[t]) \
            -2.37767e+06 * log(b.wall_temperature_roof[t]) \
            -644766 * log(b.flowrate_coal_raw[t]) \
            -9.59737e+06 * log(b.SR[t]) \
            -1.57952e+07 * exp(b.mf_H2O_coal_raw[t]) \
            +8.10169e+06 * exp(b.SR_lf[t]) \
            -0.414281 * b.wall_temperature_waterwall[t, 2]**2 \
            -8.98981 * b.wall_temperature_waterwall[t, 7]**2 \
            -3654.23 * b.flowrate_coal_raw[t]**2 \
            -21.8999 * b.flowrate_coal_raw[t]**3 \
            +0.503427 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 8] \
            -0.089291 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 13] \
            +0.414521 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 9] \
            -0.0926811 * b.wall_temperature_waterwall[t, 2]*b.secondary_air_inlet.temperature[t] \
            -1.27019 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 11] \
            +7.5139 * b.wall_temperature_waterwall[t, 3]*b.flowrate_coal_raw[t] \
            -112.029 * b.wall_temperature_waterwall[t, 3]*b.SR[t] \
            +1.43679 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_roof[t] \
            +192.576 * b.wall_temperature_waterwall[t, 4]*b.SR[t] \
            -2.14251 * b.wall_temperature_waterwall[t, 5]*b.secondary_air_inlet.temperature[t] \
            +1535.88 * b.wall_temperature_waterwall[t, 7]*b.mf_H2O_coal_raw[t] \
            -16151.4 * b.wall_temperature_waterwall[t, 7]*b.SR[t] \
            +1659.33 * b.wall_temperature_waterwall[t, 8]*b.mf_H2O_coal_raw[t] \
            -0.767835 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_roof[t] \
            -0.600427 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 11] \
            -38.1635 * b.wall_temperature_waterwall[t, 11]*b.flowrate_coal_raw[t] \
            -250.644 * b.wall_temperature_waterwall[t, 12]*b.SR[t] \
            +0.779036 * b.wall_temperature_waterwall[t, 13]*b.wall_temperature_waterwall[t, 14] \
            -19.9073 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +1.45918 * b.wall_temperature_waterwall[t, 14]*b.secondary_air_inlet.temperature[t] \
            -1.06075 * b.wall_temperature_platen[t]*b.wall_temperature_roof[t] \
            -8.19138 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -682.175 * b.wall_temperature_platen[t]*b.SR[t] \
            -621.094 * b.wall_temperature_roof[t]*b.SR[t] \
            -3438.25 * b.wall_temperature_roof[t]*b.SR_lf[t] \
            +30.9672 * b.wall_temperature_roof[t]*b.ratio_PA2coal[t] \
            -587541 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -242606 * b.flowrate_coal_raw[t]*b.SR[t] \
            +106700 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +385.744 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -6676.14 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +1.82598e+07 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            -10529.7 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            +7471.83 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            +1.02902e+06 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -1482.81 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +4.28189 * (b.wall_temperature_waterwall[t, 7]*b.SR[t])**2 \
            -0.228191 * (b.wall_temperature_waterwall[t, 10]*b.SR[t])**2 \
            +9238.91 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            -8721.36 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            +75.6653 * (b.flowrate_coal_raw[t]*b.SR[t])**3)',
        12: '(3872.84 * b.wall_temperature_waterwall[t, 1] \
            -356.661 * b.wall_temperature_waterwall[t, 2] \
            -314.183 * b.wall_temperature_waterwall[t, 3] \
            -1041.41 * b.wall_temperature_waterwall[t, 4] \
            +1293.47 * b.wall_temperature_waterwall[t, 5] \
            +127.535 * b.wall_temperature_waterwall[t, 6] \
            -587.39 * b.wall_temperature_waterwall[t, 7] \
            -30.5484 * b.wall_temperature_waterwall[t, 8] \
            -233.72 * b.wall_temperature_waterwall[t, 9] \
            +1226.77 * b.wall_temperature_waterwall[t, 10] \
            +4906.7 * b.wall_temperature_waterwall[t, 11] \
            -21142 * b.wall_temperature_waterwall[t, 12] \
            +654.435 * b.wall_temperature_waterwall[t, 13] \
            -2689.62 * b.wall_temperature_waterwall[t, 14] \
            +6699.87 * b.wall_temperature_platen[t] \
            +1567.79 * b.wall_temperature_roof[t] \
            +1.50371e+06 * b.flowrate_coal_raw[t] \
            -1.84478e+07 * b.mf_H2O_coal_raw[t] \
            -7.69392e+06 * b.SR[t] \
            -1.79886e+07 * b.SR_lf[t] \
            -4798.9 * b.secondary_air_inlet.temperature[t] \
            -183598 * b.ratio_PA2coal[t] \
            -1.7949e+06 * log(b.wall_temperature_waterwall[t, 1]) \
            -1.73896e+06 * log(b.wall_temperature_waterwall[t, 11]) \
            +1.08083e+07 * log(b.wall_temperature_waterwall[t, 12]) \
            -1.46925e+06 * log(b.wall_temperature_waterwall[t, 13]) \
            +1.14705e+06 * log(b.wall_temperature_waterwall[t, 14]) \
            -3.79629e+06 * log(b.wall_temperature_platen[t]) \
            -995945 * log(b.flowrate_coal_raw[t]) \
            +213553 * log(b.mf_H2O_coal_raw[t]) \
            +1.0122e+06 * exp(b.SR[t]) \
            -15401.3 * b.flowrate_coal_raw[t]**2 \
            +7.49425e+06 * b.SR_lf[t]**2 \
            +124.313 * b.flowrate_coal_raw[t]**3 \
            +0.328915 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 5] \
            -0.444571 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 13] \
            -1.75528 * b.wall_temperature_waterwall[t, 1]*b.secondary_air_inlet.temperature[t] \
            +0.529667 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 9] \
            +0.335859 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_platen[t] \
            -1210.92 * b.wall_temperature_waterwall[t, 2]*b.mf_H2O_coal_raw[t] \
            -0.797568 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 11] \
            +8.74363 * b.wall_temperature_waterwall[t, 3]*b.flowrate_coal_raw[t] \
            +590.456 * b.wall_temperature_waterwall[t, 3]*b.SR[t] \
            +0.538997 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 11] \
            +579.815 * b.wall_temperature_waterwall[t, 4]*b.SR[t] \
            -2.30992 * b.wall_temperature_waterwall[t, 5]*b.secondary_air_inlet.temperature[t] \
            +0.779268 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_waterwall[t, 9] \
            +1291.09 * b.wall_temperature_waterwall[t, 7]*b.mf_H2O_coal_raw[t] \
            +973.997 * b.wall_temperature_waterwall[t, 8]*b.mf_H2O_coal_raw[t] \
            +0.113785 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_platen[t] \
            -0.48171 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_roof[t] \
            -0.928725 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 11] \
            -1.30138 * b.wall_temperature_waterwall[t, 11]*b.wall_temperature_waterwall[t, 14] \
            +0.196111 * b.wall_temperature_waterwall[t, 12]*b.wall_temperature_waterwall[t, 13] \
            -51.1074 * b.wall_temperature_waterwall[t, 12]*b.flowrate_coal_raw[t] \
            +0.807018 * b.wall_temperature_waterwall[t, 13]*b.wall_temperature_waterwall[t, 14] \
            -13.8925 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +2.44503 * b.wall_temperature_waterwall[t, 13]*b.secondary_air_inlet.temperature[t] \
            +2.33683 * b.wall_temperature_waterwall[t, 14]*b.secondary_air_inlet.temperature[t] \
            -5.50345 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -10.5945 * b.wall_temperature_roof[t]*b.flowrate_coal_raw[t] \
            -741.123 * b.wall_temperature_roof[t]*b.SR[t] \
            -510935 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -484123 * b.flowrate_coal_raw[t]*b.SR[t] \
            +82219.5 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +307.455 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -5683.32 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +1.31002e+07 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            -8586.79 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            +6331.18 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            +665512 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -915.588 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +8162.68 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2)',
        13: '(1109.75 * b.wall_temperature_waterwall[t, 1] \
            +24.7662 * b.wall_temperature_waterwall[t, 2] \
            +360.653 * b.wall_temperature_waterwall[t, 3] \
            -711.742 * b.wall_temperature_waterwall[t, 4] \
            +27073.4 * b.wall_temperature_waterwall[t, 5] \
            -1532.11 * b.wall_temperature_waterwall[t, 7] \
            +430.757 * b.wall_temperature_waterwall[t, 9] \
            +1286.7 * b.wall_temperature_waterwall[t, 10] \
            +1670.22 * b.wall_temperature_waterwall[t, 11] \
            -25340.7 * b.wall_temperature_waterwall[t, 12] \
            +27233.9 * b.wall_temperature_waterwall[t, 13] \
            +70.5537 * b.wall_temperature_waterwall[t, 14] \
            -28386.6 * b.wall_temperature_platen[t] \
            +1829.98 * b.wall_temperature_roof[t] \
            +440346 * b.flowrate_coal_raw[t] \
            -4.85573e+06 * b.mf_H2O_coal_raw[t] \
            -958725 * b.SR[t] \
            -2.32709e+06 * b.SR_lf[t] \
            -4208.62 * b.secondary_air_inlet.temperature[t] \
            -264105 * b.ratio_PA2coal[t] \
            -330702 * log(b.wall_temperature_waterwall[t, 1]) \
            +33237.7 * log(b.wall_temperature_waterwall[t, 4]) \
            -1.00714e+07 * log(b.wall_temperature_waterwall[t, 5]) \
            +569845 * log(b.wall_temperature_waterwall[t, 7]) \
            +8.28968e+06 * log(b.wall_temperature_waterwall[t, 12]) \
            -5.87903e+06 * log(b.wall_temperature_waterwall[t, 13]) \
            +253169 * log(b.wall_temperature_waterwall[t, 14]) \
            +8.38567e+06 * log(b.wall_temperature_platen[t]) \
            -737308 * log(b.wall_temperature_roof[t]) \
            -1.06106e+06 * log(b.flowrate_coal_raw[t]) \
            -2.49954e+06 * log(b.SR[t]) \
            -9.68149 * b.wall_temperature_waterwall[t, 5]**2 \
            +9.41298 * b.wall_temperature_waterwall[t, 12]**2 \
            -17.7275 * b.wall_temperature_waterwall[t, 13]**2 \
            +14.4525 * b.wall_temperature_platen[t]**2 \
            +981.461 * b.flowrate_coal_raw[t]**2 \
            -1.18891e+07 * b.mf_H2O_coal_raw[t]**2 \
            +4.30556e-05 * b.wall_temperature_waterwall[t, 6]**3 \
            -26.2018 * b.flowrate_coal_raw[t]**3 \
            +1.68091e+07 * b.mf_H2O_coal_raw[t]**3 \
            +0.0939684 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 8] \
            -0.20426 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 13] \
            -0.0883019 * b.wall_temperature_waterwall[t, 1]*b.flowrate_coal_raw[t] \
            -309.54 * b.wall_temperature_waterwall[t, 1]*b.SR_lf[t] \
            -0.879469 * b.wall_temperature_waterwall[t, 1]*b.secondary_air_inlet.temperature[t] \
            +129.155 * b.wall_temperature_waterwall[t, 1]*b.ratio_PA2coal[t] \
            +0.157583 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 9] \
            -518.811 * b.wall_temperature_waterwall[t, 2]*b.mf_H2O_coal_raw[t] \
            +0.530736 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 4] \
            -0.603945 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 9] \
            -0.753218 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 11] \
            +199.589 * b.wall_temperature_waterwall[t, 3]*b.SR[t] \
            +0.176046 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 11] \
            +152.519 * b.wall_temperature_waterwall[t, 4]*b.SR[t] \
            +1000.99 * b.wall_temperature_waterwall[t, 5]*b.SR_lf[t] \
            +0.36363 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_waterwall[t, 9] \
            +0.788635 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_waterwall[t, 12] \
            -0.0930805 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_roof[t] \
            -604.051 * b.wall_temperature_waterwall[t, 9]*b.mf_H2O_coal_raw[t] \
            -0.655676 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 11] \
            -0.817886 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 14] \
            -0.711442 * b.wall_temperature_waterwall[t, 11]*b.wall_temperature_waterwall[t, 14] \
            +0.0229465 * b.wall_temperature_waterwall[t, 12]*b.wall_temperature_waterwall[t, 13] \
            +0.715136 * b.wall_temperature_waterwall[t, 13]*b.wall_temperature_waterwall[t, 14] \
            -21.9173 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            -520.634 * b.wall_temperature_waterwall[t, 13]*b.SR[t] \
            +1.08606 * b.wall_temperature_waterwall[t, 13]*b.secondary_air_inlet.temperature[t] \
            +0.590081 * b.wall_temperature_waterwall[t, 14]*b.secondary_air_inlet.temperature[t] \
            -0.778078 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -501.52 * b.wall_temperature_platen[t]*b.SR[t] \
            -458.257 * b.wall_temperature_roof[t]*b.SR[t] \
            -300782 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            +69179.1 * b.flowrate_coal_raw[t]*b.SR[t] \
            +45189.7 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +168.826 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -2752.67 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +6.64076e+06 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            -4219.58 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            +4085.68 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            +437897 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -492.504 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +4885.73 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            -5626.05 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            +40.4748 * (b.flowrate_coal_raw[t]*b.SR[t])**3)',
        14: '(354.487 * b.wall_temperature_waterwall[t, 1] \
            -60.8645 * b.wall_temperature_waterwall[t, 2] \
            +327.396 * b.wall_temperature_waterwall[t, 3] \
            -1456.36 * b.wall_temperature_waterwall[t, 7] \
            +362.079 * b.wall_temperature_waterwall[t, 9] \
            +985.094 * b.wall_temperature_waterwall[t, 10] \
            -15673.4 * b.wall_temperature_waterwall[t, 11] \
            -83.4322 * b.wall_temperature_waterwall[t, 12] \
            -16319.3 * b.wall_temperature_waterwall[t, 13] \
            +68526.3 * b.wall_temperature_waterwall[t, 14] \
            -32620.5 * b.wall_temperature_platen[t] \
            +3619.67 * b.wall_temperature_roof[t] \
            +320878 * b.flowrate_coal_raw[t] \
            -4.78943e+06 * b.mf_H2O_coal_raw[t] \
            -1.57962e+07 * b.SR[t] \
            -1.23409e+06 * b.SR_lf[t] \
            -1973.52 * b.secondary_air_inlet.temperature[t] \
            -219033 * b.ratio_PA2coal[t] \
            -200963 * log(b.wall_temperature_waterwall[t, 1]) \
            +98301.9 * log(b.wall_temperature_waterwall[t, 3]) \
            +817844 * log(b.wall_temperature_waterwall[t, 7]) \
            +7.5546e+06 * log(b.wall_temperature_waterwall[t, 11]) \
            -91544.2 * log(b.wall_temperature_waterwall[t, 12]) \
            +5.29877e+06 * log(b.wall_temperature_waterwall[t, 13]) \
            -1.95837e+07 * log(b.wall_temperature_waterwall[t, 14]) \
            +9.89108e+06 * log(b.wall_temperature_platen[t]) \
            -1.68907e+06 * log(b.wall_temperature_roof[t]) \
            -950165 * log(b.flowrate_coal_raw[t]) \
            +107663 * log(b.mf_H2O_coal_raw[t]) \
            +1.00977e+07 * log(b.SR[t]) \
            -135582 * log(b.secondary_air_inlet.temperature[t]) \
            +1.54014e+06 * exp(b.SR[t]) \
            +6.45563 * b.wall_temperature_waterwall[t, 13]**2 \
            -32.5108 * b.wall_temperature_waterwall[t, 14]**2 \
            +16.0267 * b.wall_temperature_platen[t]**2 \
            +1020.99 * b.flowrate_coal_raw[t]**2 \
            +0.0038864 * b.wall_temperature_waterwall[t, 11]**3 \
            -23.3243 * b.flowrate_coal_raw[t]**3 \
            -0.19899 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 13] \
            -0.363486 * b.wall_temperature_waterwall[t, 1]*b.flowrate_coal_raw[t] \
            -0.239156 * b.wall_temperature_waterwall[t, 1]*b.secondary_air_inlet.temperature[t] \
            +93.3993 * b.wall_temperature_waterwall[t, 1]*b.ratio_PA2coal[t] \
            +0.156182 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 9] \
            -0.0202177 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_platen[t] \
            -0.436573 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 9] \
            -0.455785 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 11] \
            +149.628 * b.wall_temperature_waterwall[t, 3]*b.SR[t] \
            +0.0307972 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 8] \
            +0.0633193 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 6] \
            +0.2472 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_waterwall[t, 9] \
            +0.539863 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_waterwall[t, 12] \
            -24.6396 * b.wall_temperature_waterwall[t, 7]*b.flowrate_coal_raw[t] \
            -0.174682 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_roof[t] \
            -535.921 * b.wall_temperature_waterwall[t, 9]*b.mf_H2O_coal_raw[t] \
            -0.557081 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 14] \
            +2.71052 * b.wall_temperature_waterwall[t, 10]*b.flowrate_coal_raw[t] \
            -0.794394 * b.wall_temperature_waterwall[t, 10]*b.secondary_air_inlet.temperature[t] \
            -0.594428 * b.wall_temperature_waterwall[t, 11]*b.wall_temperature_waterwall[t, 14] \
            +0.242245 * b.wall_temperature_waterwall[t, 13]*b.wall_temperature_waterwall[t, 14] \
            -4.38229 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            -14.2876 * b.wall_temperature_waterwall[t, 14]*b.flowrate_coal_raw[t] \
            -491.212 * b.wall_temperature_platen[t]*b.mf_H2O_coal_raw[t] \
            -406.335 * b.wall_temperature_platen[t]*b.SR[t] \
            -379.661 * b.wall_temperature_roof[t]*b.SR[t] \
            -257600 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            +99274 * b.flowrate_coal_raw[t]*b.SR[t] \
            +28183 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +80.0701 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -1951.5 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +4.3693e+06 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            -3278.37 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            +3236.46 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            +320678 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -309.344 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +0.000468526 * (b.wall_temperature_waterwall[t, 7]*b.flowrate_coal_raw[t])**2 \
            +4.7235e-05 * (b.wall_temperature_waterwall[t, 8]*b.flowrate_coal_raw[t])**2 \
            +4052.08 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            -4222.33 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            +0.000904438 * (b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t])**2 \
            +27.4312 * (b.flowrate_coal_raw[t]*b.SR[t])**3)',
      'pl': '(-1166.56 * b.wall_temperature_waterwall[t, 1] \
            -675.095 * b.wall_temperature_waterwall[t, 2] \
            +2514.51 * b.wall_temperature_waterwall[t, 3] \
            -983.723 * b.wall_temperature_waterwall[t, 4] \
            +2330.69 * b.wall_temperature_waterwall[t, 5] \
            +362.806 * b.wall_temperature_waterwall[t, 6] \
            -7375.6 * b.wall_temperature_waterwall[t, 7] \
            -4202.08 * b.wall_temperature_waterwall[t, 8] \
            +1141.48 * b.wall_temperature_waterwall[t, 9] \
            +8484.16 * b.wall_temperature_waterwall[t, 10] \
            +5905.73 * b.wall_temperature_waterwall[t, 11] \
            +7386.94 * b.wall_temperature_waterwall[t, 12] \
            +11007.4 * b.wall_temperature_waterwall[t, 13] \
            -706.412 * b.wall_temperature_waterwall[t, 14] \
            +189001 * b.wall_temperature_platen[t] \
            -663.012 * b.wall_temperature_roof[t] \
            +3.37318e+06 * b.flowrate_coal_raw[t] \
            -3.87781e+07 * b.mf_H2O_coal_raw[t] \
            -7.55876e+06 * b.SR[t] \
            +5.36976e+08 * b.SR_lf[t] \
            -24912.5 * b.secondary_air_inlet.temperature[t] \
            -1.62488e+06 * b.ratio_PA2coal[t] \
            +191925 * log(b.wall_temperature_waterwall[t, 1]) \
            +280264 * log(b.wall_temperature_waterwall[t, 5]) \
            +5.72596e+06 * log(b.wall_temperature_waterwall[t, 7]) \
            -2.47873e+06 * log(b.wall_temperature_waterwall[t, 10]) \
            -2.90641e+06 * log(b.wall_temperature_waterwall[t, 12]) \
            -8.91549e+06 * log(b.wall_temperature_waterwall[t, 13]) \
            -4.73042e+07 * log(b.wall_temperature_platen[t]) \
            -6.16404e+06 * log(b.flowrate_coal_raw[t]) \
            +699130 * log(b.mf_H2O_coal_raw[t]) \
            -5.10172e+06 * log(b.SR[t]) \
            -2.9072e+08 * log(b.SR_lf[t]) \
            -9.40002e+07 * exp(b.SR_lf[t]) \
            -95.6481 * b.wall_temperature_platen[t]**2 \
            +6.12999 * b.wall_temperature_roof[t]**2 \
            -2066.95 * b.flowrate_coal_raw[t]**2 \
            -83.1843 * b.flowrate_coal_raw[t]**3 \
            -0.554054 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 13] \
            -6.63217 * b.wall_temperature_waterwall[t, 1]*b.flowrate_coal_raw[t] \
            +643.644 * b.wall_temperature_waterwall[t, 1]*b.ratio_PA2coal[t] \
            +2.74375 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 9] \
            -900.098 * b.wall_temperature_waterwall[t, 2]*b.SR[t] \
            +0.248714 * b.wall_temperature_waterwall[t, 2]*b.secondary_air_inlet.temperature[t] \
            -2.85519 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 9] \
            -2.73086 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 11] \
            +1241.63 * b.wall_temperature_waterwall[t, 3]*b.SR[t] \
            +1.78941 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 11] \
            +1.17457 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 12] \
            +0.870737 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 13] \
            -2873.6 * b.wall_temperature_waterwall[t, 5]*b.mf_H2O_coal_raw[t] \
            -5.59825 * b.wall_temperature_waterwall[t, 5]*b.secondary_air_inlet.temperature[t] \
            +1.62361 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_waterwall[t, 9] \
            -218.918 * b.wall_temperature_waterwall[t, 7]*b.flowrate_coal_raw[t] \
            +2919.25 * b.wall_temperature_waterwall[t, 7]*b.mf_H2O_coal_raw[t] \
            +5.36545 * b.wall_temperature_waterwall[t, 8]*b.wall_temperature_waterwall[t, 14] \
            +3158.34 * b.wall_temperature_waterwall[t, 8]*b.mf_H2O_coal_raw[t] \
            +322.653 * b.wall_temperature_waterwall[t, 8]*b.SR[t] \
            -1.50986 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_roof[t] \
            -2.46079 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 11] \
            -3.55384 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 14] \
            +23.7953 * b.wall_temperature_waterwall[t, 10]*b.flowrate_coal_raw[t] \
            -4.9544 * b.wall_temperature_waterwall[t, 11]*b.wall_temperature_waterwall[t, 14] \
            -2.72784 * b.wall_temperature_waterwall[t, 12]*b.wall_temperature_roof[t] \
            -1658.9 * b.wall_temperature_waterwall[t, 12]*b.mf_H2O_coal_raw[t] \
            +152.683 * b.wall_temperature_waterwall[t, 12]*b.SR[t] \
            +1.7608 * b.wall_temperature_waterwall[t, 13]*b.wall_temperature_waterwall[t, 14] \
            -36.076 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +6.70234 * b.wall_temperature_waterwall[t, 13]*b.secondary_air_inlet.temperature[t] \
            +7.0803 * b.wall_temperature_waterwall[t, 14]*b.secondary_air_inlet.temperature[t] \
            -623.313 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            +6995.08 * b.wall_temperature_platen[t]*b.mf_H2O_coal_raw[t] \
            -7698.95 * b.wall_temperature_platen[t]*b.SR[t] \
            -2378.81 * b.wall_temperature_roof[t]*b.SR[t] \
            -38.7111 * b.wall_temperature_roof[t]*b.ratio_PA2coal[t] \
            -1.97965e+06 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            +303198 * b.flowrate_coal_raw[t]*b.SR[t] \
            +228298 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +655.481 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -14129.1 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +2.62538e+07 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            -22257.2 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            +22108.4 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            +2.40177e+06 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -2276.36 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +0.00398202 * (b.wall_temperature_waterwall[t, 7]*b.flowrate_coal_raw[t])**2 \
            +0.000472314 * (b.wall_temperature_waterwall[t, 11]*b.flowrate_coal_raw[t])**2 \
            +0.513637 * (b.wall_temperature_waterwall[t, 11]*b.SR[t])**2 \
            +24092.9 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            -23924.9 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            +0.00567433 * (b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t])**2 \
            +158.634 * (b.flowrate_coal_raw[t]*b.SR[t])**3)',
    'roof': '(21726.1 * b.wall_temperature_waterwall[t, 1] \
            -594.784 * b.wall_temperature_waterwall[t, 2] \
            +262.963 * b.wall_temperature_waterwall[t, 3] \
            -63.3506 * b.wall_temperature_waterwall[t, 5] \
            +135.253 * b.wall_temperature_waterwall[t, 6] \
            -1427.81 * b.wall_temperature_waterwall[t, 7] \
            -427.891 * b.wall_temperature_waterwall[t, 8] \
            +113.322 * b.wall_temperature_waterwall[t, 9] \
            +1368.63 * b.wall_temperature_waterwall[t, 10] \
            +66.8422 * b.wall_temperature_waterwall[t, 11] \
            -16289.4 * b.wall_temperature_waterwall[t, 12] \
            +1417.92 * b.wall_temperature_waterwall[t, 13] \
            +1512.89 * b.wall_temperature_waterwall[t, 14] \
            -30229.9 * b.wall_temperature_platen[t] \
            +13784 * b.wall_temperature_roof[t] \
            +243631 * b.flowrate_coal_raw[t] \
            -5.91623e+06 * b.mf_H2O_coal_raw[t] \
            -1.93078e+06 * b.SR[t] \
            -1.34208e+06 * b.SR_lf[t] \
            -2139.39 * b.secondary_air_inlet.temperature[t] \
            -216815 * b.ratio_PA2coal[t] \
            -7.73099e+06 * log(b.wall_temperature_waterwall[t, 1]) \
            +334378 * log(b.wall_temperature_waterwall[t, 2]) \
            +78052.6 * log(b.wall_temperature_waterwall[t, 5]) \
            +556781 * log(b.wall_temperature_waterwall[t, 7]) \
            +5.57566e+06 * log(b.wall_temperature_waterwall[t, 12]) \
            -770763 * log(b.wall_temperature_waterwall[t, 13]) \
            -1.04818e+06 * log(b.wall_temperature_waterwall[t, 14]) \
            +9.08822e+06 * log(b.wall_temperature_platen[t]) \
            -5.07528e+06 * log(b.wall_temperature_roof[t]) \
            -775440 * log(b.flowrate_coal_raw[t]) \
            +91240.4 * log(b.mf_H2O_coal_raw[t]) \
            -354870 * log(b.SR[t]) \
            -7.57492 * b.wall_temperature_waterwall[t, 1]**2 \
            +5.8658 * b.wall_temperature_waterwall[t, 12]**2 \
            +14.7655 * b.wall_temperature_platen[t]**2 \
            +1803.07 * b.flowrate_coal_raw[t]**2 \
            -0.0065371 * b.wall_temperature_roof[t]**3 \
            -25.4959 * b.flowrate_coal_raw[t]**3 \
            -0.335457 * b.wall_temperature_waterwall[t, 1]*b.wall_temperature_waterwall[t, 13] \
            +91.6571 * b.wall_temperature_waterwall[t, 1]*b.ratio_PA2coal[t] \
            +0.228331 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 9] \
            -0.418731 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 9] \
            +0.321897 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_waterwall[t, 12] \
            -0.215099 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_roof[t] \
            +107.049 * b.wall_temperature_waterwall[t, 4]*b.mf_H2O_coal_raw[t] \
            -0.076551 * b.wall_temperature_waterwall[t, 6]*b.wall_temperature_waterwall[t, 14] \
            -0.0291378 * b.wall_temperature_waterwall[t, 6]*b.wall_temperature_roof[t] \
            +0.396889 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_waterwall[t, 9] \
            +0.601134 * b.wall_temperature_waterwall[t, 7]*b.wall_temperature_waterwall[t, 14] \
            +0.576428 * b.wall_temperature_waterwall[t, 8]*b.wall_temperature_waterwall[t, 14] \
            +0.0946749 * b.wall_temperature_waterwall[t, 8]*b.wall_temperature_platen[t] \
            -0.153844 * b.wall_temperature_waterwall[t, 9]*b.wall_temperature_roof[t] \
            -0.408191 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 11] \
            -0.631577 * b.wall_temperature_waterwall[t, 10]*b.wall_temperature_waterwall[t, 14] \
            +4.26333 * b.wall_temperature_waterwall[t, 10]*b.flowrate_coal_raw[t] \
            -0.909089 * b.wall_temperature_waterwall[t, 10]*b.secondary_air_inlet.temperature[t] \
            +305.541 * b.wall_temperature_waterwall[t, 11]*b.SR[t] \
            +0.37501 * b.wall_temperature_waterwall[t, 13]*b.wall_temperature_waterwall[t, 14] \
            -5.55432 * b.wall_temperature_waterwall[t, 13]*b.flowrate_coal_raw[t] \
            +0.459927 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -362.269 * b.wall_temperature_platen[t]*b.SR[t] \
            -11.4827 * b.wall_temperature_roof[t]*b.flowrate_coal_raw[t] \
            -542.021 * b.wall_temperature_roof[t]*b.SR[t] \
            -20.7479 * b.wall_temperature_roof[t]*b.ratio_PA2coal[t] \
            -251820 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            +87360.4 * b.flowrate_coal_raw[t]*b.SR[t] \
            +29535.7 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +121.994 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -2034.64 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            +4.68421e+06 * b.mf_H2O_coal_raw[t]*b.SR[t] \
            -3289.59 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            +2922.8 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            +346073 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            -327.061 * b.secondary_air_inlet.temperature[t]*b.ratio_PA2coal[t] \
            +3924.73 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            -4066.05 * (b.flowrate_coal_raw[t]*b.SR[t])**2 \
            +27.2454 * (b.flowrate_coal_raw[t]*b.SR[t])**3)',
   'flyash': '(exp(-0.00622998 * b.wall_temperature_waterwall[t, 1] \
            +0.000753772 * b.wall_temperature_waterwall[t, 2] \
            -0.000120601 * b.wall_temperature_waterwall[t, 3] \
            -0.000451688 * b.wall_temperature_waterwall[t, 8] \
            -0.000571427 * b.wall_temperature_waterwall[t, 9] \
            -0.00172271 * b.wall_temperature_waterwall[t, 10] \
            -0.00232964 * b.wall_temperature_waterwall[t, 11] \
            -0.000550575 * b.wall_temperature_waterwall[t, 14] \
            -0.0020169 * b.wall_temperature_platen[t] \
            +1.27841 * b.flowrate_coal_raw[t] \
            -2.31661 * b.mf_H2O_coal_raw[t] \
            +144.922 * b.SR[t] \
            -689.253 * b.SR_lf[t] \
            +0.00445568 * b.secondary_air_inlet.temperature[t] \
            +4.16487 * log(b.wall_temperature_waterwall[t, 1]) \
            +0.978169 * log(b.wall_temperature_waterwall[t, 2]) \
            -8.20549 * log(b.flowrate_coal_raw[t]) \
            -106.113 * log(b.SR[t]) \
            +354.404 * log(b.SR_lf[t]) \
            +41.4263 * log(b.secondary_air_inlet.temperature[t]) \
            -7.96304 * exp(b.SR[t]) \
            +123.098 * exp(b.SR_lf[t]) \
            -0.0239891 * b.flowrate_coal_raw[t]**2 \
            +0.000136547 * b.flowrate_coal_raw[t]**3 \
            -0.00161642 * b.wall_temperature_waterwall[t, 2]*b.SR[t] \
            -1.68072e-08 * b.wall_temperature_waterwall[t, 4]*b.wall_temperature_waterwall[t, 6] \
            -1.21607e-07 * b.wall_temperature_waterwall[t, 5]*b.wall_temperature_waterwall[t, 12] \
            -2.29202e-05 * b.wall_temperature_waterwall[t, 7]*b.ratio_PA2coal[t] \
            +1.62909e-05 * b.wall_temperature_waterwall[t, 8]*b.flowrate_coal_raw[t] \
            +1.41773e-05 * b.wall_temperature_waterwall[t, 9]*b.flowrate_coal_raw[t] \
            +9.95354e-05 * b.wall_temperature_waterwall[t, 10]*b.flowrate_coal_raw[t] \
            +2.11008e-06 * b.wall_temperature_waterwall[t, 11]*b.wall_temperature_platen[t] \
            +2.50283e-05 * b.wall_temperature_waterwall[t, 11]*b.flowrate_coal_raw[t] \
            +0.00279471 * b.wall_temperature_waterwall[t, 14]*b.mf_H2O_coal_raw[t] \
            +1.07429e-05 * b.wall_temperature_platen[t]*b.flowrate_coal_raw[t] \
            -0.29238 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -0.276297 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            -4.82612e-05 * b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            +0.00955259 * b.mf_H2O_coal_raw[t]*b.secondary_air_inlet.temperature[t] \
            -0.100695 * b.SR[t]*b.secondary_air_inlet.temperature[t] \
            -0.00535995 * b.SR_lf[t]*b.secondary_air_inlet.temperature[t] \
            -4.13947e-06 * (b.wall_temperature_waterwall[t, 4]*b.mf_H2O_coal_raw[t])**2 \
            -9.92196e-10 * (b.wall_temperature_waterwall[t, 10]*b.flowrate_coal_raw[t])**2 \
            +0.00992987 * (b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t])**2 \
            +0.00443128 * (b.flowrate_coal_raw[t]*b.SR_lf[t])**2 \
            +4.68424e-09 * (b.flowrate_coal_raw[t]*b.secondary_air_inlet.temperature[t])**2 \
            +2.68687e-05 * (b.SR[t]*b.secondary_air_inlet.temperature[t])**2))',
     'NOx': '(2.3602 * b.wall_temperature_waterwall[t, 1] \
            -0.63586 * b.wall_temperature_waterwall[t, 2] \
            -0.419591 * b.wall_temperature_waterwall[t, 3] \
            -0.79299 * b.wall_temperature_waterwall[t, 4] \
            +2.1729 * b.wall_temperature_waterwall[t, 5] \
            +0.548457 * b.wall_temperature_waterwall[t, 6] \
            -0.210731 * b.wall_temperature_waterwall[t, 7] \
            +0.0156876 * b.wall_temperature_waterwall[t, 8] \
            -30.1708 * b.wall_temperature_waterwall[t, 11] \
            +1.24455 * b.wall_temperature_waterwall[t, 12] \
            -1.43424 * b.wall_temperature_waterwall[t, 13] \
            -36.0068 * b.wall_temperature_roof[t] \
            -719.511 * b.flowrate_coal_raw[t] \
            +829.462 * b.mf_H2O_coal_raw[t] \
            +2524.64 * b.SR[t] \
            +858556 * b.SR_lf[t] \
            +0.931998 * b.secondary_air_inlet.temperature[t] \
            -3035.01 * b.ratio_PA2coal[t] \
            -41.3988 * log(b.wall_temperature_waterwall[t, 1]) \
            +345.771 * log(b.wall_temperature_waterwall[t, 4]) \
            -475.665 * log(b.wall_temperature_waterwall[t, 5]) \
            +10555.4 * log(b.wall_temperature_waterwall[t, 11]) \
            +1477.9 * log(b.wall_temperature_waterwall[t, 13]) \
            +13202 * log(b.wall_temperature_roof[t]) \
            +410.98 * log(b.flowrate_coal_raw[t]) \
            -448668 * log(b.SR_lf[t]) \
            -574355 * exp(b.SR_lf[t]) \
            +54.594 * exp(b.ratio_PA2coal[t]) \
            +0.0116597 * b.wall_temperature_waterwall[t, 11]**2 \
            +0.0127286 * b.wall_temperature_roof[t]**2 \
            +9.3546 * b.flowrate_coal_raw[t]**2 \
            +573633 * b.SR_lf[t]**2 \
            -0.0385928 * b.flowrate_coal_raw[t]**3 \
            -1.91667 * b.wall_temperature_waterwall[t, 1]*b.SR_lf[t] \
            -0.165436 * b.wall_temperature_waterwall[t, 1]*b.ratio_PA2coal[t] \
            +0.000911488 * b.wall_temperature_waterwall[t, 2]*b.wall_temperature_waterwall[t, 5] \
            +0.000553343 * b.wall_temperature_waterwall[t, 3]*b.wall_temperature_roof[t] \
            +0.000510379 * b.wall_temperature_waterwall[t, 4]*b.secondary_air_inlet.temperature[t] \
            -0.00756922 * b.wall_temperature_waterwall[t, 5]*b.flowrate_coal_raw[t] \
            -0.975577 * b.wall_temperature_waterwall[t, 5]*b.mf_H2O_coal_raw[t] \
            -1.41217 * b.wall_temperature_waterwall[t, 5]*b.SR_lf[t] \
            -0.157395 * b.wall_temperature_waterwall[t, 5]*b.ratio_PA2coal[t] \
            -0.000771437 * b.wall_temperature_waterwall[t, 6]*b.wall_temperature_waterwall[t, 11] \
            +0.00671823 * b.wall_temperature_waterwall[t, 7]*b.flowrate_coal_raw[t] \
            -0.00104727 * b.wall_temperature_waterwall[t, 11]*b.wall_temperature_waterwall[t, 12] \
            -0.519887 * b.wall_temperature_waterwall[t, 13]*b.SR[t] \
            -0.00189109 * b.wall_temperature_roof[t]*b.secondary_air_inlet.temperature[t] \
            -11.3429 * b.flowrate_coal_raw[t]*b.mf_H2O_coal_raw[t] \
            -7.93051 * b.flowrate_coal_raw[t]*b.SR[t] \
            +585.026 * b.flowrate_coal_raw[t]*b.SR_lf[t] \
            +20.9453 * b.flowrate_coal_raw[t]*b.ratio_PA2coal[t] \
            -2200.27 * b.SR[t]*b.SR_lf[t] \
            +3210.17 * b.SR_lf[t]*b.ratio_PA2coal[t] \
            +0.00155857 * (b.wall_temperature_waterwall[t, 7]*b.mf_H2O_coal_raw[t])**2 \
            -0.00034074 * (b.wall_temperature_waterwall[t, 12]*b.SR_lf[t])**2 \
            -5.59723 * (b.flowrate_coal_raw[t]*b.SR_lf[t])**2 \
            -0.0798057 * (b.flowrate_coal_raw[t]*b.ratio_PA2coal[t])**2 \
            -40.4625 * (b.SR_lf[t]*b.ratio_PA2coal[t])**3)'
        }