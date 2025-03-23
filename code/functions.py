from haversine import haversine, Unit

# HAY 155 STOPS
# NOTA: no evaluar STOPs q ya tiene PUNTO
DISTANCIA_MAXIMA = 100000 # en metros

def closest_point(row_stop, df_points):
    #print(f"\tEvaluando para stop {row_stop['id']}_{row_stop['name']}")
    sorted_points_df = df_points.sort_values(by='datetime')
    
    min_dis = DISTANCIA_MAXIMA
    min_id_point, nav_min_dis = -1, 360
    while not sorted_points_df.empty:
        row_point = sorted_points_df.iloc[0]
        dis, nav = medirDistancia(row_stop, row_point)
        if dis < min_dis:
            min_dis = dis
            min_id_point = row_point['id_point']
            nav_min_dis = nav
        if dis < 10:
            break
            
        sorted_points_df = sorted_points_df.iloc[1:]
    
    #print(f"\tPunto mas cercano para el stop {row_stop['id']}_{row_stop['name']}: {min_id_point} con distancia {min_dis} y navegacion {nav_min_dis}")
    #print("="*50)
    return min_id_point, min_dis, nav_min_dis
    
    
# RETORNA DISTANCIA EN METROS (M)
def medirDistancia(stop_row, point_row):
    # 1° si navegacion es NO ES SIMILAR 
    nav = abs(stop_row['navigation'] - point_row['navigation'])
    if nav > 45: return DISTANCIA_MAXIMA, nav
    
    # 2° convertimos a tuplas
    stop  = ( stop_row['latitude'],  stop_row['longitude'])
    point = (point_row['latitude'], point_row['longitude'])
    
    # 3° calculamos distancia y retonamos
    distancia = round(haversine(point, stop, unit=Unit.METERS), 2)
    
    #print(f"\t\tCon Punto {point_row['id_point']} ({point_row['datetime']}):\tdistancia={distancia}\tnagivation={nav} ({stop_row['navigation']}, {point_row['navigation']})")
    return distancia, nav
    
#from haversine import haversine as hvs, Unit
# FUNCION: 
# def searchStopsPoints(row, stops, r_nav=45, r_dtec=60):
#     # verificar la navegacion y el radio de distancia
#     stops = stops[abs(stops['navigation'] - row['navigation']) <= r_nav]
#     stops['dis'] = stops['latitude_longitude'].apply(lambda stop: round(hvs(row['latitude_longitude'], stop, unit=Unit.METERS), 2))
#     stops = stops[stops['dis'] <= r_dtec]
    
#     # preparar el output
#     row['stop'] = str(stops.loc[stops['dis'].idxmin(), 'id']) if len(stops) != 0 else np.nan
#     row['dis'] = float(stops.loc[stops['dis'].idxmin(), 'dis']) if len(stops) != 0 else 0    
#     #row['long_lati'] = row['latitude_longitude']
#     return row

# # FUNCION: CALCULA EL TIEMPO EN SEG DE UN PUNTO CON SU ANTERIOR
# def time_travel(row, df):
#     if {row['init_stop'], row['end_stop']}.issubset(set(df.index)):
#         # print('if')
#         ti, te =  df.loc[row['init_stop'], 'datetime'], df.loc[row['end_stop'], 'datetime']
#         row['date_time_init'] = ti
#         row['date_time_end'] = te
#         time = abs((ti - te).total_seconds())
        
#         #row['time_travel'] =  time if time < 300 else np.nan
#         row['time_travel'] =  time
#         row['init_idp'], row['end_idp'] = df.loc[row['init_stop'], 'id'], df.loc[row['end_stop'], 'id']

#         row['ini_lat'] = df.loc[row['init_stop'], 'latitude_longitude']
#         row['end_lat'] = df.loc[row['end_stop'], 'latitude_longitude']

#         row['veh'] = df.loc[row['init_stop'], 'vehicle_id']
#         row['lap'] = df.loc[row['init_stop'], 'lap']
#         row['date'] = df.loc[row['init_stop'], 'date']

#     else:
#         # print('else')
#         row['date_time_init'] = np.nan
#         row['date_time_end'] = np.nan
#         row['time_travel'] = np.nan
#         row['init_idp'] = np.nan
#         row['end_idp'] = np.nan
#         row['veh'] = np.nan
#         row['lap'] = np.nan
#         row['date'] = np.nan
        
#     return row
