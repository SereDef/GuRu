from shiny import ui, module, render, reactive

from definitions.terms_and_styles import overview_icon_dict

from definitions.overview_page_backend import q_table, m_table, \
    filter_overview_table, search_overview_table, \
    overview_table_style, overview_table_height, display_measure_description


@module.server
def overview_reactivity(input, output, session, label = 'Questionnaires'):

    if label == 'Questionnaires':

        time_choices = ['Prenatal', '2 months', '6 months', 
                         '1 year', '1.5 years', '2 years', '2.5 years', '3 years', 
                         '4 years', '6 years', '8 years', '10 years', 
                         '14 years', '18 years']
         
        legend = ui.markdown(f'&emsp;'
                    f'{overview_icon_dict["mother-self"]} Mother self-report &emsp;&emsp;'
                    f'{overview_icon_dict["partner-self"]} Partner self-report &emsp;&emsp;'
                    f'{overview_icon_dict["child-self"]} Child self-report &emsp;&emsp;'
                    f'{overview_icon_dict["mother-child"]} Mother about the child &emsp;&emsp;'
                    f'{overview_icon_dict["partner-child"]} Partner about the child &emsp;&emsp;'
                    f'{overview_icon_dict["teacher-child"]} Teacher about child<br>'
                    f'&emsp;<span style="color:grey">Click on any row below to display '
                    f'more information about the measure selected.</span>')
    else:

        time_choices = ['Prenatal', 'Birth', '6 weeks', '3 months', '6 months', 
                        '1 year', '3 years', 
                        '4 years', '6 years', '10 years', 
                        '14 years', '18 years']
        
        legend = ui.markdown(f'&emsp;'
                    f'{overview_icon_dict["[mother]"]} Mother &emsp;&emsp;'
                    f'{overview_icon_dict["[father]"]} Partner &emsp;&emsp;'
                    f'{overview_icon_dict["[child]"]} Child &emsp;&emsp;'
                    f'{overview_icon_dict["[subsample-mother]"]} Mother (sub-sample) &emsp;&emsp;'
                    f'{overview_icon_dict["[subsample-father]"]} Partner (sub-sample) &emsp;&emsp;'
                    f'{overview_icon_dict["[subsample-child]"]} Child (sub-sample)<br>'
                    f'&emsp;<span style="color:grey">Click on any cell to display '
                    f'more information about the measure selected.</span>')
        
    # Update the overview UI input --------------------------------------------------
    # @reactive.effect
    # def _():
    #     all_time = input.overview_switch_time()

    #     if all_time:
    #         ui.update_selectize(id='overview_selected_time',
    #                             selected=time_choices)

    # @reactive.effect
    # def _():
    #     selected_times = input.overview_selected_time()

    #     if len(selected_times) < len(time_choices):
    #         ui.update_switch(id='overview_switch_time', value=False)
    # @reactive.Effect
    # def _():
    #     # Get the selected timepoints as a list
    #     selected_times = input.overview_selected_time()
    #     print("Selected timepoints:", selected_times)
    
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
        return legend

    # @reactive.effect
    # def _():
    #     if overview_df.data().nrow() > 0:
    #         selected_measures = list(overview_df.data_view(selected=True)["Measure"])
    #         if len(selected_measures) > 0:
    #             ui.notification_show(
    #                 ui.markdown(display_measure_description(selected_measures)),
    #                                  duration=10)
    @reactive.effect
    def _():
        df = input.overview_df_data()
        if df.shape[0] > 0:
            selected = input.overview_df_data_view(selected=True)
            selected_measures = list(selected["Measure"])
            if selected_measures:
                ui.notification_show(
                    ui.markdown(display_measure_description(selected_measures)),
                    duration=10
                )
