from shiny import ui
from faicons import icon_svg

# Individual component groups ==========================================================================================
# page_id = 'publications'


def publications_page(tab_name):
    return ui.nav_panel(" Publications",
                        ui.markdown('This section is under construction. Check out the [PURE website](https://pure.eur.nl/en/publications/) for a complete list of publications'),
                        icon=icon_svg('newspaper'),
                        value=tab_name)
