from shiny import App, ui, render, reactive
from pathlib import Path

from definitions.overview_page_ui import overview_page
from definitions.variable_page_ui import variable_page
from definitions.datawiki_page_ui import datawiki_page
from definitions.publications_page_ui import publications_page

from definitions.overview_page_server import overview_reactivity
from definitions.variable_page_server import variable_reactivity

from definitions.terms_and_styles import variable_time_choices

here = Path(__file__).parent

css_file = here / 'css' / 'custom_styles.css'
logo_img = here / 'www'

app_ui = ui.page_fluid(
    ui.include_css(css_file),
    ui.page_navbar(
        # ui.nav_spacer(),
        overview_page(tab_name='overview_page'),
        variable_page(tab_name='variable_page'),
        datawiki_page(tab_name='datawiki_page'),
        publications_page(tab_name='publications_page'),

        id='main_navbar',
        selected='variable_page',  # 'overview_page',
        position='fixed-top',  # Navbar is pinned at the top
        bg='white',
        fillable=True,
        padding=[130, 20, 20],  # top, left-right, bottom in px
        window_title='GuRu',
        title=ui.img(src='GuRu_logo.png', alt='Generation R data dictionary app', height='100px'),
    )
)


def server(input, output, session):

    overview_reactivity(input, output)
    variable_reactivity(input, output)


app = App(app_ui, server, static_assets=logo_img)
