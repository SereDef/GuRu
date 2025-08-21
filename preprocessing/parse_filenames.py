import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    import pandas as pd
    return (pd,)


@app.cell
def _(pd):
    # Ideally, but HTTP Error 403: FORBIDDEN
    # report_url ="https://erasmusmc.sharepoint.com/:x:/r/sites/GenRWiki/Gedeelde%20documenten/WIKI/Data/Report_DatawikiFiles_Wiki.xlsx?d=w67cbe43cc4584921ab3a2d11f9efeb62&csf=1&web=1&e=WixABk"

    # Downloaded on 21/08/2025
    report_file = "Report_DatawikiFiles_Wiki.xlsx"

    xls = pd.read_excel(report_file, sheet_name=None, engine="openpyxl")

    # print(xls.keys()) # check sheet names can be used as global variables  

    # Extract all sheets
    for sheet in xls.keys():
        df = xls[sheet]
        print(f"{sheet}: {list(df.columns)}")
        globals()[sheet] = df

    # Stack filenames
    df = pd.concat([globals()[sheet] for sheet in xls.keys() if sheet != "Abbrevations"])

    df
    return (df,)


@app.cell
def _(df, pd):
    new_filenames = pd.DataFrame(pd.unique(df.DATAFILE), columns = ["file_name"])

    # Split into parts without assigning directly
    split_file_names = new_filenames["file_name"].str.split("_")

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
    return (valid_filenames,)


@app.cell
def _(Abbrevations):
    Abbrevations
    return


@app.cell
def _(Abbrevations, valid_filenames):
    def print_problem(variable, values, check_abbr=True):
        if not isinstance(values, list): 
            values = [values]
        problem = valid_filenames.loc[valid_filenames[variable].str.contains("|".join(values)), "file_name"]

        if (variable == "data") & check_abbr:

            abbr_match = {
                s: [(acronym, desc)
                    for acronym, desc in zip(Abbrevations.Abbrevation, Abbrevations.Definition) if acronym in s] for s in problem}
        
            for f, abbr in abbr_match.items():
                if len(abbr) == 0:
                    abbr = "NO MATCHING ABBRIVIATIONS"
                else: 
                    abbr = f"Abbr: {abbr[0][0]} = {abbr[0][1]}"

            
                print(f"{f.ljust(60)}{abbr}")
        else:
            [print(f) for f in problem]
    
    return (print_problem,)


@app.cell
def _(valid_filenames):
    valid_filenames.subject.value_counts()
    return


@app.cell
def _(print_problem):
    print_problem("subject", "MotherSubgroup")
    return


@app.cell
def _(valid_filenames):
    valid_filenames.timepoint.value_counts()
    return


@app.cell
def _(print_problem):
    print_problem("timepoint", "covariates")

    print_problem("timepoint", ["Pregancy","App17"])

    print_problem("timepoint", ["13Y","6Y","2011-2012Y","2008-2012Y"])

    print_problem("timepoint", ["0-10Y","Mult-9-13Y","Multi-0-9Y"])
    return


@app.cell
def _(valid_filenames):
    valid_filenames.date.value_counts()
    return


@app.cell
def _(valid_filenames):
    valid_filenames.data.value_counts()
    return


@app.cell
def _():
    # print_problem("data", "DXA")
    # print_problem("data", "Weight")
    return


@app.cell
def _(df):
    df[['DATAFILE', 'HISTORIC_DATAFILE']].value_counts()
    return


if __name__ == "__main__":
    app.run()
