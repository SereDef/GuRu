from shiny import ui, reactive
from faicons import icon_svg

from definitions.terms_and_styles import banner_panel

# Individual component groups ==========================================================================================
page_id = 'datadive'

# (key, title, icon, placeholder text) for each curated data subset
SUBSETS = [
    ('omics', 'OMICS', 'dna',
     'Placeholder for the **OMICS data** dive: genetics, methylation, metabolomics, etc. '
     'Describe here what is available, how it is structured, and how to request access.'),
    ('neuro', 'Neuroimaging', 'brain',
     'Placeholder for the **Neuroimaging** dive: structural and functional MRI, DTI, and derived measures. '
     'Describe the available scans, processing pipelines, and relevant files.'),
    ('growth', 'Growth', 'seedling',
     'Placeholder for the **Growth** dive: anthropometry, BMI trajectories, bone and body composition. '
     'Describe the longitudinal measures and how they are harmonised.'),
    ('parenting', 'Parenting', 'person-breastfeeding',
     'Placeholder for the **Parenting** dive: parenting behaviour, home environment, and family context. '
     'Describe the questionnaires and observational measures collected.'),
]


def _subset_card(key, title, icon):
    """A big clickable card that opens the matching subset page."""
    return ui.input_action_button(
        id=f'{page_id}_open_{key}',
        label=ui.TagList(icon_svg(icon, height='2.5em'), ui.div(title, class_='datadive-card-title')),
        class_='datadive-card')


def _subset_panel(key, title, icon, placeholder):
    """One hidden panel per subset, with a back link to the landing view."""
    return ui.nav_panel(
        title,
        ui.input_action_link(id=f'{page_id}_back_{key}',
                             label=ui.TagList(icon_svg('arrow-left'), ' Back to Data Dives'),
                             class_='datadive-back'),
        ui.h3(ui.TagList(icon_svg(icon), ' ', title), style='color: var(--genr-blue); margin-top: 10px;'),
        ui.markdown(placeholder),
        value=key)


def datadive_page(tab_name):

    landing = ui.nav_panel(
        'home',
        ui.markdown('Dive into curated views of specific data domains. '
                    'Pick a topic below to explore what is available:'),
        ui.layout_columns(*[_subset_card(k, title, icon) for k, title, icon, _ in SUBSETS],
                          col_widths=(3, 3, 3, 3),
                          gap='20px',
                          style='margin-top: 20px;'),
        value='home')

    subset_panels = [_subset_panel(k, title, icon, text) for k, title, icon, text in SUBSETS]

    return ui.nav_panel(' Data Dives',
                        banner_panel,
                        ui.div(
                            ui.navset_hidden(landing, *subset_panels,
                                             id=f'{page_id}_nav', selected='home'),
                            style='margin: 20px 30px;'),
                        icon=icon_svg('person-swimming'),
                        value=tab_name)


# Reactivity ===========================================================================================================
def datadive_reactivity(input, output):

    def _register(key):
        @reactive.effect
        @reactive.event(input[f'{page_id}_open_{key}'])
        def _open():
            ui.update_navs(f'{page_id}_nav', selected=key)

        @reactive.effect
        @reactive.event(input[f'{page_id}_back_{key}'])
        def _back():
            ui.update_navs(f'{page_id}_nav', selected='home')

    for key, *_ in SUBSETS:
        _register(key)
