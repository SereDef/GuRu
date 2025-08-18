from shiny import ui, module
from faicons import icon_svg
import json

from definitions.ui_elements import timepoint_selector, checkbox_selector, search_panel, \
    discrete_timepoint_slider
from definitions.terms_and_styles import user_input_panel_style, banner_panel, \
    subject_choices, reporter_choices

# Individual component groups ==========================================================================================
page_id = 'overview'

@module.ui
def overview_tab(label: str):

    if label == 'Questionnaires':
        time_choices = ['Prenatal', '2 months', '6 months', '1 year', '1.5 years', 
                        '2 years', '2.5 years', '3 years', '4 years', '6 years', 
                        '8 years', '10 years', '14 years', '18 years', '22 years']
        # Only show the reporter checkbox on the Quesitonnaires tab
        reporter_checkbox = checkbox_selector(page_id=page_id,
                                              item_id='selected_reporters',
                                              item_label='Reported by:',
                                              options_dict=reporter_choices)

    else:
        time_choices = ['Prenatal', 'Birth', '6 weeks', '3 months', '6 months', 
                        '1 year', '3 years', '4 years', '6 years', '10 years', 
                        '14 years', '18 years', '22 years']
        reporter_checkbox = ui.div(style="flex: 1;")  # Spacer

    # timepoint_slider = timepoint_selector(page_id=page_id, 
    #                                       time_choices=time_choices)

    discrete_slider = discrete_timepoint_slider(id=f'{page_id}_selected_time', 
                                                labels=time_choices, 
                                                header='Select time point(s)')
    
    subject_checkbox = checkbox_selector(page_id=page_id,
                                        item_id='selected_subjects',
                                        item_label='Information about:',
                                        options_dict=subject_choices)

    return ui.nav_panel(
        # Tab title
        label,
        # Selection pane
        ui.div(
            ui.row(discrete_slider, 
                   style='margin-bottom: 100px; margin-top: 20px; margin-left: 30px; margin-right: 35px;'),
            ui.row(ui.layout_columns(
                search_panel(page_id=page_id), 
                subject_checkbox,
                reporter_checkbox, 
                col_widths=(7, 3, 2), 
                gap = '0px',
                style='margin-bottom: 0px;')),
            style=user_input_panel_style),
        # Output
        ui.output_ui(id=f'{page_id}_legend'),
        ui.output_data_frame(id=f'{page_id}_df')
    )

def overview_page(tab_name):

    return ui.nav_panel(' Data overview',
                        banner_panel,
                        ui.navset_pill(
                            ui.nav_spacer(),
                            overview_tab('questionnaire', label='Questionnaires'),
                            overview_tab('measurements', label='Hands-on measurements'),
                            ui.nav_panel('Other', 'TODO'),
                            id=f'{page_id}_navbar'),
                        icon=icon_svg('binoculars'),
                        value=tab_name)

