# try:
#     import unzip_requirements
# except ImportError:
#     pass

import asyncio
import json
import os

from shared import get_all_to_retry, call_lambda_sync


def orchestrator(event, ctx):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_all_to_retry())

    for list_ids in result:
        print("LIST_IDS", list_ids)

        call_lambda_sync('ip-read_from_contact_flow', json.dumps({
            "list_ids": list_ids
        }))


if __name__ == '__main__':
    os.environ['host'] = 'localhost'
    os.environ['user'] = 'robot'
    os.environ['password'] = '123456'
    os.environ['db'] = 'robot'

    orchestrator({}, {})
