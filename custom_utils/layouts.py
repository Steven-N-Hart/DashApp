from dash import html
from dash import dcc

datasets = ['DLMP-AI/ID-Consultation', 'DLMP-AI/m087494_ganomaly']

dataset_layout = html.Div([
    dcc.Dropdown(
        id="dataset_name_dropdown",
        options=[{"label": x, "value": x}
                 for x in datasets],
        value=datasets[0],
        multi=False
    ),

])



lo = html.Div(children=[
    html.H1("Issues"),
    dcc.Graph(id='issue-assigned'),
    html.Br(),
    html.H1("Milestones"),
    html.Div([
        dcc.Graph(id='milestone-map'),
        dcc.Graph(id='milestone-gauge'),
        ],
        style={'columnCount': 2}
    ),
    html.Table(id='milestones-table'),
    html.Div(id='gh-milestones', style={'display': 'none'}),
    html.Div(id='gh-issues', style={'display': 'none'})
])