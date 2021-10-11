from dash_utils.utils import generate_table
import pandas as pd
import id_dashboard.id_utils as id

# First, make sure you import the required objects for building callbacks
from dash.dependencies import Input, Output
from dash_utils.callback_manager import CallbackManager

# My special callback manager. Use this instead of "@app.callback"
callback_manager = CallbackManager()


@callback_manager.callback(
    Output('gh-issues', 'children'),       # Define the output to be in the 'intermediate-ds' variable
    [
        Input('dataset_name_dropdown', 'value')
    ]
)
def get_data(value):
    issue_df = id.get_gh_issues()
    issue_df.reset_index(drop=True, inplace=True)
    print(f'ISSUES: {issue_df}')
    return issue_df.to_json()

@callback_manager.callback(
    Output('gh-milestones', 'children'),       # Define the output to be in the 'intermediate-ds' variable
    [
        Input('dataset_name_dropdown', 'value')
    ]
)
def get_data(value):
    milestones_df = id.get_gh_milestones()
    milestones_df.reset_index(drop=True, inplace=True)
    return milestones_df.to_json()


@callback_manager.callback(Output('issues-table', 'children'), [Input('gh-issues', 'children')])
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data)
    return generate_table(dff)

@callback_manager.callback(Output('milestones-table', 'children'), [Input('gh-milestones', 'children')])
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data)
    return generate_table(dff)