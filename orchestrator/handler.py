import asyncio
import json

from shared import call_lambda, chunks


def orchestrator(event, ctx):
    print(event)
    print(ctx)

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(call_lambda('ip-execute_sql', json.dumps({
        "get_by_id": None,
        "save_list": None,
        "get_all_retry": True
    }), 'RequestResponse'))

    print(result)

    result = chunks([item['id'] for item in await result], 100)

    invoke = []
    for list_ids in result:
        invoke.append(
            call_lambda('lambda', json.dumps({
                "list_ids": list_ids
            }))
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*invoke))
