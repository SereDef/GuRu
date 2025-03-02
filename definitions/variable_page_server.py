from shiny import ui, render, reactive

from definitions.terms_and_styles import variable_time_choices

from definitions.backend_calculations import filter_variable_table, display_variable_info
# from definitions.backend_calculations import filter_overview_table, search_overview_table, \
#     overview_table_style, overview_table_height, display_measure_description


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
                                     selected_reporters=input.variable_selected_reporters())


    @render.data_frame
    def variable_df():

        return render.DataTable(data=_filter_variable_table(), # filters=True,
                                selection_mode='rows',
                                width='98%', height='500px',
                                styles=None) # metadata_table_style)

    @render.ui
    def variable_selected_rows():
        row_ids = variable_df.cell_selection()['rows']
        if row_ids:
            info = display_variable_info(row_ids)
        else:
            info = 'None'
        return ui.markdown(f'Variables selected: {info}')