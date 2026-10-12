from shiny import ui, module, render, reactive

from definitions.variable_page_backend import variable_table_style, variable_table_height, \
    filter_variable_table, search_variable_table, grey_separators, \
    display_variable_info, MAX_DISPLAY_ROWS


@module.server
def variable_reactivity(input, output, session):

    # Search parameters are captured only when the Search button is clicked ----------
    search_params = reactive.value(None)

    @reactive.effect
    @reactive.event(input.variable_search_button)
    def _capture_search_params():
        search_params.set({
            'search_terms': input.variable_search_terms().split(';'),
            'search_domains': list(input.variable_search_domains1()),
            'search_mode': input.variable_search_mode(),
            'case_sensitive': input.variable_search_case_sensitive(),
            'use_regex': input.variable_search_regex(),
        })

    # Single source for the displayed table: file filter (live) + search (on click) --
    @reactive.calc
    def _variable_table():
        table = filter_variable_table(selected_filenames=input.variable_selected_files())

        params = search_params()
        if params is not None:
            table = search_variable_table(table, **params)

        return table

    @render.data_frame
    def variable_df():
        # Search/filter already ran on the full table; only cap what is shipped to the client
        table = grey_separators(_variable_table().head(MAX_DISPLAY_ROWS))

        return render.DataTable(data=table,
                                selection_mode='rows',
                                width='98%',
                                height=variable_table_height(table.shape[0]),
                                styles=variable_table_style(table))

    @render.ui
    def variable_table_note():
        n_total = _variable_table().shape[0]

        if n_total > MAX_DISPLAY_ROWS:
            note = f'Showing the first **{MAX_DISPLAY_ROWS:,}** of **{n_total:,}** variables — ' \
                   f'use search to narrow the results and/or click on any row(s) to display additional information (under the table)'
        else:
            note = f'**{n_total:,}** variable(s) found.'

        return ui.markdown(note)

    @render.ui
    def variable_selected_rows():
        # Read the selection straight from the current view so it stays correct
        # regardless of any filtering or searching that has been applied.
        selected = variable_df.data_view(selected=True)

        if selected.shape[0] == 0:
            return ui.markdown('Variables selected: None')

        info = display_variable_info(selected['Variable name'].tolist())
        return ui.HTML(f'<div class="var-summary">{info}</div>')
