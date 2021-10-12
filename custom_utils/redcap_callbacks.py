import pandas as pd
from custom_utils.utils import generate_table
from custom_utils import redcap_utils as ru
from dash.dependencies import Input, Output
from custom_utils.callback_manager import CallbackManager
import plotly.graph_objects as go
import plotly.express as px

callback_manager = CallbackManager()

@callback_manager.callback(
    Output('rc-records', 'children'),
    [
        Input('dataset_name_dropdown', 'value')
    ]
)
def get_data(value):
    records = ru.get_redcap_data(value)
    return records.to_json()


@callback_manager.callback(
    Output('rc-records-table', 'children'),
    [
        Input('rc-records', 'children')
    ]
)
def update_table(jsonified_cleaned_data):
    return generate_table(pd.read_json(jsonified_cleaned_data))


@callback_manager.callback(
    Output('rc-stain-count', 'figure'),
    [
        Input('rc-records', 'children'), Input('dataset_name_dropdown', 'value')
    ]
)
def update_chart(jsonified_cleaned_data, dataset_name):
    df = pd.read_json(jsonified_cleaned_data)
    if dataset_name == 'DLMP-AI/ID-Consultation':
        fig = px.histogram(df,
                           x="sub_project",
                           pattern_shape='prc_scanning_complete',
                            color="slide_stain")
    elif dataset_name == 'DLMP-AI/m087494_ganomaly':
        fig = None
    return fig



@callback_manager.callback(
    Output('rc-annotations', 'figure'),
    [
        Input('rc-records', 'children'), Input('dataset_name_dropdown', 'value')
    ]
)
def update_chart(jsonified_cleaned_data, dataset_name):
    df = pd.read_json(jsonified_cleaned_data)
    df.reset_index(inplace=True)
    if dataset_name == 'DLMP-AI/ID-Consultation':
        fig = px.bar(df, y="sub_project", x=['anno_chady', 'anno_trynda', 'annot_tom'])
        fig.update_layout(barmode="group")
    elif dataset_name == 'DLMP-AI/m087494_ganomaly':
        fig = None
    return fig
