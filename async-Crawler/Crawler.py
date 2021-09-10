from re import I
from urllib.parse import parse_qs, quote, unquote, urlparse, urlunparse, urljoin, urlencode
from timeit import default_timer as dt
from bs4 import BeautifulSoup
from request import *
import asyncio
import aiohttp

times = dt()

class Crawler:
    def __init__(self, url,**reqinfo) -> None:
        self.tags = {
            'href':['a', 'link', 'area', 'base'],
            'src':['img', 'script', 'iframe', 'embed', 'audio', 'input', 'script', 'source', 'track', 'video'],
            'action':['form'],
            'data':['object'],
        }
        UserAgent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}

        reqinfo.setdefault('timeout', 3)
        reqinfo.setdefault('headers', UserAgent)

        self.URLists = set()
        self.url = url
        self.redurl = url
        self.reqinfo = reqinfo
        self.MainURLParsing = urlparse(url)

    async def main(self) -> dict:

        await self.getLinks(self.url)
        return await self.QueryEmpty()

    def Crawler(self, url, **reqinfo) -> None:
        self.url = url

        if reqinfo: self.reqinfo = reqinfo

        return Crawler(self.url, **reqinfo)

    async def getLinks(self, url = None) -> None:

        requrl = await self.LinkChecks(url)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(requrl, **self.reqinfo) as res:
                    soup = BeautifulSoup(await res.text(), 'html.parser')
                    for attribute, tagname in self.tags.items():
                        for element in soup.find_all(tagname):
                            if attribute in element.attrs:
                                if element.attrs[attribute] not in self.URLists:
                                    NewLink = element.get(attribute)
                                    self.URLists.add(NewLink)
                                    await self.getLinks(NewLink)
        except:
            pass

    async def LinkChecks(self, url) -> str:
        if url:
            RequestURLString = urljoin(self.redurl, url)
            return RequestURLString

    async def QueryEmpty(self) -> set:

        URListTemp = set()

        for url in self.URLists:
            if url:
                URLParams = urlparse(url)

                if URLParams.query:
                    QueryString = parse_qs(URLParams.query)
                    for key in QueryString.keys():
                        QueryString[key] = ''
                    QueryString = unquote(urlencode(dict(sorted(QueryString.items())), doseq=True))
                    UNURL = urljoin(
                        self.url, urlunparse(URLParams._replace(query  = QueryString))
                    )

                    URListTemp.add(UNURL)

        return URListTemp
    def run(self, url = None, **reqinfo) -> None:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(asyncio.gather(self.main()))

C = Crawler('http://')