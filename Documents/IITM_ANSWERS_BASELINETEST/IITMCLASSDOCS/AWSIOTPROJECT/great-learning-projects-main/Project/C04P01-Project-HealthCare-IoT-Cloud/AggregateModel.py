import Database
import datetime
import RawDataModel


class AggregateModel:
    def __init__(self, deviceid, starttime, endtime, datatype, average_value):
        self.deviceid = deviceid
        self.starttime = starttime
        self.endtime = endtime
        self.datatype = datatype
        self.average_value = average_value

    @classmethod
    def upload_to_dynamodb(cls, aggregate_data, table_name):
        database_obj = Database('BSM_agg_data')
        
        for data in aggregate_data:
            item_obj = cls(data['deviceid'], data['start_time'], data['end_time'],
                        data['average_value'])
            item = Database.create_dynamodb_item(item_obj)
            
            try:
                database_obj.create_item(item)
                print("Uploaded item:", item)
            except Exception as e:
                print(f'Error uploading item to DynamoDB: {e}')


    @staticmethod
    def get_aggregate_data(sensor_data_list, deviceid, datatype):
        aggregate_data = []
        sensor_data_list.sort(key=lambda x: x.timestamp)  # Sort by timestamp
        
        start_time = datetime.strptime(sensor_data_list[0].timestamp, "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.strptime(sensor_data_list[-1].timestamp, "%Y-%m-%d %H:%M:%S.%f")
        
        current_time = start_time
        while current_time <= end_time:
            next_time = current_time + datetime.timedelta(minutes=15)
            data_sum = 0
            count = 0
            
            for sensor_data in sensor_data_list:
                timestamp = datetime.strptime(sensor_data.timestamp, "%Y-%m-%d %H:%M:%S.%f")
                if current_time <= timestamp < next_time and sensor_data.deviceid == deviceid:
                    data_sum += sensor_data.value
                    count += 1
            
            if count > 0:
                average_value = data_sum / count
                aggregate_data.append({
                    'deviceid': deviceid,
                    'start_time': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'end_time': next_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'average_value': average_value,
                    'datatype' : datatype
                })
            
            current_time = next_time
        
        return aggregate_data