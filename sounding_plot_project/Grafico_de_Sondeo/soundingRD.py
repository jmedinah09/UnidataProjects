import datetime 
from   siphon.simplewebservice.wyoming import WyomingUpperAir
from   metpy.units import units, pandas_dataframe_to_unit_arrays
import matplotlib.pyplot as plt
import metpy.plots as plots
import metpy.calc as mpcalc
import numpy as np
import pandas as pd
from   matplotlib.pyplot import imread
from   metpy.interpolate import interpolate_1d

##################### DATETIME SETTINGS #######################################
print("Setting up Date and Time")

obs_hour = 12
am_pm = "a"
dt = datetime.date.today()
current_year      = dt.year
current_month     = dt.month
current_day       = dt.day

current_datetime  = datetime.datetime(current_year, current_month, current_day, obs_hour)
#current_datetime = datetime.datetime(2021, 10, 11, 12) #sept-10-2017 @ 0000z

Dias_de_la_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
tday              = current_datetime.weekday()
Dia_de_la_semana  = Dias_de_la_semana[tday]

Meses_del_Ano     = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre',
                     'Octubre', 'Noviembre', 'Diciembre']
Mes_del_Ano       = Meses_del_Ano[current_month]

if  datetime.datetime.now().hour > 17 or datetime.datetime.now().hour == 0:
    am_pm = "p"

# fecha_y_hora          = f'{Dia_de_la_semana} {current_day} de {Mes_del_Ano} de {current_year} - 8:00 {am_pm}.m.'
fecha_y_hora          = f'{Dia_de_la_semana} {current_day} de {Mes_del_Ano} de {current_year} - 2:00 p.m.'
print(fecha_y_hora)

#if  (datetime.datetime.now().hour > 17) or (0 <= datetime.datetime.now().hour <= 6):
if  datetime.datetime.now().hour > 17 or datetime.datetime.now().hour == 0:
    obs_hour = 00
    dt = datetime.date.today() + datetime.timedelta(days=1)

    current_year      = dt.year
    current_month     = dt.month
    current_day       = dt.day
    current_datetime  = datetime.datetime(current_year, current_month, current_day, obs_hour)
    #current_datetime = datetime.datetime(2022, 3, 18, 00) #sept-10-2017 @ 0000z

##################### WY SERVER CONNECTION #######################################
# print('Connecting to WY Server...')
# station = '78486'
# i       = 1
# while True:
#     try:
#         df = WyomingUpperAir.request_data(current_datetime, station)
#         d  = pandas_dataframe_to_unit_arrays(df)
#         print('Connected Succesfully!')
#         break
#     except:
#         print(f'Attempt {i} failed.')
#         i = i +1
#         continue

##################### LOCAL CONNECTION #######################################

print("Using local data")

filename = f"/mnt/c/Users/Carla/Desktop/Jose/UnidataProjects/sounding_plot_project/Grafico_de_Sondeo/xRepBufr.txt"
d = pd.read_table(filename, sep='\s+', names=['TIME'    ,    'pressure' ,   'height' ,  'temperature',   'RH',     
                                              'dewpoint',    'direction',     'speed',  '8042'],  encoding='cp1252', 
                                               on_bad_lines='skip')
d = d.drop([0, 1, 2, 3, 4]) 
d = d.drop(['TIME', '8042', 'RH'], axis = 1)

d = d.replace('---', np.nan)
# d = d.dropna(subset=('pressure', 'height', 'temperature', 'dewpoint', 'direction', 'speed'), 
#              how='all').reset_index(drop=True)

d = d.dropna(axis=0)

d['pressure']      = pd.to_numeric(d['pressure'])
d['height']        = pd.to_numeric(d['height'])
d['temperature']   = pd.to_numeric(d['temperature'])
d['dewpoint']      = pd.to_numeric(d['dewpoint'])
d['direction']     = pd.to_numeric(d['direction'])
d['speed']         = pd.to_numeric(d['speed'])

# print('Writing up into a excel file...')

# writer = pd.ExcelWriter(f'/mnt/c/Users/Carla/Desktop/Grafico_de_Sondeo/{current_day}-{current_month}-{current_year}-{obs_hour}Z-78486.xlsx', 
#                         engine='xlsxwriter', mode='a', if_sheet_exists = 'replace')
# d.to_excel(writer, sheet_name='Sheet1')
# writer.save()

column_units = {
                'pressure'   : 'hPa',
                'height'     : 'meter',
                'temperature': 'degC',
                'dewpoint'   : 'degC',
                'direction'  : 'degrees',
                'speed'      : 'knot',
                }
d  = pandas_dataframe_to_unit_arrays(d, column_units=column_units)

d['u_wind'], d['v_wind'] = mpcalc.wind_components(d['speed']*1.94384, d['direction'])


##################### 	PLOT  #######################################

print('Initializing plot')

mandatory_levels = [1000, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100]

fig = plt.figure(figsize=(20, 20))
skew = plots.SkewT(fig, rotation = 45)

skew.plot(d['pressure'], d['temperature'], 'b', linewidth = 6)
skew.plot(d['pressure'], d['dewpoint'], 'b', linewidth = 2)

skew.ax.set_ylim(1050, 100)
skew.ax.set_xlim(-30, 40)

fig.suptitle(f'Sondeo Atmosferico de Santo Domingo (MDSD - 78486),\n{fecha_y_hora}', x = 0.84, y = 0.93, 
             weight = 'bold', horizontalalignment= 'right', fontsize = 28, color = 'b')
#fig.suptitle('Domingo 25 de julio de 2021 - 8:00 a.m.', fontsize = 20, y=0.)
plt.xlabel('Temperatura (C)', fontsize = 28)
plt.ylabel('Presion (hPa) & Altitud (m)', fontsize = 28)
plt.yticks(ticks=mandatory_levels, fontsize = 20)
plt.xticks(fontsize = 20)

interval = np.logspace(2, 3) * units.hPa
idx = mpcalc.resample_nn_1d(d['pressure'], interval)
skew.plot_barbs(d['pressure'][idx], d['u_wind'][idx], d['v_wind'][idx], barbcolor = 'blue', length=10)

skew.plot_dry_adiabats(colors = 'green', linewidth = 0.4, alpha = 0.7)
skew.plot_moist_adiabats(colors = 'green', linewidth = 0.4, alpha = 0.7)

p_space = np.linspace(100, max(skew.ax.get_ylim())) * units.mbar
skew.plot_mixing_lines(pressure = p_space, colors = 'green', linewidth = 0.4, alpha = 0.7)
#skew.plot_mixing_lines(colors = 'green', linewidth = 0.4, alpha = 0.7)

#interval = [k for k in range(1000, 0, -100)] * units.hPa
interval = mandatory_levels * units.hPa
idx = mpcalc.resample_nn_1d(d['pressure'], interval)
for p, t, h  in zip(d['pressure'][idx], d['temperature'][idx], d['height'][idx]):
    if p >= 100 * units.hPa:
        skew.ax.text(0.01, p, f'{round(h.m, 0)} metros', fontsize=16, 
                     transform = skew.ax.get_yaxis_transform(which='tick2'))

##################### 	CALCULATING THERMODYNAMIC INDEXES  #######################################
print("Calculating thermodynamic indexes")

#https://stackoverflow.com/questions/65985185/cape-cin-returning-incorrect-values

# Calculate the mixed parcel--need to pass pressure as an additional variable to "mix" so that we get
# an appropriate "average pressure" to use as the mixed parcel

parcel_temperature, parcel_dewpoint, mixed_pressure = mpcalc.mixed_layer(d['pressure'], d['temperature'],
                                                           d['dewpoint'], d['pressure'],
                                                           height=d['height'], depth=500 * units.m)

# Replace the lowest part of the sounding with the mixed value
pressure_mixed    = np.concatenate([np.atleast_1d(mixed_pressure), d['pressure'][d['pressure'] < mixed_pressure]])
temperature_mixed = np.concatenate([np.atleast_1d(parcel_temperature), 
                                    d['temperature'][d['pressure'] < mixed_pressure]])
dewpoint_mixed    = np.concatenate([np.atleast_1d(parcel_dewpoint), d['dewpoint'][d['pressure'] < mixed_pressure]])

# Calculate the parcel profile, including the LCL--this interpolates the sounding to the level of the LCL
# as well, so that the profile and all variables have the same points

parcel_path_LCL = mpcalc.parcel_profile(pressure_mixed, parcel_temperature, parcel_dewpoint)
skew.plot(pressure_mixed, parcel_path_LCL, color = 'k', linewidth = 0.8)


lcl_pressure, lcl_temperature = mpcalc.lcl(mixed_pressure, parcel_temperature, parcel_dewpoint)
lfc_pressure, lfc_temperature = mpcalc.lfc(pressure_mixed, temperature_mixed, dewpoint_mixed, which = 'bottom')
el_pressure, el_temperature   = mpcalc.el(pressure_mixed, temperature_mixed, dewpoint_mixed)

cape, cin = mpcalc.cape_cin(pressure_mixed, temperature_mixed, dewpoint_mixed, parcel_path_LCL)
mask      = pressure_mixed >= lfc_pressure
skew.shade_cape(pressure_mixed, temperature_mixed, parcel_path_LCL)
skew.shade_cin(pressure_mixed[mask], temperature_mixed[mask], parcel_path_LCL[mask])

cape_mu, cin_mu = mpcalc.most_unstable_cape_cin(pressure_mixed, temperature_mixed, dewpoint_mixed)

li = mpcalc.lifted_index(pressure_mixed, temperature_mixed, parcel_path_LCL)

pw = mpcalc.precipitable_water(d['pressure'], d['dewpoint'])


idx    = np.where(d['pressure'] == 850 * units.hPa)
idx    = idx[0][0]
t_850  = d['temperature'][idx]
td_850 = d['dewpoint'][idx]
ws_850 = d['speed'][idx]
wd_850 = d['speed'][idx]
pressure_set_from_850  = d['pressure'][idx:]
parcel_path_850 = mpcalc.parcel_profile(pressure_set_from_850, d['temperature'][idx], d['dewpoint'][idx])

idx    = np.where(d['pressure'] == 500 * units.hPa)
idx    = idx[0][0]
t_500  = d['temperature'][idx]
tp_500 = parcel_path_LCL[idx].to(units.degC)
ws_500 = d['speed'][idx]
wd_500 = d['speed'][idx]

idx    = np.where(d['pressure'] == 700 * units.hPa)
idx    = idx[0][0]
t_700  = d['temperature'][idx]
td_700 = d['dewpoint'][idx]

idx    = np.where(pressure_set_from_850 == 500 * units.hPa)
idx    = idx[0][0]
tp_500_850 = parcel_path_850[idx].to(units.degC)

kinx   = ( t_850  - t_500 ) + td_850 - ( t_700 - td_700 ) 
ctot   =   td_850 - t_500 
vtot   =   t_850  - t_500 
totl   = ( t_850  - t_500 ) + ( td_850 - t_500 )
show   =   t_500  - tp_500_850

#######SWET = 12 * TD850 + 20 * TERM2 + 2 * SKT850 + SKT500 + SHEAR 
a = 0
wd_500_850 = wd_500.m - wd_850.m
if 130 <= wd_850.m <= 250 and 210 <= wd_500.m <= 310 and  wd_500_850 > 0 and ws_500.m >= 15 and ws_850.m >= 15:
    a = 1
    
b=0
if totl.m > 49:
    b = 1
    
swet = 12*td_850.m + 20 * b * totl.m + 2*ws_850.m + ws_500.m + 125 * a *(float(np.sin(wd_500.m - wd_850.m)) + 0.2)

#######Frezing Level
# freezing_temperature = 0 * units.degC
# zero_temp_index = np.abs(d['temperature'] - freezing_temperature).argmin()
# freezing_level  = d['height'][zero_temp_index]
# closest_to_zero = np.abs(d['temperature'] - freezing_temperature)[zero_temp_index]
# if closest_to_zero.m > 1 or closest_to_zero.m < -1:
#     freezing_level = 9999 * units.degC
    

freezing_level_pressure = interpolate_1d(units.Quantity(0, 'degC'), d['temperature'], d['pressure'])
freezing_level_height   = interpolate_1d(units.Quantity(0, 'degC'), d['temperature'], d['height'])

if np.isnan(pw.m):
    pw=-9999*units.mm
if cape < 0:
    print(f'WARNING: Calculated cape is negative: {cape}')
    cape = -9999*units.hPa
if np.isnan(lfc_temperature.m):
    lfc_temperature = -9999*units.hPa
    lfc_pressure = -9999*units.hPa
if np.isnan(el_pressure.m):
    el_pressure    = -9999*units.hPa
    el_temperature = -9999*units.hPa
   

##################### 	PLOTTING THERMODYNAMIC INDEXES  #######################################

print('Writing index Column')
print("*"*100)

props      = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

txts     = [f'LAT  = 18.43', f'LON = -69.88', f'ALT = 14.00 m',            
            f'LCLT = {round(lcl_temperature.m, 1)} C', f'LCLP = {int(lcl_pressure.m)} hPa', 
            f'LFCT = {round(lfc_temperature.m, 1)} C', f'LFCP = {int(lfc_pressure.m)} hPa',
            f'ELT  = {round(el_temperature.m, 1)} C', f'ELP = {int(el_pressure.m)} hPa',
            f'CAPE = {int(cape.m)} J/kg', f'CIN = {int(cin.m)} J/kg',
            f'CAPE_mu = {int(cape_mu.m)} J/kg', f'CIN_mu = {int(cin_mu.m)} J/kg',
            f'LIFT = {round(float(li.m), 1)}', f'PW = {int(pw.m)} mm', f'K = {int(kinx.m)}',
            f'CTOT = {int(ctot.m)}', f'VTOT = {int(vtot.m)}', f'TOTL = {int(totl.m)}',
            f'SWET = {int(swet)}', f'T500 = {round(t_500.m, 1)} C', f'SHOW = {round(show.m, 1)}',
            f'FZLP = {int(freezing_level_pressure.m)} hPa', 
            f'FZLH = {int(freezing_level_height.m)} m']
xtxt = 1.1
ytxt = 0.99
for txt in txts:
    print(txt)
    skew.ax.text(xtxt, ytxt, txt, transform=skew.ax.transAxes, fontsize=24,
                 verticalalignment='top', bbox=props)
    ytxt = ytxt - 0.04
print("*"*100)
##################### 	DISCUSSION  #######################################


if cape.m < 1000:
    str_cape = 'poco favorable'
else:
    str_cape = 'favorable'
if li.m > 0:
    str_li = 'desfavorable'
else:
    str_li = 'favorbale'
    
    
if pw.m < 30:
    str_pw = 'poca humedad'
elif 30 <= pw.m <= 45:
    str_pw = 'humedad favorable'
else:
    str_pw = 'mucha humedad'
    
    
if kinx.m < 25:
    str_kinx = 'poca probabilidad de tormentas eletricas'
elif 25 <= kinx.m <= 35:
    str_kinx = 'probabilidad de tormentas eletrica dispersas'
else:
    str_kinx = 'alta probabilidad de tormentas electricas'
    

if vtot.m < 25:
    str_vtot = 'debil gradiente vertical de temperatura'
else:
    str_vtot = 'fuerte gradiente vertical de temperatura'
    
    
if totl.m < 45:
    str_totl = 'poca probabilidad de tormentas electricas'
elif 45 <= totl.m <= 55:
    str_totl = 'alta probabilidad de tormentas electricas'
else: 
    str_totl = 'probabilidad de tiempo severo'
    
    
if int(swet) < 200:
    str_swet = 'poca'
elif 200 <= int(swet) < 250:
    str_swet = 'moderada'
elif 250 <= int(swet) < 350:
    str_swet = 'alta'
else:
    str_swet = 'muy alta'
    
    
if show.m > 3:
    str_show = 'ambiente seco, poca probabilidad de tormentas electricas'
elif 3 >= show.m > 1:
    str_show = 'ligero contenido de humedad, probabilidad de algunos chubascos y tronadas aisladas'
elif 1 >= show.m > -2:
    str_show = 'probabilidad de aguaceros y tormentas electricas dispersas'
elif -3 >= show.m > -6:
    str_show = 'probabilidad de fuertes aguaceros y tormentas electricas'
else:
    str_show = 'probabilidad de fuertes aguaceros y tormentas electricas y tiempo severo'

print('Writing final report')

a = '-'*100
Discusion = f'''
Discusion (experimental - generada automaticamente)
{a}
El agua precipitable en la capa profunda fue estimada 
en unos {int(pw.m)} mm, indicando {str_pw} en nuestra masa de aire 
para que ocurran precipitaciones. Por otro lado, la energia disponible 
calulada en el CAPE es de unos {int(cape.m)} J/kg, por tanto, la 
atmosfera se encuentra bajo condiciones {str_cape} para que 
ocurran tormentas electricas.

Por otro lado, la inestabilidad estimada por el Lifted Index es {str_li} con un
valor de {round(float(li.m), 1)} mientras que el Show Walter Index arrojo un valor de {round(show.m, 1)} indicando
{str_show}. 
El K Index es de {int(kinx.m)}, por tanto, existe {str_kinx}.

El Total Totals Index arrojo un valor de {int(totl.m)} indicando
{str_totl} dado que existe 
{str_vtot} entre los niveles mandatarios 850 hPa 
y 500 hPa.

Finalmente, la probabilidad de que ocurra tiempo severo (aguaceros muy 
fuertes, tormentas electricas numerosos y frecuentes, intensas rafagas de 
viento, granizadas o tornados) estimada por el Severe Weather Theat Index
es {str_swet} dado que su valor es de {int(swet)}.
{a}
'''
props = dict(boxstyle='round', facecolor='lightblue', alpha=0.5)
xtxt = 0
ytxt = -0.1

skew.ax.text(xtxt, ytxt, Discusion, transform=skew.ax.transAxes, fontsize=24,
                 verticalalignment='top', bbox=props)
logo = imread('onamet-110X32.png')
fig.figimage(logo, 90, 1350, zorder=100)

#skew.ax.set_facecolor('')
fig.patch.set_facecolor('whitesmoke')

fig.savefig(f"/mnt/c/Users/Carla/Desktop/Jose/UnidataProjects/sounding_plot_project/Grafico_de_Sondeo/{current_day}-{current_month}-{current_year}-{obs_hour}Z-78486.png", 
			 dpi=fig.dpi, bbox_inches='tight')


print('Plot has been generated and saved succesfully')
print("*"*100)
print(Discusion)



