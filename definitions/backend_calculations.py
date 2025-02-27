import pandas as pd
import faicons as fa
from shiny import ui

from GuRu.definitions.style_sheet import guru_colors

# ======================================================================================================================
# Read, cleanup & style OVERVIEW TABLE
# ======================================================================================================================

overview_table, q_description = pd.read_excel('assets/content_questionnaires.xlsx', sheet_name=None).values()

# DataTable does not support multiIndex dataframes for now
# index = pd.MultiIndex.from_frame(overview_table[['concept','measure']])
# overview_table_grouped = pd.DataFrame(overview_table[timepoints].values, index=index, columns=timepoints)

# Replace all reporter-subject information with the corresponding icons
icon_dict = {'mother-self': ui.span(fa.icon_svg('square'), style=f'color: {guru_colors["mother-darkshade"]};'),
             'mother-child': ui.span(fa.icon_svg('square'), style=f'color: {guru_colors["child-darkshade"]};'),
             'partner-self': ui.span(fa.icon_svg('diamond'), style=f'color: {guru_colors["father-darkshade"]};'),
             'partner-child': ui.span(fa.icon_svg('diamond'), style=f'color: {guru_colors["child-darkshade"]};'),
             'child-self': ui.span(fa.icon_svg('circle'), style=f'color: {guru_colors["child-darkshade"]};'),
             'teacher-child': ui.span(fa.icon_svg('star-of-life'), style=f'color: {guru_colors["child-darkshade"]};')
             }

timepoint_cols = [c for c in overview_table.columns if c not in ['id', 'concept', 'measure']]

for col in timepoint_cols:
    # Create a copy original text column for search
    overview_table[f'{col}_txt'] = overview_table[col]
    # Initiate icon_recoded column (this has better performance than assigning directly)
    icon_recoded = list()
    for value in overview_table[col]:
        if pd.notna(value) and value != '':
            icons = [icon_dict[v] for v in value.split(' ')]
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


def overview_table_style(nrows, ncols):

    custom_table_style = [
                # background color rows
                {'rows': list(range(0, nrows, 2)),
                 'style': {'background-color': guru_colors['background-lightgrey']}},
                # {'rows': list(range(1, overview_table.shape[0], 2)),
                #  'style': {'background-color': 'white'}},
                # concept column
                {'cols': [0],
                 'style': {'max-width': '150px'}},
                # measure column
                {'cols': [1],
                 'style': {'min-width': '450px', 'font-weight': 'bold'}},
                # timepoint & n_observed columns
                {'cols': list(range(2, ncols)),
                 'style': {'max-width': '50px', 'text-align': 'center'}},
    ]

    return custom_table_style


def subset_overview_table(selected_timepoints,
                          selected_subjects,
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
    if selected_timepoints not in [('All',), 'None', None] or len(selected_timepoints) == 0:
        times = list(selected_timepoints)
        if 'All' in times:
            times.remove('All')
        column_subset = dict((k, overview_columns[k]) for k in overview_columns.keys()
                             if k in ['concept', 'measure']+times)
    else:
        times = [k for k in overview_columns.keys() if k not in ['concept', 'measure']]
        column_subset = overview_columns

    # User selected subject ---------------------------------
    if len(selected_subjects) < 3:
        search_terms = list()
        if 'child' in selected_subjects: search_terms.extend(['child-', '-child'])
        if 'mother' in selected_subjects: search_terms.append('mother-self')
        if 'father' in selected_subjects: search_terms.append('partner-self')

        table = table[table[[f'{t}_txt' for t in times]].apply(
            lambda row: row.astype(str).str.contains('|'.join(search_terms)).any(), axis=1)]

    # User selected reporter ---------------------------------
    reporter_choices = {'child': 'Child',
                        'mother': 'Mother / main caregiver',
                        'father': 'Father / partner',
                        'teacher': 'Teacher'}

    # Rename and subset columns
    table_clean = table.rename(columns=column_subset)[[*column_subset.values()]]
    # Remove empty rows
    table_clean = table_clean[table_clean[list(column_subset.values())[2:]].apply(
        lambda row: any(row.values != ''), axis=1)]

    nrow, ncol = table_clean.shape
    if nrow == 0:
        table_style = None
    else:
        table_style = overview_table_style(nrow, ncol)

    return table_clean, table_style


def display_measure_description(selected_measures):

    sub_table = q_description.loc[q_description['measure'].isin(selected_measures), ]

    vars_info_list = list()
    for r in sub_table.index:
        var_info = f'**{sub_table.loc[r, "measure"]}**<br>' \
                   f'{sub_table.loc[r, "description"]}'
        vars_info_list.append(var_info)

    vars_info = '<br><br>'.join(vars_info_list)

    return '<br><br>' + vars_info



# ======================================================================================================================
# Read, cleanup & style METADATA TABLE
# ======================================================================================================================

metadata_table = pd.read_csv('./assets/metadata_questionnaires.csv', index_col=0)

# Validated questionnaires are now links to the relevant papers
metadata_table['questionnaire'] = [ui.markdown(f'<a href="{doi}" target="_blank">{q_name}</a>') if pd.notna(q_name)
                                   else '' for doi, q_name in zip(metadata_table['questionnaire_ref'],
                                                                  metadata_table['questionnaire'])]

display_columns = {'var_name': 'Variable name',   # 0
                   'var_label': 'Variable label', # 1
                   'timepoint': 'Timepoint(s)',   # 2
                   'subject': 'Subject',          # 3
                   'n_observed': 'N observed',    # 4
                   'reporter': 'Reporter',        # 5
                   'questionnaire': 'Reference',  # 6
                   'constructs': 'Construct(s)',  # 7
                   'orig_file': 'File name(s)'}   # 8

custom_styles = [
            {'rows': None, 'cols': None,  # Apply to all rows and columns
             'style': {'max-width': '80px',
                       'height': '30px',
                       'overflow': 'hidden', 'text-overflow': 'ellipsis', 'white-space': 'nowrap'}
             },
            # var_name column
            {'cols': [0],
             'style': {'max-width': '100px', 'font-weight': 'bold'}},
            # var_label & orig_file columns
            {'cols': [1, 8],
             'style': {'max-width': '450px'}},
            # timepoint & n_observed columns
            {'cols': [2, 4],
             'style': {'text-align': 'center'}},
            # questionnaire column
            {'cols': [6],
             'style': {'max-width': '150px'}},
]


def pill_style(table, var, var_pos):

    pill_styler = list()
    for k in table[var].dropna().unique():
        try:
            pill_styler.append({
                'rows': table.index[table[var] == k].tolist(),
                'cols': [var_pos],
                'style': {'border-radius': '25px', 'padding': '1px 10px',
                          'text-align': 'center', 'display': 'inline-block',
                          'background-color': guru_colors[f'{k}-lightshade']}
            })

        except:
            pass

    return pill_styler


subject_styler = pill_style(metadata_table, 'subject', 3)
reporter_styler = pill_style(metadata_table, 'reporter', 5)

metadata_table_clean = metadata_table.rename(columns=display_columns)[[*display_columns.values()]]
metadata_table_style = custom_styles+subject_styler+reporter_styler


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
