from sympy import symbols
import numpy as np
from .struct_var import Struct

theta_p = np.array([0.7, 3.3, 0.25]) # theta nominal pdn
theta_c = np.array([3000, 20, 2.3e5]) # theta nominal clima

## Photosynthesis model
s, mol_CO2, mol_air, mol_phot, m, d, C, g, mol_O2, pa, ppm, MJ, n_f  = symbols('s mol_CO2 mol_air mol_phot m d C g mol_O2 pa ppm MJ n_f')
mu_mol_CO2 = 1e-6 * mol_CO2
mu_mol_phot = 1e-6 * mol_phot
mu_mol_O2 = 1e-6 * mol_O2
mg = 1e-3*g


LOCAL_CI_CONST = {     
    ################## local Ci_rhs constants ################## 
    'Ci': Struct(typ='State', varid='Ci', prn=r'$C_i$',\
                    desc="Intracellular CO2", units=ppm , val=410),
    'A': Struct(typ='State', varid='A', prn=r'$A$',\
           desc="Assimilation rate", units= g * (m**-2), val=15), 
}


INPUTS = {
        ################## Inputs Ci_rhs values ##################
        ## Inputs
        'C1': Struct( typ='State', varid='C1', prn=r'$C_1$',\
           desc="CO2 concentration in the greenhouse air", \
           units= mg * m**-3, val=738), 
        
        'RH': Struct(typ='State', varid='RH', prn=r'$RH$',\
           desc="Relative humidity percentage in the greenhouse air", \
           units=1, val=50),
        
        'T': Struct( typ='State', varid='T', prn=r'$T$',\
            desc="Greenhouse air temperature", units= C , val=20),
        
        'PAR': Struct( typ='State', varid='PAR', prn=r'$PAR$',\
            desc="PAR radiation", units=mu_mol_phot * (m**-2) * d**-1 , val=300.00)
}       


GLOBAL_CI_CONST = {
        ################## global Ci_rhs constants ##################
        ### Stomatal Resistance Calculation
        'k_Ag': Struct( typ='Cnts', varid='k_Ag', \
           desc="Constant for units transformation", \
           units= m**3 * g**-1 * s**-1 * mu_mol_CO2 * mol_air**-1, val=1),
        
        'r_m': Struct( typ='Cnts', varid='r_m', \
           desc="minimal stomatal resistance", \
           units= s * m**-1, val=100),
        
        'C_ev1': Struct( typ='Cnts', varid='C_ev1', \
           desc="Constant in the formula of f_R", \
           units= mu_mol_phot * (m**-2) * d**-1, val=4.3),
        
        'C_ev2': Struct( typ='Cnts', varid='C_ev2', \
           desc="Constant in the formula of f_R", \
           units= mu_mol_phot * (m**-2) * d**-1 , val=0.54),
        
        'k_fc': Struct( typ='Cnts', varid='k_fc', \
           desc="Constant for units completation", \
           units= mu_mol_CO2 * mol_air**-1, val=1),
        
        'C_ev3d': Struct( typ='Cnts', varid='C_ev3d', \
           desc="Constant in the formula of f_C", \
           units= mol_air * mu_mol_CO2**-1, val=6.1e-7),
        
        'C_ev3n': Struct( typ='Cnts', varid='C_ev3n', \
           desc="Constant in the formula of f_C", \
           units= mol_air * mu_mol_CO2**-1, val=1.1e-11),
        
        'S': Struct( typ='Cnts', varid='S', \
           desc="Constant in the formula of Sr", \
           units= m**2 * d * mu_mol_phot**-1, val=-1),
        
        'Rs': Struct( typ='Cnts', varid='Rs', \
           desc="Radiation setpoint to switch day and night", \
           units= mu_mol_phot * (m**-2) * d**-1, val=5),
        
        'C_ev4d': Struct( typ='Cnts', varid='C_ev4d', \
           desc="Constant in the formula of f_C", \
           units= pa**-1, val=4.3e-6),
        
        'C_ev4n': Struct( typ='Cnts', varid='C_ev4n', \
           desc="Constant in the formula of f_C", \
           units= pa**-1, val=5.2e-6),
        
        ## CO2 absorption
        'ks': Struct( typ='Cnts', varid='ks', \
           desc="Stomatal ratio", \
           units= 1, val=0.5),
        
        'Rb': Struct( typ='Cnts', varid='Rb', \
           desc="Stomatal resistance of the canopy boundary layer", \
           units= s * m**-1, val=711),
        
        ## Assimilates
        'k_d': Struct( typ='Cnts', varid='k_d', \
           desc="factor to transform s**-1 into d**-1", units=1, val=1),
        
        'k_T': Struct( typ='Cnts', varid='k_T', \
           desc="Auxiliary constant to add temperature units", units= C, val=1.0),
        
        'k_JV': Struct( typ='Cnts', varid='k_JV', \
           desc="Auxiliary constant which transforms the units of the electron transport rate, J to those of the maximum Rubisco rate, V_cmax", \
           units= mu_mol_CO2 * mu_mol_phot**-1, val=1.0),
        
        'fc': Struct( typ='Cnts', varid='fc', \
           desc="Factor to transform mu-mols_CO2/sec to grms_CH20/day", \
           units= g * d * mu_mol_CO2**-1 , val=3.418181e-1), # 7.891414141414142e-6
        
        'phi': Struct( typ='Cnts', varid='phi', \
           desc="Ratio of oxigenation to carboxylation rates", \
           units= mu_mol_O2 * mu_mol_CO2**-1, val=2),
        
        'O_a': Struct( typ='Cnts', varid='O_a', \
           desc="O2 concentration in the enviroment", \
           units= mu_mol_O2 * mol_air**-1, val=210000),
        
        'V_cmax25': Struct( typ='Cnts', varid='V_cmax25', \
           desc="Maximum Rubisco Rate, per unit area", \
           units= mu_mol_CO2 * (m**-2) * d**-1, val=200),
        
        'Q10_Vcmax': Struct( typ='Cnts', varid='Q10_Vcmax', \
           desc="Temperatura response of Vcmax", \
           units=1, val=2.4), 
        
        'K_C25': Struct( typ='Cnts', varid='K_C25', \
           desc="Michaelis-Menten for CO2", \
           units= mu_mol_CO2 * mol_air**-1 , val=300),
        
        'Q10_KC': Struct(typ='Cnts', varid='Q10_KC', \
           desc="Temperatura response of Michaelis-Menten for CO2", \
           units=1, val=2.1),
        
        'K_O25': Struct( typ='Cnts', varid='K_O25', \
           desc="Michaelis-Menten for O2", \
           units= mu_mol_O2 * mol_air**-1 , val=3e5),
        
        'Q10_KO': Struct( typ='Cnts', varid='Q10_KO', \
           desc="Temperatura response of Michaelis-Menten for O2", \
           units=1, val=1.2),
        
        'tau_25': Struct( typ='Cnts', varid='tau_25', \
           desc="Specificity factor", \
           units=1 , val=2600),
        
        'Q10_tau': Struct( typ='Cnts', varid='Q10_tau', \
           desc="Temperatura response of specificity factor", \
           units=1, val=2.1), 
        
        'J_max': Struct( typ='Cnts', varid='J_max', \
           desc="Maximum electron transport rate", \
           units= mu_mol_phot * (m**-2) * d**-1, val=400),
        
        'ab': Struct( typ='Cnts', varid='ab', \
           desc="Leafs absorbance", \
           units=1 , val=0.85),
        
        'f': Struct( typ='Cnts', varid='f', \
           desc="Correction factor for the spectral quality of the light", \
           units=1 , val=0.15),
        
        'theta': Struct( typ='Cnts', varid='theta', \
           desc="Empirical factor", \
           units=1 , val=theta_c[0]),
}


STATEPARTIAL_Q = {     
    ################## StatePartial Q_rhs constants ##################
    'Q': Struct( typ='StatePartial', varid='Q', prn=r'$Q$',\
           desc="Weight of all fruits for plant", units= g, val=0.0),
        
    'm_k': Struct( typ='StatePartial', varid='m_k', prn=r'$m_k$',\
           desc="Simulation number of fruits harvested for plant", units= n_f, val=0.0),
        
    'n_k': Struct( typ='StatePartial', varid='n_k', prn=r'$n_k$',\
           desc="Number of fruits harvested for plant", units= n_f, val=0),

    'h_k': Struct( typ='StatePartial', varid='h_k', prn=r'$h_k$',\
           desc="Weight of all harvested fruits for plant", units= g, val=0.0),

    'Q_h': Struct( typ='StatePartial', varid='Q_h', prn=r'$H$',\
           desc="Accumulated weight of all harvested fruits for plant", units= g, val=0.0),

    'Y_sum': Struct(typ='StatePartial', varid='Y_sum', prn=r'$Y_{sum}$',\
           desc="Sum of all potentail growths", units= g/d**2, val=0.0)
}

GLOBAL_Q_CONST = {
            ### Constants, shared by all plants.  Shared Cnts cannot be local
    'k1_TF': Struct( typ='Cnts', varid='k1_TF', prn=r'$k1_TF$',\
           desc="Aux in function TF", units= MJ * m**-2 * d**-1, val=300.0),

    'k2_TF': Struct( typ='Cnts', varid='k2_TF', prn=r'$k2_TF$',\
           desc="Aux in function TF", units= C * d**-1, val=1.0)
}

LOCAL_Q_CONST = {
    ################## Local Q_rhs constants ##################
    'k3_TF':Struct( typ='Cnts', varid='k3_TF', prn=r'$k3_{TF}$',\
       desc="Aux in function TF", units= n_f * C**-1, val=1.0),
    'dw_ef':Struct( typ='Cnts', varid='dw_ef', prn=r'$dw_{efficacy}$',\
       desc="Constant in t_wg for fruits", units= 1, val=1.3),
    
    'dw_ef_veg':Struct( typ='Cnts', varid='dw_ef_veg', prn=r'$dw_{efficacy}$',\
       desc="Constant in t_wg for vegetative part", units= 1, val=1.15),
    'a_ef':Struct( typ='Cnts', varid='a_ef', prn=r'$a_{efficacy}$',\
       desc="Matching constant in remaining assimilates", units= 1/m**2, val=1.0),
    'C_t':Struct( typ='Cnts', varid='C_t', prn=r'$C_t$',\
       desc="Constant in Y_pot", units= C * d, val=131.0),
    'B':Struct( typ='Cnts', varid='B', prn=r'$B$',\
       desc="Constant in Y_pot", units= (C * d)**-1, val=0.017),
    'D':Struct( typ='Cnts', varid='D', prn=r'$D$',\
       desc="Constant in Y_pot", units= 1, val=0.011),
    'M':Struct( typ='Cnts', varid='M', prn=r'$M$',\
       desc="Constant in Y_pot", units= g, val=60.7),
    
    'a':Struct( typ='Cnts', varid='a', prn=r'$a$',\
       desc="Constant in Y_pot_veg", units= 1, val=theta_p[1]),
    
    'b':Struct( typ='Cnts', varid='b', prn=r'$b$',\
       desc="Constant in Y_pot_veg", units= 1, val=theta_p[2])
}



CONSTANTS = {**LOCAL_CI_CONST, **LOCAL_Q_CONST, **GLOBAL_Q_CONST, **STATEPARTIAL_Q, **GLOBAL_CI_CONST, **INPUTS}


