import asyncio
import json

from shared import Data


def on_error(event, ctx):
    loop = asyncio.get_event_loop()
    id_store = event['Details']['ContactData']['Attributes']['id']
    store = Data({
        "id": id_store
    }, 'pdv')

    loop.run_until_complete(store.find())

    if store is not None:
        loop.run_until_complete(store.save_retry())


if __name__ == '__main__':
    with open('./event.json') as file:
        on_error(json.loads(file.read()), {})
