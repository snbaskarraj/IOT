import datetime
import Database

class RawDataModel:
    def __init__(self, deviceid, timestamp, datatype, value):
        self.deviceid = deviceid
        self.timestamp = timestamp
        self.datatype = datatype
        self.value = value


    @classmethod
    def from_dynamodb_response(cls, items):
        sensor_data_list = []

        for item in items:
            deviceid = item['deviceid']['S']
            timestamp = item['timestamp']['S']
            datatype = item['datatype']['S']
            value = int(item['value']['N'])

            sensor_data = cls(deviceid, timestamp, datatype, value)
            sensor_data_list.append(sensor_data)

        return sensor_data_list


    @staticmethod
    def read_data_from_dynamodb():
        # Create a Database Object
        database_obj = Database('BSM_DATA')

        try:
            # Read data from DynamoDB table
            response = database_obj.get_all_items()

            # Return the items from the response
            transformed_data = RawDataModel.from_dynamodb_response(response)

            return transformed_data

        except Exception as e:
            print(f'Error reading data from DynamoDB table: {e}')
            return []
