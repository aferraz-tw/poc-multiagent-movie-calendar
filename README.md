# Generative-AI-Experiments-movies-multiagent

That repository contains a project with the object to generate a release calendar for movies in Brazil.
For movie-nerds is sometimes hard to keep updated with release dates and most aggregated information in the internet are for US dates, which is almost always different from the brazilian agenda.

## The Business Problem

Given a set of movie names, print theirs names ordered by ascending release date. 
If none date has been found it should come at the final of the list, followed by a comment. 

At the moment, movies that were release before 2024 are considered as not found.

### Input example (currently hardcoded):
```
movies_list = ["Anora", "Gladiador 2", "The Piano Lesson", "Conclave", "Emilia Perez", "Blitz", "Saturday Night", "The Brutalist"]
```

### Output example:

```
Anora - 2024-10-31 00:00:00
Gladiador 2 - 2024-11-15 00:00:00
The Piano Lesson - 2024-11-22 00:00:00
Conclave - 2024-12-05 00:00:00
Emilia Perez - 2025-02-06 00:00:00
Blitz - Não encontrei nenhuma informação confiável sobre a data de estreia do filme Blitz nos cinemas brasileiros em 2024. As informações encontradas são sobre a estreia em festivais, streaming (Apple TV+ em 22 de Novembro) ou em outros países.
Saturday Night - Embora haja muitas informações sobre o filme, nenhuma fonte confiável confirma a data de estreia no Brasil.
The Brutalist - Não foi possível encontrar data confiável. O filme será exibido na Mostra Internacional de Cinema de São Paulo em 2024, mas a data de estreia no Brasil para o público em geral ainda não foi divulgada.
```

## Installation Guide

### Prerequisites

You should have installed Python 3.12 or later.

This project uses [uv package manager](https://github.com/astral-sh/uv), so you should have it also installed.

### Installing packages

```
uv sync
```

## Running Crew

### Enviroment Setup

To run this project you should create a fila named ``.env`` with the following enviroment variables:

```
GEMINI_API_KEY=<your-gemini-key>
SERPER_API_KEY=<your-seper-api-key>
```

The gemini key is used for acessing the Gemini models as the "brain" of the agents. You can easily generate a API key [in the AI studio](https://aistudio.google.com/app/apikey) (costs may apply). 

The Serper is API that index Google and allows to run semantic search on its content. It is used to find information about the movies on the internet.
You can generate a free-trial api key to test for 2,500 queries on [their webpage](https://serper.dev/).

### Executing

If using vscode the project contains a couple of usefull launch scripts.
If you wish to manually execute:

#### Execute Crew
```
uv run ./src/inference.py
```

#### Generate new Crew Model
```
uv run ./src/generate_model.py
```

## Solution 


## TODO List
- [x] Add installation Guide
- [x] Get best model instead of hardcoded.
- [x] Enhance Readme.
- [ ] Add movies list as input parameter.
- [ ] Guide to run only with open source models.
- [ ] Add unitests.
- [ ] Generate MLFlow endpoint.
- [ ] How to Monitor solution?
