from road_safety_model import roadsafety as rs

from flask import Flask, request
from flask_cors import CORS, cross_origin

import json

rso = rs.RoadSafety()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def home():
    return "<p>Hello, World!</p>"


@app.route("/api/get-distribution") #month, day, suburb, speed, weather, light
@cross_origin()
def api_dist():
    args = request.args.to_dict()
    print(args)
    for key in args.keys():
        if args[key] == "":
            args[key] = None
    props = rso.get_distribution(args["month"], args["day"], args["suburb"], args["speed"], args["weather"], args["lighting"])
    return json.dumps({
        "filters": args,
        "distribution": props
    })


@app.route("/api/get-suburbs")
@cross_origin()
def api_burbs():
    sub_list = rso.get_suburbs()
    return json.dumps({
        "suburbs": sub_list
    })

@app.route("/api/get-lightings")
@cross_origin()
def api_lights():
    light_list = rso.get_lightings()
    return json.dumps({
        "lightings": light_list
    })

@app.route("/api/get-weathers")
@cross_origin()
def api_weathers():
    weather_list = rso.get_weathers()
    return json.dumps({
        "weathers": weather_list
    })

