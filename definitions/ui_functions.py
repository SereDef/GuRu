from shiny import ui

from definitions.terms_and_styles import guru_colors, user_input_panel_style, \
    subject_choices, reporter_choices, \
    overview_time_choices, variable_time_choices


def timepoint_selector(id, time_options):
    # Cannot input custom labels into a slider, so I use a selection menu (for now)

    return ui.div(ui.h6('Time point(s)'),
                  ui.input_switch(id=f'{id}_switch_time', label='All available', value=True),
                  ui.input_selectize(id=f'{id}_selected_time', label='',
                                     choices=time_options,
                                     selected=list(time_options.keys()),
                                     multiple=True,
                                     width='95%'))


def checkbox_selector(id, label, options_dict):

    return ui.input_checkbox_group(id=id, label=ui.h6(label),
                                   choices=options_dict,
                                   selected=list(options_dict.keys()))


def search_panel(id):

    search_domains = {'Category': 'Categories',
                      'Measure': 'Measures',
                      'description': 'Descriptions'}

    search_group = ui.div(
        ui.input_text(id=f'{id}_search_terms',
                      label=ui.h6('Search'),
                      value='',
                      width='100%'),
        ui.layout_columns(
            ui.input_switch(id=f'{id}_search_case_sensitive',
                            label='Case sensitive',
                            value=False),
            ui.input_checkbox_group(id=f'{id}_search_domains',
                                    label='Search in:',
                                    choices=search_domains,
                                    selected=list(search_domains.keys())),
            ui.input_action_button(id=f'{id}_search_button',
                                   label='Search',
                                   class_='guru-button'),
            gap='10px')
    )

    return search_group


# ======================================================================================================================


def overview_page(tab_name):

    return ui.nav_panel('Measures overview',
                        # ui.include_css(css_file),
                        # Selection pane
                        ui.layout_columns(
                            timepoint_selector(id='overview', time_options=overview_time_choices),
                            checkbox_selector(id='overview_selected_subjects',
                                              label='Information about:',
                                              options_dict=subject_choices),
                            checkbox_selector(id='overview_selected_reporters',
                                              label='Reported by:',
                                              options_dict=reporter_choices),
                            search_panel(id='overview'),
                            col_widths=(3, 2, 2, 5),  # negative numbers for empty spaces
                            gap='15px',
                            style=user_input_panel_style),
                        # Output
                        ui.output_data_frame(id='overview_df'),
                        ui.output_ui(id='overview_selected_rows'),

                        value=tab_name)


def variable_page(tab_name):
    return ui.nav_panel('Variable metadata',
                        # Selection pane
                        ui.layout_columns(
                            timepoint_selector(id='variable', time_options=variable_time_choices),
                            checkbox_selector(id='variable_selected_subjects',
                                              label='Information about:',
                                              options_dict=subject_choices),
                            checkbox_selector(id='variable_selected_reporters',
                                              label='Reported by:',
                                              options_dict=reporter_choices),
                            col_widths=(3, 2, 2, -5),  # negative numbers for empty spaces
                            gap='30px'
                        ),
                        # Output
                        ui.output_data_frame(id='variable_df'),
                        ui.output_ui(id='variable_selected_rows'),

                        value=tab_name)
