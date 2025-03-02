from shiny import ui
from faicons import icon_svg

from definitions.ui_elements import timepoint_selector, checkbox_selector, search_panel
from definitions.terms_and_styles import guru_colors, user_input_panel_style, \
    subject_choices, reporter_choices, variable_time_choices

# Individual component groups ==========================================================================================
page_id = 'variable'


def variable_questionnaire_tab():
    return ui.nav_panel(
        'Questionnaires',
        # Selection pane
        ui.layout_columns(
            timepoint_selector(page_id=page_id, time_choices=variable_time_choices),
            checkbox_selector(page_id=page_id,
                              item_id='selected_subjects',
                              item_label='Information about:',
                              options_dict=subject_choices),
            checkbox_selector(page_id=page_id,
                              item_id='selected_reporters',
                              item_label='Reported by:',
                              options_dict=reporter_choices),
            search_panel(page_id='variable'),
            col_widths=(3, 2, 2, 5),
            gap='15px',
            style=user_input_panel_style),
        # Output
        ui.output_data_frame(id=f'{page_id}_df'),
        ui.output_ui(id=f'{page_id}_selected_rows'),
    )


def variable_page(tab_name):
    return ui.nav_panel(' Variable metadata',
                        ui.navset_pill(
                            ui.nav_spacer(),
                            variable_questionnaire_tab(),
                            ui.nav_panel('Hands-on measurements', 'TODO'),
                            ui.nav_panel('Other', 'TODO'),
                            id=f'{page_id}_navbar'),
                        icon=icon_svg('table'),
                        value=tab_name)
