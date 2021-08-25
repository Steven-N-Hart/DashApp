import dash_html_components as html
import dash_core_components as dcc

datasets = ['iris', 'idconsult', 'tsr']

dataset_layout = html.Div([
    dcc.Dropdown(
        id="dataset_name_dropdown",
        options=[{"label": x, "value": x}
                 for x in datasets],
        value=datasets[0],
        multi=False
    )
])

