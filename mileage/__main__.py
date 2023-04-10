import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import logging
import pandas as pd
import io
import base64

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
    dash.dependencies.Output("mileage-graph", "figure"),
    [dash.dependencies.Input("units", "value"), dash.dependencies.Input("upload-data", "contents")],
    dash.dependencies.State("upload-data", "filename")
)
def define_figure(units, contents, _):

    if contents:
        _, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        if "kilometres" in df.columns and "miles" in df.columns:
            pass
        elif "kilometres" in df.columns:
            df["miles"] = df["kilometres"] * 0.62137119
        elif "miles" in df.columns:
            df["kilometres"] = df["miles"] * 1.60934
        else:
            raise Exception(f"Neither kilometres or miles found in uploaded file. Columns are {df.columns}")
    else:
        df = pd.read_csv("./data/mileage.csv")
        df["miles"] = df["kilometres"] * 0.62137119

    if "Date" not in df.columns:
        raise Exception(f"Date not found in df.columns. Columns are {df.columns}")

    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    df.set_index("Date", inplace=True)
    df.fillna(0, inplace=True)

    fig = px.line(df, x=df.index, y=units)

    rolling_avg = df[units].rolling(window=7).mean()

    fig.add_trace(go.Scatter(x=df.index, y=rolling_avg, name="7 day moving average"))

    units = {"miles": "m", "kilometres": "km"}[units]
    # figure formatting
    fig.update_yaxes(title=f"Distance per day ({units})")
    fig.update_xaxes(title="Date")
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
