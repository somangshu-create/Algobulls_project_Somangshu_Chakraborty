import pandas as pd


def indicator1(df, timeperiod: int):
    """
    Compute a moving average indicator for a given DataFrame.

    Args:
        df (pandas.DataFrame): A DataFrame containing stock data containing the
                               timestamp and the close columns

        timeperiod (int): The number of periods to use for the moving average.

    Returns:
        pandas.DataFrame: A DataFrame with two columns: 'timestamp' and
                          'indicator'. The 'indicator' column contains the
                          moving average of the 'close' column for each timestamp.
    """

    # Compute the rolling/moving average
    rolling_average = df['close'].rolling(window=timeperiod).mean()

    # Create a new DataFrame with the timestamp and rolling average columns
    result = pd.DataFrame({'timestamp': df['timestamp'],
                           'indicator': rolling_average})
    return result
