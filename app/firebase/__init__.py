import os
import base64
import json
import firebase_admin
from firebase_admin import credentials


def init_firebase():
    # Get the base64 encoded service account key from the environment variable
    base64_service_account_key = os.environ.get("FIREBASE_SERVICE_ACCOUNT_BASE64")

    # Decode the service account key
    service_account_key = base64.b64decode(base64_service_account_key).decode("utf-8")

    # Convert the service account key to a dictionary
    service_account_info = json.loads(service_account_key)

    service_account_info["private_key"] = service_account_info["private_key"].replace(
        "\\n", "\n"
    )

    # Use the service account key to authenticate
    cred = credentials.Certificate(service_account_info)

    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": "https://house-crawler-api-2851f-default-rtdb.europe-west1.firebasedatabase.app"
        },
    )
