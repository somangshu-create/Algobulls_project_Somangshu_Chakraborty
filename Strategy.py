import Script_Data
import pandas as pd
from indicator import indicator1


class Strategy:
    # initiating a object of script data class as attribute
    def __init__(self):
        self.obj = Script_Data.ScriptData()

    def generate_signals(self, script: str) -> pd.DataFrame:
        """
            Generate signals for the given script name.

            Args:
                script (str): The name of the script to generate signals for.

            Returns:
                pandas.DataFrame: A DataFrame containing the signals for the given script.
        """
        # getting the data
        stock_data = self.obj.convert_intraday_data(script)
        close_data = stock_data["close"]
        indicator_data = indicator1(df=stock_data, timeperiod=5)["indicator"]

        # Creating the dataframe
        signals = pd.DataFrame({"timestamp": stock_data["timestamp"]})

        # Initializing all timestamps with no signal then changing according to the data
        signals["signal"] = "NO_SIGNAL"

        # Modifying the signals dataframe for buy and sell timestamps
        for index in range(0, len(indicator_data)):
            # close and indicator data Crossed and Cut Upwards
            if close_data.iloc[index] > indicator_data.iloc[index] and \
                    close_data.iloc[index - 1] < indicator_data.iloc[index - 1]:
                signals.at[index, "signal"] = "BUY"

            # close and indicator data crossed and cut downwards
            elif close_data.iloc[index] < indicator_data.iloc[index] and \
                    close_data.iloc[index - 1] > indicator_data.iloc[index - 1]:
                signals.at[index, "signal"] = "SELL"

            else:
                continue

        # getting the indexes with no signal and dropping them
        index_names = signals[signals["signal"] == "NO_SIGNAL"].index
        signals.drop(labels=index_names, inplace=True)

        return signals


# creating a object from strategy class
strategy = Strategy()
df = strategy.generate_signals("GOOGL")
print(df)
