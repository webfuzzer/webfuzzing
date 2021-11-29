import discord
import asyncio
from discord import channel
from discord.embeds import Embed #비동기적 코드 동작
from discord.ext import commands
import tldextract as tld
import sys,os,re


Token='OTEwMzQyMTQ4MjY2ODExNDEz.YZRcMQ.wzwkkwd-XJL_IjK78XgFWxzVJP4'
bot = commands.Bot(command_prefix="!")

class DiscordBot:
    def __init__(self):
        pass
        
    @bot.event
    async def on_ready(self): 
        print(f"{bot.user.name} is working.")
        await bot.change_presence(status=discord.Status.online, activity=None)

    @bot.event
    async def on_message(self,message): 
        content = message.content 
        guild = message.guild 
        author = message.author 
        channel = message.channel

        args=content.split(" ")
        argc=len(args)
        
        if content.startswith('!'):
            if argc >= 2:
                for arg in args:
                # name=argc[1]
                    command=args[0]
                    argv = re.split("\s+", content[1:])
                    print(argv)
                    commands(argv[0])
        else:
            await channel.send("input {} value".format(args[0]))
             
class Command:

    wfb_channel={}
    category_id=''

    async def __init__(self):
        pass

    @bot.command()
    async def info(self):
        greet = discord.Embed(title=f"{bot.user.name}",\
                        description=f"Discord Bot Name : {bot.user.name}"+"\n"\
                                    f"Discord Bot ID : {bot.user.id}"+"\n"\
                                    f"Discord Bot Version : {discord.__version__}"+"\n"\
                                        , color=0x00aaaa)
        await channel.send(embed=greet)   

    @bot.command()
    async def Category(self,args):
        for arg in args: 
            if arg:
                if True in[arg == i.name for i in self.guild.categories]:
                    await channel.send(f"[{arg}] is existed. input other category name")                                    
                else:
                    category = await self.guild.create_category(arg)
                    category_id=category
                    print(f'Create Category : {category.name}')
                    self.Fuzzing()
                    await channel.send(f'Create [{category.name}] Category Completed')
            else:
                await channel.send("YOU CAN'T FUZZING! SO , Please Input Category Name!") 
            
    @bot.command()
    async def Fuzzing(self,args,wfb_channel,category_id):                
        for arg in args:
            domain = tld.extract(arg).domain
            if domain:
                if True in [domain == i.name for i in self.guild.text_channels]:
                    await channel.send("this URL is existed. Input other URL")
                else:    
                    channelcreate = await self.create_text_channel(domain, category=category_id)
                    wfb_channel[channelcreate.name] = arg
                    print(f'[{channelcreate.name}] Channel ID : {self.channel.id}')

                    await channel.send(f'Create [{self.channel.name}] Channel Completed')
            else:
                await channel.send(f"DO NOT NEED FUZZING?")

    @bot.event
    async def on_guild_channel_create(self,channel,wfb_channel):
        if channel.category:
            if channel.category.name == wfb_channel[channel.name]:
                await channel.send(f'{wfb_channel[channel.name]}[{channel.category.name}] Fuzzing Start!')

    bot.run(Token)
class Report:
    async def __init__(self, name,method,URL,payload):
        self.name=name
        self.method=method
        self.URL=URL
        self.payload=payload
        self.Report()

    @bot.command()
    async def Report(name,method,URL,payload):
        report = discord.Embed(title=f"{(name)} 취약점 발생!! ",\
            description=f"method : {method}"+"\n"\
                        f"URL : {URL}"+"\n"\
                        f"payload : {payload}"+"\n", color=0x00aaaa)

        await channel.send(embed=report,category=DiscordBot.category_id)

DiscordBot()