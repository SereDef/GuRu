import re
import pandas as pd
# from shiny import ui

# from definitions.terms_and_styles import guru_colors


# Single source of truth for the variable table.
# Columns: variable, label, type, n, summary, files, n_files
metadata_table = pd.read_parquet('assets/variable_metadata_20261009.parquet')

# --- References (validated questionnaires) are not part of this source for now ---
# metadata_table['questionnaire'] = [ui.markdown(f'<a href="{doi}" target="_blank">{q_name}</a>') if pd.notna(q_name)
#                                    else '' for doi, q_name in zip(metadata_table['questionnaire_ref'],
#                                                                   metadata_table['questionnaire'])]

# Upper bound on rows sent to the browser. Filtering/searching run server-side on the
# full table first, so search behaves as if everything were loaded; this only caps how
# many matching rows are shipped, keeping the client responsive on broad views.
MAX_DISPLAY_ROWS = 10_000

# Raw column -> column shown in the table (order matters, defines column positions)
display_columns = {'variable': 'Variable name',  # 0
                   'label': 'Variable label',    # 1
                   'type': 'Type',               # 2
                   'n': 'N observed',            # 3
                   'files': 'File name(s)'}      # 4

# ======================================================================================================================
# Stylers


def variable_table_height(nrows):
    if nrows == 0:
        return '70px'

    return f'{int(min(420, 20 + 50 * nrows))}px'


# --- Subject / Reporter pills are not shown for now ---
# def pill_style(table, var, var_pos):
#
#     pill_styler = list()
#     current_table = table.reset_index()
#     for k in current_table[var].unique():
#         try:
#             pill_styler.append({
#                 'rows': current_table.index[current_table[var] == k].tolist(),
#                 'cols': [var_pos],
#                 'style': {'border-radius': '25px', 'padding': '1px 10px',
#                           'text-align': 'center', 'display': 'inline-block',
#                           'background-color': guru_colors[f'{k}-lightshade']}
#             })
#         except:
#             pass
#     return pill_styler


def variable_table_style(table):

    return [
        # Cut cells with text that is too long
        {'rows': None, 'cols': None,
         'style': {'height': '30px', 'overflow': 'hidden', 'text-overflow': 'ellipsis', 'white-space': 'nowrap'}},
        # Variable name column
        {'cols': [0],
         'style': {'min-width': '100px', 'font-weight': 'bold'}},
        # Variable label & File name(s) columns
        {'cols': [1, 4],
         'style': {'min-width': '400px', 'max-width': '500px'}},
        # Type & N observed columns
        {'cols': [2, 3],
         'style': {'text-align': 'center'}},
    ]


# ================================================================================
# Filters


def filter_variable_table(selected_filenames,
                          # selected_timepoints, selected_subjects, selected_reporters,
                          table=metadata_table):

    # --- Time point / subject / reporter selection is disabled for now ---
    # if (len(selected_subjects) == 0) or (len(selected_reporters) == 0):
    #     return pd.DataFrame(columns=display_columns.values())
    # if len(selected_subjects) < 3:
    #     table = table.loc[table['subject'].str.contains('|'.join(list(selected_subjects)), na=False), ]
    # if len(selected_reporters) < 4:
    #     table = table.loc[table['reporter'].str.contains('|'.join(list(selected_reporters)), na=False), ]

    # User selected files ------------------------------------------------
    if len(selected_filenames) > 0:
        pattern = '|'.join(re.escape(f) for f in selected_filenames)
        table = table.loc[table['files'].str.contains(pattern, na=False, regex=True)]

    # Rename and subset columns
    return table.rename(columns=display_columns)[[*display_columns.values()]]


def search_variable_table(table,
                          search_terms,
                          search_domains,
                          search_mode='contains',
                          case_sensitive=False,
                          use_regex=False):

    # Keep only searchable domains that are actually present in the table
    search_domains = [c for c in search_domains if c in table.columns]
    terms = [t.strip() for t in search_terms if t.strip()]

    if len(search_domains) == 0 or len(terms) == 0:
        return table

    # Build a single regex that honours the chosen search mode
    if use_regex:
        pattern = '|'.join(terms)
    else:
        escaped = [re.escape(t) for t in terms]
        if search_mode == 'starts with':
            pattern = '|'.join(f'^{t}' for t in escaped)
        elif search_mode == 'ends with':
            pattern = '|'.join(f'{t}$' for t in escaped)
        else:  # 'contains'
            pattern = '|'.join(escaped)

    # Vectorised OR across the selected columns (no per-row apply)
    mask = pd.Series(False, index=table.index)
    for col in search_domains:
        mask |= table[col].str.contains(pattern, case=case_sensitive, regex=True, na=False)

    return table[mask]


def display_variable_info(var_names, table=metadata_table):

    # Look up the selected variables by name (unique key), preserving selection order
    sub_table = table.set_index('variable').loc[list(var_names)]

    vars_info_list = list()
    for var_name, row in sub_table.iterrows():
        label = row['label'] if pd.notna(row['label']) else ''
        var_info = f'**{var_name}**: {label}<br>' \
                   f'{row["type"]} variable: {row["summary"]}'
        vars_info_list.append(var_info)

    return '<br><br>' + '<br><br>'.join(vars_info_list)
