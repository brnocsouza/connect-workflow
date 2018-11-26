import asyncio
import json
import os

from shared import get_environment, Data, call_lambda, start_outbound_voice_contact


def robot(event, ctx):
    loop = asyncio.get_event_loop()
    environment = get_environment()

    lambda_response = [
        call_lambda('ip-execute_sql', json.dumps({"get_by_id": item, "save_list": None}), 'RequestResponse')
        for item in event['list_ids']
    ]

    all_stores = loop.run_until_complete(asyncio.gather(*lambda_response))
    all_stores = loop.run_until_complete(parse_response(all_stores))

    all_stores = [Data(item, 'pdv') for item in all_stores]

    [print(str(item)) for item in all_stores]

    if len(all_stores) > 0:
        tasks = [start_outbound_voice_contact(item, environment) for item in all_stores]
        tasks_resolved = loop.run_until_complete(asyncio.gather(*tasks))
        tasks_to_save = [item.to_dict() for item in tasks_resolved if item is not None]

        request = json.dumps({"get_by_id": None, "save_list": tasks_to_save})
        loop.run_until_complete(call_lambda('ip-execute_sql', request))


async def parse_response(tasks):
    responses = [json.loads(await item.get('Payload').read()) for item in tasks]
    return responses


if __name__ == '__main__':
    os.environ['QueueId'] = "9d9b5e42-706e-414b-a928-cd9b0e9e3d99"
    os.environ['ContactFlowId'] = "447092bd-a341-4c23-aafd-f835b0abfdf0"
    os.environ['InstanceId'] = "2fab8ba3-2b08-4eb8-b1ce-12da2e9c014d"
    os.environ['BotName'] = "Ricardo"

    os.environ['host'] = "chatbot-ip.cxcgjwehdjin.us-east-1.rds.amazonaws.com"
    os.environ['user'] = "lex_root"
    os.environ['password'] = "iGGyrkZV5F"
    os.environ['db'] = "chatbot"
    os.environ['port'] = "3306"

    robot({
        # "list_ids": [1]
        "list_ids": [1, 2, 3]
    }, {})
