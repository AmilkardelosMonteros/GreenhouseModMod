
from sympy import symbols
from .struct_var import Struct

mt, mg, m, C, s, W, mg_CO2, J, g, mol_CH2O = symbols('mt mg m C s W mg_CO2 J g mol_CH2O')

mt, mg, m, C, s, W, mg_CO2, J, Pa, kg_water, kg, K, ppm, m_cover, kg_air = symbols('mt mg m C s W mg_CO2 J Pa kg_water kg K ppm m_cover kg_air')  # Symbolic use of base phisical units

mt, mg, m, C, s, W, mg_CO2, J, Pa, kg_water, kg, K, ppm, kmol, kg_air, kg_vapour, mxn = symbols('mt mg m C s W mg_CO2 J Pa kg_water kg K ppm kmol kg_air kg_vapour mxn')  # Symbolic use of base phisical units
ok = 'OK'
# from .constants import ALPHA, BETA, GAMMA, DELTA, EPSIL, ETA, LAMB, RHO, TAU, NU, PHI, PSI, OMEGA
#theta = np.array([3000, 20, 7.2*(10**4)]) # psi2 = 7.2*(10**4)
nrec = 1

################## Constants ##################
OTHER_CONSTANTS = {     
    ################## other constants ################## 
    'etagas':      Struct(typ='Cnts', varid='etagas', prn=r'$\eta_{gas}$',
                    desc="Energy efficiency of natural gas", units=1, val=35.26, ok='checar unidades'),  
    'qgas':    Struct(typ='Cnts', varid='qgas', prn=r'$q_{gas}$',
                    desc="Cost of natural gas", units=1, val=2.45, ok='checar unidades'),      
    'q_co2_ext': Struct(typ='Cnts', varid='q_co2_ext', prn=r'$\q_{CO_2}_{ext}$',
                    desc="Cost of the gas from the external source", units=mxn * kg**-1, val=3.5, ok='tomado de la tesis'),     
    'T_cal':     Struct(typ='Cnts', varid='T_cal', prn=r'$T_{cal}$',
                    desc="Maximum temperature of the boiler", units=1, val=95, ok='falta las unidades'),           
    'sigma':     Struct(typ='Cnts', varid='sigma', prn=r'$\sigma$',
                    desc="Stefan-Boltzmann constant", units=W * m**-2 * K**-4, val=5.670e-8, ok=ok), 
    'etadrain':  Struct(typ='Cnts', varid='etadrain', prn=r'$\eta_{drain}$',
                    desc="Missing", units=1, val=30, ok='falta descripción y unidades'),
    'model_noise': Struct(val = MODEL_NOISE,ok = 'Controla si se agrega o no aleatoriedad al modelo')
}

COSTS = {
    'Qh2o': Struct(typ='State', varid='Qh2o', prn=r'$Q_{H2O}$',
                    desc="Water cost ", units=mxn * kg, val=0, rec=nrec, ok=ok),
    'Qgas': Struct(typ='State', varid='Qgas', prn=r'$Q_{Gas}$',
                    desc="Fuel cost (natural gas)", units=mxn * m**-2, val=0, rec=nrec, ok=ok), 
    'Qco2': Struct(typ='State', varid='Qco2', prn=r'$Q_{CO2}$',
                    desc="CO2 cost ", units=mxn * kg, val=0, rec=nrec, ok='revisar unidades')
}