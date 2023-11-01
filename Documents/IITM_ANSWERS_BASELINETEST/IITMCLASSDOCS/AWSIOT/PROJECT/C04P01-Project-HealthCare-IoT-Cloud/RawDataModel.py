import json


class RawDataModel:
    def __init__(self, device_id, timestamp, sensor_type, value):
        self.device_id = device_id
        self.timestamp = timestamp
        self.sensor_type = sensor_type
        self.value = value

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @classmethod
    def from_json(cls, json_data):
        return cls(
            device_id=json_data['device_id'],
            timestamp=json_data['timestamp'],
            sensor_type=json_data['sensor_type'],
            value=json_data['value']
        )