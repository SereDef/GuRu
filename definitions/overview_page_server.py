from shiny import ui, module, render, reactive

from definitions.terms_and_styles import overview_icon_legend

from definitions.overview_page_backend import q_table, m_table, \
    filter_overview_table, search_overview_table, \
    overview_table_style, overview_table_height, display_measure_description


@module.server
def overview_reactivity(input, output, session, label = 'Questionnaires'):

    legend = overview_icon_legend[label]
    
    # Update the overview table ----------------------------------------------------
    @reactive.Calc
    def _filter_overview_table():
        if label == 'Questionnaires':
            selected_reporters = input.overview_selected_reporters()
            table = q_table 
        else: 
            selected_reporters = None
            table = m_table

        return filter_overview_table(selected_timepoints=input.overview_selected_time(),
                                     selected_subjects=input.overview_selected_subjects(),
                                     selected_reporters=selected_reporters,
                                     table=table)

    @reactive.Effect
    @reactive.event(input.overview_search_button)
    async def _search_overview_table():
        search_terms = input.overview_search_terms().split(';')

        # Dynamically gather all inputs starting with 'overview_search_domains'
        variable_search_domains = []
        for variable_search_col in [1, 2, 3]:
            variable_search_id = f'overview_search_domains{variable_search_col}'
            variable_search_input = input[variable_search_id]()
            if variable_search_input:
                variable_search_domains.extend(list(variable_search_input))
                
        
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
                                selection_mode="rows",
                                width='100%',
                                height=table_height,
                                styles=table_style)

    @render.ui
    def overview_legend():
        return ui.div(legend, style='margin-top: 20px;')

    @reactive.effect
    def row_info():
        df = overview_df.data()
        if df.shape[0] > 0:
            selected_measures = list(overview_df.data_view(selected=True)["Measure"])
            if selected_measures:
                ui.notification_show(
                    ui.markdown(display_measure_description(selected_measures)),
                    duration=10
                )
