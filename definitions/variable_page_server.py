from shiny import ui, module, render, reactive

from definitions.variable_page_backend import variable_table_style, variable_table_height, \
    filter_variable_table, search_variable_table, \
    display_variable_info

@module.server
def variable_reactivity(input, output, session, label = 'Questionnaires'):

    # Update the variable table ----------------------------------------------------
    @reactive.Calc
    def _filter_variable_table():

        if label == 'Questionnaires':
            selected_reporters = input.variable_selected_reporters()
        else: 
            selected_reporters = None

        return filter_variable_table(  # selected_timepoints=input.variable_selected_time(),
                                     selected_subjects=input.variable_selected_subjects(),
                                     selected_reporters=selected_reporters,
                                     selected_filenames=input.variable_selected_files()
        )

    @reactive.Effect
    @reactive.event(input.variable_search_button)
    async def _search_variable_table():
        search_terms = input.variable_search_terms().split(';')

        variable_search_domains = list(input.variable_search_domains1())+list(input.variable_search_domains2())

        search_results_table = search_variable_table(table=_filter_variable_table(),
                                                     search_terms=search_terms,
                                                     search_domains=variable_search_domains,
                                                     case_sensitive=input.variable_search_case_sensitive())

        await variable_df.update_data(search_results_table)

    @render.data_frame
    def variable_df():
        table_style = variable_table_style(_filter_variable_table())
        table_height = variable_table_height(_filter_variable_table().shape[0])

        return render.DataTable(data=_filter_variable_table(),  # filters=True,
                                selection_mode='rows',
                                width='98%', height=table_height,
                                styles=table_style)

    @render.ui
    def variable_selected_rows():
        row_ids = variable_df.cell_selection()['rows']
        if row_ids:
            info = display_variable_info(row_ids)
        else:
            info = 'None'
        return ui.markdown(f'Variables selected: {info}')