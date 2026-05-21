import json
import boto3
import uuid
import random
from datetime import datetime

# AWS Clients
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

# DynamoDB Table
table = dynamodb.Table('IncidentLogs')

# SNS Topic ARN
TOPIC_ARN = 'arn:aws:sns:ap-south-1:342677170246:server-health-alerts'


def lambda_handler(event, context):

    # Simulated incidents
    incidents = [
        ("HIGH_CPU_USAGE", 95),
        ("MEMORY_SPIKE", 89),
        ("FAILED_LOGIN_ATTEMPTS", 70),
        ("SERVER_DOWN", 100),
        ("HIGH_ERROR_RATE", 92)
    ]

    incident_type, cpu_usage = random.choice(incidents)

    timestamp = str(datetime.utcnow())

    # Alert message
    message = f"""
ALERT DETECTED

Incident Type: {incident_type}
CPU Usage: {cpu_usage}%
Timestamp: {timestamp}
"""

    # Send SNS Email Alert
    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject='Cloud Monitoring Alert',
        Message=message
    )

    # Store Incident in DynamoDB
    table.put_item(
        Item={
            'incident_id': str(uuid.uuid4()),
            'incident_type': incident_type,
            'cpu_usage': str(cpu_usage),
            'timestamp': timestamp,
            'status': 'OPEN'
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Incident processed successfully!')
    }
