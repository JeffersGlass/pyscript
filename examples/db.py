import asyncio

import aiomysql
import js

print("Before")


async def test_example(loop):
    try:
        print("Start")

        pool = await aiomysql.create_pool(
            host="sql9.freemysqlhosting.net",
            port=3306,
            user="sql9595551",
            password="MZchkR2tKN",
            db="mysql",
            loop=loop,
        )
        print("before with")
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                print("Within with")
                await cur.execute(
                    "CREATE TABLE 'USERS' (`id` int(11) NOT NULL AUTO_INCREMENT, `email` varchar(255) COLLATE utf8_bin NOT NULL, PRIMARY KEY (`id`));"
                )
                print("After execute")
                js.console.log(cur.description)
                (r,) = await cur.fetchone()
                assert r == 42
        pool.close()
        await pool.wait_closed()
    except Exception as err:
        js.console.error(str(err))


asyncio.create_task(test_example(pyscript.loop))
