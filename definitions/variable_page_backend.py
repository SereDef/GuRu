import pandas as pd
from shiny import ui

from definitions.terms_and_styles import guru_colors


metadata_table = pd.read_csv('assets/metadata_questionnaires.csv', index_col=0)

# Validated questionnaires are now links to the relevant papers
metadata_table['questionnaire'] = [ui.markdown(f'<a href="{doi}" target="_blank">{q_name}</a>') if pd.notna(q_name)
                                   else '' for doi, q_name in zip(metadata_table['questionnaire_ref'],
                                                                  metadata_table['questionnaire'])]

# ======================================================================================================================
# Stylers


def variable_table_height(nrows):
    if nrows == 0:
        return '70px'

    return f'{int(min(420, 20 + 50 * nrows))}px'


def pill_style(table, var, var_pos):

    pill_styler = list()

    current_table = table.reset_index()

    for k in current_table[var].unique():
        try:
            pill_styler.append({
                'rows': current_table.index[current_table[var] == k].tolist(),
                'cols': [var_pos],
                'style': {'border-radius': '25px', 'padding': '1px 10px',
                          'text-align': 'center', 'display': 'inline-block',
                          'background-color': guru_colors[f'{k}-lightshade']}
            })
        except:
            pass

    return pill_styler


def variable_table_style(table):

    table_style = [
        # Cut cells wi text that is too long
        {'rows': None, 'cols': None,
         'style': {'height': '30px', 'overflow': 'hidden', 'text-overflow': 'ellipsis', 'white-space': 'nowrap'}},
        # var_name column
        {'cols': [0],
         'style': {'min-width': '100px', 'font-weight': 'bold'}},
        # var_label & orig_file columns
        {'cols': [1, 7],
         'style': {'min-width': '400px', 'max-width': '500px'}},
        # timepoint & n_observed columns
        {'cols': [2, 4],
         'style': {'text-align': 'center'}},
        # questionnaire column
        {'cols': [6],
         'style': {'max-width': '150px'}}
                  ] + pill_style(table, 'Subject', 3) + pill_style(table, 'Reporter', 5)

    return table_style



# ================================================================================
# Filters


def filter_variable_table(  # selected_timepoints,
                          selected_subjects,
                          selected_reporters,
                          selected_filenames,
                          table=metadata_table):

    display_columns = {'var_name': 'Variable name',   # 0
                       'var_label': 'Variable label', # 1
                       'timepoint': 'Timepoint(s)',   # 2
                       'subject': 'Subject',          # 3
                       'n_observed': 'N observed',    # 4
                       'reporter': 'Reporter',        # 5
                       'questionnaire': 'Reference',  # 6
                       'orig_file': 'File name(s)'}   # 7

    # User selected time point ----------------------------
    # if (selected_timepoints is None) or (len(selected_timepoints) == 0) or \
    if (len(selected_subjects) == 0) or (len(selected_reporters) == 0):
        # Return an empty table
        # TODO: empty timepoints could be meaningful?
        empty_table = pd.DataFrame(columns=display_columns.values())

        return empty_table

    # TODO subset time

    # User selected subject and reporter ---------------------------------
    if len(selected_subjects) < 3:
        table = table.loc[table['subject'].str.contains('|'.join(list(selected_subjects)), na=False), ]

    if len(selected_reporters) < 4:
        table = table.loc[table['reporter'].str.contains('|'.join(list(selected_reporters)), na=False), ]

    # User selected files ------------------------------------------------
    if len(selected_filenames) > 0:
        table = table.loc[table['orig_file'].str.contains('|'.join(list(selected_filenames)), na=False), ]

    # Rename and subset columns
    table_clean = table.rename(columns=display_columns)[[*display_columns.values()]]

    return table_clean


def search_variable_table(table,
                          search_terms,
                          search_domains,
                          case_sensitive):
    if len(search_domains) == 0:
        return table

    if 'constructs' in search_domains:
        table = table.merge(metadata_table[['var_name', 'constructs']], how='left',
                            left_on='Variable name', right_on='var_name')

    table_clean = table[table[list(search_domains)].apply(
        lambda row: row.astype(str).str.contains('|'.join(search_terms), case=case_sensitive).any(), axis=1)]

    if 'constructs' in search_domains:
        table_clean = table_clean.drop('constructs', axis=1)

    return table_clean


def display_variable_info(row_ids, table=metadata_table):

    sub_table = table.loc[sorted(row_ids), ]

    vars_info_list = list()
    for r in sub_table.index:
        var_info = f'**{sub_table.loc[r, "var_name"]}**: {sub_table.loc[r, "var_label"]}<br>' \
                   f'{sub_table.loc[r, "var_type"]} variable: ' \
                   f'{sub_table.loc[r, "descriptives"]}'
        vars_info_list.append(var_info)

    vars_info = '<br><br>'.join(vars_info_list)

    return '<br><br>' + vars_info
