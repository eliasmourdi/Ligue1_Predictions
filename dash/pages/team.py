import panel as pn
import numpy as np
import pandas as pd
import hvplot.pandas

teams = ["PSG", "Lyon", "Marseille", "Nice", "Rennes", "Lille", "Monaco"]

team_selector = pn.widgets.Select(name="Choisir une équipe", options=teams)

# Fake matches
def get_team_matches(team):
    return pd.DataFrame({
        "Date": pd.date_range("2024-01-01", periods=5),
        "Opponent": ["Lille", "Monaco", "Rennes", "Nice", "Strasbourg"],
        "Score": ["2-1", "1-3", "0-0", "4-2", "1-1"]
    })

def get_team_form(team):
    df = pd.DataFrame({"Journée": range(1, 11), "Points": np.random.randint(0, 3, 10)})
    return df.hvplot.line(x="Journée", y="Points", title=f"Forme de {team}")

@pn.depends(team=team_selector)
def team_view_fn(team):
    return pn.Column(
        f"## {team}",
        "### Derniers matchs :",
        pn.widgets.Tabulator(get_team_matches(team)),
        "### Forme récente :",
        get_team_form(team)
    )

team_view = pn.Column("## 🏳️‍🌈 Analyse d'équipe", team_selector, team_view_fn)
