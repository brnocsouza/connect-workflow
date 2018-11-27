import json

import boto3
from botocore.exceptions import ClientError


def orchestrator(event, ctx):
    result = call_lambda('ip-execute_sql', json.dumps({
        "get_by_id": None,
        "save_list": None,
        "get_all_retry": True
    }), 'RequestResponse')

    print(result)

    if result is not None:
        result = chunks(result, 100)

        for list_ids in result:
            call_lambda('ip-read_from_contact_flow', json.dumps({"list_ids": list_ids}))


def call_lambda(function_name: str, payload: str, invocationType: str = 'Event'):
    try:
        client = boto3.client('lambda')
        print(client)

        response = client.invoke(
            FunctionName=function_name,
            InvocationType=invocationType,
            Payload=payload
        )

        return response

    except ClientError as ex:
        print(ex)
        return None


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


if __name__ == '__main__':
    orchestrator({}, {})
