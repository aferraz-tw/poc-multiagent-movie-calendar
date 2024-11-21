import mlflow
from mlflow.tracking import MlflowClient

def get_best_crew():
    runs = mlflow.search_runs(order_by=["metrics.accuracy DESC"])

    best_run = runs.iloc[0]
    run_id = best_run.run_id
    
    client = MlflowClient()
    best_model_version = client.search_model_versions(f"run_id='{run_id}'")[0]
    
    model_uri = f"models:/{best_model_version.name}/{best_model_version.version}"
    loaded_model = mlflow.pyfunc.load_model(model_uri=model_uri)

    return loaded_model

