from __future__ import print_function
import time
import base64
import boto3
import json

print('kinesisStreamMessageConsumer:module init - start')

HISTORY_SIZE = 10
STREAM_NAME = 'devicesDataStream'
SHARD_ITERATOR_TYPE = 'AT_SEQUENCE_NUMBER'

kinesis = boto3.client('kinesis')

print('kinesisStreamMessageConsumer:module init - end')

def lambda_handler(lambda_events, context):
    print('kinesisStreamMessageConsumer:lambda_handler - start')

    # lambda is invoked on each record, so we take it
    lambda_event = lambda_events['Records'][0]
    event_id = lambda_event['eventID']
    shard_id = event_id.split(':')[0]

    # extract relevant data from event
    kinesis_record = lambda_event['kinesis']
    kinesis_data = extract_main_record_data(kinesis_record)
    timestamp = kinesis_data['timestamp']

    # extract history
    sequence_num = kinesis_data['sequence_num']
    history = get_history(shard_id=shard_id, sequence_num=sequence_num)

    records_for_analysis = {
        'lambda_record_event_id': event_id,
        'kinesis_start_sequent_num': sequence_num,
        'record': kinesis_data['data'],
        'history': history
    }

    print(records_for_analysis)
    print('kinesisStreamMessageConsumer:lambda_handler - end: Successfully processed {} lambda event with {} records of history from {}.'.format(event_id, len(history), timestamp))

def get_history(**kwargs):
    print('kinesisStreamMessageConsumer:get_history - start')
    history = []
    shared_iterator_response = kinesis.get_shard_iterator( \
        StreamName=STREAM_NAME, \
        ShardIteratorType=SHARD_ITERATOR_TYPE, \
        ShardId=kwargs['shard_id'], \
        StartingSequenceNumber=kwargs['sequence_num'], \
    )

    shared_iterator = shared_iterator_response['ShardIterator']
    print('kinesisStreamMessageConsumer:get_history - got shard iterator: {}'.format(shared_iterator))

    response = kinesis.get_records(
        ShardIterator=shared_iterator,
        Limit=HISTORY_SIZE
    )

    print('kinesisStreamMessageConsumer:get_history - got records')
    for kinesis_record in response['Records']:
        record_data = extract_history_record_data(kinesis_record)['data']
        history.append(record_data)

    print('kinesisStreamMessageConsumer:get_history - end. processes {} records'.format(len(history)))

    return history

def extract_main_record_data(kinesis_record):
    print('kinesisStreamMessageConsumer:extract_main_record_data - start')

    # keys from kinesis and from lambda are different in their case (PartitionKey vs. partitionKey)
    kineses_record_low_case_keys = dict((k.lower(),v) for k,v in kinesis_record.iteritems())

    # create data dict / obj
    data_str = base64.b64decode(kineses_record_low_case_keys['data'])
    data_obj = json.loads(data_str)
    timestamp = time.strftime('%d-%m-%Y %H:%M:%S.f', time.localtime(kineses_record_low_case_keys['approximatearrivaltimestamp']))

    data = {
        'partition_key': kineses_record_low_case_keys['partitionkey'],
        'sequence_num': kineses_record_low_case_keys['sequencenumber'],
        'data': data_obj,
        'timestamp': timestamp
    }

    print('kinesisStreamMessageConsumer:extract_main_record_data - end')
    return data


def extract_history_record_data(kinesis_record):
    print('kinesisStreamMessageConsumer:extract_history_record_data - start')

    # keys from kinesis and from lambda are different in their case (PartitionKey vs. partitionKey)
    kineses_record_low_case_keys = dict((k.lower(),v) for k,v in kinesis_record.iteritems())

    # create data dict / obj
    data_str = kineses_record_low_case_keys['data']
    data_obj = json.loads(data_str)
    timestamp = kineses_record_low_case_keys['approximatearrivaltimestamp']

    data = {
        'data': data_obj,
        'timestamp': timestamp
    }

    print('kinesisStreamMessageConsumer:extract_history_record_data - end')
    return data
