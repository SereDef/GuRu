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
                                  'Please check that the information is correct before reporting it.<br>' \
                                  '&ensp;If you spot any errors or missing information, please let us know using GitHub issues or email.*'), 
                      style='display: inline-flex; padding-bottom: 0px; padding-top: 15px; padding-left: 20px; border-radius: 30px; ' \
                            'font-size: 17px; color: #A32219; background-color: #ffeae5; border: 1px solid #A32219;')

user_input_panel_style = f'padding-top: 20px; padding-right: 30px; padding-left: 30px; padding-bottom: 0px;' \
                         f'border-radius: 30px; ' \
                         f'background-color: {guru_colors["background-lightblue"]}'

# zorder = 'position: relative; z-index: 1;' # not needed in the end :) 
overview_icon_dict = {'mother-self': ui.span(icon_svg('square'), style=f'color: {guru_colors["mother-darkshade"]};'),
                      'mother-child': ui.span(icon_svg('square'), style=f'color: {guru_colors["child-darkshade"]};'),
                      'partner-self': ui.span(icon_svg('diamond'), style=f'color: {guru_colors["father-darkshade"]};'),
                      'partner-child': ui.span(icon_svg('diamond'), style=f'color: {guru_colors["child-darkshade"]};'),
                      'child-self': ui.span(icon_svg('circle'), style=f'color: {guru_colors["child-darkshade"]};'),
                      'teacher-child': ui.span(icon_svg('star-of-life'), style=f'color: {guru_colors["child-darkshade"]};'),
                      # measurement table
                      '[mother]': ui.span(icon_svg('square'), style=f'color: {guru_colors["mother-darkshade"]};'),
                      '[father]': ui.span(icon_svg('diamond'), style=f'color: {guru_colors["father-darkshade"]};'),
                      '[child]': ui.span(icon_svg('circle'), style=f'color: {guru_colors["child-darkshade"]};'),
                      '[subsample-mother]': ui.span(icon_svg('square'), style=f'color: {guru_colors["mother-darkshade"]}; stroke: black; stroke-width: 100px;'),
                      '[subsample-father]': ui.span(icon_svg('diamond'), style=f'color: {guru_colors["father-darkshade"]}; stroke: black; stroke-width: 100px;'),
                      '[subsample-child]': ui.span(icon_svg('circle'), style=f'color: {guru_colors["child-darkshade"]}; stroke: black; stroke-width: 100px;'),
                      }

overview_icon_legend = {
  'Questionnaires': ui.markdown(f'&emsp;'
                    f'{overview_icon_dict["mother-self"]} Mother self-report &emsp;&emsp;'
                    f'{overview_icon_dict["partner-self"]} Partner self-report &emsp;&emsp;'
                    f'{overview_icon_dict["child-self"]} Child self-report &emsp;&emsp;'
                    f'{overview_icon_dict["mother-child"]} Mother about the child &emsp;&emsp;'
                    f'{overview_icon_dict["partner-child"]} Partner about the child &emsp;&emsp;'
                    f'{overview_icon_dict["teacher-child"]} Teacher about child<br>'
                    f'&emsp;<span style="color:grey">Click on any row below to display '
                    f'more information about the measure selected.</span>'),
  'Measurements': ui.markdown(f'&emsp;'
                    f'{overview_icon_dict["[mother]"]} Mother &emsp;&emsp;'
                    f'{overview_icon_dict["[father]"]} Partner &emsp;&emsp;'
                    f'{overview_icon_dict["[child]"]} Child &emsp;&emsp;'
                    f'{overview_icon_dict["[subsample-mother]"]} Mother (sub-sample) &emsp;&emsp;'
                    f'{overview_icon_dict["[subsample-father]"]} Partner (sub-sample) &emsp;&emsp;'
                    f'{overview_icon_dict["[subsample-child]"]} Child (sub-sample)<br>'
                    f'&emsp;<span style="color:grey">Click on any cell to display '
                    f'more information about the measure selected.</span>'),
  'Other': ''
}                    

subject_choices = {'child': 'Child',
                   'mother': 'Mother / main caregiver',
                   'father': 'Father / partner'}
                 # 'family': 'Family'}

reporter_choices = {'child': 'Child',
                    'mother': 'Mother / main caregiver',
                    'father': 'Father / partner',
                    'teacher': 'Teacher'}

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

time_points_available = {

  'overview': {
    'Questionnaires' : ['Prenatal', '2 months', '6 months', '1 year', '1.5 years', 
                        '2 years', '2.5 years', '3 years', '4 years', '6 years', 
                        '8 years', '10 years', '14 years', '18 years', '22 years'],
    'Hands-on measurements': ['Prenatal', 'Birth', '6 weeks', '3 months', '6 months', 
                        '1 year', '3 years', '4 years', '6 years', '10 years', 
                        '14 years', '18 years', '22 years'],
    'Other': []
  },

  'variable': {
    'Questionnaires' : ['1st trimester','2nd trimester', '3rd trimester', 'Birth',
                        '2 months', '6 months', '1 year', '2 years', '3 years', '6 years', 
                        '10 years', '14 years', '18 years'],
    'Hands-on measurements': ['1st trimester','2nd trimester', '3rd trimester', 'Birth',
                        '2 months', '6 months', '1 year', '2 years', '3 years', '6 years', 
                        '10 years', '14 years', '18 years'],
    'Other': []
  }

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

