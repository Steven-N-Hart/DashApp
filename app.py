import dash
import dash_html_components as html

from iris.iris_callbacks import callback_manager as i_cb
from iris.iris_layouts import iris_lo
from dash_utils.utils import callback_manager as l_cb
from dash_utils.layouts import dataset_layout



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
i_cb.attach_to_app(app)
l_cb.attach_to_app(app)


app.layout = html.Div([
    dataset_layout,
    iris_lo,
])



if __name__ == '__main__':
    app.run_server(debug=True)