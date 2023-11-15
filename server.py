import dash
from dash import dcc
from dash import html
import plotly.express as px
import sim
import pandas as pd
import asyncio
import threading


def displayGraphs():
    # stats = sim.getStats()
    # print(stats)

    heightChart = px.line(x=sim.time,
                          y=sim.height,
                          title='Height')
    df = pd.DataFrame({
        'time': sim.time,
        'in': sim.inFlow,
        'out': sim.outFlow
    })
    flowChart = px.line(df, x='time', y=df.columns[1:3], title='Flow')
    voltChart = px.line(x=sim.time,
                        y=sim.volt,
                        title='Voltage')

    return html.Div(children=[
        html.H1(children='Hello Dash'),
        html.Div(children='''
            Dash: A web application framework for Python.
            '''),
        dcc.Graph(
            id='height',
            figure=heightChart
        ),
        dcc.Graph(
            id='flow',
            figure=flowChart
        ),
        dcc.Graph(
            id='volt',
            figure=voltChart
        )
    ])


simulation = threading.Thread(target=sim.sim, daemon=True)
simulation.start()
app = dash.Dash(__name__)
app.layout = displayGraphs
app.run_server(debug=True)
