from wine_project.common import Job
import pandas as pd 
import mlflow
import os

class BatchJob(Job):

    def launch(self):
        self.logger.info("Launching batch job")
        self.logger.info("Running the batch scoring job")

        # Preprocess
        wine_data = pd.read_csv('/dbfs/mnt/data/winequality-red.csv',sep=";")
        wine_data.head()
        features = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
                       'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
                              'pH', 'sulphates', 'alcohol']
        x = wine_data[features]
#        mlflow.set_tracking_uri("databricks://cmr:cmr")
        # Run the batch scoring
        model_path="models:/sk-learn-linear-reg-model/None"
        model = mlflow.pyfunc.load_model(model_path)
        wine_data["predicted"] = model.predict(x)
        wine_data.to_csv("/dbfs/mnt/data/winequality-red-enriched.csv")

        self.logger.info("Batch job finished!")


if __name__ == "__main__":
    job = BatchJob()
    job.launch()
