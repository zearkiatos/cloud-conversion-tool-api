from flask import Flask, request, jsonify
import json
from google.oauth2 import service_account
from googleapiclient import discovery
import base64
from config import Config

config = Config()

TASK_POSTED, = config.TOPICS





credentials = service_account.Credentials.from_service_account_file(
    config.GOOGLE_PUB_SUB_CREDENTIALS, scopes=['https://www.googleapis.com/auth/cloud-platform']
)

pubsub = discovery.build('pubsub', 'v1', credentials=credentials)

def publish_message(project_id:str, topic:str, message):
        topic_path = f'projects/{project_id}/topics/{topic}'
        message_string = json.dumps(message)
        data = base64.b64encode(message_string.encode('utf-8')).decode('latin1')
        print(message_string)
        print(data)
        try:
            body = {
                'messages': [
                    {
                        'data': data,
                    }
                ]
            }
            pubsub.projects().topics().publish(topic=topic_path, body=body).execute()
            return jsonify({'message': 'Message published successfully'})
        except Exception as ex:
              raise ex