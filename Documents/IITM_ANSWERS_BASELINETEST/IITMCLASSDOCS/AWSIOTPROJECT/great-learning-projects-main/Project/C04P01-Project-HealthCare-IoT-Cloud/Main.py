import itertools
import RawDataModel

data = RawDataModel.read_data_from_dynamodb()
print(data)


def group_sensor_data(sensor_data_list):
    grouped_data = []
    
    # Sort the sensor data list by deviceid and datatype
    sorted_data = sorted(sensor_data_list, key=lambda x: (x.deviceid, x.datatype))
    
    # Group the sorted data by deviceid and datatype
    for key, group in itertools.groupby(sorted_data, key=lambda x: (x.deviceid, x.datatype)):
        deviceid, datatype = key
        data_group = list(group)
        
        # Create a dictionary with deviceid, datatype, and data group
        grouped_item = {
            'deviceid': deviceid,
            'datatype': datatype,
            'data': data_group
        }
        
        grouped_data.append(grouped_item)
    
    return grouped_data

def check_rule(aggregate_data, rule):
    type_filter = rule['type']
    avg_min = rule['avg_min']
    avg_max = rule['avg_max']
    trigger_count = rule['trigger_count']

    count = 0
    for data in aggregate_data:
        if data['average_value'] < avg_min or data['average_value'] > avg_max:
            count += 1
            if count == trigger_count:
                return True
        else:
            count = 0

    return False
