from shiny import ui
from faicons import icon_svg

# Individual component groups ==========================================================================================
# page_id = 'datawiki'


def datawiki_page(tab_name):
    return ui.nav_panel(" DataWiki map",
                        'TODO',
                        icon=icon_svg('book-atlas'),
                        value=tab_name)
