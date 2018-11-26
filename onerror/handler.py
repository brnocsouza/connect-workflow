import asyncio
import json
import os

from shared import Data


def on_error(event, ctx):
    try:
        loop = asyncio.get_event_loop()
        id_store = event['Details']['ContactData']['Attributes']['id']

        print('ID_STORE', id_store)

        store = Data({
            "id": id_store
        }, 'pdv')

        # Find and fill
        loop.run_until_complete(store.find())

        print(store)

        # loop.run_until_complete(store.save_retry())

        print('END')
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    os.environ['host'] = "chatbot-ip.cxcgjwehdjin.us-east-1.rds.amazonaws.com"
    os.environ['user'] = "lex_root"
    os.environ['password'] = "iGGyrkZV5F"
    os.environ['db'] = "chatbot"
    os.environ['port'] = "3306"

    with open('./event.json') as file:
        on_error(json.loads(file.read()), {})
