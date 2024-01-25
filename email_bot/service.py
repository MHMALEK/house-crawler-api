from mailjet_rest import Client

api_key = 'a720a708bbca56c0d31a78ec088f6c4f'
api_secret = '49598ad4e20619efc8f6c34b499f463f'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

import logging
def send_email(subject, body, to_email, from_email):
    data = {
    'Messages': [
        {
        "From": {
            "Email": from_email,
            "Name": 'Netherland House Checker'
        },
        "To": [
            {
            "Email": to_email,
            "Name": "House Checker"
            }
        ],
        "Subject": subject,
        "TextPart": body,
        "HTMLPart": "",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    logging.warning(f"Sending email with data {data}")
    result = mailjet.send.create(data=data)
    
    print(result.status_code)            