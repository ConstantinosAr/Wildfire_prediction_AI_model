import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import model_from_json
from matplotlib import pyplot


# load dataset
no_fire_dataset = pd.read_csv('random_data_without_fire.csv').values
fire_dataset = pd.read_csv('variables_on_fire.csv').values

# get balanced data
rowsno = fire_dataset.shape[0]
rows = [np.random.randint(0,no_fire_dataset.shape[0]-1) for i in range(rowsno)]

# split to input and output
X_no_fire = no_fire_dataset[rows,3:no_fire_dataset.shape[1]-1]
Y_no_fire = no_fire_dataset[rows,no_fire_dataset.shape[1]-1]
X_fire = fire_dataset[:,3:fire_dataset.shape[1]-1]
Y_fire = fire_dataset[:,fire_dataset.shape[1]-1]

# convert object arrays to float ones
X_no_fire = np.array(X_no_fire, dtype=np.float)
Y_no_fire = np.array(Y_no_fire, dtype=np.float).reshape((-1,1))
X_fire = np.array(X_fire, dtype=np.float)
Y_fire = np.array(Y_fire, dtype=np.float).reshape((-1,1))

# normalize input
# create scaler for no fire data
X_no_fire_scaler = MinMaxScaler(feature_range=(0,1))
# fit scaler on data
X_no_fire_scaler.fit(X_no_fire)
# apply transform
X_no_fire_norm = X_no_fire_scaler.transform(X_no_fire)

# create scaler for fire data
X_fire_scaler = MinMaxScaler(feature_range=(0,1))
# fit scaler on data
X_fire_scaler.fit(X_fire)
# apply transform
X_fire_norm = X_fire_scaler.transform(X_fire)

# split data to training and testing
X_no_fire_train, X_no_fire_test, Y_no_fire_train, Y_no_fire_test = train_test_split(X_no_fire_norm, Y_no_fire, test_size=0.3)
X_fire_train, X_fire_test, Y_fire_train, Y_fire_test = train_test_split(X_fire_norm, Y_fire, test_size=0.3)

assert (X_no_fire.shape[1] == X_fire.shape[1] and Y_fire.shape[1] == Y_no_fire.shape[1])

X_train = np.vstack((X_fire_train, X_no_fire_train))
Y_train = np.vstack( (Y_fire_train, Y_no_fire_train))
X_test = np.vstack((X_fire_test, X_no_fire_test))
Y_test = np.vstack( (Y_fire_test, Y_no_fire_test))

# define keras model
model = Sequential()
model.add(Dense(25, input_dim=X_fire.shape[1], activation='relu'))
model.add(Dense(25, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
history = model.fit(X_train, Y_train, epochs=100, batch_size=32, validation_data=(X_test, Y_test), verbose=0)

# evaluate the keras model
# training
_, accuracy = model.evaluate(X_train, Y_train, verbose=0)
#print('Training Accuracy: %.2f' % (accuracy*100))

# testing
_, accuracy = model.evaluate(X_test, Y_test, verbose=0)
#print('Testing Accuracy: %.2f' % (accuracy*100))

'''
# plot loss during training
pyplot.subplot(211)
pyplot.title('Loss')
pyplot.plot(history.history['loss'], label='train')
pyplot.subplot(212)
pyplot.title('Val Loss')
pyplot.plot(history.history['val_loss'], label='val_loss')
pyplot.show()
'''

# serialize model to JSON
model_json = model.to_json()
with open("classification_model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("classification_model.h5")


'''
# load json and create model
json_file = open('classification_model.json', 'r')
loaded_classification_model_json = json_file.read()
json_file.close()
loaded_classification_model = model_from_json(loaded_classification_model_json)
# load weights into new model
loaded_classification_model.load_weights("classification_model.h5")
'''