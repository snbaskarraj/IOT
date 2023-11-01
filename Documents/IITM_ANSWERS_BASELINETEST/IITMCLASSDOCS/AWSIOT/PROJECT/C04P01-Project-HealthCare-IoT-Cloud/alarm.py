"""
/*
 *
 * This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
 * OF ANY KIND, either express or implied. See the License for the specific language
 * governing permissions and limitations under the License.
 */
 """
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta
import json

from botocore.exceptions import ClientError


class Alarm:
    def __init__(self, stime, etime, devid, filename):
        self._stime = stime
        self._etime = etime
        self._devid = devid
        self._alerts = self.readalert(filename)
        self._response = self.getdata(stime, etime, devid)

    @property
    def devid(self):
        return self._devid

    @property
    def stime(self):
        return self._stime

    @property
    def etime(self):
        return self._etime

    @property
    def alerts(self):
        return self._alerts

    @property
    def response(self):
        return self._response

    def readalert(self, filename):
        # Read the alert rules
        alerts_config_file = open(filename)
        alerts_config = json.loads(alerts_config_file.read())
        alerts_config_file.close()
        dict = {}
        # Iterating through each rule and parsing the alert value
        for item in alerts_config:
            for k, v in item.items():
                if k == 'HeartRate':
                    for key, value in v.items():
                        if key == 'min':
                            dict['hmin'] = value
                        if key == 'max':
                            dict['hmax'] = value
                        if key == 'trigger_count':
                            dict['hrcount'] = value
                if k == 'Temperature':
                    for key, value in v.items():
                        if key == 'min':
                            dict['tmin'] = value
                        if key == 'max':
                            dict['tmax'] = value
                        if key == 'trigger_count':
                            dict['trcount'] = value
        # set the member variable
        return dict

    def getdata(self, stime, etime, devid):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('BSMAggregate')
        st = stime.isoformat()
        et = etime.isoformat()
        try:
            response = table.query(
                KeyConditionExpression=Key('device').eq(devid) & Key('timestamp').between(st, et)
            )
            return response
        except ClientError as e:
            print(e.response['Error']['Message'])

    def checkhralert(self):
        prevtime = 0
        h_count = 0
        if self.response['Count'] > 0:
            for s in range(self.response['Count']):
                tme = datetime.fromisoformat(self.response['Items'][s]['timestamp'])
                if prevtime == 0:
                    prevtime = tme
                # Adding the iot devices data to the appropriate device_id list
                if int(self.response['Items'][s]['payload']['HeartRate']['min']) < self.alerts['hmin'] or \
                        int(self.response['Items'][s]['payload']['HeartRate']['max']) > self.alerts['hmax']:
                    if (tme - prevtime) == timedelta(minutes=1):
                        h_count = h_count + 1
                        # print(self.response['Items'][s]['payload']['HeartRate'])
                        if h_count == self.alerts['hrcount']:
                            print("Threshold for HeartRate failed " + str(tme))
                            self.store(tme, "Threshold for HeartRate failed")
                            h_count = 0
                            prevtime = tme

                        else:
                            prevtime = tme
                    else:
                        h_count = 0
                        prevtime = tme

    def checktempalert(self):
        prevtime = 0
        t_count = 0
        if self.response['Count'] > 0:
            for s in range(self.response['Count']):
                tme = datetime.fromisoformat(self.response['Items'][s]['timestamp'])
                if prevtime == 0:
                    prevtime = tme
                if float(self.response['Items'][s]['payload']['Temperature']['min']) < self.alerts['tmin'] or \
                        float(self.response['Items'][s]['payload']['Temperature']['max']) > self.alerts['tmax']:
                    if (tme - prevtime) == timedelta(minutes=1):
                        t_count = t_count + 1
                        # print(self.response['Items'][s]['payload']['Temperature'])
                        if t_count == self.alerts['trcount']:
                            print("Threshold for Temperature failed " + str(tme))
                            self.store(tme, "Threshold for Temperature failed")
                            t_count = 0
                            prevtime = tme
                        else:
                            prevtime = tme
                    else:
                        t_count = 0
                        prevtime = tme

    def store(self, time, alert):
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('BSMAlerts')

        # Write to dynamoDB
        try:
            table.put_item(
                Item={'device': self.devid, 'timestamp': time.isoformat(), 'rule': alert}
            )
        except ClientError as e:
            print(e.response['Error']['Message'])