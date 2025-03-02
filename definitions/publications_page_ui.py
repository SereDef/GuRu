from shiny import ui
from faicons import icon_svg

# Individual component groups ==========================================================================================
# page_id = 'publications'


def publications_page(tab_name):
    return ui.nav_panel(" Publications",
                        'TODO',
                        icon=icon_svg('newspaper'),
                        value=tab_name)
