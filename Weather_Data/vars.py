from Struct_weather import Struct_weather

Vars = {'Time_Stamp' : Struct_weather(orig_name='Time Stamp',new_name='Time_units'),
        'Year': Struct_weather(orig_name='Year'),
        'Month':Struct_weather(orig_name = 'Month'),
        'Day':Struct_weather(orig_name = 'Day'),
        'Hour' : Struct_weather(orig_name='Hour'),
        'Minute':Struct_weather(orig_name='Minute'),
        'Temperature': Struct_weather(orig_name = 'Temperature', units= 'C',new_name = 'I5', obs = '2m above gnd'),
        'Relative_Humidity': Struct_weather(orig_name='Relative Humidity',units='%',new_name='RH',obs = '2 m above gnd'),
        'Total_Cloud_Cover': Struct_weather(orig_name='Total Cloud Cover',units='%',obs = ' sfc'),
        'High_Cloud_Cover':Struct_weather(orig_name= 'High Cloud Cover',units='%',obs='high cld lay'),
        'Medium_Cloud_Cover': Struct_weather(orig_name='Medium Cloud Cover',units='%',obs='mid cld lay'),
        'Low_Cloud_Cover': Struct_weather(orig_name='Low Cloud Cover',units='%',obs='low cld lay'),
        'Shortwave_Radiation': Struct_weather(orig_name='Shortwave Radiation',units='W m-2',new_name='I2',obs='sfc'),
        'Wind_Speed10m': Struct_weather(orig_name='Wind Speed10m',units='km h-1',new_name='I8',obs= '10 m above gnd'),
        'Wind_Direction10m': Struct_weather(orig_name='Wind Direction10m',units='km h-1',obs = '10 m above gnd'),
        'Wind_Speed80m': Struct_weather(orig_name='Wind Speed80m',units='km h-1',obs= '80 m above gnd'),
        'Wind_Direction80m': Struct_weather(orig_name='Wind Direction80m',units='km h-1',obs = '80 m above gnd'),
        'Wind_Speed900mb': Struct_weather(orig_name='Wind Speed900mb',units='km h-1',obs= '900 mb'),
        'Wind_Direction900mb': Struct_weather(orig_name='Wind Direction900mb',units='km h-1',obs = '900 mb')
}