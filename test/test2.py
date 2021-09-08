import aiohttp
import asyncio
import time


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:

        url = 'http://localhost'
        futures = [asyncio.ensure_future(fetch(session, url))
                   for i in range(1, 50)]
        print(futures)
        res = await asyncio.gather(*futures)
        return res

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    start = time.time()
    result = loop.run_until_complete(main())
    print(result)
    end = time.time()
    print(f"elapsed time = {end - start}s")
    loop.close()

# import requests
# import time


# url = 'http://localhost'


# def sync_fetch():
#     res = [requests.get(url)
#            for i in range(1, 50)]
#     return res


# if __name__ == '__main__':

#     start = time.time()
#     sync_fetch()
#     end = time.time()
#     print(f"elapsed time = {end - start}s")

# import requests

# for i in range(1,100):
#     r = requests.get('http://localhost')
#     print(i)