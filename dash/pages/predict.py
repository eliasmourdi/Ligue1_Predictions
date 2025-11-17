import panel as pn
import numpy as np

teams = ["PSG", "Lyon", "Marseille", "Nice", "Rennes", "Lille", "Monaco"]

home_team = pn.widgets.Select(name="Équipe domicile", options=teams)
away_team = pn.widgets.Select(name="Équipe extérieure", options=teams)

predict_button = pn.widgets.Button(name="Prédire", button_type="primary")
prediction_pane = pn.pane.Markdown("### Score prédit : _aucune prédiction_")

def predict_score(event):
    home_goals = np.random.poisson(1.5)
    away_goals = np.random.poisson(1.2)
    prediction_pane.object = f"### Score prédit : **{int(home_goals)} - {int(away_goals)}**"

predict_button.on_click(predict_score)

predict_view = pn.Column(
    "## 🎯 Prédictions",
    "Choisissez 2 équipes pour obtenir une prédiction :",
    home_team,
    away_team,
    predict_button,
    pn.Spacer(height=20),
    prediction_pane
)
