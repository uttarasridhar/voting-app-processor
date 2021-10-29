#!/usr/bin/env python3

from boto3 import resource
from os import getenv
from time import sleep
import requests
import json

def get_queue_details():
    sqs = resource('sqs')
    return sqs.Queue(getenv('COPILOT_QUEUE_URI'))

def ship_votes(batch_votes):
    endpoint = str(getenv('COPILOT_SERVICE_DISCOVERY_ENDPOINT'))
    url = 'http://api.' + endpoint + ':8080/votes/batch'
    votes = {
        "votes": batch_votes
    }
    post_data = requests.post(url, data = json.dumps(votes))
    print(post_data.text)
    return

def receive():
    queue = get_queue_details()
    while True:
        # Reset the batch data dict on every run
        _batch_data = []
        # do we enable long polling? https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs-example-long-polling.html#id5
        for message in queue.receive_messages():
            print("MESSAGE CONSUMED: {}".format(message.body))
            msgbody = json.loads(message.body)
            msg = json.loads(msgbody["Message"])
            # Store message in list as dict
            _batch_data.append({
                'voter_id': msg["voter_id"],
                'vote': msg["vote"],
            })
            print(message.delete())
            sleep(1)
        
        ship_votes(_batch_data)
        
if __name__ == '__main__':
    receive()