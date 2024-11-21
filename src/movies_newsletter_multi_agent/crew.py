import pandas as pd
import mlflow

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from movies_newsletter_multi_agent.domain.movie import MovieReleaseDate
from movies_newsletter_multi_agent.tools.search_in_web import search_about_movies_in_web


@CrewBase
class MoviesNewsletterMultiAgentCrew(mlflow.pyfunc.PythonModel):
    """MoviesNewsletterMultiAgent crew"""
    
    def __init__(self, *, 
                 release_serch_llm_model="gemini/gemini-1.5-pro",
                 pydantic_formatting_llm_model="gemini/gemini-1.5-pro",
                 verbose=False):
        
        self.release_serch_llm_model = release_serch_llm_model
        self.pydantic_formatting_llm_model = pydantic_formatting_llm_model
        self.verbose = verbose

    @agent
    def release_search_agent(self) -> Agent:
        brain = LLM(model=self.release_serch_llm_model,
                    temperature=0)
        
        return Agent(
            config=self.agents_config["release_search_agent"],
            tools=[search_about_movies_in_web],
            llm=brain,
            verbose=self.verbose,
        )

    @task
    def release_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["release_search_task"],
            verbose=self.verbose,
        )
        
    @agent
    def pydantic_formatter_agent(self) -> Agent:
        brain = LLM(model=self.pydantic_formatting_llm_model,
                    temperature=0)

        return Agent(
            config=self.agents_config["pydantic_formatter_agent"],
            llm=brain,
            verbose=self.verbose,
        )
        
    @task
    def pydantic_formatting_task(self) -> Task:
        return Task(
            config=self.tasks_config["pydantic_formatting_task"],
            verbose=self.verbose,
            output_pydantic=MovieReleaseDate,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MoviesNewsletterMultiAgent crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=self.verbose
        )
        
    def predict(self, context, model_input, params=None) -> pd.DataFrame:
        movie_names = model_input['movie_name'].tolist()
        
        result = []
        
        for movie_name in movie_names:
            
            inputs = {"movie_name": movie_name, 
                      "movie_schema": MovieReleaseDate.model_json_schema()}

            crew_instance = self.crew()
            crew_instance.kickoff(inputs=inputs)
            
            pydantic_result = crew_instance.tasks[1].output.pydantic
            
            error_object = {
                "title": movie_name,
                "comment": "Error",
            }
            
            result.append(pydantic_result.dict() if pydantic_result else error_object)
            
        df_result = pd.DataFrame(result)
        return df_result 
        
    async def predict_async(self, movie_name:str) -> MovieReleaseDate:
        inputs = {"movie_name": movie_name, 
                  "movie_schema": MovieReleaseDate.model_json_schema()}

        crew_instances = self.crew()
        await crew_instances.kickoff_async(inputs=inputs)
        
        pydantic_result = crew_instances.tasks[1].output.pydantic    
        return pydantic_result