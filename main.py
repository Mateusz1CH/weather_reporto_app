from flask import Flask, render_template

import webscraping as web
import constants as c

app = Flask(__name__)

def get_data():
    weather = web.weather(c.cities_coordinates['Krakow']['lat'], c.cities_coordinates['Krakow']['lon'])
    pollution = web.pollution(c.cities_coordinates['Krakow']['lat'], c.cities_coordinates['Krakow']['lon'])
    return weather.weather_data(), pollution.pollution_data()

@app.route("/")
def index():
    pass
print(get_data())