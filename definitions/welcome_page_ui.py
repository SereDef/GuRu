from shiny import ui
from shinywidgets import output_widget

from faicons import icon_svg
from definitions.terms_and_styles import placeholder_panel

page_id = 'welcome'

def welcome_page(tab_name):

    return ui.nav_panel(' Welcome!',
                        placeholder_panel('This *Timeline* plot is a placeholder, the age spans and assessment ids need to be cleaned and updated with additional info.' \
                            '&ensp;A **sample size overlap tool** based on the same data is also currently under development'),
                        ui.page_fluid(output_widget("timeline", fillable=True)),
                        icon=icon_svg('gamepad'),
                        value=tab_name)