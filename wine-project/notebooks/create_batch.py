# COMMAND ----------

dbutils.fs.cp("/mnt/data/winequality-red.csv","/mnt/test",recurse=True)
dbutils.fs.ls("/mnt/data")

# COMMAND ----------



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

import mlflow
model_path="models:/sk-learn-linear-reg-model/None"
model = mlflow.pyfunc.load_model(model_path)
model.predict(x_test)

# COMMAND ----------

# Preprocess
import pandas as pd 
wine_data = pd.read_csv('/dbfs/mnt/data/winequality-red.csv',sep=";")
wine_data.head()
features = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
       'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
       'pH', 'sulphates', 'alcohol']
x = wine_data[features]

# Run the batch scoring
import mlflow
model_path="models:/sk-learn-linear-reg-model/None"
model = mlflow.pyfunc.load_model(model_path)
wine_data["predicted"] = model.predict(x)
wine_data.to_csv("/dbfs/mnt/data/winequality-red-enriched.csv")

# COMMAND ----------


