# Design pattern for DLMP-AI
In order to keep things simple and maintain context separation, 
we need to keep data and code separate for the different studies.  
This is done by maintaining a folder for each project. An example is 
the `iris` dataset.  Let's look at the folder structure:
```bash
iris/
|--- __init__.py
|--- iris_callbacks.py
|--- iris_layouts.py
```
## __init__.py
This file can be empty, but it's necessary to have when you want to import from that folder.

## iris_callbacks.py
This is where callbacks specific to the `iris` dataset should go.  Callbacks are really just definitions
for when and how to modify the data as fields change. 

### Working with graphs
An example for getting data for a graph object is below:

```python
# First, make sure you import the required objects for building callbacks
from dash.dependencies import Input, Output
from custom_utils.callback_manager import CallbackManager

# My special callback manager. Use this instead of "@app.callback"
callback_manager = CallbackManager()


# This is an example of returning a graph. 
@callback_manager.callback(
    Output("output_id", "figure"),  # Defines the output key and type
    [Input("input_id", "value")]  # Defines where the data are coming from
)
def update_bar_chart(df):  # One Input is defined above, so there must be 1 variable name here
    # some function that does some data munging
    fig = ''  # Build a figure object however you want
    return fig
```

### Working with dataframes
Working with data frames can be a bit trickier than graphs.  The reason is that the dataframes 
usually contain more data, and therefore we want to perform actions on them much less frequently than
plotting pieces of data from them.  To do this, we'll actually have to create an intermediate step with its
own callback function.

```python
from somewhere import get_dataset # some sort of data maniputlation code

@callback_manager.callback(
    Output('intermediate-ds', 'children'),       # Define the output to be in the 'intermediate-ds' variable
    [
        Input('dataset_name_dropdown', 'value')
    ]
)
def get_data(value):
    # some expensive clean data step and or filtering
    cleaned_df = get_dataset(value)
    # convert to JSON so it can be passed around easier
    return cleaned_df.to_json()
```
Now, anytime we want to use that data, we just have to create another callback that uses 'intermediate-ds'
as input. In this case, we'll assign the output to the field 'table'. I'll also import my handy JSON->HTML
table generator code from the `dash_utils` directory.

```python
from custom_utils.utils import generate_table


@callback_manager.callback(Output('table', 'children'), [Input('intermediate-ds', 'children')])
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data)
    return generate_table(dff)

```

## iris_layouts.py
Now that we have the callbacks defined, we need a place to put them. Notice above in the 
[Working with graphs](working-with-graphs) section, we specified an output 
(`output_id`) and an input (`input_id`). Those two components must be defined in the layouts definition.

#### Working with graphs
First, let's make a graph-style object
```python
datasets = ['iris', 'idconsult', 'tsr']

dataset_layout = html.Div([
    dcc.Dropdown(
        id="input_id",                   # This gets used in the callback an Input
        options=[{"label": x, "value": x}
                 for x in datasets],
        value=datasets[0],
        multi=False
    ),
    dcc.Graph(id='output_id')            # This section is where the callback output goes
])
```
### Working with dataframes
For the dataframes example, we created a 'table' and a 'intermediate-value' object. Naturally,
each of these requires a definition in your layouts as well. We'll save these to a variable we can 
import into the main app script later. It's nice to wrap them in an `html` div element.
```python
iris_lo = html.Div(children=[
    html.Table(id='table'),
    html.Div(id='intermediate-ds', style={'display': 'none'})
])
```

## app.py
Now that our callbacks and layouts for the `iris` dataset are defined in thier own files, we need to 
make sure the main `app.py` knows how and when to use them. First, we need to import the code we want to bring into the 
main app. We always need to import the callback_manager from each callback file. I like to import them `as` something
since there will be one from every module, like this:

```python
from iris.iris_callbacks import callback_manager as i_cb    
from iris.iris_layouts import iris_lo # Now import the layout element we created
```
Now we need to instantiate the app and register each of the callback methods with my special
callback manager function:
```python
app = dash.Dash()
i_cb.attach_to_app(app) # Do this for all context managers (one for each callback.py file)
```
Then, create the main div element
```python
app.layout = html.Div([
    iris_lo,                # Any other layouts, just comma delimit them here
])
```
Now make the app responsive:
```python
if __name__ == '__main__':
    app.run_server(debug=True)
```