import asyncio
import os

from shared import get_environment, start_outbound_voice_contact, Data, get_all_data_in, call_lambda


def robot(event, ctx):
    loop = asyncio.get_event_loop()
    environment = get_environment()

    call_lambda()
    all_stores = loop.run_until_complete(get_all_data_in(event['list_ids']))

    all_stores = [Data(item, 'pdv') for item in all_stores]

    [print(str(item)) for item in all_stores]

    if len(all_stores) > 0:
        tasks = [start_outbound_voice_contact(item, environment) for item in all_stores]
        tasks_resolved = loop.run_until_complete(asyncio.gather(*tasks))
        tasks_to_save = [item.save() for item in tasks_resolved if item is not None]
        loop.run_until_complete(asyncio.gather(*tasks_to_save))


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
        "list_ids": [1]
        # "list_ids": [1, 2, 3]
    }, {})
