import firebase_admin
from firebase_admin import credentials


def init_firebase():
    cred = credentials.Certificate(
        "./house-crawler-api-2851f-firebase-adminsdk-gd2sx-aae4c937b8.json"
    )
    firebase_admin.initialize_app(cred, {
        'databaseURL' : 'https://house-crawler-api-2851f-default-rtdb.europe-west1.firebasedatabase.app'
    })
