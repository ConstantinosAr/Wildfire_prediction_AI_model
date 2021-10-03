import numpy
import csv
import requests
from io import StringIO
from tkinter import *
from tkcalendar import *
from tktimepicker import AnalogPicker
import os
import folium
import json
import random
import math




def calculate():

    
    create_map()

    os.startfile('map.html')


# ======================================================
#                CREATE MAP GRID DATA   
# ======================================================

def locations():
    locations = []
    #1st square
    for long in range(-121, -118):
        for lat in range(36,39):
            new_elem = (lat,long)
            if new_elem not in locations:
                locations.append(new_elem)

    #2nd square        
    for long in range(-123, -119):
        for lat in range(38,41):
            new_elem = (lat,long)
            if new_elem not in locations:
                locations.append(new_elem)
                
    #3rd square        
    for long in range(-124, -120):
        for lat in range(40,43):
            new_elem = (lat,long)
            locations.append(new_elem)
    return locations



# ======================================================
#                     DEMO FUNCTION   
# ======================================================

def generate_random_warnings():
    locations_lst = locations()
    locations_lst_new = []

    for location in locations_lst:
        x = random.randint(1,10)                                        # FIRE WARNING AI MODEL RETURNS WARNING LEVELS (GREEN, ORANGE, RED)
        if x < 7:
            warning = 'green'
        elif x < 9:
            warning = 'orange'
        else:
            warning = 'red'

        if warning == 'red' or warning == 'orange':                                 # IMPACT PREDICTION AI MODEL RETURN RADIUS OF DANGER ZONE
            r = random.randint(1000,10000)
            locations_lst_new.append([location[0], location[1], warning, r])
        else:
            locations_lst_new.append([location[0], location[1], warning, 0])

    return locations_lst_new




# ======================================================
#                    CREATE MAP   
# ======================================================

def create_map():
    m = folium.Map(location=[38, -122], zoom_start=6.5, tiles="Stamen Terrain")
    locations_lst_new = generate_random_warnings()
    for location in locations_lst_new:
        if location[2] == 'green':
            folium.Marker(
                location=[location[0], location[1]],
                popup="Safe zone",
                icon=folium.Icon(color="green", icon='fire'),
            ).add_to(m)

        if location[2] == 'orange':
            folium.Marker(
                location=[location[0], location[1]],
                popup="Warning zone",
                icon=folium.Icon(color="orange", icon='fire'),
            ).add_to(m)

        if location[2] == 'red':
            folium.Marker(
                location=[location[0], location[1]],
                popup="Danger zone",
                icon=folium.Icon(color="red", icon="fire"),
            ).add_to(m)
        
        if location[3] != 0 and location[2] == 'red':
            folium.vector_layers.Circle((location[0], location[1]), radius=location[3], color="red").add_to(m)
        if location[3] != 0 and location[2] == 'orange':
            folium.vector_layers.Circle((location[0], location[1]), radius=location[3], color="orange").add_to(m)
    

    m.save("map.html")



# ======================================================
# GET WARNING PREDICTION FOR RANDOM MAP DATA PREDICTIONS
# ======================================================

def point_predictions(amount, model):
    '''
    Predictions for predefined points for demonstration.
    @:param amount  number of points to be generated
    :return: location coordinates and probability
    '''
    # load dataset
    no_fire_dataset = pd.read_csv('random_data_without_fire.csv').values
    fire_dataset = pd.read_csv('variables_on_fire.csv').values

    no_fire_rows = [np.random.randint(0, no_fire_dataset.shape[0] - 1) for i in range(int(amount/2))]
    fire_rows = [np.random.randint(0, fire_dataset.shape[0] - 1) for i in range(int(amount / 2))]

    # split to input and output
    X_no_fire = no_fire_dataset[no_fire_rows, 3:no_fire_dataset.shape[1] - 1]
    no_fire_coords = no_fire_dataset[no_fire_rows, 1:3]
    X_fire = fire_dataset[fire_rows, 3:fire_dataset.shape[1] - 1]
    fire_coords = fire_dataset[fire_rows, 1:3]

    # cast data from object to float
    X_no_fire = np.array(X_no_fire, dtype=np.float)
    no_fire_coords = np.array(no_fire_coords, dtype=np.float)
    X_fire = np.array(X_fire, dtype=np.float)
    fire_coords = np.array(fire_coords, dtype=np.float)

    # stack testing data
    X = np.vstack((X_fire, X_no_fire))
    coords = np.vstack((fire_coords, no_fire_coords))

    # evaluate data
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    probability = model.predict(X, verbose=0)

    return np.hstack((coords, probability))


# ==================================================================
#  USE WARNING AI MODEL FOR WARNING LEVEL PREDICTION FOR GRID DATA   
# ==================================================================

def csv_point_predictions(filename):
    '''
    Predictions for points in a csv file.
    @:param filename  cvs file name
    :return: location coordinates and probability
    '''
    # load dataset
    dataset = pd.read_csv(filename).values

    # split to input and output
    X = dataset[:, 2:dataset.shape[1]]
    coords = dataset[:, :2]

    # cast data from object to float
    X = np.array(X, dtype=np.float)
    coords = np.array(coords, dtype=np.float)

    # evaluate data
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    probability = model.predict(X, verbose=0)

    return np.hstack((coords, probability))