from requests import get
import pandas as pd

API_KEY = "WCZLB5W1OAOM2ZVF"
URL = "https://www.alphavantage.co/query"


class ScriptData:

    def __init__(self):
        # Define the attributes
        self.apikey = API_KEY
        self.baseurl = URL
        self.data = {}

    def fetch_intraday_data(self, script):
        # Define the API Parameters
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": script,
            "interval": "5min",
            "apikey": self.apikey
        }

        # sending request to  API alphavantage
        response = get(url=self.baseurl, params=params)
        stock_data = response.json()

        # Check if the response is successful
        if "Error Message" in stock_data:
            print("Error:", stock_data["Error Message"])
            return None

        # Return the Raw data
        return stock_data

    def convert_intraday_data(self, script):
        columns = ["timestamp", "open", "high", "low", "close", "volume"]
        intraday_data = self.fetch_intraday_data(script)

        # Converting to pandas dataframe with the specified columns
        if intraday_data is not None:
            time_series = intraday_data['Time Series (5min)']
            #  creating the dataframe
            df = pd.DataFrame.from_dict(data=time_series, orient="index")
            df = df.rename(columns={
                "1. open": "open",
                "2. high": "high",
                "3. low": "low",
                "4. close": "close",
                "5. volume": "volume"
            })

            # Using the Timestamp as index
            df.index = pd.to_datetime(df.index)

            # Required Data type conversions
            df = df.astype(float)
            df["volume"] = df["volume"].astype(int)

            # Adding Timestamp Column
            df["timestamp"] = df.index

            # Reset the index to start at 0 and use it as the row number
            df = df.reset_index(drop=True)

            # Reorder the columns to have 'timestamp' as the first column
            cols = df.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            df = df[cols]
            return df
        else:
            return None

    # Overloading some functions
    def __getitem__(self, script):
        # Check if the intraday data for the script is already in data attribute/cache
        if script in self.data:
            return self.data[script]
        else:
            # store and cache the data in the form of a pandas dataframe
            intraday_data = self.convert_intraday_data(script)
            self.data[script] = intraday_data
        return intraday_data

    def __setitem__(self, script, data):
        # Cache the data for the symbol
        self.data[script] = data

    def __contains__(self, script):
        # Check if the intraday data for the symbol is already in the data cache
        return script in self.data




