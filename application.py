from flask import Flask, render_template
import requests
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def decrypt(key):
    decrypted = ""
    for char in key:
        decrypted += chr(ord(char) - 1)
    return decrypted

@app.route("/<origin>/<destination>")
def walk():
    key = "BJ{bTzDYx8Kb{Zyut`fp1jQzvo3zuYiGFqxigYR"
    URL = "https://maps.googleapis.com/maps/api/directions/json"
    PARAMS = {
        "origin": origin,
        "destination": destination,
        "mode": "walking",
        "key": decrypt(key)
    }
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    print(data)