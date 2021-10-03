import requests
import csv
from io import StringIO
import datetime
import random


# -----------------------------------
# |           MAP DATA              |
# -----------------------------------
def map_fires_from_file(filename, new_filename):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        with open(new_filename, 'w', newline='') as csvNew:
            fieldnames = ['Latitude', 'Longitude', 'Started', 'Extinguished']
            csv_write = csv.DictWriter(csvNew, fieldnames, delimiter=',')
            csv_write.writeheader()
            for row in reader:
                if not(row['Latitude'] == '0.0'):
                    csv_write.writerow({'Latitude': row['Latitude'], 'Longitude': row['Longitude'], 'Started': row['Started'], 'Extinguished': row['Extinguished']})


# -----------------------------------
# |          REQUEST DATA           |
# -----------------------------------
def request(start_time, end_time, interval, latitude, longitude, parameters):
    
    ####    DATA    ######
    date_time = f'{start_time}--{end_time}:PT{interval}H'
    #parameters = f't_max_2m_{interval}h:C'
    coordinates = f'{latitude},{longitude}'
    parameters = f'leaf_wetness:idx, elevation:m, drought_index:idx, lightning_strikes_10km_{interval}h:x, precip_{interval}h:mm, relative_humidity_50m:p, soil_moisture_index_-15cm:idx, solar_power:kW, t_max_200m_{interval}h:C, wind_speed_mean_200m_{interval}h:kmh, pressure_mean_200m_{interval}h:Pa'   
    coordinates = f'{latitude},{longitude}'
    #   reference = 'https://api.meteomatics.com/2021-10-01T00:00:00Z--2021-10-02T00:00:00Z:PT6H/leaf_wetness:idx/51.5073219,-0.1276474/html'
    ####    REQUEST   ######
    url_string = f'https://student_marangis:dD3OWA0p2ukrB@api.meteomatics.com/{date_time}/{parameters}/{coordinates}/csv'
    r = requests.get(url_string)
    return (r.text)


def random_dates(times):
    counter = 0;
    with open('random_data_without_fire.csv', 'w', newline='') as csvNew:
        fieldnames = ['Date', 'Latitude', 'Longitude', 'Leaf_Wetness','Elevation',  'Drought', 'Lightning_Stikes', 'Precipitation', 'Relative_Humidity', 'Soil_Moisture', 'Solar_Power', 'Temperature', 'Wind_Speed', 'Atmospheric_Pressure', 'isFire']
        csv_write = csv.DictWriter(csvNew, fieldnames, delimiter=',')
        csv_write.writeheader()
        for i in range(times):
            x = random.randrange(0,100)
            if x < 33:
                latitude = random.randrange(400, 420)
                latitude = latitude / 10
                interval = '24'
                longitude = random.randrange(-1223, -1190)
                longitude = longitude / 10
            elif x < 66:
                latitude = random.randrange(380, 400)
                latitude = latitude / 10
                interval = '24'
                longitude = random.randrange(-1230, -1200)
                longitude = longitude / 10
            else:
                latitude = random.randrange(360, 380)
                latitude = latitude / 10
                interval = '24'
                longitude = random.randrange(-1213, -1180)
                longitude = longitude / 10
            #parameters = f'leaf_wetness:idx,elevation:m,drought_index:idx,lightning_strikes_10km_{interval}h:x,precip_{interval}h:mm,relative_humidity_50m:p,soil_moisture_index_-15cm:idx,solar_power:kW,t_max_200m_{interval}h:C,wind_speed_mean_200m_{interval}h:kmh,pressure_mean_200m_{interval}h:Pa'
            d = random.randint(1, 28)
            d2 = d + 1
            if d < 9:
                d = f'0{d}'
                d2 = f'0{d2}'
            elif d == 9:
                d = f'0{d}'
            m = random.randint(1, 12)
            if (m < 10):
                m = f'0{m}'
            y = random.randint(2014, 2021)
            start_date = f'{y}-{m}-{d}T00:00:00Z'
            end_date = f'{y}-{m}-{d2}T00:00:00Z'
            req = request(start_date,end_date, interval, latitude, longitude, None)
            req = req.replace(';', ',')
            req_new = StringIO(req)
            csv_response = csv.DictReader(req_new, delimiter=',')
            for line in csv_response:
                #csv_write.writerow({'Latitude': row['Latitude'], 'Longitude': row['Longitude'], 'Temp1': line['t_max_2m_24h:C']})
                csv_write.writerow({'Date': line['validdate'],
                                    'Latitude': latitude,
                                    'Longitude': longitude,
                                    'Leaf_Wetness': line['leaf_wetness:idx'],
                                    'Elevation': line['elevation:m'],
                                    'Drought': line['drought_index:idx'],
                                    'Lightning_Stikes': line[f'lightning_strikes_10km_{interval}h:x'],
                                    'Precipitation': line[f'precip_{interval}h:mm'],
                                    'Relative_Humidity': line['relative_humidity_50m:p'],
                                    'Soil_Moisture': line['soil_moisture_index_-15cm:idx'],
                                    'Solar_Power': line['solar_power:kW'],
                                    'Temperature': line[f't_max_200m_{interval}h:C'],
                                    'Wind_Speed': line[f'wind_speed_mean_200m_{interval}h:kmh'],
                                    'Atmospheric_Pressure': line[f'pressure_mean_200m_{interval}h:Pa'],
                                    'isFire': '0'})
                break
            counter += 1
            print(f'Finished: {counter}')

# -----------------------------------
# |            FILE 1               |
# -----------------------------------

def getData():
    interval = '24'
    counter = 0
    with open('mapped_data.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            with open('variables_on_fire_new.csv', 'w', newline='') as csvNew:
                #fieldnames = ['Latitude', 'Longitude', 'Temp1']
                fieldnames = ['Date', 'Latitude', 'Longitude', 'Leaf_Wetness','Elevation',  'Drought', 'Lightning_Stikes', 'Precipitation', 'Relative_Humidity', 'Soil_Moisture', 'Solar_Power', 'Temperature', 'Wind_Speed', 'Atmospheric_Pressure', 'isFire']
                csv_write = csv.DictWriter(csvNew, fieldnames, delimiter=',')
                csv_write.writeheader()
                for row in reader:
                    req = request(row['Started'], row['Extinguished'], interval, row['Latitude'], row['Longitude'], None)
                    print('Done')
                    req = req.replace(';', ',')
                    req_new = StringIO(req)
                    csv_response = csv.DictReader(req_new, delimiter=',')
                    for line in csv_response:
                        #csv_write.writerow({'Latitude': row['Latitude'], 'Longitude': row['Longitude'], 'Temp1': line['t_max_2m_24h:C']})
                        csv_write.writerow({'Date': line['validdate'],
                                            'Latitude': row['Latitude'],
                                            'Longitude': row['Longitude'],
                                            'Leaf_Wetness': line['leaf_wetness:idx'],
                                            'Elevation': line['elevation:m'],
                                            'Drought': line['drought_index:idx'],
                                            'Lightning_Stikes': line[f'lightning_strikes_10km_{interval}h:x'],
                                            'Precipitation': line[f'precip_{interval}h:mm'],
                                            'Relative_Humidity': line['relative_humidity_50m:p'],
                                            'Soil_Moisture': line['soil_moisture_index_-15cm:idx'],
                                            'Solar_Power': line['solar_power:kW'],
                                            'Temperature': line[f't_max_200m_{interval}h:C'],
                                            'Wind_Speed': line[f'wind_speed_mean_200m_{interval}h:kmh'],
                                            'Atmospheric_Pressure': line[f'pressure_mean_200m_{interval}h:Pa'],
                                            'isFire': '1'})
                    counter += 1
                    print(f'Finished random: {counter}')
                    break

getData()

def add_acres_burned():
    acres_burned = []
    with open('California_Fire_Incidents.csv', 'r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not(row['Latitude'] == '0.0'):
                if row['AcresBurned']:
                    acres_burned.append(row['AcresBurned'])
                else:
                    acres_burned.append('0')
        with open('regression_data_copy.csv', 'r', newline='') as csvOld:
            with open('regression_data_with_acres_burned.csv', 'w', newline='') as csvNew:
                fieldnames = ['Leaf_Wetness',
                            'Elevation', 
                            'Drought', 
                            'Lightning_Stikes', 
                            'Precipitation', 
                            'Relative_Humidity', 
                            'Soil_Moisture', 
                            'Solar_Power', 
                            'Temperature', 
                            'Wind_Speed', 
                            'Atmospheric_Pressure', 
                            'AcresBurned']
                reader = csv.DictReader(csvOld, delimiter=',')
                writer = csv.DictWriter(csvNew, fieldnames, delimiter=',')
                writer.writeheader()
                i = -1
                for line in reader:
                    i += 1
                    writer.writerow({'Leaf_Wetness': line['Leaf_Wetness'],
                                        'Elevation': line['Elevation'],
                                        'Drought': line['Drought'],
                                        'Lightning_Stikes': line[f'Lightning_Stikes'],
                                        'Precipitation': line[f'Precipitation'],
                                        'Relative_Humidity': line['Relative_Humidity'],
                                        'Soil_Moisture': line['Soil_Moisture'],
                                        'Solar_Power': line['Solar_Power'],
                                        'Temperature': line['Temperature'],
                                        'Wind_Speed': line['Wind_Speed'],
                                        'Atmospheric_Pressure': line['Atmospheric_Pressure'],
                                        'AcresBurned': acres_burned[i]})                    




















































