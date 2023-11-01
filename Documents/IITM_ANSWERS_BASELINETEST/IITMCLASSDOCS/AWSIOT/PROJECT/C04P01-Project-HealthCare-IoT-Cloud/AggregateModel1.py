import datetime

class AggregateModel:
    def __init__(self, db):
        self.db = db

    def aggregate(self, raw_data):
        # Fetch raw data within the specified time range
        raw_data = self.db.fetch_data_within_range(start_time, end_time)

        agg_data = {}

        for entry in raw_data:
            deviceid = entry['deviceid']
            sensor_type = entry['type']  # Assuming each raw data entry has a 'type' field indicating the sensor type
            timestamp = datetime.datetime.strptime(entry['timestamp'], '%Y-%m-%d %H:%M:%S')
            minute_key = timestamp.strftime('%Y-%m-%d %H:%M')

            if deviceid not in agg_data:
                agg_data[deviceid] = {}

            if sensor_type not in agg_data[deviceid]:
                agg_data[deviceid][sensor_type] = {}

            if minute_key not in agg_data[deviceid][sensor_type]:
                agg_data[deviceid][sensor_type][minute_key] = {
                    'count': 0,
                    'total': 0,
                    'min': float('inf'),
                    'max': float('-inf')
                }

            value = entry['value']
            agg_data[deviceid][sensor_type][minute_key]['count'] += 1
            agg_data[deviceid][sensor_type][minute_key]['total'] += value
            agg_data[deviceid][sensor_type][minute_key]['min'] = min(agg_data[deviceid][sensor_type][minute_key]['min'],
                                                                     value)
            agg_data[deviceid][sensor_type][minute_key]['max'] = max(agg_data[deviceid][sensor_type][minute_key]['max'],
                                                                     value)

        # Store the aggregated data in DynamoDB
        for deviceid, sensors in agg_data.items():
            for sensor_type, data in sensors.items():
                for minute, stats in data.items():
                    avg = stats['total'] / stats['count']
                    self.db.put_agg_data({
                        'deviceid': deviceid,
                        'type': sensor_type,
                        'timestamp': minute + ":00",  # add seconds back for consistency
                        'avg': avg,
                        'min': stats['min'],
                        'max': stats['max']
                    })
