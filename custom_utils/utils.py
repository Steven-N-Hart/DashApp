import plotly.express as px
from custom_utils.callback_manager import CallbackManager
from dash import html

callback_manager = CallbackManager()

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def get_dataset(dataset_name):
    """
    Return either the iris data set (for debugging/dev), ID-Consultation, or TSR

    :param dataset_name: dataset to show (iris, idconsult, tsr)

    :return: pandas dataframe
    """
    # Get data

    if dataset_name == 'iris':
        df = px.data.iris()
        return df

    elif dataset_name == 'idconsult':
        return None
    elif dataset_name == 'tsr':
        return None
    else:
        raise ValueError("dataset_name must be one of 'iris', 'idconsult', or 'tsr'!")