import boto3
from boto3.dynamodb.conditions import Key

class Database:
    def __init__(self):
        self.client = boto3.client('dynamodb')
        self.resource = boto3.resource('dynamodb')

    def create_agg_table(self):
        table = self.resource.create_table(
            TableName='bsm_agg_data',
            KeySchema=[
                {
                    'AttributeName': 'deviceid',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'deviceid',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Wait for the table to be created
        table.meta.client.get_waiter('table_exists').wait(TableName='bsm_agg_data')
        print('Table is ready!')

    def put_agg_data(self, data):
        table = self.resource.Table('bsm_agg_data')
        table.put_item(Item=data)

    def get_agg_data(self, deviceid, start_time, end_time):
        table = self.resource.Table('bsm_agg_data')
        response = table.query(
            KeyConditionExpression=Key('deviceid').eq(deviceid) & Key('timestamp').between(start_time, end_time)
        )
        return response['Items']



    def fetch_raw_data(self, start_time, end_time):
        table = self.resource.Table('bsm_data')
        # Assuming 'deviceid' is the partition key and 'timestamp' is the sort key for the bsm_data table.
        # This will get all raw data for all devices in the specified time range
        response = table.scan(
            FilterExpression=Key('timestamp').between(start_time, end_time)
        )
        return response['Items']
