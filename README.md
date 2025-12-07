# Ligue 1 match predictions

Welcome to this project focused on predicting the outcomes of Ligue 1 football matches using data science techniques!

# Project objectives

- Collect, clean and aggregate Ligue 1 match data across multiple seasons
- Build a structured and reproducible data preprocessing pipeline
- Perform feature engineering to extract meaningful insights from raw match data
- Train and evaluate machine learning models to predict match results
- Visualize results and future predictions with an interactive platform

# Results / added value
- Prediction of a final result football Ligue 1 match (home win, draw, away win) with more than 60% accuracy
- According to the previous prediction, prediction of the goals scored by the two teams involved in the match
- Creation of a dashboard dedicated to interactive exploration and scenario analysis

# How to use this repo?

Before all the steps below, you can create a virtual environment from the requirements.txt file in the root of this repo.

After setting up the environment, you can run the entire pipeline, from cleaning to modeling. The project workflow is organized into notebooks located in the notebooks directory:
- 01-cleaning notebook: clean raw data (remove unnecessary columns, rename columns/values). Input is therefore raw data files, output is cleaned dataframes
- 02-preprocessing notebook: generate features/indicators for predictions, such as team performance in recent matches and head-to-head history. More details about created indicators in this section are in the Preprocessing class documentation or in the config.yaml file
- 03-data_analysis notebook: explore data distributions, correlations, and insights
- 04-modeling notebook: train 2 ML models. First, a primary model to predict match outcomes (home, draw, away). Knowing these issue probabilities, secondary models aim at predicting the number of goals scored by each team

Each notebook is based on the config.yaml file for project-specific settings. These notebooks also rely on utility py files, located in the src directory.

After that, ML models dedicated to predict Ligue 1 match scores will be saved in specific directories indicated in the config.yaml file.

# How to generate a new prediction?

The 'dash' folder in this repo allows to understand the construction of a Streamlit dashboard allowing to generate new predictions.

This dashboard is composed by 4 pages:
- a home page, with general information and hypotheses

<img width="1404" height="753" alt="image" src="https://github.com/user-attachments/assets/22ada752-4338-4e33-915b-7448d1e885f6" />


- a general page, providing an overview of main metrics in football analytics


<img width="1820" height="594" alt="image" src="https://github.com/user-attachments/assets/b0059941-7d92-4caa-8f8e-2314a3f86b7e" />


- a team page, allowing to focus on a certain team


<img width="1823" height="717" alt="image" src="https://github.com/user-attachments/assets/5305b1ac-a67f-4c92-b689-6ea83c4cec8c" />
<img width="1829" height="764" alt="image" src="https://github.com/user-attachments/assets/bebc860a-5bd8-4eb1-b5a7-0e7f85c5c7c6" />


- a prediction page, allowing to predict the score of a Ligue 1 match with previously saved models


<img width="1858" height="656" alt="image" src="https://github.com/user-attachments/assets/1e898326-8e0e-44c3-9284-60f3d90cc0fb" />
<img width="1861" height="851" alt="image" src="https://github.com/user-attachments/assets/6411cd0a-42e7-4a06-9da2-e0317aba729d" />


To use this dashboard, please follow the next instructions:
- clone this repo
- run the 4 notebooks as explained in the 'How to use this repo' section, to load data and models
- in the terminal, activate your virtual environment and then run 'streamlit run dash/app.py' (you need to locate in the root folder)

A web page will open, with the dashboard ready to be used.

# To do list
- improve feature engineering with new variables: coach changes, best player injured, European matches during last week, travel distance,...
- improve preprocessing pipeline to reduce run time
- include absolute and relative features in dashboarding pipeline
