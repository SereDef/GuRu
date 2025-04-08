from shiny import ui, module
from faicons import icon_svg

from definitions.ui_elements import timepoint_selector, checkbox_selector, search_panel
from definitions.terms_and_styles import guru_colors, user_input_panel_style, banner_panel, \
    subject_choices, reporter_choices, overview_time_choices

# Individual component groups ==========================================================================================
page_id = 'overview'

@module.ui
def overview_tab(label: str):

    if label == 'Questionnaires':
        reporter_checkbox = checkbox_selector(page_id=page_id,
                                                   item_id='selected_reporters',
                                                   item_label='Reported by:',
                                                   options_dict=reporter_choices)
    else:
        reporter_checkbox = ui.div(style="flex: 1;")  # Spacer

    return ui.nav_panel(
        label,
        # Selection pane
        ui.layout_columns(
            timepoint_selector(page_id=page_id, time_choices=overview_time_choices),
            checkbox_selector(page_id=page_id,
                              item_id='selected_subjects',
                              item_label='Information about:',
                              options_dict=subject_choices),
            reporter_checkbox,
            search_panel(page_id=page_id),
            col_widths=(3, 2, 2, 5),
            gap='15px',
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

