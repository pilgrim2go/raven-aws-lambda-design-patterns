## Creating a Python Lambda that consumes Kinesis or DynamoDB records, and writes counters to DynamoDB and CloudWatch

Copyright (c) 2015-2016 Giving.com Ltd, trading as JustGiving, or its affiliates. All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.”

I have included two example AWS Lambda functions for time series analysis. One for processing DynamoDB Streams records and the other for Kinesis Streams records. They create a running count of distinct events over time (days, hours, minutes). The setup process for IAM roles and DynamoDB table are described in [Analyze a Time Series in Real Time with AWS Lambda, Amazon Kinesis and Amazon DynamoDB Streams](http://blogs.aws.amazon.com/bigdata/post/Tx148NMGPIJ6F6F/Analyze-a-Time-Series-in-Real-Time-with-AWS-Lambda-Amazon-Kinesis-and-DynamoDB-S).

![](/images/RavenLambdaKinesisandDynamoDB.png "RAVEN Platform Serverless Time Series Analysis with AWS Lambda, Amazon Kinesis and DynamoDB Streams")

Setting Up the Lamdba Function:

1. Select Blue print
   * Kinesis-process-record-python or dynamodb-process-stream-python

2. Configure event sources
   * Event source type: Kinesis or DynamoDB Streams
   * Kinesis stream / DynamoDB: web-analytics (select your event source)
   * Batch sise: 100
   * Starting position: Trim horizon

3. Configure function
   * Name: myKineisFunction
   * Description: An Amazon Kinesis stream processor that logs the data being published.
   * Runtime: Python 2.7
   * Lambda function code: Insert the Python Lambda code, note I've combined the cloudWatch and DynamoDB counter in one function.  
   * Handler: lambda_function.lambda_handler
   * Role: lambda_kinesis_role (Depends on you IAM roles setup)
   * Memory: 128MB
   * Timeout: 2 min 0 sec
   * VPC: No VPC  (Depends on VPC, test with No VPC)

4. Review
   * Enable event source: one you have tested with the sample event this can be enabled
   * Create Function
  
# Testing the function
1. Click on Code > Testing
2. Select Sample event temaplate > Kinesis or DynamoDB, copy the contents of the data-sample* folder or you can print out records into CloudWatch logs and paste them in.
  * *Note ClouwWatch only accepts date that is up to two week old. If you get an exception "The parameter MetricData.member.1.Timestamp must specify a time within the past two weeks" then for
  * Kineis decode, change the "utc_timestamp" and reencode the data, e.g. use https://www.base64decode.org/
  * DynamoDB modiy the "utc_timestamp" field directly
3. Save and test
4. You will see the log output
5. Next steps:
  * You can now view your data in DynamoDB or ClouwWatch. See [Analyze a Time Series in Real Time with AWS Lambda, Amazon Kinesis and Amazon DynamoDB Streams](http://blogs.aws.amazon.com/bigdata/post/Tx148NMGPIJ6F6F/Analyze-a-Time-Series-in-Real-Time-with-AWS-Lambda-Amazon-Kinesis-and-DynamoDB-S) for details.
  * You can also chart the data in near-realtime using JavaScript, see [Serverless Dynamic Real-Time Dashboard with AWS DynamoDB, S3 and Cognito](https://medium.com/@rfreeman/serverless-dynamic-real-time-dashboard-with-aws-dynamodb-a1a7f8d3bc01)
  * You can enable the Event Source once you have tested the function

Copyright (c) 2015-2016 Giving.com Ltd, trading as JustGiving, or its affiliates. All Rights Reserved.
Licensed under the Apache License, Version 2.0 license. See LICENSE file in the project root for full license information.
