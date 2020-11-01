from flask import Flask
from flask import request
from capparselib.parsers import CAPParser
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# use a service account to initialize firebase
cred = credentials.Certificate("firebase_project/firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


app = Flask(__name__)

@app.route('/', methods=['POST'])
def retrieve():
    print(request.data)
    message = CAPParser(request.data).as_dict()[0]

    print(message)

    sender = message['cap_sender'].text
    message_id = message['cap_id'].text

    doc_ref = db.collection(sender).document(message_id)
    doc_ref.set(formatForFirebase(message))

    print(formatForFirebase(message))

    return "updated"


def formatForFirebase(cap_message):
    db_entry = {}
    db_entry['dateTime'] = cap_message['cap_sent'].text
    for info in cap_message['cap_info']:
        sensor_data = {}
        for parameter in info['cap_parameter']:
            sensor_data[parameter['valueName'].text] = parameter['value'].text
        db_entry[info['cap_sender_name'].text] = sensor_data
    return db_entry