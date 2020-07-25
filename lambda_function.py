import json
import random
import os
import boto3
from botocore.exceptions import ClientError


def get_highlights(bucket, obj):
    s3 = boto3.resource('s3')

    content_object = s3.Object(bucket, obj)
    print("getting highlights for ", obj)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    return json_content

def parse_highlights(highlights):
    quotes = {}
    # randomly generate 2 numbers for book indices
    while len(quotes.keys()) < 3:
        book_index = random.randint(0, len(highlights["books"])-1)
        book_quotes = highlights["books"][book_index]["highlights"]
        title = highlights["books"][book_index]["title"]
        if title in quotes:
            continue
        # for each book, randomly generate 2 numbers for quote indices
        num_quotes = 2
        if len(book_quotes) == 1:
            num_quotes = 1
        quote_indices = []
        for x in range(num_quotes):
            # no repeats
            quote_index = -1
            while quote_index == -1 or quote_index in quote_indices:
                quote_index = random.randint(0, len(book_quotes)-1)
            quote_indices.append(quote_index)
            quote = book_quotes[quote_index]["text"]
            if title in quotes:
                quotes[title].append(quote)
            else:
                quotes[title] = [quote]

    return quotes


def format_highlights(selected_highlights):
    body_text = "<html><head></head><body>"
    for book in selected_highlights:
        body_text += "<h3>Selected quotes from " + book + "</h3>\n"
        for quote in selected_highlights[book]:
            body_text += "<p>" + quote + "</p>\n\n"
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
            Source=email,
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
        selected_highlights = parse_highlights(all_highlights)
        email_text = format_highlights(selected_highlights)
        send_email(email_text, email)
    
    return {
        'statusCode': 200,
        'body': ""
    }
