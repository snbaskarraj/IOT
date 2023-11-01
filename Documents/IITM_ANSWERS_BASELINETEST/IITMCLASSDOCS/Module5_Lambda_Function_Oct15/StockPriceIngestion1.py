import json
import boto3
import sys
import yfinance as yf
import time
import random
import datetime

# Your goal is to get per-hour stock price data for a time range for the ten stocks specified in the doc.
# Further, you should call the static info API for the stocks to get their current 52WeekHigh and 52WeekLow values.
# You should craft individual data records with information about the stockid, price, price timestamp, 52WeekHigh and 52WeekLow values and push them individually on the Kinesis stream

def get_stock_data(stock_symbol):
    today = datetime.date.today()
    yesterday = datetime.date.today() - datetime.timedelta(1)
    
    # Download per-hour stock price data
    data = yf.download(stock_symbol, start=yesterday, end=today, interval='1h')
    
    # Fetch 52-week high and low using yfinance's Ticker
    stock_info = yf.Ticker(stock_symbol)
    week52_high = stock_info.info.get("fiftyTwoWeekHigh")
    week52_low = stock_info.info.get("fiftyTwoWeekLow")
    
    return data, week52_high, week52_low

def push_to_kinesis(stream_name, data_record):
    kinesis.put_record(
        StreamName=stream_nam,
        Data=json.dumps(data_record),
        PartitionKey=str(random.randint(1, 100))
    )

# Initialize AWS Kinesis client
kinesis = boto3.client('kinesis', region_name="us-east-1")  # Modify this line of code according to your region.

# Specify the stocks you want to fetch data for
stocks_to_fetch = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "NVDA", "INTC", "IBM", "AMD"]

for stock_symbol in stocks_to_fetch:
    stock_data, week52_high, week52_low = get_stock_data(stock_symbol)
    
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
