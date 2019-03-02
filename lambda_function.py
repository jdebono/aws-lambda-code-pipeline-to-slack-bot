"""
Slack chat-bot Lambda handler.
"""
import boto3
import os
import json
import urllib

SLACK_URL = 'https://slack.com/api/chat.postMessage'

# WEB HOOK URL and CHANNEL from the environment.
TOKEN = os.environ['SLACK_TOKEN']
CHANNEL = os.environ['SLACK_CHANNEL']

def lambda_handler(event, context):
    """Handle an incoming CodePipeline Execution State Change from Cloudwatch rule.
    """

    # Get Params
    pipeline = event['detail']['pipeline']
    executionId = event['detail']['execution-id']
    status = event['detail']['state']
    stage = event['detail']['stage']
    
    if stage.lower() == "Source".lower():
        return '200 OK'

    # Get Pipeline execution details.
    client = boto3.client('codepipeline')
    pipelineDetails = client.get_pipeline_execution(
        pipelineName=pipeline,
        pipelineExecutionId=executionId
    )

    # Format Slack Message.
    message = '*Commit*\n' + pipelineDetails['pipelineExecution']['artifactRevisions'][0]['revisionSummary']
    message = message + '\n*Link*\n' + pipelineDetails['pipelineExecution']['artifactRevisions'][0]['revisionUrl']
    color = {
        'SUCCEEDED': 'good',
        'FAILED': 'danger',
        'STARTED': '#4682B4'
    }.get(status, '#2a2a2a')

    # JSON Payload.
    payload = {
        'channel': CHANNEL,
        'attachments': [
            {
                'color': color,
                'text': message,
                'fields': [
                    {
                        'title': 'Stage',
                        'value': stage.title(),
                        'short': 'true'
                    },
                    {
                        'title': 'Status',
                        'value': status.title(),
                        'short': 'true'
                    }
                ],
            }
        ]
    }
    # Construct the HTTP request that will be sent to the Slack API.
    request = urllib.request.Request(
        SLACK_URL,
        method='POST',
        data=json.dumps(payload).encode('utf-8')
    )
    # Add Headers.
    request.add_header('Authorization', 'Bearer ' + TOKEN)
    request.add_header('Content-Type', 'application/json')
    
    # Make the Request.
    urllib.request.urlopen(request).read()

    # Return Success.
    return '200 OK'
