from shiny import ui, module
from faicons import icon_svg

from definitions.ui_elements import file_selector, search_panel
# from definitions.ui_elements import discrete_timepoint_slider, checkbox_selector
from definitions.terms_and_styles import user_input_panel_style, banner_panel
# from definitions.terms_and_styles import subject_choices, reporter_choices, \
#     variable_time_choices, time_points_available

# Individual component groups ==========================================================================================
page_id = 'variable'


@module.ui
def variable_tab():

    # --- Time point / subject / reporter selection is disabled for now ---
    # timepoint_slider = discrete_timepoint_slider(id=f'{page_id}_selected_time',
    #                                              labels=time_points_available[page_id]['Questionnaires'],
    #                                              header='Select time point(s)')
    # subject_checkbox = checkbox_selector(page_id=page_id, item_id='selected_subjects',
    #                                      item_label='Information about:', options_dict=subject_choices)
    # reporter_checkbox = checkbox_selector(page_id=page_id, item_id='selected_reporters',
    #                                       item_label='Reported by:', options_dict=reporter_choices)

    return ui.div(
        # Selection pane
        ui.div(
            # ui.row(timepoint_slider,
            #        style='margin-bottom: 100px; margin-top: 20px; margin-left: 30px; margin-right: 35px;'),
            ui.row(ui.layout_columns(
                search_panel(page_id=page_id),
                file_selector(page_id=page_id),
                col_widths=(7, 5),
                gap='0px',
                style='margin-bottom: 0px;')),
            style=user_input_panel_style),
        # Output
        ui.div(ui.output_ui(id=f'{page_id}_table_note'), style='margin: 10px 0 0 20px; color: grey;'),
        ui.output_data_frame(id=f'{page_id}_df'),
        ui.output_ui(id=f'{page_id}_selected_rows'),
    )


def variable_page(tab_name):

    # One big table for all variables (questionnaires and hands-on measurements combined)
    return ui.nav_panel(' Variable metadata',
                        banner_panel,
                        variable_tab('variable'),
                        icon=icon_svg('table'),
                        value=tab_name)
