# Ligue 1 match predictions

Welcome to this project focused on predicting the outcomes of Ligue 1 football matches using data science techniques.

## Project objectives

- Collect, clean and aggregate Ligue 1 match data across multiple seasons
- Build a structured and reproducible data processing pipeline
- Perform feature engineering to extract meaningful insights from raw match data
- Train and evaluate machine learning models to predict match results
- Visualize predictions interactively to improve the model

## To-do list

- Achieve utils.py (with ranking per category functions)
- Create modeling files
- Create a visualization pipeline for post processing and model calibration
- Refactor and organize code (group functions into classes, DAG-style logic)
- Write a tutorial for running all the code


   ### BROUILLON de doc

  Faire un DAG pour que ce soit plus clair

  1) cleaning : on ne garde que les colonnes de date, les équipes, les buts marqués, le résultat final et les côtes des différents bookmarkers. Il suffit de run le notebook et ça nous met les df train et test dans le bon dossier. Une saison pour le test, tout le reste pour le train.
