from flask import jsonify
import concurrent.futures
from http import HTTPStatus
import asyncio
import json
from concurrent import futures
from google.cloud import pubsub_v1
from typing import Callable
from config import Config

config = Config()

def publish_message(topic: str, message):
        try:
            print(config.GOOGLE_PROJECT_ID)
            print(topic)
            print(message)
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(config.GOOGLE_PROJECT_ID, topic)
            message_stringify = json.dumps(message)
            publish_futures=[]
            def get_callback(publish_future, data):
                  def callback(publish_future):
                        try:
                            print(publish_future.result(timeout=2))
                        except futures.TimeoutError as ex:
                            raise ex
                  return callback
            data = message_stringify.encode('utf-8')
            future = publisher.publish(topic_path, data)
            future.add_done_callback(get_callback(future, data))
            publish_futures.append(future)
            futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

            print(f"Published messages with error handler to {topic_path}.")

        except Exception as ex:
              raise ex