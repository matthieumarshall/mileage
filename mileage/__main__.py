import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from mileage.data import df
import logging

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
        dcc.Dropdown(id="units", options=dropdown_options, value="kilometres"),
        dcc.Graph(id="mileage-graph")
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

if __name__ == "__main__":
    app.run_server(debug=True)
