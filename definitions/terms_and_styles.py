from shiny import ui
from faicons import icon_svg

guru_colors = {'background-lightblue': '#e2e9f1',
               'background-lightgrey': '#F2F2F2',
               'genR-blue': '#2c3c94',
               'genR-lightblue': '#84a8cc',
               'mother-lightshade': '#ffeae5',
               'mother-darkshade': '#A32219',
               'father-lightshade': '#e5f4ff',  # '#E9FFFB',
               'father-darkshade': '#5B9F84',
               'child-lightshade': '#fff292',
               'child-darkshade': '#F5C242',
               }

banner_panel = ui.div(ui.span(icon_svg('circle-exclamation'), style='color: #A32219'), 
                      ui.markdown('&ensp;*This app is currently <ins>under development</ins>! ' \
                                  'Please check that the information is correct before reporting it. ' \
                                  'If you spot any errors or missing information, please let us know using GitHub issues or email.*'), 
                      style='display: inline-flex; padding-bottom: 0px; padding-top: 15px; padding-left: 20px; border-radius: 30px; ' \
                            'font-size: 17px; color: #A32219; background-color: #ffeae5; border: 1px solid #A32219;')

user_input_panel_style = f'padding-top: 20px; padding-right: 30px; padding-left: 30px; ' \
                         f'border-radius: 30px; ' \
                         f'background-color: {guru_colors["background-lightblue"]}'

overview_icon_dict = {'mother-self': ui.span(icon_svg('square'), style=f'color: {guru_colors["mother-darkshade"]};'),
                      'mother-child': ui.span(icon_svg('square'), style=f'color: {guru_colors["child-darkshade"]};'),
                      'partner-self': ui.span(icon_svg('diamond'), style=f'color: {guru_colors["father-darkshade"]};'),
                      'partner-child': ui.span(icon_svg('diamond'), style=f'color: {guru_colors["child-darkshade"]};'),
                      'child-self': ui.span(icon_svg('circle'), style=f'color: {guru_colors["child-darkshade"]};'),
                      'teacher-child': ui.span(icon_svg('star-of-life'), style=f'color: {guru_colors["child-darkshade"]};')
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

