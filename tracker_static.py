import requests
import pandas as pd
import plotly.express as px 
import datetime

def get_position():
    URL = "http://api.open-notify.org/iss-now.json"
    request = requests.get(URL).json()

    #print(request)
    latitude = request['iss_position']['latitude']
    longitude = request['iss_position']['longitude']
    timestamp = datetime.datetime.fromtimestamp(request['timestamp'])
    #print(f"Current location: [{latitude},{longitude}]")
    return [latitude,longitude,timestamp]

def plotter():
    data = pd.read_csv("coordinates.csv")
    fig = px.scatter_geo(data, lat='latitude', lon='longitude')
    fig.update_layout(title = 'World map', title_x=0.5)
    fig.show()

plotter()
