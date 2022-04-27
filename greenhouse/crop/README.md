# Modelos de fotosintesis:

## (A) Surrogate: 

Consiste de una función concava en PAR y Ca 
            (CO2 atmosférico) que simula  el comportamiento 
            de la fotosintesis. 
             
## (B) Simplificado: 
Considera el modelo completo de Farquhar, von Caemmerer 
               & Berry 1980 (FvCB-1980), pero se asumen que: 

1) La conductancia del CO2 en los estomas es tal que 
                  la concentración del CO2 intracelular (Ci) es el 68% 
                  de la concentración del CO2 atmosférico  (Ca). Es decir:
                       Cippm = 0.67*(0.554*Ca) (C1*)*0.67 
                  En el modelo Ca esta mg * m**-3  ylo debemos trasnformar a ppm.
                  En Factor de conversion es 1 mg * m**-3 = 0.556 ppm
                  El 67% se toma de Vanthoor que a su vez lo toma de 
                  Evans and Farquhar (1991). Ellos asumen que esto da el CO2
                  a pasando los estimas (esto es Ci).
2) La conductancia de Ci a través de la membrana mesofilica es 
                  constante y esta dada por g_t = g_m = 0.14  mu_mul m**-2 s**-1 ppm**-1 
                  (= mol m**−2 s**−1 bar**−1)

Con estas suposiciones el para el CO2 en los sitios de carboxilacion (Cc) 
                  es: A = g_t(Cc - Cippm )
                  De esta ecuación combinada con FvCB-1980 se obtienen las ecuaciones 
                  cuadráticas para A_R y A_F (los asimilados limitados por Rubisto y Radiación) 

## (C) Estomatas variables: 

Considera el modelo completo de Farquhar, von Caemmerer 
               & Berry 1980 (FvCB-1980), pero se asumen que: 

1) La conductancia del CO2 en los estomas  (g_s) varia segun la 
               concentración de CO2, radiación global y deficit de presión de valor según 
               el modelo de Stanghellini 1980.  En realidad este modelo es para la resistrencia
               del H2O en los estomas. La resistencia (rs_s) se mide en unidades de s * m**-1, 
              y la conductancia sería:  g_s = rs**-1 (1.66)**-1. Para transformar este valor a las  las uniddades de mu_mol_CH20 * ppm_CO2**-1 * m**-2 s**-1 necesitmos multiplicar a 
               gs * (0.553/0.044) ver función  gsf.     
               
2) En este modelo no se toman en cuenta la conductancia de Ci a través de la membrana mesofilica. 