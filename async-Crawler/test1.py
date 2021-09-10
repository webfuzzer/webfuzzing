# import asyncio
# import aiohttp
# import requests
# from timeit import default_timer as dt


# s = dt()
# url = 'http://localhost/'
# data = []


# async def get_html():
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             data.append(await response.text())

# loop = asyncio.get_event_loop()
# loop.run_until_complete(
#     asyncio.gather(
#         *(get_html(),)
#     )
# )
# print(dt()-s)
# print(data)
from timeit import default_timer as dt
import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup


times = dt()

URL = 'http://localhost'

tags = {
    'href':['a', 'link', 'area', 'base'],
    'src':['img', 'script', 'iframe', 'embed', 'audio', 'input', 'script', 'source', 'track', 'video'],
    'action':['form'],
    'data':['object'],
}

URLists = set()

# def _request(url = None):
#     if not url:
#         url = URL
#     print(url)
#     try:
#         html = requests.get(url).text
#         soup = BeautifulSoup(html, 'html.parser')

#         for attribute, tagname in tags.items():
#             for element in soup.find_all(tagname):
#                 if attribute in element.attrs:
#                     if element.attrs[attribute] not in URLists:
#                         NewLink = element.get(attribute)
#                         URLists.add(NewLink)
#                         _request(NewLink)
#     except:
#         pass
# async def _request(url = None):
#     if not url:
#         url = URL 
#     print(url)
#     async with aiohttp.ClientSession() as session:
#         async with session.get(URL) as response:
#             soup = BeautifulSoup(await response.text(), 'html.parser')
#             for attribute, tagname in tags.items():
#                 for element in soup.find_all(tagname):
#                     if attribute in element.attrs:
#                         if element.attrs[attribute] not in URLists:
#                             NewLink = element.get(attribute)
#                             URLists.add(NewLink)
#                             await _request(NewLink)

# async def run():
#     loop = asyncio.get_event_loop()
#     return loop.run_until_complete(
#         asyncio.gather(
#             *(_request(),)
#         )
#     )



# test()
# print(dt() - times)
# print(URLists)
# async def _request(url = None):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(URL) as response:
#             return await response.text()

# def run():
#     loop = asyncio.get_event_loop()
#     return loop.run_until_complete(
#         asyncio.gather(
#             *(_request(URL),)
#         )
#     )
# print(dt() - times)
# print(run())

async def _request(url = None):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            print(f"links : {response.links}")
            print(f"method : {response.method}")
            print(f"ok :{response.ok}")
            print(f"url : {response.url}")
            print(f"reason : {response.reason}")
            print(f"start :{response.start}")
            print(f"url_obj : {response.url_obj}")
            print(f"version : {response.version}")
            print(f"wait_for_close : {response.wait_for_close}")
            print(f"cookies : {response.cookies}")
            print(f"history : {response.history}")
            print(f"host : {response.host}")
            # print(f"_headers : {response._headers}")
            print(f"headers : {response.headers}")
            print(f"release : {response.release}")
            print(f"response.request_info")
            # print(f"raw_headers : {response.raw_headers}")
            # for i in dir(response):
            #     print(i)
            return response.status

def run():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        asyncio.gather(
            *(_request(URL),)
        )
    )
print(dt() - times)
print(run())