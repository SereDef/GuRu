import pandas as pd
from shiny import ui

from definitions.terms_and_styles import guru_colors, overview_icon_dict

# ======================================================================================================================
# Read, cleanup & style OVERVIEW TABLE
# ======================================================================================================================

q_table, q_description = pd.read_excel('assets/content_questionnaires.xlsx', 
                                       sheet_name=None).values()

m_table, m_description = pd.read_excel('assets/content_measurements.xlsx', 
                                       sheet_name=None).values()

def iconize_table(table, paste_back_space=''):
    """
    Replace text with icons.
    :param table: DataFrame to be cleaned
    :return: cleaned DataFrame
    """
    timepoint_cols = [c for c in table.columns if c not in ['Concept', 'Measure']]

    icon_table = table.copy()
    for col in timepoint_cols:
        # Create a copy original text column for search
        icon_table[f'{col}_txt'] = icon_table[col]
        # Initiate icon_recoded column (this has better performance than assigning directly)
        icon_recoded = list()
        for value in icon_table[col]:
            if pd.notna(value) and value != '':
                icons = [overview_icon_dict[v] if v in overview_icon_dict.keys() else 
                         f'{paste_back_space}{v}{paste_back_space}' for v in value.split(' ')]
                icon_recoded.append(ui.span(*icons))
            else:
                icon_recoded.append('')
        # Assign recoded value
        icon_table[col] = icon_recoded
 
    return icon_table


q_table = iconize_table(q_table)
m_table = iconize_table(m_table, paste_back_space=' ')

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
                          table):
    
    if selected_reporters is None: selected_reporters = [None]

    # User selected time point ----------------------------
    if (selected_timepoints is None) or \
            (len(selected_timepoints) == 0) or \
            (len(selected_subjects) == 0) or \
            (len(selected_reporters) == 0):
        # Return an empty table
        # Filter columns that do NOT contain the specified substrings
        clean_col_names = [col for col in table.columns if 'txt' not in col]
        # Subset the DataFrame to keep only the filtered columns
        empty_table = pd.DataFrame(columns=clean_col_names)

        return empty_table

    times = [c for c in table.columns if all(sub not in c for sub in ['Concept', 'Measure', 'txt'])]

    if len(selected_timepoints) < len(times): 
        times = list(selected_timepoints)
    
    # Clean up any timepoints that are not in dataframe (TMP)
    # times = table.columns.intersection(times)

    column_subset = ['Concept', 'Measure'] + times

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
    table_clean = table[column_subset]

    # Remove any leftover empty rows
    table_clean = table_clean[table_clean[list(column_subset)[2:]].apply(
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
