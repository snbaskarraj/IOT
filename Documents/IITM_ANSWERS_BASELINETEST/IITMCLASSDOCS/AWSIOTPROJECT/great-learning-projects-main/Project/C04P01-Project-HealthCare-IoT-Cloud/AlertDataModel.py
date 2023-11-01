class AlertDataModel:
    def __init__(self, deviceid, start_time, end_time, datatype, average_value, rule):
        self.deviceid = deviceid
        self.start_time = start_time
        self.end_time = end_time
        self.datatype = datatype
        self.average_value = average_value
        self.rule = rule



    @classmethod
    def create_alerts(cls, aggregate_data, rules):
        alerts = []
        
        for rule in rules:
            type_filter = rule['type']
            avg_min = rule['avg_min']
            avg_max = rule['avg_max']
            trigger_count = rule['trigger_count']
            
            count = 0
            for data in aggregate_data:
                if data['datatype'] == type_filter and (data['average_value'] < avg_min or data['average_value'] > avg_max):
                    count += 1
                    if count == trigger_count:
                        alert = cls(data['deviceid'], data['start_time'], data['end_time'], data['average_value'], data['datatype'], rule)
                        alerts.append(alert)
                        break
                else:
                    count = 0
        
        return alerts
