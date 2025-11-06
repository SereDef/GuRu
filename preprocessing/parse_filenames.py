import marimo

__generated_with = "0.14.17"
app = marimo.App(width="columns")


@app.cell(column=0, hide_code=True)
def _(mo):
    mo.md(r"""### Set-up""")
    return


@app.cell
def _():
    import marimo as mo

    from pyprojroot.here import here

    proj_dir = str(here())

    import pandas as pd
    return mo, pd, proj_dir


@app.cell
def _(proj_dir):
    proj_dir

    return


@app.cell
def _(pd, proj_dir):
    # Ideally, but HTTP Error 403: FORBIDDEN
    # report_url ="https://erasmusmc.sharepoint.com/:x:/r/sites/GenRWiki/Gedeelde%20documenten/WIKI/Data/Report_DatawikiFiles_Wiki.xlsx?d=w67cbe43cc4584921ab3a2d11f9efeb62&csf=1&web=1&e=WixABk"

    # Downloaded on 21/08/2025
    claudia_report_file = f"{proj_dir}/preprocessing/Report_DatawikiFiles.xlsx"

    _xls = pd.read_excel(claudia_report_file, sheet_name=None, engine="openpyxl")

    # print(xls.keys()) # check sheet names can be used as global variables  

    # Extract all sheets
    for sheet in _xls.keys():
        df = _xls[sheet]
        print(f"{sheet}: {list(df.columns)}")
        globals()[sheet] = df

    # Stack filenames
    df = pd.concat([globals()[sheet].assign(sheet=sheet) for sheet in _xls.keys() if sheet not in [
        'Archive','Abbreviations', 'Update_20251021']])

    # df
    return (df,)


@app.cell
def _(df, pd):
    # Get unique pairs of old-new file names
    new_filenames = df[['HISTORIC_DATAFILE','DATAFILE']].drop_duplicates().reset_index(drop=True)
    new_filenames.columns = ['old_file_name', 'file_name']

    # Split into parts without assigning directly
    split_file_names = new_filenames['file_name'].str.split("_")

    # Explected splits 
    expected_info = ["subject", "data", "timepoint", "date"]

    # Identify problematic rows
    mask = split_file_names.map(len) != len(expected_info)
    problematic_files = new_filenames.loc[mask, "file_name"].tolist()

    if len(problematic_files) > 0:
        print("Problematic files:")
        [print(f) for f in problematic_files]

    # Keep only rows with exactly 4 parts
    valid_filenames = new_filenames.loc[~mask].copy()
    valid_filenames[expected_info] = pd.DataFrame(split_file_names[~mask].tolist(), index=valid_filenames.index)

    valid_filenames
    return new_filenames, valid_filenames


@app.cell
def _(Abbreviations, valid_filenames):
    def print_problem(variable, values, check_abbr=True, precise=False):

        if isinstance(values, list): 
            values = "|".join(values)
            var_scope = variable

        else: # handle strings
            if len(values) == 1: # if only one letter, match precisely 
                values = f'_{values}_'
                var_scope = 'file_name'
            else:
                var_scope = variable

        problem = valid_filenames.loc[valid_filenames[var_scope].str.contains(values), "file_name"]

        if (variable == "data") & check_abbr:

            abbr_match = {
                s: [(acronym, desc)
                    for acronym, desc in zip(Abbreviations.Abbreviation, Abbreviations.Definition) 
                    if acronym in s] for s in problem}

            for f, abbr in abbr_match.items():
                if len(abbr) == 0:
                    abbr = "NO MATCHING ABBREVIATIONS"
                else: 
                    abbr = '\n'.join([f"Abbr: {abbr[i][0]} = {abbr[i][1]}" for i in range(len(abbr))])


                print(f"{f.ljust(60)}{abbr}")
        else:
            [print(f) for f in problem]

    return (print_problem,)


@app.cell
def _(valid_filenames):
    from datetime import datetime

    def validate_dates(date_series, fmt="%Y%m%d"):
        for d in date_series:
            try:
                datetime.strptime(d, fmt)
            except ValueError:
                print(d)
                return False
        return True

    dates = valid_filenames.date.value_counts()

    validate_dates(dates.index)
    return


@app.cell(disabled=True)
def _(new_filenames):
    # Saving this for manual edit 
    file_track = new_filenames.copy()
    file_track['file_name_proposal'] = file_track['file_name']
    file_track['notes'] = ''

    # Sort by data 
    file_track['data'] = file_track['file_name'].str.split('_').str[1]
    file_track = file_track.sort_values(by='data').drop(columns=['data'])

    # with pd.ExcelWriter('Report_DatawikiFiles_corrected.xlsx') as writer:
    #     file_track.to_excel(writer, sheet_name='File names', index=False)
    #     Abbreviations.to_excel(writer, sheet_name='Abbreviations', index=False)
    return


@app.cell
def _(pd, proj_dir):
    corrected_filenames_file = f"{proj_dir}/preprocessing/Report_DatawikiFiles_corrected.xlsx"

    corrected_filenames = pd.read_excel(corrected_filenames_file, sheet_name=0, engine="openpyxl")
    corrected_filenames
    return (corrected_filenames,)


@app.cell
def _(corrected_filenames):
    corrected_filenames[corrected_filenames['notes'].str.contains('remove', na=False, case=False)]
    return


@app.cell
def _(corrected_filenames):
    filenames_df = corrected_filenames[~corrected_filenames['notes'].str.contains('remove', na=False, case=False)]
    filenames_df
    # Split into parts without assigning directly
    # split_file_names2 = filenames_df['file_name_proposal'].str.split("_")

    # # Explected splits 
    # # expected_info = ["subject", "data", "timepoint", "date"] # already defined

    # # Identify problematic rows
    # mask2 = split_file_names2.map(len) != len(expected_info)
    # problematic_files2 = filenames_df.loc[mask2, "file_name_proposal"].tolist()

    # if len(problematic_files2) > 0:
    #     print("Problematic files:")
    #     [print(f) for f in problematic_files2]

    # # Keep only rows with exactly 4 parts
    # valid_filenames2 = filenames_df.loc[~mask2].copy()
    # valid_filenames2[expected_info] = pd.DataFrame(split_file_names2[~mask2].tolist(), index=valid_filenames2.index)

    # valid_filenames2
    return (filenames_df,)


@app.cell
def _(filenames_df):
    filenames_df.subject.value_counts()
    return


@app.cell
def _(filenames_df):
    # filenames_df.source.str.split(".").str[0].value_counts().sort_index().to_csv('assets/measurement_timeline.csv')
    filenames_df.source.str.split(".").str[0].value_counts().sort_index()
    return


@app.cell(column=1, hide_code=True)
def _(mo):
    mo.md(r"""### Old vs. new file pairing""")
    return


@app.cell
def _(Update_20251021, df, mo):
    # update_sheet_diff
    mo.ui.tabs({'in other tabs only': Update_20251021[~Update_20251021['Filename'].isin(df['DATAFILE'])], 
                'in update tab only': df[~df['DATAFILE'].isin(Update_20251021['Filename'])]})
    return


@app.cell
def _(mo, valid_filenames):
    # c = valid_filenames['old_file_name'].value_counts()
    # c[c > 1]

    mo.ui.tabs({'multiple old files': valid_filenames[valid_filenames['old_file_name'].duplicated(keep=False)],
                'multiple new files': valid_filenames[valid_filenames['file_name'].duplicated(keep=False)]})
    return


@app.cell(column=2, hide_code=True)
def _(mo):
    mo.md(r"""### Subject info""")
    return


@app.cell
def _(valid_filenames):
    valid_filenames.subject.value_counts()
    return


@app.cell
def _(print_problem):
    for prob_subject in ['ChildFocus', 
                         'Father', 
                         'Partner', 
                         'Parent']:
        print('')
        print_problem("subject", prob_subject)
    return


@app.cell(column=3, hide_code=True)
def _(mo):
    mo.md(r"""### Time point info""")
    return


@app.cell
def _(valid_filenames):
    valid_filenames.timepoint.value_counts().sort_index()
    return


@app.cell
def _(print_problem):
    for prob_time in ['2008-2012Y|2011-2012Y', 'covariates']:
        print('')
        print_problem("timepoint", prob_time)
    return


@app.cell
def _(print_problem):
    print_problem("timepoint", 'FocusVisit14')
    return


@app.cell(column=4, hide_code=True)
def _(mo):
    mo.md(r"""### Data info""")
    return


@app.cell
def _(valid_filenames):
    data_counts = valid_filenames.data.value_counts()
    data_counts
    return (data_counts,)


@app.cell
def _(data_counts, mo):
    data_slider = mo.ui.number(start= 0, stop=data_counts.shape[0], step=1)
    data_slider
    return (data_slider,)


@app.cell
def _(data_counts, data_slider, print_problem):
    this_data = data_counts.index[data_slider.value]
    print(this_data)
    print_problem("data", this_data)
    return (this_data,)


@app.cell(column=5)
def _(Abbreviations):
    Abbreviations
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Also print out the full df to inspect variable differences""")
    return


@app.cell
def _(df, this_data):
    if len(this_data) == 1: 
        search = f'_{this_data}_'
    else: 
        search = this_data
    df[df['DATAFILE'].str.contains(search)]
    return


@app.cell
def _(mo):
    search_string = mo.ui.text()
    search_string
    return (search_string,)


@app.cell
def _(df, search_string):
    df[df['DATAFILE'].str.contains(search_string.value)]
    return


@app.cell
def _(print_problem, search_string):
    print(search_string.value)
    print_problem("data", search_string.value)
    return


if __name__ == "__main__":
    app.run()
