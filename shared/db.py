import os
import typing
from typing import List

import aiomysql


def get_connection_info():
    return {
        "host": os.environ['host'] if 'host' in os.environ else 'localhost',
        "user": os.environ['user'] if 'user' in os.environ else 'robot',
        "password": os.environ['password'] if 'password' in os.environ else '123456',
        "db": os.environ['db'] if 'db' in os.environ else 'robot',
        "port": int(os.environ['port']) if 'port' in os.environ else 4306
    }


async def connect():
    data = get_connection_info()

    # Connect to the database
    return await aiomysql.connect(
        host=data['host'],
        user=data['user'],
        password=data['password'],
        db=data['db'],
        port=data['port'],
        charset='utf8mb4',
        autocommit=True,
        cursorclass=aiomysql.cursors.DictCursor
    )


def parse_data(item):
    item['status'] = ord(item['status'])
    item['answers'] = ord(item['answers'])

    return item


async def get_all_to_retry():
    con = await connect()
    cursor = await con.cursor()

    sql = """SELECT id
             FROM `pdv`
             WHERE `status` = 0
                AND `retries` < 4
                AND (
                    `retry_when` IS NULL
                    OR `retry_when` < NOW()
                    )"""

    await cursor.execute(sql)
    return [item['id'] for item in await cursor.fetchall()]


async def get_data(id_record: int):
    con = await connect()
    cursor = await con.cursor()

    sql = """SELECT *
             FROM `pdv`
             WHERE `id` = %s"""

    await cursor.execute(sql, (id_record,))
    return parse_data(await cursor.fetchone())


async def get_all_data_in(ids_record: List[int]):
    con = await connect()
    cursor = await con.cursor()
    sql = """SELECT *
             FROM `pdv`
             WHERE `id` IN (%s)"""

    list_data = []
    for item in chunks(ids_record, 20):
        format_strings = ','.join(['%s'] * len(item))
        local_sql = sql % format_strings

        await cursor.execute(local_sql, tuple(item))
        list_data += await cursor.fetchall()

    for item in list_data:
        item['status'] = ord(item['status'])
        item['answers'] = ord(item['answers'])

    return list_data


async def execute(sql, data):
    try:
        con = await connect()
        cursor = await con.cursor()
        await cursor.execute(sql, tuple(data))
    except Exception as ex:
        print(ex)


async def find_all(sql, data):
    try:
        con = await connect()
        cursor = await con.cursor()
        await cursor.execute(sql, tuple(data))
        list_data = await cursor.fetchall()

        for item in list_data:
            item['status'] = ord(item['status'])
            item['answers'] = ord(item['answers'])

        return list_data
    except Exception as ex:
        print(ex)
        return None


async def find_many(sql, data) -> typing.Union[typing.Iterable, None]:
    try:
        con = await connect()
        cursor = await con.cursor()
        await cursor.execute(sql, tuple(data))
        list_data = await cursor.fetchmany()

        for item in list_data:
            item['status'] = ord(item['status'])
            item['answers'] = ord(item['answers'])

        return list_data
    except Exception as ex:
        print(ex)
        return None


async def find(sql, data):
    try:
        con = await connect()
        cursor = await con.cursor()
        await cursor.execute(sql, tuple(data))
        item = await cursor.fetchone()
        item['status'] = ord(item['status'])
        item['answers'] = ord(item['answers'])

        return item
    except Exception as ex:
        print(ex)
        return None
