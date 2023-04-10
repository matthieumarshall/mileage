from dash import dcc
from dash import html
from dash import Dash
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
import logging
from pandas import read_csv, to_datetime
from io import StringIO
import base64

logging.basicConfig(filename="mileage.log", level=logging.DEBUG)

dropdown_options = [
    {"label": "miles", "value": "miles"},
    {"label": "kilometres", "value": "kilometres"},
]

logging.info(f"dropdown_options are {dropdown_options}")

app = Dash(__name__)

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
                'width': '100%',
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
        dcc.Graph(id="mileage-graph")
    ]
)

@app.callback(
    Output("mileage-graph", "figure"),
    [Input("units", "value"), Input("upload-data", "contents")],
    State("upload-data", "filename")
)
def define_figure(units, contents, _):

    if contents:
        _, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = read_csv(StringIO(decoded.decode('utf-8')))
        if "kilometres" in df.columns and "miles" in df.columns:
            pass
        elif "kilometres" in df.columns:
            df["miles"] = df["kilometres"] * 0.62137119
        elif "miles" in df.columns:
            df["kilometres"] = df["miles"] * 1.60934
        else:
            raise Exception(f"Neither kilometres or miles found in uploaded file. Columns are {df.columns}")
    else:
        df = read_csv("./data/mileage.csv")
        df["miles"] = df["kilometres"] * 0.62137119

    if "Date" not in df.columns:
        raise Exception(f"Date not found in df.columns. Columns are {df.columns}")

    df["Date"] = to_datetime(df["Date"], format="%d/%m/%Y")
    df.set_index("Date", inplace=True)
    df.fillna(0, inplace=True)

    units_name = {"miles": "m", "kilometres": "km"}[units]
    rolling_avg = df[units].rolling(window=7).mean()
    data = [
        go.Scatter(x=df.index, y=df[units], name=f"Distance per day ({units_name})", line={"width":0.5}),
        go.Scatter(x=df.index, y=rolling_avg, name=f"7 day moving average ({units_name})", line={"width":3})
    ]

    layout = go.Layout(title="Distance plot", legend={"x":1, "y":1})
    fig = go.Figure(data=data, layout=layout)

    # figure formatting
    fig.update_yaxes(title=f"Distance per day ({units_name})")
    fig.update_xaxes(title="Date")
    return fig

if __name__ == "__main__":
    app.run_server()
