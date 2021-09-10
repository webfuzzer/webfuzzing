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
def test():
    async def _request(url = None):
        if not url:
            url = URL 
        print(url)
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                for attribute, tagname in tags.items():
                    for element in soup.find_all(tagname):
                        if attribute in element.attrs:
                            if element.attrs[attribute] not in URLists:
                                NewLink = element.get(attribute)
                                URLists.add(NewLink)
                                await _request(NewLink)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            *(_request(),)
        )
    )

test()
print(dt() - times)

# async def getLinks(self, url = None) -> None:

#         requrl = await self.LinkChecks(url)

#         print(url)
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(requrl) as response:
#                     soup = BeautifulSoup(await response.text(), 'html.parser')
#                     for attribute, tagname in self.tags.items():
#                         for element in soup.find_all(tagname):
#                             if attribute in element.attrs:
#                                 if element.attrs[attribute] not in self.URLists:
#                                     NewLink = element.get(attribute)
#                                     self.URLists.add(NewLink)
#                                     await self.getLinks(NewLink)
#         except:
#             pass
