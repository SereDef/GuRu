from shiny import ui, render, reactive

from definitions.terms_and_styles import variable_time_choices

from definitions.variable_page_backend import variable_table_style, variable_table_height, \
    filter_variable_table, search_variable_table, \
    display_variable_info


def variable_reactivity(input, output):

    # Update the variable UI input --------------------------------------------------
    @reactive.effect
    def _():
        all_time = input.variable_switch_time()

        if all_time:
            ui.update_selectize(id='variable_selected_time',
                                selected=[t for period in variable_time_choices.keys()
                                          for t in variable_time_choices[period]])

    @reactive.effect
    def _():
        selected_times = input.variable_selected_time()

        if len(selected_times) < sum(len(t) for t in variable_time_choices.values()):
            ui.update_switch(id='variable_switch_time', value=False)

    # Update the variable table ----------------------------------------------------
    @reactive.Calc
    def _filter_variable_table():
        return filter_variable_table(  # selected_timepoints=input.variable_selected_time(),
                                     selected_subjects=input.variable_selected_subjects(),
                                     selected_reporters=input.variable_selected_reporters(),
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