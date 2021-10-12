from dash import html
from dash import dcc

rc_lo = html.Div([
    html.Table(id='rc-records-table'),
    dcc.Graph(id='rc-annotations'),
    dcc.Graph(id='rc-stain-count'),
    html.Div(id='rc-records', style={'display': 'none'}),
])