"""
/*
 *
 * This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
 * OF ANY KIND, either express or implied. See the License for the specific language
 * governing permissions and limitations under the License.
 */
 """
from datetime import datetime, timedelta

import boto3

import alarm
import aggregate

# Loop aggregate function per minute between prevday and today
# aggregate data per minute within that range

iot_data = boto3.client('iot', region_name='us-east-1')

etime = datetime.today()  # datetime.date(2021, 1, 15)
stime = etime - timedelta(minutes=60)  # datetime.date(2021, 1, 14)
deviceid = 'BSM_G101'
filename = 'alarm.json'

response = iot_data.list_things(thingTypeName='BedSideMonitor')
devices = response["things"]

device_list = []
for d in devices:
    deviceid = d["thingName"]
    device_list.append(deviceid)

for deviceid in device_list:
    print("Summarizing for device id: " + deviceid)
    aggr = aggregate.Aggregate(stime, etime, deviceid)
    aggr.aggregate()

    alm = alarm.Alarm(stime, etime, deviceid, filename)
    alm.checkhralert()
    alm.checktempalert()