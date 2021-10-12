from dash.dependencies import Input, Output
from custom_utils.callback_manager import CallbackManager
import pandas as pd
from custom_utils.utils import get_dataset, generate_table
import plotly.express as px

# Import the custom call-back manager
callback_manager = CallbackManager()

# Annotate the function with the callback manager, defining the inputs and output id
@callback_manager.callback(
    Output('intermediate-value', 'children'),
    [
        Input('dataset_name_dropdown', 'value')
    ]
)
def get_data(value):
    # some expensive clean data step and or filtering
    cleaned_df = get_dataset(value)
    return cleaned_df.to_json()

@callback_manager.callback(Output('table', 'children'), [Input('intermediate-value', 'children')])
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data)
    return generate_table(dff)

@callback_manager.callback(
    Output('graph', 'figure'),
    [
        Input('intermediate-value', 'children'),
        Input('iris_x_value', 'value'),
        Input('iris_y_value', 'value')
    ])
def update_graph(jsonified_cleaned_data, x_value, y_value):
    dff = pd.read_json(jsonified_cleaned_data)
    figure = px.scatter(dff, x=x_value, y=y_value)
    return figure