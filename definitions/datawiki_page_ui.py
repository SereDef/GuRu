import pandas as pd
from shiny import ui, render, reactive
from faicons import icon_svg

# from definitions.ui_elements import file_selector

from definitions.terms_and_styles import user_input_panel_style


# ==========================================================================================
page_id = 'datawiki'

# Read cleaned datawiki scrape
datawiki_sheets = pd.read_excel('assets/DataWiki_scrape_120922.xlsx', sheet_name=None, index_col=0)
# combine all sheets to a single dataframe
datawiki_table = pd.concat(datawiki_sheets.values()).rename(columns={
    'Period': 'Period', 'Type': 'Data type', 'Sub1': 'Sub-header 1', 'Sub2': 'Sub-header 2',
    'File': 'File name', 'PIs': 'PIs'})


def file_selector(page_id):
    file_options = list(datawiki_table['File name'].unique())

    return ui.input_selectize(id=f'{page_id}_selected_files',
                              label=ui.tooltip(ui.h6('File(s) ', icon_svg('circle-info')),
                                               'Type or select a file name. When none is selected, all files are shown.',
                                               id=f'{page_id}_files_info_tooltip',
                                               placement='right'),
                              choices=file_options,
                              selected=[],
                              multiple=True,
                              width='100%')


def period_selector(page_id):
    period_options = list(datawiki_table['Period'].unique())

    return ui.input_selectize(id=f'{page_id}_selected_periods',
                              label=ui.h6('Period'),
                              choices=period_options,
                              selected=[],
                              multiple=True,
                              width='95%')


def datatype_selector(page_id):
    datatype_options = list(datawiki_table['Data type'].unique())

    return ui.input_selectize(id=f'{page_id}_selected_datatypes',
                              label=ui.h6('Data type'),
                              choices=datatype_options,
                              selected=[],
                              multiple=True,
                              width='95%')


def datawiki_page(tab_name):
    return ui.nav_panel(" DataWiki map",
                        # Selection pane
                        ui.div(
                            ui.layout_columns(
                                period_selector(page_id=page_id),
                                datatype_selector(page_id=page_id),
                                file_selector(page_id=page_id),
                                col_widths=(3, 3, 6),
                                gap='15px'),
                            style=user_input_panel_style),
                        # Output
                        ui.output_data_frame(id=f'{page_id}_df'),

                        icon=icon_svg('book-atlas'),
                        value=tab_name)

datawiki_table_style = [
        # Cut cells with text that is too long
        # {'rows': None, 'cols': None,
        #  'style': {'height': '30px', 'overflow': 'hidden', 'text-overflow': 'ellipsis', 'white-space': 'nowrap'}},
        # Period column
        {'cols': [0],
         'style': {'width': '50px'}},
        # Type columns
        {'cols': [1],
         'style': {'min-width': '200px', 'max-width': '200px'}},
        # Sub1 ans Sub2 columns
        {'cols': [2],
         'style': {'min-width': '10px', 'max-width': '100px'}},
        {'cols': [3],
         'style': {'min-width': '1px', 'max-width': '100px'}},
        # File column
        {'cols': [4],
         'style': {'min-width': '50px', 'font-weight': 'bold'}},
        # PIs column
        {'cols': [5],
         'style': {'min-width': '10px', 'max-width': '100px'}}
]

# Server side ==================


def filter_datawiki_table(selected_periods,
                          selected_datatypes,
                          selected_filenames,
                          table=datawiki_table):

    if len(selected_periods) > 0:
        table = table.loc[table['Period'].str.contains('|'.join(list(selected_periods)), na=False, regex=False), ]

    if len(selected_datatypes) > 0:
        table = table.loc[table['Data type'].str.contains('|'.join(list(selected_datatypes)), na=False, regex=False), ]

    if len(selected_filenames) > 0:
        table = table.loc[table['File name'].str.contains('|'.join(list(selected_filenames)), na=False, regex=False), ]

    return table


def datawiki_reactivity(input, output):

    # Update the variable table ----------------------------------------------------
    @reactive.Calc
    def _filter_datawiki_table():
        return filter_datawiki_table(selected_periods=input.datawiki_selected_periods(),
                                     selected_datatypes=input.datawiki_selected_datatypes(),
                                     selected_filenames=input.datawiki_selected_files())

    @render.data_frame
    def datawiki_df():
        # table_style = variable_table_style(_filter_variable_table())
        # table_height = variable_table_height(_filter_variable_table().shape[0])

        return render.DataTable(data=_filter_datawiki_table(),
                                selection_mode='rows',
                                width='98%', height='600px',
                                styles=datawiki_table_style)

