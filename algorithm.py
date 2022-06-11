from googlemaps import convert
from tokenize import String
import googlemaps
import pandas as pd
import sqlite3

gmaps = googlemaps.Client(key="AIzaSyAcZ1jE7ZPYFR32EOTo4tWbXUU3hw09078")
newdf = pd.read_csv('/Users/SaadDev/Desktop/Projects/StreetSmart/assets/data/final.csv')
database = r"/Users/SaadDev/Desktop/Projects/StreetSmart/assets/data/final.db"
global min_lat, max_lat, min_lng, max_lng


def search(x, y):
    global min_lat, max_lat, min_lng, max_lng
    db = r"/Users/SaadDev/Desktop/Projects/StreetSmart/assets/data/final.db"
    con = sqlite3.connect(db)
    org = gmaps.geocode(x)
    des = gmaps.geocode(y)

    org_lat = org[0]['geometry']['location']['lat']
    org_lng = org[0]['geometry']['location']['lng']

    des_lat = des[0]['geometry']['location']['lat']
    des_lng = des[0]['geometry']['location']['lng']

    if org_lat > des_lat:
        max_lat = org_lat
        min_lat = des_lat
    elif org_lat < des_lat:
        max_lat = des_lat
        min_lat = org_lat

    if org_lng > des_lng:
        max_lng = org_lng
        min_lng = des_lng
    elif org_lng < des_lng:
        max_lng = des_lng
        min_lng = org_lng

    cur = con.cursor()
    p = (min_lat, max_lat, min_lng, max_lng)
    cur.execute('''SELECT * FROM final WHERE Latitude BETWEEN ? AND ? AND Longitude BETWEEN ? AND ? ''', p)
    ans = cur.fetchall()
    a = []
    for i in ans:
        a.append(i)
    return a

def directions(client, origin, destination,
               mode=None, waypoints=None, alternatives=False, avoid=None,
               language=None, units=None, region=None, departure_time=None,
               arrival_time=None, optimize_waypoints=False, transit_mode=None,
               transit_routing_preference=None, traffic_model=None):
    """

    :param origin: The address or latitude/longitude value from which you wish
        to calculate directions.
    :type origin: string, dict, list, or tuple
    value: org_input FLUTTER

    :param destination: The address or latitude/longitude value from which
        you wish to calculate directions. You can use a place_id as destination
        by putting 'place_id:' as a prefix in the passing parameter.
    :type destination: string, dict, list, or tuple
    value: des_input FLUTTER

    :param mode: Specifies the mode of transport to use when calculating
        directions. One of "driving", "walking", "bicycling" or "transit"
    :type mode: string
    value: const "walking"

    :param alternatives: If True, more than one route may be returned in the
        response.
    :type alternatives: bool
    value: const True

    :param avoid: Indicates that the calculated route(s) should avoid the
        indicated features.
    :type avoid: list or string
    value: searchrange.sqlsearch(org_input, des_input) PYTHON

    :param optimize_waypoints: Optimize the provided route by rearranging the
        waypoints in a more efficient order.
    :type optimize_waypoints: bool
    value: const True

    :param transit_routing_preference: Specifies preferences for transit
        requests. Valid values are "less_walking" or "fewer_transfers"
    :type transit_routing_preference: string

    :rtype: list of routes

    """

    params = {
        "origin": convert.latlng(origin),
        "destination": convert.latlng(destination)
    }

    if mode:
        if mode not in ["driving", "walking", "bicycling", "transit"]:
            raise ValueError("Invalid travel mode.")
        params["mode"] = mode

    if waypoints:
        waypoints = convert.location_list(waypoints)
        if optimize_waypoints:
            waypoints = "optimize:true|" + waypoints
        params["waypoints"] = waypoints

    if alternatives:
        params["alternatives"] = "true"

    if avoid:
        params["avoid"] = convert.join_list("|", avoid)

    if language:
        params["language"] = language

    if units:
        params["units"] = units

    if region:
        params["region"] = region

    if departure_time:
        params["departure_time"] = convert.time(departure_time)

    if arrival_time:
        params["arrival_time"] = convert.time(arrival_time)

    if departure_time and arrival_time:
        raise ValueError("Should not specify both departure_time and"
                         "arrival_time.")

    if transit_mode:
        params["transit_mode"] = convert.join_list("|", transit_mode)

    if transit_routing_preference:
        params["transit_routing_preference"] = transit_routing_preference

    if traffic_model:
        params["traffic_model"] = traffic_model

    return client._request("/maps/api/directions/json", params).get("routes", [])

