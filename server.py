from ssl import ALERT_DESCRIPTION_NO_RENEGOTIATION
from flask import Flask, request, jsonify
import algorithm
import googlemaps

gmaps = googlemaps.Client(key="AIzaSyAcZ1jE7ZPYFR32EOTo4tWbXUU3hw09078")


# create new app
app = Flask(__name__)


@app.route('/')
def main():
    return 'StreetSmart.py'

@app.route('/database/<x>/<y>')
def search(x, y):
    return str(algorithm.search(x,y))

@app.route('/route/<x>/<y>')
def route(x,y):
    d = gmaps.directions(origin=x,destination=y,mode='transit',avoid=search(x,y),alternatives=True)[0]
    return d


if __name__ == "__main__":
    app.run(debug=True)
