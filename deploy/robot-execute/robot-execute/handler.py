try:
    import unzip_requirements
except ImportError:
    pass

import asyncio
import os

from shared import Data, get_environment, start_outbound_voice_contact, get_all_data_in


def robot(event, ctx):
    loop = asyncio.get_event_loop()
    environment = get_environment()

    all_stores = loop.run_until_complete(get_all_data_in(event['list_ids']))

    all_stores = [Data(item, 'pdv') for item in all_stores]

    if len(all_stores) > 0:
        tasks = [start_outbound_voice_contact(item, environment) for item in all_stores]
        tasks_resolved = loop.run_until_complete(asyncio.gather(*tasks))
        tasks_to_save = [item.save() for item in tasks_resolved if item is not None]
        loop.run_until_complete(asyncio.gather(*tasks_to_save))

		
