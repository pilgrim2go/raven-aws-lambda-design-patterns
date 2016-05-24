#!/usr/bin/env python
# Copyright (c) 2015-2016 Giving.com Ltd, trading as JustGiving, or its affiliates. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 license. See LICENSE file in the project root for full license information.
# A copy of the License is located in the "license" file accompanying this file. 
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and limitations under the License.

import base64
import json
import boto3
from datetime import datetime
from collections import defaultdict

def update_dynamo_event_counter(tableName, event_name, event_datetime, event_count=1, dynamodb = boto3.resource(service_name='dynamodb', region_name='eu-west-1')):
        table = dynamodb.Table(tableName)
        response = table.update_item(
        Key={
            'EventName': event_name, 
            'DateHour': event_datetime
        },
        ExpressionAttributeValues={":value":event_count},
        UpdateExpression="ADD EventCount :value")

def put_cloudwatch_metric(event_name, event_datetime, event_count=1, cwc=boto3.client('cloudwatch', region_name='eu-west-1')):
    metricData=[{
            'MetricName': event_name,
            'Timestamp': datetime.strptime(event_datetime, '%Y-%m-%dT%H:%M:%S'),
            'Value': event_count,            
            'Unit': 'Count'
        },]
    response = cwc.put_metric_data(Namespace="PocKinesisLambdaCounterTest",MetricData=metricData)    

def lambda_handler(event, context):
    minute_event_counter = defaultdict(int) #Used for ClouldWatch
    hour_event_counter = defaultdict(int) #Used for DynamoDB counters
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        payload_json = json.loads(payload)
        try: 
            event_type=str(payload_json['event'])
        except Exception as e:            
            print('Error no event type detected')
            event_type='NULL'
        try: 
            hour_event_time=str(payload_json['utc_timestamp'].split(':', 1)[0] + ':00:00')
            minute_event_time=str(payload_json['utc_timestamp'].rsplit(':', 1)[0] + ':00')
            hour_event_counter[(event_type, hour_event_time)] += 1
            minute_event_counter[(event_type, minute_event_time)] += 1
        except Exception as e:            
            print('Error no event time detected')
            
        
    for key,val in hour_event_counter.iteritems():
        print "%s, %s = %s" % (str(key[0]), str(key[1]), str(val))
        update_dynamo_event_counter('poc-raven-lambda-event-counters', key[0], key[1], int(val))   
    for key,val in minute_event_counter.iteritems():
        print "%s, %s = %s" % (str(key[0]), str(key[1]), str(val))
        put_cloudwatch_metric(key[0], key[1], int(val))
    return 'Successfully processed {} records.'.format(len(event['Records']))