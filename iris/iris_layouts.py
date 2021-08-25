import dash_html_components as html
import dash_core_components as dcc

available_fields = ['petal_width',
                    'sepal_width',	'petal_length',	'petal_width',
                    'species',	'species_id']

iris_lo = html.Div(children=[
    html.H1(children='Iris table'),
    dcc.Dropdown(
        id="iris_x_value",
        options=[{"label": x, "value": x}
                 for x in available_fields],
        value='species',
        multi=False
    ),
    dcc.Dropdown(
        id="iris_y_value",
        options=[{"label": x, "value": x}
                 for x in available_fields],
        value='petal_width',
        multi=False
    ),
    dcc.Graph(id='graph'),
    html.Table(id='table'),
    html.Div(id='intermediate-value', style={'display': 'none'})
], style={'columnCount': 2})

