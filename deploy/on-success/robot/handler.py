try:
    import unzip_requirements
except ImportError:
    pass

import asyncio
import json

from shared import Data


def on_success(event, ctx):
    loop = asyncio.get_event_loop()

    id_store: int = event['Details']['ContactData']['Attributes']['id']
    lex_store: str = event['Details']['ContactData']['Attributes']['Lex']

    print('ID_STORE', id_store)
    print('LEX_STORE', lex_store)

    store = Data({
        "id": id_store,
        "answers": True if str(lex_store).lower() == "positivo" else False,
        "status": True
    }, 'pdv')

    # print(str(store))

    loop.run_until_complete(store.save())

    print('COMPLETE')
