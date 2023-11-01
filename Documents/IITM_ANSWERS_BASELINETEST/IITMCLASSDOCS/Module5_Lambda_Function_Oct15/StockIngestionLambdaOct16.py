import json
import boto3
import base64
from datetime import datetime

# Initialize AWS clients
kinesis_client = boto3.client('kinesis')
dynamodb_client = boto3.client('dynamodb')
sns_client = boto3.client('sns')

dynamodb_table_name = 'stock_alerts'
sns_topic_arn = 'arn:aws:sns:us-east-1:279123003175:stock'

def lambda_handler(event, context):
    alerts_generated = set()  # Use a set to track alerts generated for stocks on the same day

    for record in event['Records']:
        # Kinesis data- base64 encoded, decoding here
        payload = base64.b64decode(record["kinesis"]["data"]).decode('utf-8')

        payload_dict = json.loads(payload)
        stock_symbol = payload_dict.get('stock_symbol')
        timestamp = payload_dict.get('timestamp')
        price = payload_dict.get('price')
        high_52week = payload_dict.get('52WeekHigh')
        low_52week = payload_dict.get('52WeekLow')

        if stock_symbol and timestamp and price and high_52week and low_52week:
            # Find the thresholds for POI
            threshold_max = float(high_52week) * 0.8  # 80% of 52-week max
            threshold_min = float(low_52week) * 1.2   # 120% of 52-week min

            # Check if the price meets the conditions
            if price >= threshold_max or price <= threshold_min:
                # Check if an alert has already been generated for this stock - today
                today_date = datetime.now().date().isoformat()
                alert_key = f"{stock_symbol}-{today_date}"

                if alert_key not in alerts_generated:
                    # Store the payload in DynamoDB table
                    dynamodb_client.put_item(
                        TableName=dynamodb_table_name,
                        Item={
                            'stock_symbol': {'S': stock_symbol},
                            'timestamp': {'S': timestamp},
                            'price': {'N': str(price)},
                            '52week_high': {'N': str(high_52week)},
                            '52week_low': {'N': str(low_52week)}
                        }
                    )

                    # Send to the SNS topic an alert notification
                    sns_client.publish(
                        TopicArn=sns_topic_arn,
                        Message=f"Point of Interest Detected - Stock: {stock_symbol}, Timestamp: {timestamp}, Price: {price}, 52weekHigh: {high_52week}, 52weekLow: {low_52week}"
                    )

                    # Add the alert_key to the set to mark the alert as generated for today to avoid repeat alerts for a stock
                    alerts_generated.add(alert_key)
        else:
            print("Missing required attributes in payload")
    
    return {
        'statusCode': 200,
        'body': 'Records processed successfully'
    }
