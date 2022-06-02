# Databricks notebook source
import joblib


# COMMAND ----------

from sklearn.externals import joblib

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

dbutils.fs.cp("/mnt/data/winequality-red.csv","/mnt/test",recurse=True)


# COMMAND ----------

dbutils.fs.ls("/mnt/data")

# COMMAND ----------

!pip install scikit-learn

# COMMAND ----------

import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection  import train_test_split
wine_data = pd.read_csv('/dbfs/mnt/data/winequality-red.csv',sep=";")
wine_data.head()

# COMMAND ----------

wine_data.describe() 

# COMMAND ----------

correlation = wine_data.corr()
print(correlation)
import matplotlib.pyplot as plt
fig = plt.subplots(figsize=(10,10))
sns.heatmap(correlation,vmax=1,square=True,annot=True,cmap='Blues')

# COMMAND ----------

features = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
       'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
       'pH', 'sulphates', 'alcohol']
x = wine_data[features]
y = wine_data['quality']
regressor = LinearRegression()
regressor.fit(x_train,y_train)
#plotting features vs quality
sns.pairplot(wine_data,x_vars=features,y_vars='quality',kind='reg',size=7,aspect=0.5)

# COMMAND ----------

x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=3)


# COMMAND ----------

regressor = LinearRegression()
regressor.fit(x_train,y_train)

# COMMAND ----------

accuracy = regressor.score(x_test, y_test)
"Accuracy: {}%".format(int(round(accuracy * 100)))

# COMMAND ----------

!pip freeze | grep "sklearn"

# COMMAND ----------

import mlflow
import mlflow.sklearn

with mlflow.start_run(run_name="YOUR_RUN_NAME") as run:
    registry_uri = f'databricks://cmr:cmr'
    mlflow.set_registry_uri(registry_uri)
    wine_data = pd.read_csv('/dbfs/mnt/data/winequality-red.csv',sep=";")
    wine_data.head()

    features = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
           'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density','pH', 'sulphates', 'alcohol']
    x = wine_data[features]
    y = wine_data['quality']
    x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=3)

    regressor = LinearRegression()
    regressor.fit(x_train,y_train)
    accuracy = regressor.score(x_test, y_test)
    # Log parameters and metrics using the MLflow APIs
    mlflow.log_param("features",str(features))
    mlflow.log_param("accuracy", accuracy)
    mlflow.log_metrics({"accuracy": accuracy, "metric_2": 0.5 + 1})

    # Log the sklearn model and register as version 1
    mlflow.sklearn.log_model(
        sk_model=regressor,
        artifact_path="sklearn-model",
        registered_model_name="sk-learn-linear-reg-model"
    )

# COMMAND ----------


