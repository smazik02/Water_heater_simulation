from flask import Flask, redirect, url_for, render_template, request
import plotly.express as px
import sim
import pandas as pd

# app = dash.Dash(__name__)
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        return render_template("index.html")


@app.route("/start", methods=["POST"])
async def start():
    if request.method == "POST":
        if request.headers.get("Content-Type") != "application/json":
            return 'Content type not supported'
        json = request.json
        await sim.main(int(json["simTime"]), int(json["power"]), int(json["waterCap"]), float(json["temp"]))
        return {"time": sim.time, "outFlow": sim.outFlow, "e": sim.e, "volt": sim.volt, "heaterPower": sim.heaterPower, "temp": sim.temp}


# @app.route("/<name>")
# def user(name):
#     return render_template("index.html")


# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if request.method == "GET":
#         return render_template("index.html")
#     else:
#         return "Hi"


# @app.route("/admin")
# def admin():
#     return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)


# tempChart = px.line(x=sim.time,
#                     y=sim.temp,
#                     title='Water temperature')
# voltChart = px.line(x=sim.time,
#                     y=sim.volt,
#                     title='Voltage')
# powerChart = px.line(x=sim.time,
#                      y=sim.heaterPower,
#                      title='Heater power')
# inFlowChart = px.line(x=sim.time,
#                       y=sim.inFlow,
#                       title='InFlow')
# eChart = px.line(x=sim.time,
#                  y=sim.e,
#                  title='Uchyb')

# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),
#     html.Div(children='''
#         Dash: A web application framework for Python.
#         '''),
#     dcc.Graph(
#         id='height',
#         figure=tempChart
#     ),
#     dcc.Graph(
#         id='volt',
#         figure=voltChart
#     ),
#     dcc.Graph(
#         id='power',
#         figure=powerChart
#     ),
#     dcc.Graph(
#         id='imflow',
#         figure=inFlowChart
#     ),
#     dcc.Graph(
#         id='uchyb',
#         figure=eChart
#     )
# ])
