try:
    import unzip_requirements
except ImportError:
    pass

import asyncio
import json
import os

from shared import call_lambda, get_all_to_retry


def orchestrator(event, ctx):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_all_to_retry(loop))

    invoke = []
    for list_ids in result:
        invoke.append(call_lambda('lambda', json.dumps({
            "list_ids": list_ids
        })))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*invoke))


if __name__ == '__main__':
    os.environ['host'] = 'localhost'
    os.environ['user'] = 'robot'
    os.environ['password'] = '123456'
    os.environ['db'] = 'robot'

    orchestrator({}, {})
