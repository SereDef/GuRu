import pandas as pd
from shiny import ui

from definitions.terms_and_styles import guru_colors, overview_icon_dict

# ======================================================================================================================
# Read, cleanup & style OVERVIEW TABLE
# ======================================================================================================================

overview_table, q_description = pd.read_excel('assets/content_questionnaires.xlsx', sheet_name=None).values()

# DataTable does not support multiIndex dataframes for now
# index = pd.MultiIndex.from_frame(overview_table[['concept','measure']])
# overview_table_grouped = pd.DataFrame(overview_table[timepoints].values, index=index, columns=timepoints)

# Replace all reporter-subject information with the corresponding icons
timepoint_cols = [c for c in overview_table.columns if c not in ['id', 'concept', 'measure']]

for col in timepoint_cols:
    # Create a copy original text column for search
    overview_table[f'{col}_txt'] = overview_table[col]
    # Initiate icon_recoded column (this has better performance than assigning directly)
    icon_recoded = list()
    for value in overview_table[col]:
        if pd.notna(value) and value != '':
            icons = [overview_icon_dict[v] for v in value.split(' ')]
            icon_recoded.append(ui.span(*icons))
        else:
            icon_recoded.append('')
    # Assign recoded value
    overview_table[col] = icon_recoded

# This one adds an icon before the text, you gotta define them though in tags.styles...
# def replace_text_with_icons(table, var, var_pos, icon_dict):
#
#     # icon_mapping = {key: f'<i class="fas {value[0]}" style="color: {value[1]};"></i>'
#     #                 for key, value in icon_dict.items()}
#
#     icon_styler = list()
#     for k in icon_dict.keys():
#         icon_styler.append({
#             'rows': table.index[table[var] == k].tolist(),
#             'cols': [var_pos],
#             'class': icon_dict[k]
#         })
#
#     return icon_styler


# Server side ---------------------------------------------
def overview_table_height(nrows):
    if nrows == 0:
        return '70px'

    return f'{int(min(420, 20 + 50 * nrows))}px'


def overview_table_style(nrows, ncols):
    if nrows == 0:
        return None

    custom_table_style = [
                # background color rows
                {'rows': list(range(0, nrows, 2)),
                 'style': {'background-color': guru_colors['background-lightgrey']}},
                # {'rows': list(range(1, overview_table.shape[0], 2)),
                #  'style': {'background-color': 'white'}},
                # concept column
                {'cols': [0],
                 'style': {'min-width': '215px'}},
                # measure column
                {'cols': [1],
                 'style': {'min-width': '480px', 'font-weight': 'bold'}},
                # timepoint & n_observed columns
                {'cols': list(range(2, ncols)),
                 'style': {'max-width': '50px', 'text-align': 'center'}},
    ]

    return custom_table_style


def filter_overview_table(selected_timepoints,
                          selected_subjects,
                          selected_reporters,
                          table=overview_table):

    overview_columns = {
        'concept': 'Category',  # 0
        'measure': 'Measure',   # 1
        'Pre': 'Pregnancy',     # 2
        '2m': '2 months',       # 3
        '6m': '6 months',       # 4
        '1y': '1 year',         # 5
        '1.5y': '1.5 years',    # 6
        '2y': '2 years',        # 7
        '2.5y': '2.5 years',    # 8
        '3y': '3 years',        # 9
        '4y': '4 years',        # 10
        '6y': '6 years',        # 11
        '8y': '8 years',        # 12
        '10y': '10 years',      # 13
        '14y': '14 years',      # 14
        '18y': '18 years',      # 15
        }

    # User selected time point ----------------------------
    if (selected_timepoints is None) or \
            (len(selected_timepoints) == 0) or \
            (len(selected_subjects) == 0) or \
            (len(selected_reporters) == 0):
        # Return an empty table
        empty_table = pd.DataFrame(columns=overview_columns)

        return empty_table

    times = [k for k in overview_columns.keys() if k not in ['concept', 'measure']]  # all available times

    if len(selected_timepoints) < len(times):
        times = list(selected_timepoints)
        column_subset = dict((k, overview_columns[k]) for k in overview_columns.keys()
                             if k in ['concept', 'measure']+times)
    else:
        column_subset = overview_columns

    # User selected subject and reporter ---------------------------------
    if (len(selected_subjects) < 3) or (len(selected_reporters) < 4):
        search_codes = list()
        if 'child' in selected_subjects:
            if 'child' in selected_reporters: search_codes.append('child-self')
            if 'mother' in selected_reporters: search_codes.append('mother-child')
            if 'father' in selected_reporters: search_codes.append('partner-child')
            if 'teacher' in selected_reporters: search_codes.append('teacher-child')
        if ('mother' in selected_subjects) & ('mother' in selected_reporters):
            search_codes.append('mother-self')
        if ('father' in selected_subjects) & ('father' in selected_reporters):
            search_codes.append('partner-self')

        table = table[table[[f'{t}_txt' for t in times]].apply(
            lambda row: row.astype(str).str.contains('|'.join(search_codes)).any(), axis=1)]

    # Rename and subset columns
    table_clean = table.rename(columns=column_subset)[[*column_subset.values()]]

    # Remove any leftover empty rows
    table_clean = table_clean[table_clean[list(column_subset.values())[2:]].apply(
        lambda row: any(row.values != ''), axis=1)]

    return table_clean  # , table_style, table_height


def search_overview_table(table,
                          search_terms,
                          search_domains,
                          case_sensitive):
    if len(search_domains) == 0:
        return table

    # Add description column to the table
    if 'description' in search_domains:
        table = table.merge(q_description[['measure', 'description']], how='left',
                            left_on='Measure', right_on='measure')

    table_clean = table[table[list(search_domains)].apply(
        lambda row: row.astype(str).str.contains('|'.join(search_terms), case=case_sensitive).any(), axis=1)]

    if 'description' in search_domains:
        table_clean = table_clean.drop('description', axis=1)
        table_clean = table_clean.drop('measure', axis=1)

    return table_clean


def display_measure_description(selected_measures):

    sub_table = q_description.loc[q_description['measure'].isin(selected_measures), ]

    vars_info_list = list()
    for r in sub_table.index:
        var_info = f'**{sub_table.loc[r, "measure"]}**<br>' \
                   f'{sub_table.loc[r, "description"]}'
        vars_info_list.append(var_info)

    vars_info = '<br><br>'.join(vars_info_list)

    return vars_info
