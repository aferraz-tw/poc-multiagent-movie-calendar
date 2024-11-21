import pandas as pd
import mlflow

from datetime import datetime
from movies_newsletter_multi_agent.crew import MoviesNewsletterMultiAgentCrew
from mlflow.models import infer_signature

mlflow.set_tracking_uri("http://localhost:5000")

def save_crew(crew):
   input_example = {"movie_name": ["Anora"]}
   output_example = {"title" : ["Anora"], "release_date" : [datetime.strptime("01/11/2024", "%d/%m/%Y")], "comment":["comment"]}
    
   signature = infer_signature(
      pd.DataFrame(input_example),
      pd.DataFrame(output_example),
   )
   mlflow.pyfunc.log_model(
         artifact_path="models/crewai",
         python_model=crew,
         registered_model_name="multi-agent-movies-br-release",
         signature=signature,
      )
             
   mlflow.log_params({
         "agents_config": crew.agents_config,
         "tasks_config": crew.tasks_config,
         "release_serch_llm_model": crew.release_serch_llm_model,
         "pydantic_formatting_llm_model": crew.pydantic_formatting_llm_model,
   })
   
def fill_null_dates_with_nat(df_test_results):
   df_test_results['release_date'] = df_test_results['release_date'].fillna(pd.Timestamp)
   df_test_results['expected_release_date'] = pd.to_datetime(df_test_results['expected_release_date'], dayfirst=True).fillna(pd.Timestamp)
   
   return df_test_results

def save_test_set(df_test_set, mlflow_run):
   csv_path = f'../data/experiments_results/test_set_{mlflow_run.info.run_id}.csv'
   df_test_set.to_csv(csv_path, index=False)
   mlflow.log_artifact(csv_path)

def evaluate_crew(crew, mlflow_run):
   df_test = pd.read_csv("../data/test-set.csv")
      
   X_test = df_test[['movie_name']]              
   y_pred = crew.predict(context={}, model_input=X_test)
      
   df_test_results = pd.concat([df_test, y_pred], axis=1)
   df_test_results = fill_null_dates_with_nat(df_test_results)
   
   eval_result = df_test_results['release_date'] == df_test_results['expected_release_date']
   accuracy = eval_result.mean() * 100
   
   print(f"Acc: {accuracy}")   
   mlflow.log_metric(key="accuracy", value=accuracy)

   save_test_set(df_test_results, mlflow_run)



if __name__ == "__main__":
   mlflow.set_tracking_uri("http://localhost:5000")
   
   release_serch_llm_model="gemini/gemini-1.5-pro"
   pydantic_formatting_llm_model="gemini/gemini-1.5-pro"
   
   crew = MoviesNewsletterMultiAgentCrew(release_serch_llm_model=release_serch_llm_model,
                                         pydantic_formatting_llm_model=pydantic_formatting_llm_model,)
    
   # Start an MLFlow run
   with mlflow.start_run() as mlflow_run: 
      save_crew(crew)     
      evaluate_crew(crew, mlflow_run)
