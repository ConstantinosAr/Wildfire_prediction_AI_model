import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from matplotlib import pyplot as plt
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from keras.models import model_from_json
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline

# load csv values
dataset = pd.read_csv('regression_data.csv').values

# input, output data
X = dataset[:, :dataset.shape[1]-1]
Y = dataset[:, dataset.shape[1]-1]

Scaler = MinMaxScaler(feature_range=(0, 1))
Scaler.fit(X)
X_norm = Scaler.transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)

model = Sequential()
model.add(Dense(X.shape[1]-1, input_dim=dataset.shape[1]-1, kernel_initializer='normal', activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(15, activation='relu'))
model.add(Dense(1, kernel_initializer='normal'))
# Compile model
model.compile(loss='mse', optimizer='adam')

# fit the keras model on the dataset
fitted = model.fit(X_train, Y_train, epochs=100, batch_size=10, verbose=0)

pred_train = model.predict(X_train)
#print(np.sqrt(mean_squared_error(Y_train,pred_train)))

pred = model.predict(X_test)
#print(np.sqrt(mean_squared_error(Y_test,pred)))

# serialize model to JSON
model_json = model.to_json()
with open("regression_model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("regression_model.h5")


'''
# load json and create model
json_file = open('regression_model.json', 'r')
loaded_regression_model_json = json_file.read()
json_file.close()
loaded_regression_model = model_from_json(loaded_regression_model_json)
# load weights into new model
loaded_regression_model.load_weights("regression_model.h5")
'''
'''
# estimator = KerasRegressor(build_fn=baseline_model, epochs=100, batch_size=5, verbose=0)
# kfold = KFold(n_splits=10)
# results = cross_val_score(estimator, X, Y, cv=kfold)
# print("Baseline: %.2f (%.2f) MSE" % (results.mean(), results.std()))

#pred_test = model.predict(X_test)

# Calculates and prints r2 score of training and testing data
#print("The R2 score on the Train set is:\t{:0.3f}".format(r2_score(Y_train, pred_train)))
#print("The R2 score on the Test set is:\t{:0.3f}".format(r2_score(Y_test, pred)))
'''

'''
# summarize history for loss
plt.plot(fitted.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
'''
