import panel as pn
import pandas as pd
import numpy as np
import hvplot.pandas  # For charts

# Fake data
matches = pd.DataFrame({
    "Date": pd.date_range("2024-01-01", periods=10),
    "Home": ["PSG", "Lyon", "Marseille", "Nice", "Rennes"] * 2,
    "Away": ["Lille", "Monaco", "Strasbourg", "Nantes", "Lens"] * 2,
    "Score": ["2-1", "0-0", "3-2", "1-1", "0-2"] * 2
})

standings = pd.DataFrame({
    "Team": ["PSG", "Nice", "Monaco", "Lille", "Rennes"],
    "Points": [45, 39, 36, 33, 30],
    "GF": [40, 28, 31, 25, 22],
    "GA": [15, 18, 20, 21, 22],
}).set_index("Team")

# Simple chart
standings_chart = standings.hvplot.bar(
    y="Points", title="Classement (points)", width=500
)

# Build view
home_view = pn.Column(
    "## 🏠 Accueil — Vue générale",
    "### Derniers matchs joués :",
    pn.widgets.Tabulator(matches, height=250),
    "### Classement actuel :",
    pn.widgets.Tabulator(standings, height=200),
    "### Graphique des points :",
    standings_chart
)
