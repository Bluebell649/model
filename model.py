# -*- coding: utf-8 -*-
"""Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UwxkUUh4ROBouKyTW_wAaMS2ZlzVd8L-
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

!pip install gdown

#collapse-output
import gdown

url = 'https://drive.google.com/file/d/1kBeVKUya96vO1l9IEz98Tl9lkqopcNUH/view?usp=sharing'
output_path = 'transection_join.csv'
gdown.download(url, output_path, quiet=False,fuzzy=True)

store_sales = pd.read_csv('transection_join.csv')
store_sales.head(10)

store_sales.info()

"""# Model (prophet)




"""

store_sales['date'] = pd.to_datetime(store_sales['date_time_of_transaction'])

store_sales = store_sales[['date','dollar_sales']]

store_sales['date'] = store_sales['date'].dt.to_period('M')
monthly_sales = store_sales.groupby('date').sum().reset_index()

monthly_sales['date'] = monthly_sales['date'].dt.to_timestamp()
monthly_sales

plt.figure(figsize=(15,5))
plt.plot(monthly_sales['date'], monthly_sales['dollar_sales'])
plt.xlabel('Date')
plt.xlabel('dollar_sales')
plt.title("Monthly Customer Sales")
plt.show()

#Rename the columns to 'ds' and 'y'
monthly_sales = monthly_sales.rename(columns={'date':'ds', 'dollar_sales':'y'})

# pip install prophet
from prophet import Prophet
# creating the prophet model object
model = Prophet()
# fitting the data
model.fit(monthly_sales)

future_dates = model.make_future_dataframe(periods=365*2, freq='D')

forecast = model.predict(future_dates)

# Plot the forecasted sales
import matplotlib.pyplot as plt
plt.figure()
model.plot(forecast, xlabel='Date', ylabel='Sales Qty')
plt.title('Sales Forecast')
plt.show()

"""# Model (XGBoost)"""

import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics

store_sales.shape

store_sales.isnull().sum()

# prompt: drop colum product_size

store_sales = store_sales.drop('product_size', axis=1)

store_sales.describe()

sns.set()

# prompt: keep only month and year in date_time_of_transaction

import pandas as pd
store_sales['date_time_of_transaction'] = pd.to_datetime(store_sales['date_time_of_transaction'])
store_sales['date_time_of_transaction'] = store_sales['date_time_of_transaction'].dt.strftime('%Y-%m')

store_sales.head(10)

encoder = LabelEncoder()

store_sales['product_description'] = encoder.fit_transform(store_sales['product_description'])
store_sales['commodity'] = encoder.fit_transform(store_sales['commodity'])
store_sales['brand'] = encoder.fit_transform(store_sales['brand'])
store_sales['date_time_of_transaction'] = encoder.fit_transform(store_sales['date_time_of_transaction'])

X = store_sales.drop(columns='units', axis=1)
Y = store_sales['units']

print(X)

print(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

print(X.shape, X_train.shape, X_test.shape)

regressor = XGBRegressor()

regressor.fit(X_train, Y_train)

# Prediction on training data
training_data_prediction = regressor.predict(X_train)

# R squared value
r2_train = metrics.r2_score(Y_train, training_data_prediction)

print('R square value = ', r2_train)

# Prediction on testing data
test_data_prediction = regressor.predict(X_test)

# R squared value
r2_test = metrics.r2_score(Y_test, test_data_prediction)

print('R square value = ', r2_test)