import asyncio
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
        "port": os.environ['port'] if 'port' in os.environ else 4306
    }


async def connect(loop):
    data = get_connection_info()
    # Connect to the database
    return await aiomysql.connect(host=data['host'],
                                  user=data['user'],
                                  password=data['password'],
                                  db=data['db'],
                                  port=data['port'],
                                  charset='utf8mb4',
                                  autocommit=True,
                                  cursorclass=aiomysql.cursors.DictCursor,
                                  loop=loop)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


async def get_all_to_retry(loop):
    con = await connect(loop)
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
    return chunks([item['id'] for item in await cursor.fetchall()], 100)


async def get_data(id_record: int):
    loop = asyncio.get_event_loop()
    con = await connect(loop)
    cursor = await con.cursor()

    sql = """SELECT *
             FROM `pdv`
             WHERE `id` = %s"""

    await cursor.execute(sql, (id_record,))
    return await cursor.fetchone()


async def get_all_data_in(ids_record: List[int]):
    loop = asyncio.get_event_loop()
    con = await connect(loop)
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

    return list_data


async def execute(loop, sql, data):
    try:
        con = await connect(loop)
        cursor = await con.cursor()
        await cursor.execute(sql, tuple(data))
    except Exception as ex:
        print(ex)


async def find_all(loop, sql, data):
    try:
        con = await connect(loop)
        cursor = await con.cursor()
        await cursor.execute(sql, tuple(data))
        return await cursor.fetchall()
    except Exception as ex:
        print(ex)


async def find_many(loop, sql, data) -> typing.Iterable:
    try:
        con = await connect(loop)
        cursor = await con.cursor()
        await cursor.execute(sql, tuple(data))
        return await cursor.fetchmany()
    except Exception as ex:
        print(ex)


async def find(loop, sql, data):
    try:
        con = await connect(loop)
        cursor = await con.cursor()
        await cursor.execute(sql, tuple(data))
        return await cursor.fetchone()
    except Exception as ex:
        print(ex)
