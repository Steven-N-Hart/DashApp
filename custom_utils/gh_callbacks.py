import datetime

from custom_utils.utils import generate_table
import pandas as pd
from custom_utils import gh_utils
from dash.dependencies import Input, Output
from custom_utils.callback_manager import CallbackManager
import plotly.graph_objects as go
import plotly.express as px

callback_manager = CallbackManager()

@callback_manager.callback(
    Output('gh-issues', 'children'),
    [
        Input('dataset_name_dropdown', 'value')
    ]
)
def get_data(value):
    issue_df = gh_utils.get_gh_issues(repo=value)
    issue_df.reset_index(drop=True, inplace=True)
    return issue_df.to_json()

@callback_manager.callback(
    Output('gh-milestones', 'children'),
    [
        Input('dataset_name_dropdown', 'value')
    ]
)
def get_data(value):
    milestones_df = gh_utils.get_gh_milestones(repo=value)
    milestones_df.reset_index(drop=True, inplace=True)
    return milestones_df.to_json()


# @callback_manager.callback(Output('issues-table', 'children'), [Input('gh-issues', 'children')])
# def update_table(jsonified_cleaned_data):
#     dff = pd.read_json(jsonified_cleaned_data)
#     return generate_table(dff)
#
# @callback_manager.callback(Output('milestones-table', 'children'), [Input('gh-milestones', 'children')])
# def update_table(jsonified_cleaned_data):
#     dff = pd.read_json(jsonified_cleaned_data)
#     return generate_table(dff)


@callback_manager.callback(Output('milestone-gauge', 'figure'), [Input('gh-milestones', 'children')])
def milestone_gauge(df):
    df = pd.read_json(df)
    total_events = df.shape[0]
    completed_events = df[df['state'] != 'open'].shape[0]
    #print(f'total_events: {total_events}, completed_events: {completed_events}')
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=completed_events,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Completed"},
        gauge={'axis': {'range': [None, total_events]}}
        )
    )
    return fig


@callback_manager.callback(Output('milestone-map', 'figure'), [Input('gh-milestones', 'children')])
def gantt(df):
    df = pd.read_json(df)
    fig = px.timeline(df,
                 x_start='now',
                 x_end='due_date',
                 y="title",
                 color='overdue')
    fig.update_yaxes(autorange="reversed")
    return fig

@callback_manager.callback(Output('issue-assigned', 'figure'), [Input('gh-issues', 'children')])
def issue_barplot(df):
    df = pd.read_json(df)
    summary = df.groupby(['assignees', 'state']).count()
    summary.reset_index(inplace=True)

    fig = px.bar(summary,
                 x="assignees",
                 y="title",
                 color='state',
                 barmode="group")

    return fig
