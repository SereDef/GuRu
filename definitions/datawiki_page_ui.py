import pandas as pd
from shiny import ui, render, reactive
from faicons import icon_svg

from definitions.ui_elements import file_selector

from definitions.terms_and_styles import user_input_panel_style


# ==========================================================================================
page_id = 'datawiki'


def datawiki_page(tab_name):
    return ui.nav_panel(" DataWiki map",
                        # Selection pane
                        ui.layout_columns(
                            # timepoint_selector(page_id=page_id, time_choices=variable_time_choices),
                            'Period selection',
                            file_selector(page_id=page_id),
                            # search_panel(page_id=page_id),
                            col_widths=(6, 6),
                            gap='15px',
                            style=user_input_panel_style),
                        # Output
                        ui.output_data_frame(id=f'{page_id}_df'),

                        icon=icon_svg('book-atlas'),
                        value=tab_name)

# Server side ==================


datawiki_table = pd.read_csv('assets/datawiki_scrape.csv', index_col=0)


def filter_datawiki_table(selected_filenames,
                          table=datawiki_table):

    if len(selected_filenames) > 0:
        table = table.loc[table['Files'].str.contains('|'.join(list(selected_filenames)), na=False), ]

    return table


def datawiki_reactivity(input, output):

    # Update the variable table ----------------------------------------------------
    # @reactive.Calc
    # def _filter_datawiki_table():
    #     return filter_datawiki_table(  # selected_timepoints=input.variable_selected_time(),
    #                                  selected_filenames=input.datawiki_selected_files()
    #     )


    @render.data_frame
    def datawiki_df():
        # table_style = variable_table_style(_filter_variable_table())
        # table_height = variable_table_height(_filter_variable_table().shape[0])

        return render.DataTable(data=datawiki_table, # _filter_datawiki_table(),  # filters=True,
                                selection_mode='rows',
                                width='98%', height='400px', # table_height,
                                styles=None) # table_style)
