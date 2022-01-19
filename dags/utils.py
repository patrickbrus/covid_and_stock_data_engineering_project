import yfinance as yf
import requests
import pandas as pd
import json
from datetime import datetime
import os

# global variables
TICKERS = ["^NDX", "^GSPC", "^GDAXI", "^STOXX50E"]
URL_COVID_DATA = "https://data.sfgov.org/resource/nfpa-mg4g.json"
URL_WEATHER_DATA = "https://meteostat.p.rapidapi.com/stations/daily"
RAPIDKEY = os.environ.get("RAPID_WEATHER_API_KEY")

def create_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("Created folder data.")

def extract_stock_data(ticker, period):
    current_ticker = yf.Ticker(ticker)
    return current_ticker.history(period=period)

def extract_covid_data(url=URL_COVID_DATA):
    return pd.read_json(url)

def extract_weather_data(url=URL_WEATHER_DATA, rapid_api_key=RAPIDKEY):
    
    querystring = {"station":"72494","start":"2020-03-01","end":"2022-01-17"}
    headers = {
    'x-rapidapi-host': "meteostat.p.rapidapi.com",
    'x-rapidapi-key': rapid_api_key
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring)

    return pd.DataFrame(json.loads(response.text)["data"])
    
def dataframe_to_csv(df, csv_filepath):
    df.to_csv(csv_filepath)

def extract_and_load_weather_data():
    print("Extract weather data...")
    create_if_not_exists("data")
    # get current date to name csv file appropriately
    current_date = datetime.now().strftime("%m_%d_%Y")
    df_weather = extract_weather_data()
    dataframe_to_csv(df_weather, os.path.join("data", f"weather_data_san_francisco_{current_date}.csv"))

def extract_and_load_covid_data():
    print("Extract covid data...")
    create_if_not_exists("data")
    # get current date to name csv file appropriately
    current_date = datetime.now().strftime("%m_%d_%Y")
    df_covid = extract_covid_data()
    dataframe_to_csv(df_covid, os.path.join("data", f"covid19_data_san_francisco_{current_date}.csv"))

def extract_and_load_stock_data():
    print("Extract stock data...")
    create_if_not_exists("data")
    initial_period = "ytd"
    for ticker in TICKERS:
        # remove leading ^ for better filenaming
        ticker_str = ticker.replace("^", "")
        current_df = extract_stock_data(ticker, period=initial_period)
        dataframe_to_csv(current_df, os.path.join("data", f"{ticker_str}.csv"))

if __name__ == "__main__":
    extract_and_load_covid_data()
    extract_and_load_stock_data()
    extract_and_load_weather_data()
    