import asyncio
import json

from shared import Data


def on_success(event, ctx):
    loop = asyncio.get_event_loop()
    id_store: int = event['Details']['ContactData']['Attributes']['id']
    lex_store: str = event['Details']['ContactData']['Attributes']['Lex']
    store = Data({
        "id": id_store,
        "answers": True if str(lex_store).lower() == "positivo" else False,
        "status": True
    }, 'pdv')

    loop.run_until_complete(store.save())


if __name__ == '__main__':
    with open('./event.json') as file:
        on_success(json.loads(file.read()), {})
