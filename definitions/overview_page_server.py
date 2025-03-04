from shiny import ui, render, reactive

from definitions.terms_and_styles import overview_time_choices, overview_icon_dict

from definitions.overview_page_backend import filter_overview_table, search_overview_table, \
    overview_table_style, overview_table_height, display_measure_description


def overview_reactivity(input, output):

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

        if len(selected_times) < len(overview_time_choices):
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

        variable_search_domains = list(input.overview_search_domains1()) + list(input.overview_search_domains2())

        search_results_table = search_overview_table(table=_filter_overview_table(),
                                                     search_terms=search_terms,
                                                     search_domains=variable_search_domains,
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
                           f'{overview_icon_dict["mother-self"]} Mother self-report &emsp;&emsp;'
                           f'{overview_icon_dict["partner-self"]} Partner self-report &emsp;&emsp;'
                           f'{overview_icon_dict["child-self"]} Child self-report &emsp;&emsp;'
                           f'{overview_icon_dict["mother-child"]} Mother about the child &emsp;&emsp;'
                           f'{overview_icon_dict["partner-child"]} Partner about the child &emsp;&emsp;'
                           f'{overview_icon_dict["teacher-child"]} Teacher about child<br>'
                           f'&emsp;<span style="color:grey">Click on any row below to display '
                           f'more information about the measure selected.</span>')

    @reactive.effect
    def _():
        if overview_df.data().shape[0] > 0:
            selected_measures = list(overview_df.data_view(selected=True)["Measure"])
            if len(selected_measures) > 0:
                ui.notification_show(ui.markdown(display_measure_description(selected_measures)),
                                     duration=10)
