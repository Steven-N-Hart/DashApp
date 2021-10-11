import dash
from dash.html import Div


from dash_utils.utils import callback_manager as l_cb
from dash_utils.layouts import dataset_layout

from id_dashboard.id_callbacks import callback_manager as id_cb
from id_dashboard.id_layouts import id_lo

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
l_cb.attach_to_app(app)
id_cb.attach_to_app(app)

app.layout = Div([
    dataset_layout,
    id_lo,
])



if __name__ == '__main__':
    app.run_server(debug=True)