from shiny import ui
from faicons import icon_svg

from definitions.backend_calculations import metadata_table
from definitions.terms_and_styles import guru_colors


def timepoint_selector(page_id, time_choices):

    # Is dictionary nested (first value is a dictionary)
    if isinstance(next(iter(time_choices.values())), dict):
        all_times = [time for period in time_choices.keys() for time in time_choices[period]]
    else:
        all_times = list(time_choices.keys())

    # Cannot input custom labels into a slider, so I use a selection menu (for now)
    return ui.div(ui.h6('Time point(s)'),
                  ui.input_switch(id=f'{page_id}_switch_time', label='All available', value=True),
                  ui.input_selectize(id=f'{page_id}_selected_time', label='',
                                     choices=time_choices,
                                     selected=all_times,
                                     multiple=True,
                                     width='95%'))


def checkbox_selector(page_id, item_id, item_label, options_dict):

    return ui.input_checkbox_group(id=f'{page_id}_{item_id}',
                                   label=ui.h6(item_label),
                                   choices=options_dict,
                                   selected=list(options_dict.keys()))


def multicol_checkbox_selector(page_id, item_id, multicol_options_dict):

    return ui.layout_columns(
        ui.input_checkbox_group(id=f'{page_id}_{item_id}1',
                                label='Matching:',
                                choices=multicol_options_dict['col1'],
                                selected=list(multicol_options_dict['col1'].keys())),
        ui.input_checkbox_group(id=f'{page_id}_{item_id}2',
                                label=ui.div('Matching:', style=f'color: {guru_colors["background-lightblue"]}; '),
                                choices=multicol_options_dict['col2'],
                                selected=list(multicol_options_dict['col2'].keys()))
    )


def search_panel(page_id):

    if page_id == 'overview':

        search_textbox = ui.input_text(id=f'{page_id}_search_terms',
                                       label=ui.tooltip(ui.h6('Search ', icon_svg('circle-info')),
                                                        'To search for more than one string, separate them with a ";"',
                                                        id=f'{page_id}_search_multiple_info_tooltip',
                                                        placement='right'),
                                       value='',
                                       width='100%')

        search_domains = {'col1': {'Category': 'Categories',
                                   'Measure': 'Measures'},
                          'col2': {'description': 'Descriptions'}}

        regex_switch = None

    elif page_id == 'variable':

        search_textbox = ui.layout_columns(
            ui.input_select(id=f'{page_id}_search_mode',
                            label=ui.tooltip(ui.h6('Search ', icon_svg('circle-info')),
                                             'To search for more than one string, separate them with a ";"',
                                             id=f'{page_id}_search_multiple_info_tooltip',
                                             placement='right'),
                            choices=['contains', 'starts with', 'ends with'],
                            selected='contains',
                            multiple=False),
            ui.input_text(id=f'{page_id}_search_terms',
                          label=ui.div('Mode', style=f'color: {guru_colors["background-lightblue"]}; '
                                                     f'margin-bottom: 5.5px'),
                          value='',
                          width='100%'),
            col_widths=[3, 9],
            gap='0px')

        search_domains = {'col1': {'Variable name': 'Variable names',
                                   'Variable label': 'Variable labels'},
                          'col2': {'Reference': 'Reference',
                                   'constructs': 'Constructs'}}

        regex_switch = ui.div(ui.input_switch(id=f'{page_id}_search_regex', label='Use RegEx', value=False),
                              style='margin-top: -10px')

    search_group = ui.div(
        search_textbox,
        ui.layout_columns(
            ui.div(
                ui.input_switch(id=f'{page_id}_search_case_sensitive',
                                label='Case sensitive',
                                value=False),
                regex_switch),
            multicol_checkbox_selector(page_id=page_id, item_id='search_domains',
                                       multicol_options_dict=search_domains),
            gap='10px',
            col_widths=[4, 8]),
        ui.div(ui.input_action_button(id=f'{page_id}_search_button',
                                      label='Search',
                                      class_='guru-button'),
               style='float: right; margin-top: -15px; margin-bottom: 20px'),
        style='margin-left: 20px')

    return search_group


def file_selector(page_id):
    file_options = [f for f in metadata_table.orig_file.unique() if ';' not in f]

    return ui.input_selectize(id=f'{page_id}_selected_file',
                              label=ui.tooltip(ui.h6('File(s) ', icon_svg('circle-info')),
                                               'Type or select a file name. When none is selected, all files are shown.',
                                               id=f'{page_id}_files_info_tooltip',
                                               placement='right'),
                              choices=file_options,
                              selected=[],
                              multiple=True,
                              width='95%')

