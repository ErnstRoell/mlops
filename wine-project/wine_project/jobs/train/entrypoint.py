from wine_project.common import Job
import pandas as pd 
from sklearn.linear_model import LinearRegression
from sklearn.model_selection  import train_test_split
import mlflow
import mlflow.sklearn
import os

class TrainJob(Job):

    def launch(self):
        self.logger.info("Starting Training Script")
        mlflow.set_experiment("/Shared/dbx/wine_project")
        with mlflow.start_run(run_name="YOUR_RUN_NAME") as run:
            
            wine_data = pd.read_csv('/dbfs/mnt/data/winequality-red.csv',sep=";")
            wine_data.head()

            features = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar','chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density','pH', 'sulphates', 'alcohol']
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
            
            mlflow.set_registry_uri(os.getenv("REGISTRY_URI"))
            # Log the sklearn model and register as version 1
            mlflow.sklearn.log_model(
                sk_model=regressor,
                artifact_path="sklearn-model",
                registered_model_name="sk-learn-linear-reg-model"
            )        


if __name__ == "__main__":
    job = TrainJob()
    job.launch()
