from shiny import ui
from faicons import icon_svg

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


def search_panel(page_id):

    search_domains = {'Category': 'Categories',
                      'Measure': 'Measures',
                      'description': 'Descriptions'}

    search_group = ui.div(
        ui.input_text(id=f'{page_id}_search_terms',
                      label=ui.tooltip(ui.h6('Search ', icon_svg('circle-info')),
                                       'To search for more than one string, separate them with a ";"',
                                       id=f'{page_id}_search_multiple_info_tooltip',
                                       placement='right'),
                      value='',
                      width='100%'),
        ui.layout_columns(
            ui.input_switch(id=f'{page_id}_search_case_sensitive',
                            label='Case sensitive',
                            value=False),
            ui.input_checkbox_group(id=f'{page_id}_search_domains',
                                    label='Matching:',
                                    # inline=True,
                                    choices=search_domains,
                                    selected=list(search_domains.keys())),
            ui.input_action_button(id=f'{page_id}_search_button',
                                   label='Search',
                                   class_='guru-button'),
            gap='10px'),
    )

    return search_group