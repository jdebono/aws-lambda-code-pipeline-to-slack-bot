## aws-lambda-code-pipeline-to-slack-bot
Send a Slack Message on an incoming CodePipeline Execution State Change from Cloudwatch rule.

### Setup

1. Set up an [incoming webhook](https://api.slack.com/incoming-webhooks) on your Slack team. Note the webhook url.
2. Create a new Lambda on AWS. Select "Python 3.6" as the runtime with a basic execution role. Add `AWSCodePipelineReadOnlyAccess` policy to your service role. Copy the code from [lambda_function.py](lambda_function.py).
3. Add Environment variables `SLACK_TOKEN` and `SLACK_CHANNEL` and set them accordingly.
4. Create a Cloudwatch rule on AWS. Set `Service Name` to "CodePipeline" and `Event Type` to "CodePipeline Stage Execution State Change". Set Targets to "Lambda function" and select your lambda function.

Sample event data:
```json
{
  "version": "0",
  "id": "CWE-event-id",
  "detail-type": "CodePipeline Stage Execution State Change",
  "source": "aws.codepipeline",
  "account": "123456789012",
  "time": "2017-04-22T03:31:47Z",
  "region": "us-east-1",
  "resources": [
    "arn:aws:codepipeline:us-east-1:123456789012:pipeline:myPipeline"
  ],
  "detail": {
    "pipeline": "myPipeline",
    "version": "1",
    "execution-id": "01234567-0123-0123-0123-012345678901",
    "stage": "Prod",
    "state": "STARTED"
  }
}
```