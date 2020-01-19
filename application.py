from flask import Flask, render_template, request
import requests
import json
from google.appengine.api import urlfetch
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def decrypt(key):
    decrypted = ""
    for char in key:
        decrypted += chr(ord(char) - 1)
    return decrypted

@app.route("/api")
def walk():
    origin = request.args.get("origin").lower().replace(" ", "+")
    destination = request.args.get("destination")
    key = "BJ{bTzDYx8Kb{Zyut`fp1jQzvo3zuYiGFqxigYR"
    URL = "https://maps.googleapis.com/maps/api/directions/json"
    PARAMS = {
        "origin": origin,
        "destination": destination,
        "mode": "walking",
        "key": decrypt(key)
    }
    r = urlfetch.fetch("{}?origin={}&destination={}&mode=walking&key={}".format(URL, origin, destination, PARAMS["key"]))
    data = json.loads(r.content)
    distance = data["routes"][0]["legs"][0]["distance"]["text"]
    duration = data["routes"][0]["legs"][0]["duration"]["value"] # in seconds
    podcast = search(duration)
    try:
        return render_template("podcast.html", name=podcast[0], url=podcast[1], genre=podcast[3])
    except:
        return str(podcast)

def search(duration):
    with open("podsample1.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        diff = 99999999
        saved = 0
        count = 0
        for row in csv_reader:
            new_diff = abs(int(row[2]) - duration)
            if new_diff < diff:
                diff = new_diff
                saved = row
            count += 1
        return saved