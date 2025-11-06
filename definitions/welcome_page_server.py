
from definitions.welcome_page_backend import make_timeline_agechild
from shinywidgets import render_widget  


def welcome_reactivity(input, output):

    @output
    @render_widget
    def timeline():
        return make_timeline_agechild()