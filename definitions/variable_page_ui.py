from shiny import ui, module
from faicons import icon_svg

from definitions.ui_elements import discrete_timepoint_slider, checkbox_selector, file_selector, search_panel
from definitions.terms_and_styles import user_input_panel_style, banner_panel, \
    subject_choices, reporter_choices, variable_time_choices, time_points_available

# Individual component groups ==========================================================================================
page_id = 'variable'

@module.ui
def variable_tab(label: str):

    timepoint_slider = discrete_timepoint_slider(id=f'{page_id}_selected_time', 
                                                labels=time_points_available[page_id][label], 
                                                header='Select time point(s)')

    if label == 'Questionnaires':
        # Only show the reporter checkbox on the Questionnaires tab
        reporter_checkbox = checkbox_selector(page_id=page_id,
                                              item_id='selected_reporters',
                                              item_label='Reported by:',
                                              options_dict=reporter_choices)
    else:
        reporter_checkbox = ui.div(style="flex: 1;")  # Spacer
    
    subject_checkbox = checkbox_selector(page_id=page_id,
                                        item_id='selected_subjects',
                                        item_label='Information about:',
                                        options_dict=subject_choices)
           
    return ui.nav_panel(
        # Tab title
        label,
        # Selection pane
        ui.div(
            ui.row(timepoint_slider, 
                   style='margin-bottom: 100px; margin-top: 20px; margin-left: 30px; margin-right: 35px;'),
            ui.row(ui.layout_columns(
                search_panel(page_id=page_id), 
                ui.div(file_selector(page_id=page_id), 
                       ui.layout_columns(subject_checkbox,
                                         reporter_checkbox, col_widths=(7, 5))),
                col_widths=(7, 5), 
                gap = '0px',
                style='margin-bottom: 0px;')),
            style=user_input_panel_style),
        # Output
        # ui.output_ui(id=f'{page_id}_legend'),
        ui.output_data_frame(id=f'{page_id}_df'),
        ui.output_ui(id=f'{page_id}_selected_rows')
    )

def variable_page(tab_name):

    return ui.nav_panel(' Variable metadata',
                        banner_panel,
                        ui.navset_pill(
                            ui.nav_spacer(),
                            variable_tab('questionnaire', label='Questionnaires'),
                            variable_tab('measurements', label='Hands-on measurements'),
                            ui.nav_panel('Other', 'TODO'),
                            id=f'{page_id}_navbar'),
                        icon=icon_svg('table'),
                        value=tab_name)

# def variable_questionnaire_tab():
#     return ui.nav_panel(
#         'Questionnaires',
#         # Selection pane
#         ui.layout_columns(
#             timepoint_selector(page_id=page_id, time_choices=variable_time_choices),
#             ui.div(
#                 ui.layout_columns(
#                     checkbox_selector(page_id=page_id,
#                                       item_id='selected_subjects',
#                                       item_label='Information about:',
#                                       options_dict=subject_choices),
#                     checkbox_selector(page_id=page_id,
#                                       item_id='selected_reporters',
#                                       item_label='Reported by:',
#                                       options_dict=reporter_choices),
#                     style="margin-bottom: 0px;"),
#                 file_selector(page_id=page_id)),
#             search_panel(page_id=page_id),
#             col_widths=(3, 4, 5),
#             gap='15px',
#             style=user_input_panel_style),
#         # Output
#         ui.output_data_frame(id=f'{page_id}_df'),
#         ui.output_ui(id=f'{page_id}_selected_rows'),
#     )