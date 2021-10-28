#!/usr/bin/env python3

from boto3 import resource
from os import getenv
from time import sleep

def get_queue_details():
    sqs = resource('sqs')
    # need to change env var based on how copilot populates the name
    return sqs.get_queue_by_name(QueueName=getenv('QUEUE_NAME'))

def ship_votes(batch_votes):
    # requests.post 
    # http://${sd_endpoint}/votes/batch
    # data: batch_votes
    return

def receive():
    queue = get_queue_details()
    while True:
        # Reset the batch data dict on every run
        _batch_data = []
        # do we enable long polling? https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs-example-long-polling.html#id5
        for message in queue.receive_messages():
            print("MESSAGE CONSUMED: {}".format(message.body))
            # Store message in list as dict
            # example: _batch_data.append({"voter_id": message.body.get(voter_id), "vote": message.body.get(vote)})
            print(message.delete())
            sleep(1)
        ship_votes(_batch_data)
        
if __name__ == '__main__':
    recieve()