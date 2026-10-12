from shiny import ui, module
from faicons import icon_svg
import json

from definitions.variable_page_backend import metadata_table
from definitions.terms_and_styles import guru_colors

# def timepoint_selector(page_id, time_choices):

#     # Is dictionary nested (first value is a dictionary)
#     if isinstance(next(iter(time_choices)), dict):
#         all_times = [time for period in time_choices for time in time_choices[period]]
#     else:
#         all_times = time_choices

#     # Cannot input custom labels into a slider, so I use a selection menu (for now)
#     return ui.div(ui.h6('Time point(s)'),
#                   ui.input_switch(id=f'{page_id}_switch_time', label='All available', value=True),
#                   ui.input_selectize(id=f'{page_id}_selected_time', label='',
#                                      choices=time_choices,
#                                      selected=all_times,
#                                      multiple=True,
#                                      width='95%'))

def discrete_timepoint_slider(id: str, labels: list, header: str = None):
    """Creates a discrete slider that works with Shiny's module system
    Args:
        id: The input ID (will be namespaced by the module)
        labels: List of labels for the slider points
    """
    header_html = f'<h6 style="margin-left: -30px; margin-top: -10px; margin-bottom: 20px;">{header}</h6>' if header else ""
    # Let the module system resolve the ID
    resolved_id = module.resolve_id(id)
    return ui.HTML(f"""
        {header_html}
        <div id="{resolved_id}" class="discrete-slider" 
             data-labels='{json.dumps(labels)}'></div>
    """)


def checkbox_selector(page_id, item_id, item_label, options_dict):

    return ui.input_checkbox_group(id=f'{page_id}_{item_id}',
                                   label=ui.h6(item_label),
                                   choices=options_dict,
                                   selected=list(options_dict.keys()))


def multicol_checkbox_selector(page_id, item_id, multicol_options_dict):
    """Lay 'Matching:' and every checkbox option out inline on a single, right-aligned row."""

    checkbox_groups = []
    # One checkbox group per key, kept separate so the server can still read
    # {page_id}_{item_id}1 / 2 / 3 independently.
    for idx, (col_key, choices_dict) in enumerate(multicol_options_dict.items(), start=1):
        checkbox_groups.append(
            ui.input_checkbox_group(
                id=f"{page_id}_{item_id}{idx}",
                label=None,            # no per-group label; 'Matching:' prefixes the whole row
                choices=choices_dict,
                selected=list(choices_dict.keys()),
                inline=True            # options on a single row
            )
        )

    # 'Matching:' label followed by all checkbox groups, all on one line (see .matching-group CSS)
    return ui.div(
        ui.h6("Matching:", class_="matching-label"),
        *checkbox_groups,
        class_="matching-group"
    )

def search_panel(page_id):

    if 'overview' in page_id:

        search_textbox = ui.input_text(id=f'{page_id}_search_terms',
                                       label=ui.tooltip(ui.h6('Search ', icon_svg('circle-info')),
                                                        'To search for more than one string, separate them with a ";"',
                                                        id=f'{page_id}_search_multiple_info_tooltip',
                                                        placement='right'),
                                       value='',
                                       width='100%')

        search_domains = {'col1': {'Concept': 'Categories'},
                          'col2': {'Measure': 'Measures'},
                          'col3': {'description': 'Descriptions'}}

        regex_switch = None

    elif 'variable' in page_id:

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
                                   'Variable label': 'Variable labels'}}
        # --- Reference / constructs search is disabled for now ---
        # 'col2': {'Reference': 'Reference', 'constructs': 'Constructs'}

        regex_switch = ui.input_switch(id=f'{page_id}_search_regex', label='Use RegEx', value=False)

    search_group = ui.div(
         ui.layout_columns(
             search_textbox,
             ui.div(ui.input_action_button(id=f'{page_id}_search_button',
                                      label='Search',
                                      class_='guru-button'),
               class_='search-button-wrap'),
             col_widths=[10, 2],
             class_='search-row'),
        ui.layout_columns(
            ui.div(
                ui.input_switch(id=f'{page_id}_search_case_sensitive',
                                label='Case sensitive',
                                value=False),
                regex_switch,
                style='display: flex; gap: 40px'),
                multicol_checkbox_selector(page_id=page_id, item_id='search_domains',
                                           multicol_options_dict=search_domains),
            gap='10px',
            col_widths=[5, 7],
            style='margin-bottom: -5px'),
        style='margin-left: 10px; margin-right: 100px')

    return search_group


def file_selector(page_id):
    # 'files' holds one or more "; "-separated file names; offer each distinct name
    file_options = sorted({f.strip() for files in metadata_table['files']
                           for f in str(files).split(';')})

    return ui.input_selectize(id=f'{page_id}_selected_files',
                              label=ui.tooltip(ui.h6('File(s) ', icon_svg('circle-info')),
                                               'Type or select a file name. When none is selected, all files are shown.',
                                               id=f'{page_id}_files_info_tooltip',
                                               placement='right'),
                              choices=file_options,
                              selected=[],
                              multiple=True,
                              width='95%')

