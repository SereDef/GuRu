from shiny import ui
from pathlib import Path

from GuRu.definitions.style_sheet import guru_colors

here = Path(__file__).parent

css_file = here / '..' / 'css' / 'custom_styles.css'

def timepoint_selector(id, time_options='stratified'):

    if time_options == 'simple':
        time_choices = {'All': 'All',
                        'Pre': 'Pregnancy',
                        '2m': '2 months',
                        '6m': '6 months',
                        '1y': '1 year',
                        '2y': '2 years',
                        '3y': '3 years',
                        '4y': '4 years',
                        '6y': '6 years',
                        '8y': '8 years',
                        '10y': '10 years',
                        '14y': '14 years',
                        '18y': '18 years'}
    else:
        time_choices = {'All': 'All',
                        'Pregnancy': {'20w': '1st trimester',
                                      '25w': '2nd trimester',
                                      '30w': '3rd trimester'},
                        'Infancy': {'0': 'birth',
                                    '2m': '2 months',
                                    '6m': '6 months'},
                        'Pre-school': {'1y': '1 year',
                                       '2y': '2 years',
                                       '3y': '3 years'},
                        'School-age': {'6y': '6 years',
                                       '10y': '10 years'},
                        'Adolescence': {'14y': '14 years',
                                        '18y': '18 years'}}

    return ui.div(ui.input_selectize(id=id, label=ui.h6('Timepoint(s)'),
                              choices=time_choices,
                              selected='All',
                              multiple=True),
                  # ui.input_slider(id='slider1', label='', min=-1, max=18, value=[-1, 18], post=' years')
                  )

# Cannot input custom labels for now
# timepoint_slider = ui.input_slider(id='timepoint_slider', label='Timepoint: ',
#                                        min=-1, max=20, value=[-1, 20], step=1),


def subject_selector(id):

    subject_choices = {'child': 'Child',
                       'mother': 'Mother / main caregiver',
                       'father': 'Father / partner'}
                       # 'family': 'Family'}

    return ui.input_checkbox_group(id=id, label=ui.h6('Info about:'),
                                   choices=subject_choices,
                                   selected=list(subject_choices.keys()))


def reporter_selector(id):

    reporter_choices = {'child': 'Child',
                        'mother': 'Mother / main caregiver',
                        'father': 'Father / partner',
                        'teacher': 'Teacher'}

    return ui.input_checkbox_group(id=id, label=ui.h6('Reported by:'),
                                   choices=reporter_choices,
                                   selected=list(reporter_choices.keys())),


def search_bar():

    search_domains = {'concept': 'Categories',
                      'measure': 'Measures',
                      'description': 'Descriptions'}

    search_group = ui.div(
        ui.input_text('search_terms', 'Search for:', '', width='100%'),
        ui.layout_columns(
            ui.input_checkbox_group(id='search_domains', label='Search in:',
                                    choices=search_domains,
                                    selected=list(search_domains.keys())),
            ui.input_switch('case_sensitive', 'Case sensitive', False),
            ui.input_action_button('go_search', 'Search'),
            gap='10px'
        )
    )

    return search_group


# ======================================================================================================================


def overview_page(tab_name):

    return ui.nav_panel('Overview',
                        # ui.include_css(css_file),
                        # Selection pane
                        ui.layout_columns(
                            timepoint_selector(id='overview_selected_time', time_options='simple'),
                            subject_selector(id='overview_selected_subjects'),
                            reporter_selector(id='overview_selected_reporter'),
                            search_bar(),
                            col_widths=(2, 2, 2, 6),  # negative numbers for empty spaces
                            gap='30px',
                            style=f'padding-top: 20px; padding-right: 30px; padding-left: 30px; ' \
                                  f'border-radius: 30px; ' \
                                  f'background-color: {guru_colors["background-lightblue"]}'
                        ),
                        # Output
                        ui.output_data_frame(id='overview_df'),
                        ui.output_ui(id='overview_selected_rows'),

                        value=tab_name)


def variable_page(tab_name):
    return ui.nav_panel('Variable table',
                        # Selection pane
                        ui.layout_columns(
                            subject_selector(id='variable_selected_subject'),
                            reporter_selector(id='variable_selected_reporter'),
                            timepoint_selector(id='variable_selected_time'),
                            col_widths=(2, 2, 3, -5),  # negative numbers for empty spaces
                            gap='30px'
                        ),
                        # Output
                        ui.output_data_frame(id='variable_df'),
                        ui.output_ui(id='variable_selected_rows'),

                        value=tab_name)
