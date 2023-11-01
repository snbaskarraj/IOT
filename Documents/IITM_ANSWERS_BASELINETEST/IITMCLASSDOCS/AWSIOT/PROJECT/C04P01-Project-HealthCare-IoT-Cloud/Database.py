import boto3

from bsm.models import RawDataModel, AggregateModel


class Database:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key):
        self.boto_client = boto3.client('dynamodb', config=boto3.client.Config(region_name=region_name,
                                                                               aws_access_key_id=aws_access_key_id,
                                                                               aws_secret_access_key=aws_secret_access_key))

    def put_raw_data(self, data):
        table_name = 'bsm_raw_data'
        self.boto_client.put_item(TableName=table_name, Item={
            'device_id': {'S': data.device_id},
            'timestamp': {'S': data.timestamp},
            'sensor_type': {'S': data.sensor_type},
            'value': {'S': data.value}
        })

    def put_aggregate_data(self, data):
        table_name = 'bsm_agg_data'
        self.boto_client.put_item(TableName=table_name, Item={
            'device_id': {'S': data.device_id},
            'sensor_type': {'S': data.sensor_type},
            'start_time': {'S': data.start_time},
            'end_time': {'S': data.end_time},
            'data': {'L': [d.to_json() for d in data.data]}
        })

    def aggregate_data(self, start_time, end_time):
            """
            Aggregates the data in the `bsm_raw_data` table for the specified time range.

            Args:
                start_time (str): The start time of the time range.
                end_time (str): The end time of the time range.

            Returns:
                List[AggregateModel]: A list of `AggregateModel` objects, each of which contains the average, minimum, and maximum values for the specified sensor type and time range.
            """

            # Get the data from the `bsm_raw_data` table for the specified time range.
            raw_data = self.get_raw_data(start_time, end_time)

            # Aggregate the data by sensor type.
            aggregated_data = {}
            for data in raw_data:
                sensor_type = data.sensor_type
                if sensor_type not in aggregated_data:
                    aggregated_data[sensor_type] = AggregateModel(
                        device_id=data.device_id,
                        sensor_type=data.sensor_type,
                        start_time=start_time,
                        end_time=end_time,
                        data=[]
                    )

                aggregated_data[sensor_type].data.append(data)

            # Calculate the average, minimum, and maximum values for each sensor type.
            for sensor_type, data in aggregated_data.items():
                data.average = sum(d.value for d in data.data) / len(data.data)
                data.minimum = min(d.value for d in data.data)
                data.maximum = max(d.value for d in data.data)

            return list(aggregated_data.values())
