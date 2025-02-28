from shiny import ui
import faicons as fa

guru_colors = {'background-lightblue': '#e2e9f1',
               'background-lightgrey': '#F2F2F2',
               'genR-blue': '#2c3c94',
               'mother-lightshade': '#ffeae5',
               'mother-darkshade': '#A32219',
               'father-lightshade': '#E9FFFB',  # e5f4ff # lightblue
               'father-darkshade': '#5B9F84',
               'child-lightshade': '#fff292',
               'child-darkshade': '#F5C242',
               }

user_input_panel_style = f'padding-top: 20px; padding-right: 30px; padding-left: 30px; ' \
                         f'border-radius: 30px; ' \
                         f'background-color: {guru_colors["background-lightblue"]}'

overview_icon_dict = {'mother-self': ui.span(fa.icon_svg('square'), style=f'color: {guru_colors["mother-darkshade"]};'),
                      'mother-child': ui.span(fa.icon_svg('square'), style=f'color: {guru_colors["child-darkshade"]};'),
                      'partner-self': ui.span(fa.icon_svg('diamond'), style=f'color: {guru_colors["father-darkshade"]};'),
                      'partner-child': ui.span(fa.icon_svg('diamond'), style=f'color: {guru_colors["child-darkshade"]};'),
                      'child-self': ui.span(fa.icon_svg('circle'), style=f'color: {guru_colors["child-darkshade"]};'),
                      'teacher-child': ui.span(fa.icon_svg('star-of-life'), style=f'color: {guru_colors["child-darkshade"]};')
                      }

subject_choices = {'child': 'Child',
                   'mother': 'Mother / main caregiver',
                   'father': 'Father / partner'}
                 # 'family': 'Family'}

reporter_choices = {'child': 'Child',
                    'mother': 'Mother / main caregiver',
                    'father': 'Father / partner',
                    'teacher': 'Teacher'}

overview_time_choices = {'Pre': 'Pregnancy',
                         '2m': '2 months',
                         '6m': '6 months',
                         '1y': '1 year',
                         '2y': '2 years',
                         '3y': '3 years',
                         '4y': '4 years',
                         '6y': '6 years',
                         '8y': '8 years',
                         '10y': '10 years',
                         '14y': '14 years',
                         '18y': '18 years'}

variable_time_choices = {'Pregnancy': {'20w': '1st trimester',
                                       '25w': '2nd trimester',
                                       '30w': '3rd trimester'},
                         'Infancy': {'0': 'birth',
                                     '2m': '2 months',
                                     '6m': '6 months'},
                         'Pre-school': {'1y': '1 year',
                                        '2y': '2 years',
                                        '3y': '3 years'},
                         'School-age': {'6y': '6 years',
                                        '10y': '10 years'},
                         'Adolescence': {'14y': '14 years',
                                         '18y': '18 years'}}



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

