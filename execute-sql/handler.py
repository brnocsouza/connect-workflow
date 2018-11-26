import asyncio
import os

from shared import Data, get_all_data_in


def execute_sql(event, ctx):
    loop = asyncio.get_event_loop()

    all_stores = []

    if event['get_by_id'] is not None:
        all_stores = loop.run_until_complete(get_all_data_in([event['get_by_id']]))
    elif event['save_list'] is not None:
        all_stores = [Data(item, 'pdv') for item in event['save_list']]
        tasks_to_save = [item.save() for item in all_stores if item is not None]
        loop.run_until_complete(asyncio.gather(*tasks_to_save))

    return all_stores


if __name__ == '__main__':
    os.environ['host'] = "chatbot-ip.cxcgjwehdjin.us-east-1.rds.amazonaws.com"
    os.environ['user'] = "lex_root"
    os.environ['password'] = "iGGyrkZV5F"
    os.environ['db'] = "chatbot"
    os.environ['port'] = "3306"

    d = execute_sql({
        "get_by_id": None,
        "save_list": [
            {
                "id": 1,
                "contact_id": 'c5cf303b-4975-46fe-967a-70cb95af8099'
            }
        ]
    }, {})

    print(d)
