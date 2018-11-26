import os
from functools import lru_cache
from typing import Union

import aioboto3
import boto3
from botocore.exceptions import ClientError

import shared

PROFILE = 'ecs'


def get_environment():
    try:
        return {
            "QueueId": os.environ['QueueId'],
            "ContactFlowId": os.environ['ContactFlowId'],
            "InstanceId": os.environ['InstanceId'],
            "BotName": os.environ['BotName'],
        }
    except KeyError:
        return None


@lru_cache(maxsize=None)
def get_session(profile=None):
    global PROFILE

    if profile is not None:
        return aioboto3.Session(profile_name=profile)
    elif PROFILE is not None:
        return aioboto3.Session(profile_name=PROFILE)
    else:
        return aioboto3


@lru_cache(maxsize=None)
def get_session_sync(profile=None):
    global PROFILE

    if profile is not None:
        return boto3.Session(profile_name=profile)
    elif PROFILE is not None:
        return boto3.Session(profile_name=PROFILE)
    else:
        return boto3


async def start_outbound_voice_contact(
        attr: shared.Data,
        environment: dict
) -> Union[shared.Data, None]:
    try:
        async with get_session().client('connect') as connect:
            response = await connect.start_outbound_voice_contact(
                DestinationPhoneNumber=attr.fone,
                ContactFlowId=environment['ContactFlowId'],
                InstanceId=environment['InstanceId'],
                QueueId=environment['QueueId'],
                Attributes={
                    'BotName': environment['BotName'],
                    'PDV': attr.name,
                    'id': str(attr.id)
                }
            )

            attr.contact_id = response['ContactId']

        return attr
    except ClientError as ex:
        print(ex)
        return None


async def call_lambda(function_name: str, payload: str):
    try:
        print(function_name)
        print(payload)

        async with get_session().client('lambda') as client:
            print(client)

            response = await client.invoke(
                FunctionName=function_name,
                InvocationType='Event',
                Payload=payload
            )

            return response
    except ClientError as ex:
        print(ex)
        return None


def call_lambda_sync(function_name: str, payload: str):
    try:
        print(function_name)
        print(payload)

        response = get_session_sync().client('lambda').invoke(
            FunctionName=function_name,
            InvocationType='Event',
            Payload=payload
        )

        return response
    except ClientError as ex:
        print(ex)
        return None
