from dash import html
from dash import dcc

rc_lo = html.Div([
    html.Table(id='rc-records-table'),
    html.Div([
        html.H1("Annotations"),
        dcc.Graph(id='rc-annotations'),
        html.H1("Slides"),
        dcc.Graph(id='rc-stain-count')
    ], style={'columnCount': 2}),
    html.Div(id='rc-records', style={'display': 'none'}),
])