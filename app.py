from shiny import App, ui, render, reactive
from pathlib import Path

from definitions.backend_calculations import \
    filter_overview_table, search_overview_table, overview_table_style, overview_table_height, \
    display_measure_description, \
    metadata_table_clean, metadata_table_style, display_variable_info

from definitions.terms_and_styles import overview_time_choices, overview_icon_dict
from definitions.ui_functions import overview_page, variable_page, datawiki_page, publications_page

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
        selected='overview_page',
        position='fixed-top',  # Navbar is pinned at the top
        bg='white',
        fillable=True,
        padding=[130, 20, 20],  # top, left-right, bottom in px
        window_title='GuRu',
        title=ui.img(src='GuRu_logo.png', alt='Generation R data dictionary app', height='100px'),
    )
)


def server(input, output, session):

    # Update the overview UI input --------------------------------------------------
    @reactive.effect
    def _():
        all_time = input.overview_switch_time()

        if all_time:
            ui.update_selectize(id='overview_selected_time',
                                selected=list(overview_time_choices.keys()))

    @reactive.effect
    def _():
        selected_times = input.overview_selected_time()

        if len(selected_times) < len(list(overview_time_choices.keys())):
            ui.update_switch(id='overview_switch_time', value=False)

    # Update the overview table ----------------------------------------------------
    @reactive.Calc
    def _filter_overview_table():
        return filter_overview_table(selected_timepoints=input.overview_selected_time(),
                                     selected_subjects=input.overview_selected_subjects(),
                                     selected_reporters=input.overview_selected_reporters())

    @reactive.Effect
    @reactive.event(input.overview_search_button)
    async def _search_overview_table():
        search_terms = input.overview_search_terms().split(';')

        search_results_table = search_overview_table(table=_filter_overview_table(),
                                                     search_terms=search_terms,
                                                     search_domains=input.overview_search_domains(),
                                                     case_sensitive=input.overview_search_case_sensitive())

        await overview_df.update_data(search_results_table)


    @output
    @render.data_frame
    def overview_df():
        nrow, ncol = _filter_overview_table().shape
        table_style = overview_table_style(nrow, ncol)
        table_height = overview_table_height(nrow)

        return render.DataTable(data=_filter_overview_table(),
                                selection_mode='rows',
                                width='100%',
                                height=table_height,
                                styles=table_style)

    @render.ui
    def overview_legend():
        return ui.markdown(f'&emsp;'
                           f'{overview_icon_dict["mother-self"]} Mother self-report &emsp;'
                           f'{overview_icon_dict["partner-self"]} Partner self-report &emsp;'
                           f'{overview_icon_dict["child-self"]} Child self-report &emsp;'
                           f'{overview_icon_dict["mother-child"]} Mother about the child &emsp;'
                           f'{overview_icon_dict["partner-child"]} Partner about the child &emsp;'
                           f'{overview_icon_dict["teacher-child"]} Teacher about child<br>'
                           f'&emsp;Click on a row to display more information about the measure selected.')

    @reactive.effect
    def _():
        if overview_df.data().shape[0] > 0:
            selected_measures = list(overview_df.data_view(selected=True)["Measure"])
            if len(selected_measures) > 0:
                ui.notification_show(ui.markdown(display_measure_description(selected_measures)),
                                     duration=10)

    @render.data_frame
    def variable_df():

        return render.DataTable(data=metadata_table_clean, filters=True,
                                selection_mode='rows',
                                width='98%', height='500px',
                                styles=metadata_table_style)

    @render.ui
    def variable_selected_rows():
        row_ids = variable_df.cell_selection()['rows']
        if row_ids:
            info = display_variable_info(row_ids)
        else:
            info = 'None'
        return ui.markdown(f'Variables selected: {info}')


app = App(app_ui, server, static_assets=logo_img)
