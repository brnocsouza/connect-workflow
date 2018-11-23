import asyncio
import datetime
from typing import Union

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

import shared


class BaseImport:
    def __init__(self, table):
        self.table = table

    def exist(self, param):
        return hasattr(self, param) and self[param] is not None

    def _save(self, id_query: Union[None, int] = None):
        table = self.table
        keys = [item for item in self.__slots__ if not item.startswith('_') and item != 'id']
        dict_data = {key: getattr(self, key) for key in keys if getattr(self, key) is not None}

        replace = tuple(dict_data.values())

        if id_query and id_query is not None:
            update_replaces = ", ".join([f"{key}=%s" for key in dict_data.keys()])
            update_query = f'UPDATE {table} SET {update_replaces} WHERE id = %s'

            replace += (id_query,)

            return update_query, replace
        else:
            insert_replaces = ', '.join(['%s'] * len(replace))
            columns = ", ".join([f"`{item}`" for item in keys])
            insert_query = f"INSERT INTO {table} ({columns}) VALUES ({insert_replaces});"

            return insert_query, replace

    def __iter__(self):
        new_dict = self.__dict__.copy()

        del new_dict['created_by']
        del new_dict['updated_by']
        del new_dict['company_id']
        del new_dict['uid']
        del new_dict['active']

        return iter(new_dict.values())

    def __getitem__(self, key):
        return getattr(self, key)


class Data(BaseImport):
    __slots__ = [
        "id",
        "name",
        "fone",
        "status",
        "contact_id",
        "retry_when",
        "retries",
        "answers",
        "_address",
        "_number",
        "_city",
        "_region",
    ]

    def __init__(self, data, table):
        super().__init__(table)

        self.id = data['id']
        self.name = data['name'] if 'name' in data else None
        self.status = data['status'] if 'status' in data else None
        self.answers = data['answers'] if 'answers' in data else None
        self._address = data['street_address'] if 'street_address' in data else None
        self._number = data['number'] if 'number' in data else None
        self._city = data['city'] if 'city' in data else None
        self._region = data['region'] if 'region' in data else None
        self.fone = data['fone'] if 'fone' in data else None
        self.retries = data['retries'] if 'retries' in data else None
        self.retry_when = data['retry_when'] if 'retry_when' in data else None
        self.contact_id = data['contact_id'] if 'contact_id' in data else None

    @property
    def street_address(self):
        address = f"{self._address}, {self._number}"

        if self._city is not None:
            address += f" na cidade {self._city}"

        if self._region is not None:
            address += f"- {self._region}"

        return address

    async def save_retry(self):
        if self.retries is not None:
            self.retries += 1
        else:
            self.retries = 1

        self.retry_when = datetime.datetime.now() + datetime.timedelta(hours=3)

        query, replace = self._save(self.id)

        loop = asyncio.get_event_loop()
        await shared.execute(loop, query, replace)

    async def save(self):
        query, replace = self._save(self.id)

        loop = asyncio.get_event_loop()
        await shared.execute(loop, query, replace)

    async def find(self):
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        loop = asyncio.get_event_loop()
        store_data = await shared.find(loop, query, (self.id,))

        self.name = store_data['name'] if 'name' in store_data else None
        self._address = store_data['street_address'] if 'street_address' in store_data else None
        self._number = store_data['number'] if 'number' in store_data else None
        self._city = store_data['city'] if 'city' in store_data else None
        self._region = store_data['region'] if 'region' in store_data else None
        self.fone = store_data['fone'] if 'fone' in store_data else None
        self.retries = store_data['retries'] if 'retries' in store_data else None
        self.retry_when = store_data['retry_when'] if 'retry_when' in store_data else None
        self.contact_id = store_data['contact_id'] if 'contact_id' in store_data else None


class Dynamo:
    def __init__(self, table):
        self.table_name = table

    @staticmethod
    def resources():
        return shared.get_session().resource('dynamodb', region_name='us-east-1')

    async def all(self):
        try:
            async with self.resources() as resource:
                table = resource.Table(self.table_name)

                query = await table.scan()

                return query['Items']
        except (ClientError, KeyError) as ex:
            print(ex)
            return None

    async def get_one(self, uid=None):
        try:
            if uid is not None:
                async with self.resources() as resource:
                    table = resource.Table(self.table_name)

                    query = await table.query(
                        KeyConditionExpression=Key('uid').eq(uid)
                    )

                    return next(iter(query['Items']), None)
            else:
                return None
        except (ClientError, KeyError) as ex:
            print(ex)
            return None

    async def save(self, data: dict):
        try:
            async with self.resources() as resource:
                table = resource.Table(self.table_name)

                item = await self.get_one(data['uid'])

                if item is not None:
                    response = await table.put_item(
                        Item=data
                    )

                    print(response)

                    return True

                return False
        except (ClientError, KeyError) as ex:
            print(ex)
            return False
