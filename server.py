import dash
from dash import dcc
from dash import html
import plotly.express as px
import sim
import pandas as pd

app = dash.Dash(__name__)

tempChart = px.line(x=sim.time,
                    y=sim.temp,
                    title='Water temperature')
voltChart = px.line(x=sim.time,
                    y=sim.volt,
                    title='Voltage')
powerChart = px.line(x=sim.time,
                     y=sim.heaterPower,
                     title='Heater power')

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for Python.
        '''),
    dcc.Graph(
        id='height',
        figure=tempChart
    ),
    dcc.Graph(
        id='volt',
        figure=voltChart
    ),
    dcc.Graph(
        id='power',
        figure=powerChart
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
