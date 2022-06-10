# Wildfire Prediction AI Model
Model to warn for wildfires and predict severity

## About
This project was created for NASA's Space Apps Challenge\
For more information please refer to our team site:\
https://2021.spaceappschallenge.org/challenges/statements/warning-things-are-heating-up/teams/brute-force-3/project

## Run Demo
To run a short display demo, use main.py.\
You will be prompted with a window to select a date.\
Continuing will generate a map with points as an html file.

## Project Files
Models are saved under regressionModel.py and classificationModel.py\
The regression model requires the regression_data.csv file to run.\
The classification model requires the random_data_without_fire.csv and variables_on_fire.csv files to run.

Data generation functions are saved under data_functions.py\
Interface functions are saved under interface_functions.py

## Libraries required
To use the model you need sklearn, tensorflow, keras, pandas, numpy, matplotlib, h5py

