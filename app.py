from shiny import App, ui, render
from pathlib import Path

from definitions.backend_calculations import \
    subset_overview_table, display_measure_description, \
    metadata_table_clean, metadata_table_style, display_variable_info

from definitions.ui_functions import overview_page, variable_page

here = Path(__file__).parent

css_file = here / 'css' / 'custom_styles.css'
logo_img = here / 'www'

app_ui = ui.page_fluid(
    ui.include_css(css_file),
    ui.page_navbar(
        # ui.nav_spacer(),
        overview_page(tab_name='overview_page'),
        variable_page(tab_name='variable_page'),
        ui.nav_panel("DataWiki scrape", 'TODO'),
        ui.nav_panel("Publications", 'TODO'),

        id='navbar',
        selected='overview_page',
        position='fixed-top',  # Navbar is pinned at the top
        bg='white',
        fillable=True,
        padding=[130, 20, 20],  # top, left-right, bottom in px
        window_title='GuRu',
        title=ui.img(src='GuRu_logo.png', alt='Generation R data dictionary app', height='100px'),
        # theme=theme_file,
    )
)


def server(input, output, session):
    @render.data_frame
    def overview_df():

        overview_table_subset, overview_table_style = subset_overview_table(
            selected_timepoints=input.overview_selected_time(),
            selected_subjects=input.overview_selected_subjects()
        )

        nrows = overview_table_subset.shape[0]

        return render.DataTable(data=overview_table_subset,
                                selection_mode='rows',
                                width='99%',
                                height=f'{int(min(500, 50*nrows))}px',
                                styles=overview_table_style)

    @render.ui
    def overview_selected_rows():
        selected_measures = list(overview_df.data_view(selected=True)["Measure"])

        if selected_measures:
            info = ui.markdown(f'Measures selected: {display_measure_description(selected_measures)}')
        else:
            info = ui.markdown(f'No measures selected. Click on a row above to display more information about the '
                               f'measure selected.')
        return info

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
