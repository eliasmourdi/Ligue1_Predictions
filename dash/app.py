import panel as pn
pn.extension()  # IMPORTANT : pas de template ici !

from pages.home import home_view
from pages.team import team_view
from pages.predict import predict_view

def app():
    tmpl = pn.template.FastListTemplate(
        title="🏆 Ligue 1 Dashboard",
        main=[home_view],
        sidebar=[pn.pane.Markdown("## Navigation"),
                 pn.layout.Divider(),
                 pn.pane.Markdown("[🏠 Accueil](?page=home)"),
                 pn.pane.Markdown("[👕 Équipes](?page=team)"),
                 pn.pane.Markdown("[⚽ Prédictions](?page=predict)")],
        theme="default",
    )
    return tmpl


app().servable()
