from shiny import ui
from shinywidgets import output_widget

from faicons import icon_svg

page_id = 'welcome'

def welcome_page(tab_name):

    return ui.nav_panel(' Welcome!',
                        ui.page_fluid(output_widget("timeline", fillable=True)),
                        icon=icon_svg('gamepad'),
                        value=tab_name)