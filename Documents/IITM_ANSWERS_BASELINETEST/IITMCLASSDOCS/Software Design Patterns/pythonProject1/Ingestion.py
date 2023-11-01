import json
import boto3
import yfinance as yf
import time
import random
import datetime
import pandas as pd


def get_weekdays_data(stock_symbol):
    today = datetime.date.today()
    end_date = today - datetime.timedelta(days=1)  # Exclude today, as data might not be available for the entire day

    # Initialize an empty DataFrame to store the data
    data = pd.DataFrame()

    # Collect data for each weekday
    while end_date.weekday() > 4:  # Skip Saturday (5) and Sunday (6)
        end_date -= datetime.timedelta(days=1)

    for _ in range(5):  # Get data for the last 5 weekdays
        start_date = end_date - datetime.timedelta(days=1)

        # Download per-hour stock price data
        weekday_data = yf.download(stock_symbol, start=start_date, end=end_date, interval='1h')

        # Concatenate the weekday data to the main DataFrame
        data = pd.concat([data, weekday_data])

        # Fetch 52-week high and low using yfinance's Ticker
        stock_info = yf.Ticker(stock_symbol)
        week52_high = stock_info.info.get("fiftyTwoWeekHigh")
        week52_low = stock_info.info.get("fiftyTwoWeekLow")

        end_date = start_date  # Move to the previous weekday

    return data, week52_high, week52_low


def push_to_kinesis(stream_name, data_record):
    kinesis.put_record(
        StreamName=stream_name,
        Data=json.dumps(data_record),
        PartitionKey=str(random.randint(1, 100))
    )


# Initialize AWS Kinesis client
kinesis = boto3.client('kinesis', region_name="us-east-1")  # Modify this line of code according to your region.

# Specify the stocks you want to fetch data for
stocks_to_fetch = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "NVDA", "INTC", "IBM", "AMD"]

for stock_symbol in stocks_to_fetch:
    stock_data, week52_high, week52_low = get_weekdays_data(stock_symbol)

    # Process the stock data and create individual records
    for index, row in stock_data.iterrows():
        data_record = {
            "stock_symbol": stock_symbol,
            "price": row["Close"],
            "timestamp": index.strftime("%Y-%m-%d %H:%M:%S"),
            "52WeekHigh": week52_high,
            "52WeekLow": week52_low
        }

        # Push the data record to the Kinesis stream
        push_to_kinesis("kinesis_stocks", data_record)  # Replace with your stream name

        # Print the data record to the console
        print("Data pushed to Kinesis:", data_record)

        # Introduce a delay to avoid rate limiting (adjust as needed)
        time.sleep(0.1)

print("Data pushed to Kinesis successfully!")