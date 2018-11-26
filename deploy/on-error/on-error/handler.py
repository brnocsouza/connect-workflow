try:
    import unzip_requirements
except ImportError:
    pass

import asyncio
import json
import os

from shared import Data


def on_error(event, ctx):
    loop = asyncio.get_event_loop()
    id_store = event['Details']['ContactData']['Attributes']['id']

    print('ID_STORE', id_store)

    store = Data({
        "id": id_store
    }, 'pdv')

    # Find and fill
    loop.run_until_complete(store.find())

    print(store)

    loop.run_until_complete(store.save_retry())

    print('END')
