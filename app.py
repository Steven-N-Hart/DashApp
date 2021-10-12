import dash
from dash.html import Div


from custom_utils.utils import callback_manager as l_cb
from custom_utils.layouts import dataset_layout
from custom_utils.gh_callbacks import callback_manager as gh_cb

from custom_utils.layouts import lo

external_stylesheets = ['https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
l_cb.attach_to_app(app)
gh_cb.attach_to_app(app)

app.layout = Div([
    dataset_layout,
    lo,
])



if __name__ == '__main__':
    app.run_server(debug=True)