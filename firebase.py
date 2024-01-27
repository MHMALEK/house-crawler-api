import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials

# Load the environment variables
load_dotenv()

# Get the service account key from the environment variables
service_account_key = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")

# Convert the string back into a JSON object
service_account_info = json.loads(service_account_key)

# Use the service account info to initialize the Firebase admin SDK
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)