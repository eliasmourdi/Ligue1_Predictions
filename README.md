# Ligue 1 match predictions

Welcome to this project focused on predicting the outcomes of Ligue 1 football matches using data science techniques!

# Project objectives

- Collect, clean and aggregate Ligue 1 match data across multiple seasons
- Build a structured and reproducible data preprocessing pipeline
- Perform feature engineering to extract meaningful insights from raw match data
- Train and evaluate machine learning models to predict match results
- Visualize results and future predictions with an intercative platform

# How to use this repo?

Before all the steps below, you can create a virtual environment from the requirements.txt file in the root of this repo.

After setting up the environment, you can run the entire pipeline, from cleaning to modeling. The project workflow is organized into notebooks located in the notebooks directory:
- 01-cleaning notebook: clean raw data (remove unnecessary columns, rename columns/values). Input is therefore raw data files, output is cleaned dataframes
- 02-preprocessing notebook: generate features/indicators for predictions, such as team performance in recent matches and head-to-head history. More details about created indicators in this section are in the Preprocessing class documentation or in the config.yaml file
- 03-data_analysis notebook: explore data distributions, correlations, and insights
- 04-modeling notebook: train 2 ML models. First, a primary model to predict match issues (home, draw, away). Knowing these issue probabilities, secondary models aim at predicting the number of goals scored by each team

Each notebook is based on the config.yaml file for project-specific settings. These notebooks also rely on utility py files, located in the src directory.

After that, ML models dedicated to predict Ligue 1 match scores will be saved in specific directories indicated in the config.yaml file.

# How to generate a new prediction?

The 'dash' folder in this repo allows to understand the construction of a dashboard allowing to generate new predictions.

This dashboard is composed by 4 pages:
- a home page, with general information and hypotheses

<img width="1390" height="737" alt="image" src="https://github.com/user-attachments/assets/d6d3a35f-f219-4568-927b-753a9acd885f" />

- a general page, providing an overview of main metrics in football analytics

<img width="1833" height="767" alt="image" src="https://github.com/user-attachments/assets/dca91597-7761-4a26-9c7d-d6e89c92845e" />

- a team page, allowing to focus on a certain team

<img width="1845" height="773" alt="image" src="https://github.com/user-attachments/assets/46a0479b-107f-485e-b35b-ceaeda2948ec" />
<img width="1498" height="833" alt="image" src="https://github.com/user-attachments/assets/91190d2c-1221-4c72-9ff2-c361f594589b" />

- a prediction page, allowing to predict the score of a Ligue 1 match with previously saved models

<img width="1815" height="753" alt="image" src="https://github.com/user-attachments/assets/80ac117b-bd42-40a1-a526-e98672bfe5d2" />
<img width="1839" height="838" alt="image" src="https://github.com/user-attachments/assets/e4e90962-48ee-4cb0-a240-b30f634e0143" />

For that purpose, and therefore to use this dashboard, please follow the next instructions:
- clone this repo
- run the 4 notebooks as explained in the 'How to use this repo' section, to load data and models
- in the terminal, activate your virtual environment and then run 'streamlit run dash/app.py' (you need to locate in the root folder)

A web page will open, with the dashboard ready to be used.


