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
        df['Entered']=df.index
        fig = px.bar(df,
                           x="sub_project",
                           y='Entered',
                           color="disease_status")
        fig.update_layout(barmode="group")

    else:
        raise ValueError("Wrong study selected")
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
    # print(f'Dataset name: {dataset_name}')
    # print(df.columns)
    if dataset_name == 'DLMP-AI/ID-Consultation':
        fig = px.bar(df, y="sub_project", x=['anno_chady', 'anno_trynda', 'annot_tom'])
        fig.update_layout(barmode="group")
    else:                                               # dataset_name == 'DLMP-AI/m087494_ganomaly':
        fig = px.histogram(df, x="sub_project", color="anno_blessed")
        fig.update_layout(barmode="group")
    return fig
