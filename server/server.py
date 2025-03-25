import flask
import json

app = flask.Flask(__name__)

@app.rout("/SERVER", methods=["GET"])
def get():
    d = open('leaderboard.json')
    data = json.load(d)
    return data

@app.rout("/TEST", methods=["POST"])
def send():
    print(json.loads(flask.request.json)["data"])
    d = open('leaderboard.json')
    data = json.load(d)
    data["score"].append(json.loads(flask.request.json)["data"][0])
    data["user"].append(json.loads(flask.request.json)["data"][1])
    with open("leaderboard.json", "w") as outfile:
        json.dump(data, outfile)
    return data["score"]

app.run()
    
