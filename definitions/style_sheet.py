from pathlib import Path
from shiny import ui

guru_colors = {'background-lightblue': '#DDE5F0',
               'background-lightgrey': '#F2F2F2',
               'genR-blue': '#2c3c94',
               'mother-lightshade': '#ffeae5',
               'mother-darkshade': '#A32219',
               'father-lightshade': '#E9FFFB',  # e5f4ff # lightblue
               'father-darkshade': '#5B9F84',
               'child-lightshade': '#fff292',
               'child-darkshade': '#F5C242',
               }

# Generate theme ----------------------------
# guru_theme = (
#     ui.Theme('lumen')
#     .add_defaults(
#         primary_color=guru_colors['genR-blue'],  # Replace primary color
#         # my_purple="#aa00aa",
#     )
#     # .add_mixins(
#     #     headings_color="$my-purple",
#     # )
# )
#
# with open(Path(__file__).parent / '..' / 'css' / 'guru_theme.css', 'w') as f:
#     f.write(guru_theme.to_css())

