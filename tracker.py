import requests
import csv
import pandas as pd
import plotly.express as px 
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import datetime


app = dash.Dash(__name__)

def get_position():
    URL = "http://api.open-notify.org/iss-now.json"
    request = requests.get(URL).json()

    #print(request)
    latitude = request['iss_position']['latitude']
    longitude = request['iss_position']['longitude']
    timestamp = datetime.datetime.fromtimestamp(request['timestamp'])
    #print(f"Current location: [{latitude},{longitude}]")
    return [latitude,longitude,timestamp]

def write_csv():
    position = get_position()
    print(position)
    
    with open('coordinates.csv', 'a',newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(position)
        
app.layout = html.Div([
    html.H1("ISS Position Tracker", style={'textAlign': 'center'}),
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # Update every 5 seconds
        n_intervals=0
    )
])

# Callback to update graph
@app.callback(
    Output('live-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    # Write new position to CSV
    write_csv()
    # Read all data from csv
    df = pd.read_csv('coordinates.csv')
    # Create the map.
    fig = px.scatter_geo(
        df,
        lat='latitude',
        lon='longitude',
        projection='natural earth',
        hover_data='timestamp'
    )
    #fig.update_layout(autosize=True)
    fig.update_traces(
        marker=dict(size=10, color=['red']*(len(df)-1) + ['blue']),
        selector=dict(mode='markers')
    )
    fig.update_geos(
        showland=True,
        landcolor="lightgray",
        showocean=True,
        oceancolor="azure"
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)