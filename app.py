import dash
from dash.html import Div
import os

from custom_utils.utils import callback_manager as l_cb
from custom_utils.layouts import dataset_layout
from custom_utils.gh_callbacks import callback_manager as gh_cb
from custom_utils.redcap_callbacks import callback_manager as rc_cb
from custom_utils.layouts import lo
from custom_utils.redcap_layouts import rc_lo

for x in ['GH_TOKEN', 'REDCAP_TSR_TOKEN', 'REDCAP_IDC_TOKEN']:
    if x not in os.environ.keys():
        raise KeyError(f"You need to set your {x} environment variable!")


external_stylesheets = ['https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
l_cb.attach_to_app(app)
gh_cb.attach_to_app(app)
rc_cb.attach_to_app(app)

app.layout = Div([
    dataset_layout,
    lo,
    rc_lo
])



if __name__ == '__main__':
    app.run_server(debug=True)