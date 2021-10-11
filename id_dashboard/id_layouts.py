from dash import html
from dash.dcc import Store

id_lo = html.Div(children=[
    html.Table(id='issues-table'),
    html.Table(id='milestones-table'),
    Store(id='gh-milestones'),
    Store(id='gh-issues')
])