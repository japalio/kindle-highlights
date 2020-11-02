import json
import random
import os
import boto3
from botocore.exceptions import ClientError

import kindle_highlights

DAILY_KINDLE_HIGHLIGHTS_EMAIL = "dailykindlehighlights@gmail.com"


def get_highlights(bucket, obj):
    s3 = boto3.resource('s3')

    content_object = s3.Object(bucket, obj)
    print("getting highlights for ", obj)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    return json_content


def format_highlights(selected_highlights):
    body_text = "<html><head></head><body>"
    for book in selected_highlights:
        body_text += "<h3>Selected highlights from " + book + "</h3>\n"
        for highlight in selected_highlights[book]:
            body_text += "<p>" + highlight + "</p>\n\n"
    body_text += "</body></html>"
    return body_text

def send_email(text, email):
    client = boto3.client('ses',region_name=os.environ.get('REGION'))
    charset = os.environ.get('CHARSET')
    subject = os.environ.get('SUBJECT')
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    email,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': charset,
                        'Data': text,
                    },
                    'Text': {
                        'Charset': charset,
                        'Data': text,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=DAILY_KINDLE_HIGHLIGHTS_EMAIL,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        print(text)
        
def lambda_handler(event, context):
    email_envar = os.environ.get('EMAIL')
    emails = email_envar.split(',')
    bucket = os.environ.get('BUCKET')
    object_envar = os.environ.get('OBJECT')
    objects = object_envar.split(',')
    for email, obj in zip(emails, objects):
        all_highlights = get_highlights(bucket, obj)
        parsed_highlights = kindle_highlights.parse_highlights(all_highlights)
        selected_highlights = kindle_highlights.select_weighted(parsed_highlights)
        email_text = format_highlights(selected_highlights)
        send_email(email_text, email)
    
    return {
        'statusCode': 200,
        'body': ""
    }
