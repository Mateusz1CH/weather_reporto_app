import config
from requests import get
import json
import constants as c
import pandas as pd

API_key = config.auth_key

#functions
def json_to_df(stream_data, search_data, column):
    """_summary_

    Args:
        stream_data (_type_): _description_
        search_data (_type_): _description_
        column (_type_): _description_

    Returns:
        _type_: _description_
    """
    stream_data = { search_data : stream_data[column][search_data] for search_data in search_data }
    stream_d2 = { k : str(v) for k,v in stream_data.items()}
    df_stream = pd.DataFrame(stream_d2, index=[0])
    return df_stream

def df_creatio(stream_data, column):
    """_summary_

    Args:
        stream_data (_type_): _description_
        column (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = {column: stream_data[column]}
    df_stream = pd.DataFrame(data, index=[0])
    return df_stream

class weather:
    """
    Creates a flatmate person who lives in the flat and pays a share of the bill
    """
    def __init__(self, lat, lon):
        self.url_weather = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}"
        self.city_w = get(self.url_weather).json()

    def weather_data(self):
        main_data = json_to_df(self.city_w, c.search_main_data, 'main')
        wind_data = json_to_df(self.city_w, c.search_wind_data, 'wind')
        cloud = json_to_df(self.city_w, c.search_cloud, 'clouds')
        new_df = pd.concat([main_data, wind_data, cloud], axis=1)
        new_df['temp_c'] = float(new_df['temp']) - 272.15
        new_df['feels_like_c'] = float(new_df['feels_like']) - 272.15
        new_df['temp_min_c'] = float(new_df['temp_min']) - 272.15
        new_df['temp_max_c'] = float(new_df['temp_max']) - 272.15
        return new_df

class pollution:
    """
    Creates a flatmate person who lives in the flat and pays a share of the bill
    """
    def __init__(self, lat, lon):
        self.url_polut = f"http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={API_key}"
        self.city_pol = get(self.url_polut).json()

    def pollution_data(self):
        polution_df = self.city_pol['list'][0]
        polution_comp_df = json_to_df(polution_df, c.pollution_comp, 'components')
        polution_comp_df['air_quality_v'] = str(polution_df['main']['aqi'])
        polution_comp_df['air_quality'] = c.polution_quality[str(polution_df['main']['aqi'])]
        return polution_comp_df