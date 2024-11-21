from crewai_tools import tool
from crewai_tools import SerperDevTool


@tool("Busca informações na web")
def search_about_movies_in_web(search_query: str):
    """Busca informações na Internet. Exemplo de como usar: search_about_movies_in_web('data estreia <nome-filme> no Brasil em 2024')"""
    search_mechanism = SerperDevTool(location="Brazil", hl="pt-br")
    search_results = search_mechanism.run(search_query=search_query)
    return search_results
