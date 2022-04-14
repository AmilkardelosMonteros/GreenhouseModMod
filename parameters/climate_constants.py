from sympy import symbols
from .struct_var import Struct

mt, mg, m, C, s, W, mg_CO2, J, g, mol_CH2O = symbols('mt mg m C s W mg_CO2 J g mol_CH2O')

mt, mg, m, C, s, W, mg_CO2, J, Pa, kg_water, kg, K, ppm, m_cover, kg_air = symbols('mt mg m C s W mg_CO2 J Pa kg_water kg K ppm m_cover kg_air')  # Symbolic use of base phisical units

mt, mg, m, C, s, W, mg_CO2, J, Pa, kg_water, kg, K, ppm, kmol, kg_air, kg_vapour, mxn = symbols('mt mg m C s W mg_CO2 J Pa kg_water kg K ppm kmol kg_air kg_vapour mxn')  # Symbolic use of base phisical units
ok = 'OK'
# from .constants import ALPHA, BETA, GAMMA, DELTA, EPSIL, ETA, LAMB, RHO, TAU, NU, PHI, PSI, OMEGA
#theta = np.array([3000, 20, 7.2*(10**4)]) # psi2 = 7.2*(10**4)
nrec = 10*24*60
MODEL_NOISE = False
mt = symbols('mt') #Minutos

################## Constants ##################
OTHER_CONSTANTS = {     
    ################## other constants ################## 
    'etagas':      Struct(typ='Cnts', varid='etagas', prn=r'$\eta_{gas}$',
                    desc="Energy efficiency of natural gas", units=1, val=35.26, ok='checar unidades'),  
    'qgas':    Struct(typ='Cnts', varid='qgas', prn=r'$q_{gas}$',
                    desc="Cost of natural gas", units=1, val=2.45, ok='checar unidades'),      
    'q_co2_ext': Struct(typ='Cnts', varid='q_co2_ext', prn=r'$\q_{CO_2}_{ext}$',
                    desc="", units=mxn * kg**-1, val=3.5, ok=ok),     # Costo del gas de la fuente externa lo tomamos al precio de la tesis 
    'T_cal':     Struct(typ='Cnts', varid='T_cal', prn=r'$T_{cal}$',
                    desc="Missing", units=1, val=95, ok='falta descripción y unidades'),          # Temperatura máxima de la caldera  
    'sigma':     Struct(typ='Cnts', varid='sigma', prn=r'$\sigma$',
                    desc="Stefan-Boltzmann constant", units=W * m**-2 * K**-4, val=5.670e-8, ok=ok), # Constante de Stefan-Boltzmann (W m−2)
    'etadrain':  Struct(typ='Cnts', varid='etadrain', prn=r'$\eta_{drain}$',
                    desc="Missing", units=1, val=30, ok='falta descripción y unidades'),
    'model_noise': Struct(val = MODEL_NOISE,ok = 'Controla si se agrega o no aleatoriedad al modelo'),
    'A_Mean': Struct( typ='State', varid='A_Mean', prn=r'$E[A]$',desc="Total mean assimilation rate", units= g * (m**-2), val=0,rec = 1440) ##Revisar

}


ALPHA ={
    ################## alpha ##################
    'alpha1': Struct(typ='Cnts', varid='alpha1', prn=r'$\alpha_1$',
                    desc="Heat capacity of one square meter of the canopy", units=J * K**-1 * m**-2, val=1.2e3, ok='Se regreso al valor original'), # Capacidad calórifica de un m^2 de dosel (theta[0])
    'alpha2': Struct(typ='Cnts', varid='alpha2', prn=r'$\alpha_2$',
                    desc="Global NIR absorption coefficient of the canopy", units=1, val=0.35, ok=ok), # Coeficiente global de absorción NIR del dosel
    'alpha3': Struct(typ='Cnts', varid='alpha3', prn=r'$\alpha_3$',
                    desc="Surface of the heating pipe", units=m**2*m**-2, val=0.3), # Superficiedelatuber ́ıadecalentamiento
    'alpha4': Struct(typ='Cnts', varid='alpha4', prn=r'$\alpha_4$',
                    desc="Convection heat exchange coefficient of canopy leaf to greenhouse air", units=W * m**-2 * K**-1, val=5, ok=ok), # Coeficiente de intercambio de calor por conveccio ́n de la hoja del dosel al aire del invernadero
    'alpha5': Struct(typ='Cnts', varid='alpha5', prn=r'$\alpha_5$',
                    desc="Specific heat capacity of greenhouse air", units=J * K**-1 * kg**-1, val=1e3, ok=ok), # Capacidadcalor ́ıficaespecificadelaire del invernadero
    'alpha6': Struct(typ='Cnts', varid='alpha6', prn=r'$\alpha_6$',
                    desc="Greenhouse floor surface area", units=m**2, val=1e4, ok=ok), # Área de la superficie del piso del invernadero
    'alpha7': Struct(typ='Cnts', varid='alpha7', prn=r'$\alpha_7$',
                    desc="Global NIR absorption coefficient of the floor", units=1, val=0.5, ok=ok), # Coeficiente global de absorcio ́n NIR del piso
    'alpha8': Struct(typ='Cnts', varid='alpha8', prn=r'$\alpha_8$',
                    desc="PAR absorption coefficient of the cover", units=1, val=1, ok='no dan el valor'), # Coeficiente de absorci ́on PAR de la cubierta # En el artículo no dan el valor
    'alpha9': Struct(typ='Cnts', varid='alpha9', prn=r'$\alpha_9$',
                    desc="NIR absorption coefficient of the cover", units=1, val=1, ok='no dan el valor')
}


BETA = {
    ################## beta ##################
    'beta1': Struct(typ='Cnts', varid='beta1', prn=r'$\beta_1$',
                    desc="Canopy extinction coefficient for PAR radiation", units=1, val=0.7, ok=ok),
    'beta2': Struct(typ='Cnts', varid='beta2', prn=r'$\beta_2$',
                    desc="Extinction coefficient for PAR radiation reflected from the floor to the canopy", units=1, val=0.7, ok=ok), 
    'beta3': Struct(typ='Cnts', varid='beta3', prn=r'$\beta_3$',
                    desc="Canopy extinction coefficient for NIR radiation", units=1, val=0.27, ok=ok)
}


GAMMA = {
    ################## gamma ##################
    'gamma':  Struct(typ='Cnts', varid='gamma', prn=r'$\gamma$',
                    desc="Psychometric constan", units=Pa * K**-1, val=65.8, ok=ok),  # Constante psicrom ́etrica #ok 
    'gamma1': Struct(typ='Cnts', varid='gamma1', prn=r'$\gamma_1$',
                    desc="Length of the heating pipe", units=m * m**-2, val=1.25, ok='ok, usé el valor de Texas'), # Longitud de la tubería de calentamiento (Almería)
    'gamma2': Struct(typ='Cnts', varid='gamma2', prn=r'$\gamma_2$',
                    desc="Latent heat of water evaporation", units=J * kg_water**-1, val=2.45e6, ok=ok), # Calor latente de evaporaci ́on del agua #ok
    'gamma3': Struct(typ='Cnts', varid='gamma3', prn=r'$\gamma_3$',
                    desc="Strength of boundary layer of canopy for vapor transport", units=s * m**-1, val=275, ok=ok), # Resistencia de la capa l ́ımite del dosel para transporte de vapor # ok
    'gamma4': Struct(typ='Cnts', varid='gamma4', prn=r'$\gamma_4$',
                    desc="Minimum stomatal resistance of the canopy", units=s * m**-1, val=82.0, ok=ok), # Resistenciaestom ́aticam ́ınimadeldosel # ok
    'gamma5': Struct(typ='Cnts', varid='gamma5', prn=r'$\gamma_5$',
                    desc="Slope of the differentiable switch for the stomatal resistance model", units=m * W**-2, val=-1, ok=ok)
}


DELTA = {
    ################## delta ##################
    'delta1': Struct(typ='Cnts', varid='delta1', prn=r'$\delta_1$',
                    desc="Radiation above the canopy that defines sunrise and sunset", units=W * m**-2, val=5, ok=ok), # Radiación por encima del dosel que define el amanecer y la puesta de sol # ok
    'delta2': Struct(typ='Cnts', varid='delta2', prn=r'$\delta_2$',
                    desc="Empirically determined parameter", units=W * m**-2, val=4.3, ok=ok), # Parámetro determinado empíricamente # ok
    'delta3': Struct(typ='Cnts', varid='delta3', prn=r'$\delta_3$',
                    desc="Empirically determined parameter", units=W * m**-2, val=0.54, ok=ok), # Parámetro determinado empíricamente # ok
    'delta4': Struct(typ='Cnts', varid='delta4', prn=r'$\delta_4$',
                    desc="Coefficient of the CO2 transpiration in the day", units=ppm**-2, val=6.1e-7, ok=ok), 
    'delta5': Struct(typ='Cnts', varid='delta5', prn=r'$\delta_5$',
                    desc="Coefficient of the CO2 transpiration in the night", units=ppm**-2, val=1.1e-11, ok=ok), 
    'delta6': Struct(typ='Cnts', varid='delta6', prn=r'$\delta_6$',
                    desc="Coefficient of the vapour pressure in the day", units=Pa**-2, val=4.3e-6, ok=ok),   
    'delta7': Struct(typ='Cnts', varid='delta7', prn=r'$\delta_7$',
                    desc="Coefficient of the vapour pressure in the night", units=Pa**-2, val=5.2e-6, ok=ok)
}


EPSIL = {
    ################## epsilon ##################
    'epsil1': Struct(typ='Cnts', varid='epsil1', prn=r'$\epsilon_1$',
                    desc="FIR emission coefficient of the heating pipe", units=1, val=0.88, ok=ok), # Coeficiente de emisión FIR de la tubería de calentamiento # ok 
    'epsil2': Struct(typ='Cnts', varid='epsil2', prn=r'$\epsilon_2$',
                    desc="Canopy FIR emission coefficient", units=1, val=1, ok=ok), # Coeficiente de emisión FIR del dosel # ok
    'epsil3': Struct(typ='Cnts', varid='epsil3', prn=r'$\epsilon_3$',
                    desc="Sky FIR emission coefficient", units=1, val=1, ok=ok), # Coeficiente de emisión FIR del cielo # ok
    'epsil4': Struct(typ='Cnts', varid='epsil4', prn=r'$\epsilon_4$',
                    desc="Floor FIR emission coefficient", units=1, val=1, ok=ok), # Coeficiente de emisión FIR del piso # ok
    'epsil5': Struct(typ='Cnts', varid='epsil5', prn=r'$\epsilon_5$',
                    desc="Thermal screen FIR emission coefficient", units=1, val=1, ok='?'), # Coeficiente de emisión FIR de la pantalla térmica
    'epsil6': Struct(typ='Cnts', varid='epsil6', prn=r'$\epsilon_6$',
                    desc="External cover FIR emission coefficient", units=1, val=0.44, ok='ok,usé el valor de Texas')
}


ETA = {
    ################## eta ##################
    'eta1':  Struct(typ='Cnts', varid='eta1', prn=r'$\eta_1$',
                    desc="Proportion of global radiation that is absorbed by greenhouse building elements", units=1, val=0.1, ok=ok),  # Proporción de la radiación global que es absorbida por los elementos de construcción del invernadero # ok
    'eta2':  Struct(typ='Cnts', varid='eta2', prn=r'$\eta_2$',
                    desc="Ratio between PAR radiation and external global radiation", units=1, val=0.5, ok=ok),  # Razón entre la radiación PAR y la radiación global externa ¿0.5?
    'eta3':  Struct(typ='Cnts', varid='eta3', prn=r'$\eta_3$',
                    desc="Ratio between NIR radiation and global external radiation", units=1, val=0.5, ok=ok),  # Razón entre la radiación NIR y la radiación global externa # ok 
    'eta4':  Struct(typ='Cnts', varid='eta4', prn=r'$\eta_4$',
                    desc="Conversion factor for CO2 of mg*m**−3 to ppm", units=ppm * mg**-1 * m**3, val=0.554, ok=ok),  # Factor de conversión de mg m−3 CO2 a ppm # ok 
    'eta5':  Struct(typ='Cnts', varid='eta5', prn=r'$\eta_5$',
                    desc="Fan-pad system efficiency", units=1, val=0.5, ok=ok),  # Eficiencia del sistema de ventilador-almohadilla # no da el valor en el articulo
    'eta6':  Struct(typ='Cnts', varid='eta6', prn=r'$\eta_6$',
                    desc="Ventilation power reduction factor", units=m**3 * m**-2 * s**-1, val=1, ok='Falta valor'),  # Factor de reduccio ́n de la potencia de ventilación # Falta valor
    'eta7':  Struct(typ='Cnts', varid='eta7', prn=r'$\eta_7$',
                    desc="Ratio between ceiling ventilation area and total ventilation area", units=1, val=0.5, ok='no dan valor en el artículo'),  # Razón entre el área de ventilación en el techo y el  área de ventilación total  # no da el valor en el articulo
    'eta8':  Struct(typ='Cnts', varid='eta8', prn=r'$\eta_8$',
                    desc="Ratio between ceiling and total ventilation area, if there is no chimney effect", units=1, val=0.9, ok=ok),  # Razón entre el área de ventilación techo y total, si no hay efecto de chimenea # ok
    'eta9':  Struct(typ='Cnts', varid='eta8', prn=r'$\eta_9$',
                    desc="", units=1, val=0, ok='No esta en el código'),  # Razón entre el área de ventilación lateral y el área de ventilación total # no hay eta9
    'eta10': Struct(typ='Cnts', varid='eta10', prn=r'$\eta_{10}$',
                    desc="Shadow effect on the discharge coefficient", units=1, val=0, ok='Falta valor, en los ejemplos del artículo no se considera'), # Efecto de la sombra sobre el coeficiente de descarga # Falta valor
    'eta11': Struct(typ='Cnts', varid='eta11', prn=r'$\eta_{11}$',
                    desc="Effect of shadow on the global wind pressure coefficient", units=1, val=0, ok='falta valor'), # Efecto de la sombra sobre el coeficiente de presión global del viento # Falta valor, aunque en los ejemplos del artículo no se considera
    'eta12': Struct(typ='Cnts', varid='eta12', prn=r'$\eta_{12}$',
                    desc="Amount of vapor that is released when a joule of sensible energy is produced by the direct air heater", units=kg_vapour * J**-1, val=4.43e-8, ok=ok), # Cantidad de vapor que es liberado cuando un joule de energía sensible es producido por el calentador de aire directo # ok
    'eta13': Struct(typ='Cnts', varid='eta13', prn=r'$\eta_{13}$',
                    desc="Amount of CO2 that is released when a joule of sensible energy is produced by the direct air heater", units=mg_CO2 * J**-1, val=0.057, ok=ok)
}

LAMB = {
    ################## lamb ##################
    'lamb1': Struct(typ='Cnts', varid='lamb1', prn=r'$\lambda_1$',
                    desc="Performance coefficient of the mechanical acceleration system", units=1, val=0, ok='Falta valor, en los ejemplos del artículo no se considera'), # Coeficiente de desempen ̃o del sistema de enfriamiento meca ́nico # Falta valor, aunque en los ejemplos del artículo no se considera
    'lamb2': Struct(typ='Cnts', varid='lamb2', prn=r'$\lambda_2$',
                    desc="Electrical capacity of the mechanical cooling system", units=W, val=0, ok='Falta valor, en los ejemplos del artículo no se considera'), # Capacidad el ́ectrica del sistema de enfriamiento meca ́nico # Falta valor, aunque en los ejemplos del artículo no se considera
    'lamb3': Struct(typ='Cnts', varid='lamb3', prn=r'$\lambda_3$',
                    desc="Convictive heat exchange coefficient between soil and greenhouse air", units=W * m**-2 * K**-1, val=1, ok='Falta valor, en los ejemplos del artículo no se considera'), # Coeficiente de intercambio de calor convictivo entre el suelo y el aire del invernadero # Falta valor, aunque en los ejemplos del artículo no se considera
    'lamb4': Struct(typ='Cnts', varid='lamb4', prn=r'$\lambda_4$',
                    desc="Heat capacity of direct air heater", units=W, val=5*(10**5), ok='Dr Antonio dio el valor'), # Capacidad calor ́ıfica del calentador de aire directo
    'lamb5': Struct(typ='Cnts', varid='lamb5', prn=r'$\lambda_5$',
                    desc="Cover surface", units=m**2, val=1.8e4, ok='ok,tomé el valor de Holanda, el de Texas es muy grande (9e4)'), # Superficie de la cubierta # ok --> tomé el valor de Holanda, el de Texas es muy grande (9e4)
    'lamb6': Struct(typ='Cnts', varid='lamb6', prn=r'$\lambda_6$',
                    desc="Variable of heat exchange by convection between the roof and the outside air", units=W * m_cover**-2 * K**-1, val=2.8, ok='ok, usé el valor de Texas'), # Variable de intercambio de calor por convecci ́on entre la cubierta y el aire exterior # ok ---> usé el valor de Texas
    'lamb7': Struct(typ='Cnts', varid='lamb7', prn=r'$\lambda_7$',
                    desc="Variable of heat exchange by convection between the roof and the outside air", units=J * m**-3 * K**-1, val=1.2, ok='ok, usé el valor de Texas'), # Variable de intercambio de calor por convecci ́on entre la cubierta y el aire exterior # ok ---> usé el valor de Texas
    'lamb8': Struct(typ='Cnts', varid='lamb8', prn=r'$\lambda_8$',
                    desc="Variable of heat exchange by convection between the roof and the outside air", units=1, val=1, ok='ok,usé el valor de Texas')
}


RHO = {
    ################## rho ##################
    'rho1':Struct(typ='Cnts', varid='rho1', prn=r'$\rho_1$',
                    desc="PAR reflection coefficient", units=1, val=0.07,ok=ok),
    'rho2': Struct(typ='Cnts', varid='rho2', prn=r'$\rho_2$',
                    desc="Floor reflection coefficient PAR", units=1, val=0.65,ok = ok), 
    'rho3': Struct(typ='Cnts', varid='rho3', prn=r'$\rho_3$',
                    desc="Air density", units=kg * m**-3, val= 1.2,ok = 'El valor es el de la densidad del aire al nivel del mar'),
    'rho4': Struct(desc='Densidad del aire a nivel del mar')
}


TAU = {
    'tau1': Struct(typ='Cnts', varid='tau1', prn=r'$\tau_1$',
                    desc="PAR transmission coefficient of the Cover", units=1, val=1,ok = 'En el artículo no dan su valor'),
    'tau2': Struct(typ='Cnts', varid='tau2', prn=r'$\tau_2$',
                    desc="FIR transmission coefficient of the Cover", units=1, val=1, ok ='En el artículo no dan su valor'),
    'tau3': Struct(typ='Cnts', varid='tau3', prn=r'$\tau_3$',
                    desc="FIR transmission coefficient of the thermal screen", units=1, val=0.11,ok = 'ok --> usé el valor de Texas')
}


NU ={
    'nu1': Struct(typ='Cnts', varid='nu1', prn=r'$\nu_1$',
                    desc="Shadowless discharge coefficient", units=1, val=0.65,ok = ok), 
    'nu2': Struct(typ='Cnts', varid='nu2', prn=r'$\nu_2$',
                    desc="Global wind pressure coefficient without shadow", units=1, val=0.1,ok=ok),
    'nu3': Struct(typ='Cnts', varid='nu3', prn=r'$\nu_3$',
                    desc="Side surface of the greenhouse", units=m**2, val=900,ok  = 'En ejemplos del artículo usan valor cero'), 
    'nu4': Struct(typ='Cnts', varid='nu4', prn=r'$\nu_4$',
                    desc="Leakage coefficien", units=1, val=1e-4,ok=ok), 
    'nu5': Struct(typ='Cnts', varid='nu5', prn=r'$\nu_5$',
                    desc="Maximum ceiling ventilation area", units=m**2, val=2e3, ok = ' 0.2*alpha6 --> ok'), 
    'nu6': Struct(typ='Cnts', varid='nu6', prn=r'$\nu_6$',
                    desc="Vertical dimension of a single open respirator", units=m, val=1,ok=ok), 
    'nu7': Struct(typ='Cnts', varid='nu7', prn=r'$\nu_7$',
                    desc="Soil thermal conductivity", units=W * m**-1 * K**-1, val=0.85, ok=ok), 
    'nu8': Struct(typ='Cnts', varid='nu8', prn=r'$\nu_8$',
                    desc="Floor to ground distance", units=m, val=0.64,ok=ok)
}


PHI = {
    ################## phi ##################
    'phi1': Struct(typ='Cnts', varid='phi1', prn=r'$\phi_1$',
                    desc="External diameter of the heating pipe", units=m, val=51e-3,ok = ok),
    'phi2': Struct(typ='Cnts', varid='phi2', prn=r'$\phi_2$',
                    desc="Average height of greenhouse air", units=m, val=4, ok = 'Se regreso a valor original'), 
    'phi3': Struct(desc='Masa molar del aire'), 
    'phi4': Struct('Altitud del invernadero'),
    'phi5': Struct(typ='Cnts', varid='phi5', prn=r'$\phi_5$',
                    desc="Water vapor contained in the fan-pad system", units=kg_water * kg_air**-1, val=0.014, ok=ok), 
    'phi6': Struct(typ='Cnts', varid='phi6', prn=r'$\phi_6$',
                    desc="Water vapor contained in the outside air", units=kg_water * kg_air**-1, val=0.0079, ok='este es el valor correcto a 21 grados C y 50 % de HR'), # Vapor de agua contenido en el aire exterior
    'phi7': Struct(typ='Cnts', varid='phi7', prn=r'$\phi_7$',
                    desc="Capacity of air flow through the pad", units=m**3 * s**-1, val=16.7,ok = ok), 
    'phi8': Struct(typ='Cnts', varid='phi8', prn=r'$\phi_8$',
                    desc="Air flow capacity of forced ventilation system", units=m**3 * s**-1, val=666.6, ok = 'https://farm-energy.extension.org/greenhouse-ventilation/'),
    'phi9': Struct(typ='Cnts', varid='phi9', prn=r'$\phi_9$',
                    desc="Fog system capacity", units=kg * s**-1, val=0.916, ok='Como en Holanda')
}


PSI = {
    ################## psi ##################
    'psi1':Struct(typ='Cnts', varid='psi1', prn=r'$\psi_1$',
                    desc="Molar mass of water", units=kg * kmol**-1, val=18,ok = ok), 
    'psi2': Struct(typ='Cnts', varid='psi2', prn=r'$\psi_2$',
                    desc="Capacity of the external CO2 source", units=mg * s**-1, val=4.3*(10**5),ok=ok),
    'psi3': Struct(typ='Cnts', varid='psi3', prn=r'$\psi_3$',
                    desc="Molar mass of the CH2O", units=g * mol_CH2O**-1, val=30.031,ok = ok)
}


OMEGA = {
    ################## omega ##################
    'omega1': Struct(typ='Cnts', varid='omega1', prn=r'$\omega_1$',
                    desc="Gravity acceleration constant", units=m * s**-2, val=9.81, ok = ok), 
    'omega2': Struct(typ='Cnts', varid='omega2', prn=r'$\omega_2$',
                    desc="Molar gas constant", units=J * kmol**-1 * K**-1, val= 8.314e3, ok = ok), 
    'omega3': Struct(typ='Cnts', varid='omega3', prn=r'$\omega_3$',\
                        desc="Percentage of CO2 absorbed by the canopy", units= 1 , val=0.03/4.0,ok = 'Deberia depender del modelo de la planta')
}

################## Inputs ##################
INPUTS ={
    'I1' : Struct(typ='Cnts', varid='I1', prn=r'$I_1$',
                    desc="Leaf area index", units=m**2 * m**-2, val=2, ok = 'Valor tesis Vanthoor'),
    'I2' : Struct(typ='State', varid='I2', prn=r'$I_2$',
                    desc="External global radiation", units=W * m**-2, rec=nrec, val=100.0, ok = 'Sin comentario'), 
    'I3' : Struct(typ='State', varid='I3', prn=r'$I_3$',
                    desc="Heating pipe temperature", units=C, val=20, ok = 'Sin comentario'),      
    'I4' : Struct(typ='State', varid='I4', prn=r'$I_4$',
                    desc="Sky temperature", units=C, val=-0.4,ok = 'Valor de España, pendiente'),      
    'I5' : Struct(typ='State', varid='I5', prn=r'$I_5$',
                    desc="Outdoor temperature", units=C, val=18, ok = 'Sin comentario'),  
    'I6' : Struct(typ='State', varid='I6', prn=r'$I_6$',
                    desc="Mechanical cooling system temperature", units=C, val = 20, ok = 'Sin comentario'),      # Mechanical cooling system temperature 
    'I7' : Struct(typ='Cnts', varid='I7', prn=r'$I_7$',
                    desc="Soil temperature", units=C, val=18, ok = 'Valor de España'),  
    'I8' : Struct(typ='State', varid='I8', prn=r'$I_8$',
                    desc="Outdoor wind speed", units=m * s**-1, val=3.2, ok = 'Sin comentario'),         
    'I9' : Struct(typ='State', varid='I9', prn=r'$I_{9}$',
                    desc="Global radiation above the canopy", units=W * m**-2, val=100, ok = ' Sin comentario'),
    'I10' : Struct(typ='Cnts', varid='I10', prn=r'$I_{10}$',
                    desc="Outdoor CO2 concentration", units=mg * m**-3, val = 668,ok = '668 mg/m**3 (370 ppm);'),
    'I11' : Struct(typ='State', varid='I11', prn=r'$I_{11}$',
                    desc= "external air vapor pressure ", units= Pa, val = 668,ok = 'Hay que calcularla,valor inicial incorrecto'),
}


################## State variables ##################
STATE_VARS = {
    'C1' : Struct(typ='State', varid='C1', prn=r'$C_1$',
                    desc="CO2 concentrartion in the greenhouse air", units=mg * m**-3, val=429.3, rec=nrec, ok='falta valor inicial'),
    'V1' : Struct(typ='State', varid='V1', prn=r'$V_1$',
                    desc="Greenhouse air vapor pressure", units=Pa, val=1200, rec=nrec, ok='https://www.dimluxlighting.com/knowledge/blog/vapor-pressure-deficit-the-ultimate-guide-to-vpd/'), 
    'T1' : Struct(typ='State', varid='T1', prn=r'$T_1$',
                    desc="Canopy temperature", units=C, val=20, rec=nrec, ok='falta valor inicial'),
    'T2' : Struct(typ='State', varid='T2', prn=r'$T_2$',
                    desc="Greenhouse air temperature", units=C, val=20, rec=nrec, ok='falta valor inicial')
}



COSTS = {
    'Qh2o': Struct(typ='State', varid='Qh2o', prn=r'$Q_{H2O}$',
                    desc="Water cost ", units=mxn * kg, val=0, rec=nrec, ok='revisar unidades'),
    'Qgas': Struct(typ='State', varid='Qgas', prn=r'$Q_{Gas}$',
                    desc="Fuel cost (natural gas)", units=mxn * m**-2, val=0, rec=nrec, ok='revisar unidades'), 
    'Qco2': Struct(typ='State', varid='Qco2', prn=r'$Q_{CO2}$',
                    desc="CO2 cost ", units=mxn * kg, val=0, rec=nrec, ok='revisar unidades'), 
    'Qelec': Struct(typ='State', varid='Qelec', prn=r'$Q_{Elec}$',\
                    desc="Costo por Electricidad", units= mxn * m**-2 * s**-1 , val=0, rec=nrec)
}



################## Controls ##################
CONTROLS = {
    'U1': Struct(typ='State', varid='U1', prn=r'$U_1$', desc="Thermal screen control", units=1, val=0, rec  = 100,ok=ok),
    'U2': Struct(typ='State', varid='U2', prn=r'$U_2$', desc="Fan and pad system control", units=1, val=0, rec  = 100,ok=ok),
    'U3': Struct(typ='State', varid='U3', prn=r'$U_3$', desc="Control of mechanical cooling system", units=1, val=0, rec  = 100,ok=ok),
    'U4': Struct(typ='State', varid='U4', prn=r'$U_4$', desc="Air heater control", units=1, val=0, rec  = 100,ok=ok),
    'U5': Struct(typ='State', varid='U5', prn=r'$U_5$', desc="External shading control", units=1, val=0, rec  = 100,ok=ok),
    'U6': Struct(typ='State', varid='U6', prn=r'$U_6$', desc="Side vents Control", units=1, val=0,rec  = 100, ok=ok),
    'U7': Struct(typ='State', varid='U7', prn=r'$U_7$', desc="Forced ventilation control", units=1, val=0, rec  = 100,ok=ok),
    'U8': Struct(typ='State', varid='U8', prn=r'$U_8$', desc="Roof vents control", units=1, val=0,rec  = 100,ok=ok),
    'U9': Struct(typ='State', varid='U9', prn=r'$U_9$', desc="Fog system control", units=1, val=0, rec  = 100,ok=ok),
    'U10': Struct(typ='State', varid='U10', prn=r'$U_{10}$', desc="Control of external CO2 source", units=1, val=0, rec  = 100,ok=ok),
    'U11': Struct(typ='State', varid='U11', prn=r'$U_{11}$', desc="", units=1, val=0,rec  = 100, ok='falta descripción')
}

FUNCTIONS = {
    ########Funciones Auxiliares para T1 (Temperatura del dosel) ########
    'r1': Struct(typ='State', varid='r1', prn=r'$r_1$', desc="Radiacion PAR absorbida por el dosel (T1+)", units=1, val=0, rec = nrec ,ok=ok),
    'r5': Struct(typ='State', varid='r5', prn=r'$r_5$', desc="Radiacion NIR absorbida por el dosel (T1+)", units=1, val=0, ok=ok),
    'r6': Struct(typ='State', varid='r6', prn=r'$r_6$', desc="Radiacion FIR que la tuberia de calentamiento le transmite al dosel (T1+)", units=1, val=0, ok=ok),
    'h1': Struct(typ='State', varid='h1', prn=r'$h_1$', desc="Intercambio de calor desde el dosel (T1-, T2+)", units=1, val=0, ok=ok),
    'l1': Struct(typ='State', varid='l1', prn=r'$l_1$', desc="Flujo de calor latente causado por transpiracion (T1-)", units=1, val=0, ok=ok),
    'r7': Struct(typ='State', varid='r7', prn=r'$r_7$', desc="Radiacion FIR que el dosel le transmite al cielo (T1-)", units=1, val=0, ok=ok),
    
    ######## Funciones Auxiliares para T1 (Temperatura del aire) ########
    'h2': Struct(typ='State', varid='h2', prn=r'$h_2$', desc="Intercambio de calor desde el dosel hacia la almohadilla de enfriamiento (T2+)", units=1, val=0, ok=ok),
    'h3': Struct(typ='State', varid='h3', prn=r'$h_3$', desc="Intercambio de calor desde el dosel hacia el sistema de enfriamiento mecanico (T2+)", units=1, val=0, ok=ok),
    'h4': Struct(typ='State', varid='h4', prn=r'$h_4$', desc="Intercambio de calor desde el dosel hacia la tuberia de calentamiento (T2+)", units=1, val=0, ok=ok),
    'h5': Struct(typ='State', varid='h5', prn=r'$h_5$', desc="Intercambio de calor desde el dosel hacia el buffer de energia pasiva (T2+)", units=1, val=0, ok=ok),
    'h6': Struct(typ='State', varid='h6', prn=r'$h_6$', desc="Intercambio de calor desde el dosel hacia el calentador de aire directo (T2+)", units=1, val=0, ok=ok),
    'r8': Struct(typ='State', varid='r8', prn=r'$r_8$', desc="Radiacion global que es absorbida por los elementos (T2+)", units=1, val=0, ok=ok),
    'h7': Struct(typ='State', varid='h7', prn=r'$h_7$', desc="Intercambio de calor desde el aire al interior hacia el aire externo(T2-)", units=1, val=0, ok=ok),
    'h10': Struct(typ='State', varid='h10', prn=r'$h_{10}$', desc="Intercambio del sistema de ventilador-almohadilla (T2-)", units=1, val=0, ok=ok),
    'l2': Struct(typ='State', varid='l2', prn=r'$l_2$', desc="Disminucion del calor latente por el sistema de neblina (T2-)", units=1, val=0, ok=ok),
    'r10': Struct(typ='State', varid='r10', prn=r'$r_{10}$', desc="FIR que el aire al interior del invernadero le transmite al cielo (T2-)", units=1, val=0, ok=ok),
    'h11': Struct(typ='State', varid='h11', prn=r'$h_{11}$', desc="Intercambio de calor desde el aire y el suelo (T2-)", units=1, val=0, ok=ok),
    
    ######## Funciones Auxiliares para V1 (Presion de Vapor) ########
    'p1': Struct(typ='State', varid='p1', prn=r'$p_1$', desc="Inter. de vapor dosel - aire del invernadero (V1+)", units=1, val=0, ok=ok),
    'p2': Struct(typ='State', varid='p2', prn=r'$p_2$', desc="Inter. de vapor aire del invernadero - almohadilla de enfriamiento (V1+)", units=1, val=0, ok=ok),
    'p3': Struct(typ='State', varid='p3', prn=r'$p_3$', desc="Inter. de vapor aire del invernadero - sistema de niebla (V1+)", units=1, val=0, ok=ok),
    'p4': Struct(typ='State', varid='p4', prn=r'$p_4$', desc="Inter. de vapor aire del invernadero - calentador de aire directo (V1+)", units=1, val=0, ok=ok),
    'p6': Struct(typ='State', varid='p6', prn=r'$p_6$', desc="Inter. de vapor aire del invernadero - el sistema de ventilador-almohadilla (V1-)", units=1, val=0, ok=ok),
    'p5': Struct(typ='State', varid='p5', prn=r'$p_5$', desc="Inter. de vapor aire del invernadero - exterior (V1-)", units=1, val=0, ok=ok),
    'p7': Struct(typ='State', varid='p7', prn=r'$p_7$', desc="Inter. de vapor aire del invernadero - sistema de enfriamiento mecanico (V1-)", units=1, val=0, ok=ok),
   
    ######## Funciones Auxiliares para C1 (Concentracion de CO2) ########
    'o1': Struct(typ='State', varid='o1', prn=r'$o_1$', desc="Inter. de CO2 aire del invernadero - calentador de aire directo (C1+)", units=1, val=0, ok=ok), 
    'o2': Struct(typ='State', varid='o2', prn=r'$o_2$', desc="Inter. de CO2 aire del invernadero - fuente externa de CO2 (C1+)", units=1, val=0, ok=ok), 
    'o3': Struct(typ='State', varid='o3', prn=r'$o_3$', desc="Inter. de CO2 aire del invernadeo - sistema de ventilador-almohadilla (C1+)", units=1, val=0, ok=ok), 
    'o4': Struct(typ='State', varid='o4', prn=r'$o_4$', desc="Inter. de CO2 aire del invernadeo - planta (C1-)", units=1, val=0, ok=ok), 
    'o5': Struct(typ='State', varid='o5', prn=r'$o_5$', desc="Inter. de CO2 aire invernadero - el exterior (C1-)", units=1, val=0, ok=ok),
    'a1': Struct(typ='State', varid='a1', prn=r'$a_1$', desc="Superficie del dosel", units=1, val=0, ok=ok), 

    ######## Funciones sub-auxiliares ######## 
    'f1': Struct(typ='State', varid='f1', prn=r'$f_1$', desc="flujo de ventilacion debido al sistema de ventilador-almohadilla", units=1, val=0, ok=ok),
    'g1': Struct(typ='State', varid='g1', prn=r'$g_1$', desc="Factor de vista desde la tuberia decalentamiento hacia el dosel", units=1, val=0, ok=ok), 
    'h4': Struct(typ='State', varid='h4', prn=r'$h_4$', desc="Inter. de calor tubería de calentamiento - aire del invernadero", units=1, val=0, ok=ok),
    'h6': Struct(typ='State', varid='h6', prn=r'$h_6$', desc="Inter. de calor aire del invernadero - el calentador de aire directo", units=1, val=0, ok=ok),
    'o2': Struct(typ='State', varid='o2', prn=r'$o_2$', desc="Inter. de CO2 aire del invernadero - la fuente externa de CO2", units=1, val=0, ok=ok),
    'q1': Struct(typ='State', varid='q1', prn=r'$q_1$', desc="Coeficiente de intercambio de vapor dosel - aire del invernadero", units=1, val=0, ok=ok),
    'q2': Struct(typ='State', varid='q2', prn=r'$q_2$', desc="Presion de vapor saturada a temperatura del dosel", units=1, val=0, ok=ok),
    'q3': Struct(typ='State', varid='q3', prn=r'$q_3$', desc="Resistencia estomatica del dosel", units=1, val=0, ok=ok),
    'q4': Struct(typ='State', varid='q4', prn=r'$q_4$', desc="Factor de resistencia estomaticapor latos niveles de CO2", units=1, val=0, ok=ok),
    'q5': Struct(typ='State', varid='q5', prn=r'$q_5$', desc="Factor de resistencia estomatica por una gran diferencia en la presión de vapor", units=1, val=0, ok=ok),
    'q7': Struct(typ='State', varid='q7', prn=r'$q_7$', desc="Auxiliar function for q8", units=1, val=0, ok=ok), 
    'q8': Struct(typ='State', varid='q8', prn=r'$q_8$', desc="Auxiliar function for q4", units=1, val=0, ok=ok),
    'q9': Struct(typ='State', varid='q9', prn=r'$q_9$', desc="Auxiliar function for q5", units=1, val=0, ok=ok),
    'q10':Struct(typ='State', varid='q10', prn=r'$q_{10}$', desc="Auxiliar function for q3", units=1, val=0, ok=ok),
    
}

NREC = {'nrec':nrec}

DT = {'dt': mt }

CONSTANTS = {**OTHER_CONSTANTS, **ALPHA, **BETA, ** GAMMA, **DELTA, **EPSIL, **ETA, **LAMB, **RHO, **TAU, 
                **NU, **PHI, **PSI, **OMEGA, **INPUTS, **STATE_VARS, **COSTS, **CONTROLS, **FUNCTIONS, **NREC, **DT} # Merge dictionaries Python 3.5<=*



