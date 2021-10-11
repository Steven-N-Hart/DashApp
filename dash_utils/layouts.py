from dash import html
from dash import dcc

datasets = ['idconsult', 'tsr']

dataset_layout = html.Div([
    dcc.Dropdown(
        id="dataset_name_dropdown",
        options=[{"label": x, "value": x}
                 for x in datasets],
        value=datasets[0],
        multi=False
    )
])

