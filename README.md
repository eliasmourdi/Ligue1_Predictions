# Ligue 1 match predictions

Welcome to this project focused on predicting the outcomes of Ligue 1 football matches using data science techniques.

# Project objectives

- Collect, clean and aggregate Ligue 1 match data across multiple seasons
- Build a structured and reproducible data preprocessing pipeline
- Perform feature engineering to extract meaningful insights from raw match data
- Train and evaluate machine learning models to predict match results
- Improve the models from model results insights

# How to use this repo?

Before all the steps below, you can create a virtual environment from the requirements.txt file in the root of this repo.

After setting up the environment, you can run the entire pipeline, from cleaning to modeling. The project workflow is organized into notebooks located in the notebooks directory:
- 01-cleaning notebook: clean raw data (remove unnecessary columns, rename columns/values). Input is therefore raw data files, output is cleaned dataframes.
- 02-preprocessing notebook: generate features/indicators for predictions, such as team performance in recent matches and head-to-head history. More details about created indicators in this section are in the Preprocessing class documentation or in the config.yaml file.
- 03-data_analysis notebook: explore data distributions, correlations, and insights.
- 04-modeling notebook: train 2 ML models. First, a primary model to predict match issues (home, draw, away). Knowing these issue probabilities, secondary models aim at predicting the number of goals scored by each team.

Each notebook is based on the config.yaml file for project-specific settings. These notebooks also rely on utility py files, located in the src directory.

After that, ML models dedicated to predict Ligue 1 match scores will be saved in specific directories indicated in the config.yaml file.
