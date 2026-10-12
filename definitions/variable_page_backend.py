import re
import pandas as pd
from datetime import datetime
from htmltools import span
# from shiny import ui

# from definitions.terms_and_styles import guru_colors


# Single source of truth for the variable table.
# Columns: variable, label, type, n, summary, files, n_files
METADATA_FILE = 'assets/variable_metadata_20261009.parquet'
metadata_table = pd.read_parquet(METADATA_FILE)

# Date embedded in the parquet filename (YYYYMMDD) -> e.g. "09 October 2026"
_date_match = re.search(r'(\d{8})', METADATA_FILE)
update_date = (datetime.strptime(_date_match.group(1), '%Y%m%d').strftime('%d %B %Y')
               if _date_match else '')

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


def grey_separators(table, cols=('Type', 'Variable label')):
    """Return a copy of `table` where ' || ' in the given columns is greyed out.

    Cells become htmltools `span` tags (not plain strings), which the data grid
    renders as HTML. A plain `str`/`HTML` would be shown literally, so a real Tag
    is required (see shiny .../render/_data_frame_utils/_html.py::ui_must_be_processed).
    """
    def grey(text):
        if pd.isna(text):
            return None
        parts = str(text).split(' || ')
        children = []
        for i, part in enumerate(parts):
            if i:
                children.append(span(' || ', style='color: #cdd5de;'))
            children.append(part)  # plain str children are HTML-escaped by htmltools
        return span(*children)

    table = table.copy()
    for col in cols:
        if col in table.columns:
            table[col] = table[col].map(grey)
    return table


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


# ======================================================================================================================
# Pretty-print the per-variable summaries (shown below the table when rows are selected)
#
# The 'summary' column packs DISTINCT per-file summaries joined by ' || ' (see
# preprocessing/02_extract_variable_metadata.R::collapse_distinct). The chunks are
# de-duplicated, so a chunk means "this distribution occurs in >=1 file" and cannot be
# mapped back to a specific file. Each chunk has one of four shapes:
#   numeric      'min: ..; 1stQ: ..; median: ..; 3rdQ: ..; max: ..; mean: ..; sd: ..'
#   categorical  '[level: count][level: count]...'  (+ optional '; ... (+k more levels)')
#   date         'from: ..; to: ..; median: ..'
#   unique       'N unique values'
# We classify each chunk by its own shape, so combination types (e.g. 'numeric || factor')
# are handled automatically.

MAX_VARIANTS = 3   # distinct variants shown per shape before collapsing to '(+N more)'
MAX_FILES = 10     # files listed before collapsing to '(+N more files)'

_NUM_KEYS = ['min', '1stQ', 'median', '3rdQ', 'max', 'mean', 'sd']
_CAT_PAIR_RE = re.compile(r'\[(.+?):\s*(-?\d+)\]')
_MORE_LEVELS_RE = re.compile(r'\(\+(\d+) more levels\)')


def _fmt_num(value):
    """Human-friendly number: '1.063e+04' -> '10,630', keep small decimals as-is."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return str(value).strip()
    if v == int(v) and abs(v) < 1e15:
        return f'{int(v):,}'
    return f'{v:.4g}'  # 4 significant figures for non-integers


def _classify_chunk(chunk):
    """Return (shape, parsed) for one summary chunk."""
    c = chunk.strip()
    if c.startswith('['):
        levels = [(name.strip(), int(count)) for name, count in _CAT_PAIR_RE.findall(c)]
        more = _MORE_LEVELS_RE.search(c)
        return 'categorical', {'levels': levels, 'more': int(more.group(1)) if more else 0}
    if c.startswith('from:') and 'to:' in c:
        parts = dict(p.split(':', 1) for p in c.split(';'))
        return 'date', {k.strip(): v.strip() for k, v in parts.items()}
    if c.startswith('min:') and '1stQ:' in c:
        stats = {}
        for p in c.split(';'):
            k, _, v = p.partition(':')
            stats[k.strip()] = v.strip()
        return 'numeric', stats
    if re.match(r'^\d+ unique values$', c):
        return 'unique', c
    return 'other', c


def _render_numeric_table(variants):
    """One table, one row per numeric variant (capped)."""
    shown, extra = variants[:MAX_VARIANTS], max(0, len(variants) - MAX_VARIANTS)
    head = ''.join(f'<th>{k}</th>' for k in _NUM_KEYS)
    rows = ''.join(
        '<tr>' + ''.join(f'<td>{_fmt_num(stats.get(k, ""))}</td>' for k in _NUM_KEYS) + '</tr>'
        for stats in shown)
    more = f'<div class="var-more">(+{extra} more variants across files)</div>' if extra else ''
    return f'<table class="var-num"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>{more}'


def _render_categorical(variants):
    """One counts+bars table per distinct level-set (capped)."""
    shown, extra = variants[:MAX_VARIANTS], max(0, len(variants) - MAX_VARIANTS)
    blocks = []
    for v in shown:
        total = sum(c for _, c in v['levels']) or 1
        rows = ''
        for name, count in v['levels']:
            pct = 100 * count / total
            rows += (f'<tr><td class="lvl">{name}</td>'
                     f'<td><div class="var-bar"><div style="width:{pct:.1f}%"></div></div></td>'
                     f'<td class="cnt">{count:,} ({pct:.0f}%)</td></tr>')
        note = f'<div class="var-more">+{v["more"]} more levels</div>' if v['more'] else ''
        blocks.append(f'<div class="var-cat-variant">'
                      f'<table class="var-cat"><tbody>{rows}</tbody></table>{note}</div>')
    if extra:
        blocks.append(f'<div class="var-more">(+{extra} more variants across files)</div>')
    return ''.join(blocks)


def _render_unique(uniques):
    """Collapse the distinct 'N unique values' chunks into a single min-max range."""
    nums = [int(m.group(1)) for u in uniques if (m := re.match(r'(\d+) unique values', u))]
    if not nums:
        return ''
    lo, hi = min(nums), max(nums)
    rng = f'<b>{lo:,}</b>' if lo == hi else f'<b>{lo:,}</b> &ndash; <b>{hi:,}</b>'
    return f'<div class="var-line">{rng} unique values</div>'


def _render_files(files_value):
    """List the files this variable appears in, capped at MAX_FILES."""
    files = [f.strip() for f in str(files_value).split(';') if f.strip()]
    if not files:
        return ''
    shown, extra = files[:MAX_FILES], max(0, len(files) - MAX_FILES)
    items = ''.join(f'<li>{f}</li>' for f in shown)
    more = f'<li class="var-more">(+{extra} more files)</li>' if extra else ''
    return (f'<div class="var-files"><div class="var-files-head">Files:</div>'
            f'<ul class="var-files-list">{items}{more}</ul></div>')


def _render_variable(var_name, row):
    label = row['label'] if pd.notna(row['label']) else ''
    chunks = [_classify_chunk(ch) for ch in str(row['summary']).split('||')]

    # Group chunks by shape, keeping first-seen order
    numeric = [p for s, p in chunks if s == 'numeric']
    categorical = [p for s, p in chunks if s == 'categorical']
    dates = [p for s, p in chunks if s == 'date']
    uniques = [p for s, p in chunks if s == 'unique']
    others = [p for s, p in chunks if s == 'other']

    summary = ''
    if numeric:
        summary += _render_numeric_table(numeric)
    if categorical:
        summary += _render_categorical(categorical)
    for d in dates[:MAX_VARIANTS]:
        summary += (f'<div class="var-line">{d.get("from", "?")} &rarr; {d.get("to", "?")} '
                    f'<span class="cnt">(median {d.get("median", "?")})</span></div>')
    summary += _render_unique(uniques)  # collapsed to a 'min - max unique values' range
    for o in others:
        summary += f'<div class="var-line">{o}</div>'

    # Split the whole block into two columns: everything about the variable on the
    # left (65%), the files it appears in on the right (35%), top-aligned so the files
    # line up with the variable name rather than with the summaries.
    left = (f'<div class="var-head"><strong>{var_name}</strong>'
            f'<span class="var-type-badge">{row["type"]}</span>'
            f'<span class="var-n">n&nbsp;= {row["n"]}</span></div>'
            f'<div class="var-label">{label}</div>'
            f'{summary}')

    return (f'<div class="var-block"><div class="var-cols">'
            f'<div class="var-col-summary">{left}</div>'
            f'<div class="var-col-files">{_render_files(row["files"])}</div>'
            f'</div></div>')


def display_variable_info(var_names, table=metadata_table):

    # Look up the selected variables by name (unique key), preserving selection order
    sub_table = table.set_index('variable').loc[list(var_names)]

    return ''.join(_render_variable(var_name, row) for var_name, row in sub_table.iterrows())
