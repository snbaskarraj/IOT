"""
/*
 *
 * This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
 * OF ANY KIND, either express or implied. See the License for the specific language
 * governing permissions and limitations under the License.
 */
 """
import boto3
import pandas as pd

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

class Aggregate:
    def __init__(self, stime, etime, devid):
        self._stime = stime
        self._etime = etime
        self._devid = devid

    @property
    def devid(self):
        return self._devid

    @property
    def stime(self):
        return self._stime

    @property
    def etime(self):
        return self._etime

    def aggregate(self):
        hrate, temp, spo2, response = [], [], [], []
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('BSM_DATA')
        datetime_index = pd.date_range(start=pd.Timestamp(self.stime), end=pd.Timestamp(self.etime), freq='1min')

        for i in range(0, len(datetime_index) - 1):
            st = datetime_index[i].isoformat()
            et = datetime_index[i + 1].isoformat()
            try:
                response = table.query(
                    KeyConditionExpression=Key('deviceid').eq(self.devid) & Key('timestamp').between(st, et)
                )
            except ClientError as e:
                print(e.response['Error']['Message'])

            if response['Count'] > 0:
                print(st, et, response['Items'])
                for s in range(len(response['Items'])):
                    # Adding the iot devices data to the appropriate device_id list
                    if response['Items'][s]['datatype'] == 'HeartRate':
                        hrate.append(response['Items'][s]['value'])
                    elif response['Items'][s]['datatype'] == 'Temperature':
                        temp.append(response['Items'][s]['value'])
                    elif response['Items'][s]['datatype'] == 'SPO2':
                        spo2.append(response['Items'][s]['value'])

                dic = {'HeartRate': pd.Series(data=hrate), 'Temperature': pd.Series(data=temp),
                       'SPO2': pd.Series(data=spo2)}  # dictionary
                df = pd.DataFrame(dic)
                f = {'HeartRate': ['min', 'max', 'mean', 'count'], 'Temperature': ['min', 'max', 'mean', 'count'],
                     'SPO2': ['min', 'max', 'mean', 'count']}  # dictionary
                dframe = df.agg(f)
                self.store(dframe, et)
            else:
                print(st, et, 'No value between the range')

    def store(self, df, et):
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('BSMAggregate')

        # Write dataframe to dynamoDB as list of dictionaries
        try:
            table.put_item(
                Item={'device': self.devid, 'timestamp': et, 'payload': df.astype(str).to_dict()}
            )
        except ClientError as e:
            print(e.response['Error']['Message'])