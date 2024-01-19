from flask import Flask, render_template, request
import plotly.express as px
import sim

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
        await sim.main(float(json["temp"]))
        return {"time": sim.time, "outFlow": sim.waterFlowLitres, "heaterPower": sim.heaterPower, "temp": sim.temp}


if __name__ == '__main__':
    app.run(debug=True)
