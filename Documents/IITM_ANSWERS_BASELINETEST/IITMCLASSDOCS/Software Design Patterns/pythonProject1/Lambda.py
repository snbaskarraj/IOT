import boto3
import json
import time
import base64
from boto3.dynamodb.conditions import Attr
from decimal import Decimal


def lambda_handler(event, context):
    print("Lambda function started...")

    # Dynamodb
    tablename = 'stockalert'
    table = boto3.resource('dynamodb').Table(tablename)

    # SNS Topic
    topic_arn = 'arn:aws:sns:us-east-1:279123003175:stock'
    sns_client = boto3.client('sns')

    # Kinesis
    my_stream_name = 'kinesis_stocks'
    kinesis_client = boto3.client('kinesis', region_name='us-east-1')

    try:
        response = kinesis_client.describe_stream(StreamName=my_stream_name)
        my_shard_id = response['StreamDescription']['Shards'][0]['ShardId']
        shard_iterator = kinesis_client.get_shard_iterator(StreamName=my_stream_name,
                                                           ShardId=my_shard_id,
                                                           ShardIteratorType='LATEST')
        my_shard_iterator = shard_iterator['ShardIterator']

        while 'NextShardIterator' in my_shard_iterator:
            record_response = kinesis_client.get_records(ShardIterator=my_shard_iterator)

            if len(record_response['Records']) > 0:
                for item in record_response['Records']:
                    try:
                        # Decode the Kinesis record data
                        decoded_data = base64.b64decode(item["Data"]).decode('utf-8')

                        # Print the decoded data from Kinesis
                        print("Record from Kinesis:", decoded_data)

                        readings = json.loads(decoded_data, parse_float=Decimal)
                        stock_symbol = readings.get('stock_symbol',
                                                    '')  # Use 'get' method to handle missing 'stock_symbol' key
                        timestamp = readings['timestamp']
                        price = float(readings['price'])  # Update variable name to 'price'
                        high_52week = float(readings['52WeekHigh'])
                        low_52week = float(readings['52WeekLow'])
                        # stockdate = readings['stockdate']

                        if price >= 0.8 * high_52week or price <= 1.2 * low_52week:
                            db_response = table.scan(
                                FilterExpression=Attr('stockid').eq(stock_symbol)  # & Attr('stockdate').eq(stockdate)
                            )
                            if db_response['Count'] == 0:
                                # Print the data before writing to DynamoDB
                                print("Data before writing to DynamoDB:", readings)

                                # Write data to DynamoDB
                                #table.put_item(
                                    #Item={'stockid': stock_symbol, 'timestamp': timestamp, 'price': str(price),
                                          #'52week_high': str(high_52week), '52week_low': str(low_52week)})
                                # 'stockdate': stockdate})

                                # Print the data after writing to DynamoDB
                                #print("Data after writing to DynamoDB:", readings)

                                # Publish to SNS topic
                                #sns_response = sns_client.publish(
                                    #TopicArn=topic_arn,
                                    #Message=json.dumps({'default': decoded_data}),
                                    #MessageStructure='json',
                                    #Subject="Price PoI reached for %s on %s" % (stock_symbol)
                                #)

                                # Print the SNS response
                                #print("SNS Response:", sns_response)

                    except Exception as e:
                        print(f"Error processing record: {str(e)}")

            # Wait for milli-seconds
            time.sleep(0.25)

    except Exception as stream_exception:
        print(f"Error while describing Kinesis stream: {str(stream_exception)}")

    print("Lambda function finished.")
