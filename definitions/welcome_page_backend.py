import pandas as pd

import plotly.graph_objects as go

events = pd.read_csv('assets/GenR_timeline.csv', index_col=None)

reporter_colors = {
        'mother': "rgba(33,150,243,0.2)",
        'partner': "rgba(76,175,80,0.2)",
        'child': 'rgba(255,193,7,0.2)',
        'mother-child': 'rgba(255,193,7,0.2)',
        'mother-partner': 'rgba(33,150,243,0.2)',
        'teacher': 'rgba(0,128,128,0.2)'
    }

period_labels = [
        {"name": "Pregnancy", "start": -0.8, "end": 0},
        {"name": "Perinatal", "start": 0.05, "end": 1},
        {"name": "Preschool", "start": 1.05, "end": 4},
        {"name": "Childhood", "start": 4.05, "end": 11},
        {"name": "Adolescence", "start": 11.05, "end": 18},
        {"name": "Young adulthood", "start": 18.05, "end": 22}
    ]

def add_background_rectangles(fig, textlabel,  x_start, x_end, y_bottom=-3, y_top=3, color='rgba(200,200,200,0.2)'):
    # Add a background with periods 
    fig.add_trace(go.Scatter(
        x=[x_start, x_end, x_end, x_start, x_start],
        y=[y_bottom, y_bottom, y_top, y_top, y_bottom],
        fill='toself',
        fillcolor=color,
        line=dict(color='rgba(0,0,0,0)'),
        mode='none',
        showlegend=False,
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=[(x_start + x_end)/2],
        y=[y_bottom + 0.25],
        text=[textlabel],
        mode='text',
        showlegend=False,
        hoverinfo='skip',
        textfont=dict(family="Arial, sans-serif", size=12, color='rgba(0,0,0,0.5)') #, weight='bold')
    ))

def rounded_rectangle(x0, y0, x1, y1, h):   
        if (x1 - x0) < 0.15: 
            h = 0.05
        rounded_bottom_left = f' M {x0+h}, {y0} Q {x0}, {y0} {x0}, {y0+h}'
        rounded_top_left = f' L {x0}, {y1-h} Q {x0}, {y1} {x0+h}, {y1}'
        rounded_top_right = f' L {x1-h}, {y1} Q {x1}, {y1} {x1}, {y1-h}'
        rounded_bottom_right = f' L {x1}, {y0+h} Q {x1}, {y0} {x1-h}, {y0}Z'

        return rounded_bottom_left + rounded_top_left+ rounded_top_right + rounded_bottom_right


def make_timeline_agechild(events=events):
    
    fig = go.Figure()

    for period in period_labels:
        add_background_rectangles(fig, textlabel = period['name'], x_start=period['start'], x_end=period['end'])

    # Add duration bars as shapes
    for event in events.itertuples(index=False):

        fig.add_shape(
            type="path",
            path=rounded_rectangle(event.min_age, event.display_y,
                                   event.max_age, event.display_y+0.4, h=0.15),
            fillcolor=reporter_colors[event.reporter],
            label=dict(text=f'\t{event.name}', textposition='middle left'),
            line=dict(width=0)
        )

    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=-0.10,  # position in normalized coordinates below the plot
        showarrow=False,
        text="<b>Age of child (years)</b>",
        font=dict(size=16, color="black", family='Arial'),
        xanchor="center",
    )

    fig.update_layout(
        title="Generation R Timeline",
        xaxis=dict(# title=dict(text="Age of child (years)", 
                   #           font=dict(size=16, family="Arial", color="black", weight="bold"),
                   #           standoff=60),  # distance in pixels to push title away from the axis ticks
                   range=[-1, 23], rangeslider=dict(visible=True)),
        yaxis=dict(range=[-3, 3]),
        plot_bgcolor='white',
        height=600,
        margin=dict(l=20, r=10, t=50, b=50)
    )

    return fig


def make_timeline():
    events = [
        {"name": "GR1001", "start": "2024-01-01", "end": "2024-03-01", "category": "Questionnaire", "level": 1},
        {"name": "GR1002", "start": "2024-03-15", "end": "2024-06-01", "category": "Questionnaire", "level": 1},
        {"name": "Visit0Y", "start": "2024-07-01", "end": "2024-07-10", "category": "Visit", "level": -1},
    ]

    fig = go.Figure()

    # Add duration bars as shapes
    for i, e in enumerate(events):
        fig.add_shape(
            type="rect",
            xref="x",
            yref="y",
            x0=e["start"],
            x1=e["end"],
            y0=e["level"],
            y1=e["level"]+0.5,
            fillcolor="rgba(33,150,243,0.2)",
            line=dict(width=0)
        )
        fig.add_trace(go.Scatter(
            x=[e["start"]],
            y=[e["level"]+0.25],
            text=[f'\t\t{e["name"]}'],
            mode="text",
            textposition="middle right",
            marker=dict(size=20, color="rgb(33,150,243)")
        ))

    fig.update_layout(
        title="Generation R Timeline",
        xaxis=dict(title="Date", type="date", rangeslider=dict(visible=True)),
        # yaxis=dict(
        #     title="Phases",
        #     showgrid=False,
        #     tickvals=list(range(len(events))),
        #     ticktext=[e["category"] for e in events]
        # ),
        height=600,
        margin=dict(l=80, r=30, t=80, b=60)
    )

    return fig