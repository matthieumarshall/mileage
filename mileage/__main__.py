import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from mileage.data import df
import logging
import pandas as pd

import io

logging.basicConfig(filename="mileage.log", level=logging.DEBUG)


dropdown_options = [
    {"label": "miles", "value": "miles"},
    {"label": "kilometres", "value": "kilometres"},
]

logging.info(f"dropdown_options are {dropdown_options}")

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Line Graph"),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '50%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=False
        ),
        dcc.Dropdown(id="units", options=dropdown_options, value="kilometres"),
        dcc.Graph(id="mileage-graph"),
        html.Br(),
        dcc.Input(id="my-input"),
    ]
)


@app.callback(
    dash.dependencies.Output("mileage-graph", "figure"),
    [dash.dependencies.Input("units", "value")]
)
def define_figure(miles_or_km):
    logging.info(f"selected column is {miles_or_km}")
    fig = px.line(df, x=df.index, y=miles_or_km)

    rolling_avg = df[miles_or_km].rolling(window=7).mean()

    fig.add_trace(go.Scatter(x=df.index, y=rolling_avg, name="7 day moving average"))

    units = {"miles": "m", "kilometres": "km"}[miles_or_km]
    # figure formatting
    fig.update_yaxes(title=f"Distance per day ({units})")
    fig.update_xaxes(title="Date")
    return fig


@app.callback(
    dash.dependencies.Output("my-input", "value"),
    [dash.dependencies.Input("units", "value")]
)
def define_textbox(miles_or_km):
    return f"You have selected {miles_or_km}"


# define the callback for uploading data and updating the graph
@app.callback(dash.dependencies.Output('mileage-graph', 'figure', allow_duplicate=True),
              dash.dependencies.Input('upload-data', 'contents'),
              dash.dependencies.State('upload-data', 'filename'),
              prevent_initial_call=True)
def update_graph(contents, _):
    if contents is not None:
        # read in the uploaded file
        df = pd.read_csv(io.BytesIO(contents[0]))
        df.fillna(0, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
        df.set_index("Date", inplace=True)
        df["miles"] = df["kilometres"] * 0.62137119

        # create a plotly figure from the data
        fig = px.line(df, x=df.index, y="kilometres")

        rolling_avg = df["kilometres"].rolling(window=7).mean()

        fig.add_trace(go.Scatter(x=df.index, y=rolling_avg, name="7 day moving average"))

        units = {"miles": "m", "kilometres": "km"}["kilometres"]
        # figure formatting
        fig.update_yaxes(title=f"Distance per day ({units})")
        fig.update_xaxes(title="Date")
        return fig

if __name__ == "__main__":
    app.run_server(debug=True)
