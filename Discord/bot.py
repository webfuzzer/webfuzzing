#from _typeshed import ReadOnlyBuffer
from unicodedata import category
import discord
import asyncio
from discord import channel
# from discord import channel
from discord.channel import CategoryChannel
from discord.embeds import Embed #비동기적 코드 동작
from discord.ext import commands
import tldextract as tld
# from Search.Vulndb import *
import sys,os,re
# default-----------------------------------------------------------------

Token='OTEwMzQyMTQ4MjY2ODExNDEz.YZRcMQ.wzwkkwd-XJL_IjK78XgFWxzVJP4'
bot = commands.Bot(command_prefix="$")
client = discord.Client()
wfb_channel={}
category_id=''
args=''

#-------------------------------------------------------------------------

# discord서버 입장시 토근 입력 받기 

# discord 시작-------------------------------------------------------------
class Discord_bot:
    def __init__(self):
        pass
        
    @client.event
    async def on_ready(): 
        print(f"{client.user.name} is working.")
        await client.change_presence(status=discord.Status.online, activity=None)

# discord 메시지 입력+ 채널생성---------------------------------------------

    @client.event
    async def on_message(message): 
        global category_id
        global wfb_channel
        global args
        # print(message)
        # print(message.content)
        
        commands={
          "info" : Discord_bot.info(),
          "Fuzzing" : Discord_bot.Fuzzing(),
          "Category" : Discord_bot.Category()  
        }
  
        content = message.content 
        #print(content)
        guild = message.guild 
        # author = message.author 
        channel = message.channel
#        content.split(' ')[1].strip()

        args=content.split(" ")
        argc=len(args)

        if content.startswith('!'):
            if argc >= 2:
            # name=argc[1]
                command=args[0]
                argv = re.split("\s+", content[1:])
                commands[argv[0]]
        else:
            await channel.send("input {} value".format(args[0]))
             
#class Command:
    #@bot.command
    async def info():
        greet = discord.Embed(title=f"{client.user.name}",\
                        description=f"Discord Bot Name : {client.user.name}"+"\n"\
                                    f"Discord Bot ID : {client.user.id}"+"\n"\
                                    f"Discord Bot Version : {discord.__version__}"+"\n"\
                                        , color=0x00aaaa)
        await channel.send(embed=greet)   

    #@bot.command
    async def Category():
        #!category=카테고리만 생성
        for arg in args: 
            if arg:
                if True in[arg == i.name for i in Discord_bot.guild.categories]:
                    await channel.send(f"[{arg}] is existed. input other category name")                                    
                else:
                    category = await Discord_bot.guild.create_category(arg)
                    category_id=category
                    print(f'Create Category : {category.name}')
                    Discord_bot.Fuzzing()
                    await channel.send(f'Create [{category.name}] Category Completed')
            else:
                await channel.send("YOU CAN'T FUZZING! SO , Please Input Category Name!") 
            
    #@bot.command
    async def Fuzzing():                
        #fuzzing url채널 생성
        for arg in args:
            domain = tld.extract(arg).domain
            if domain:
                if True in [domain == i.name for i in Discord_bot.guild.text_channels]:
                    await channel.send("this URL is existed. Input other URL")
                else:    
                    channelcreate = await Discord_bot.create_text_channel(domain, category=category_id)
                    wfb_channel[channelcreate.name] = arg
                    print(f'[{channelcreate.name}] Channel ID : {Discord_bot.channel.id}')

                    await channel.send(f'Create [{Discord_bot.channel.name}] Channel Completed')
            else:
                await channel.send(f"DO NOT NEED FUZZING?")

    @client.event
    async def on_guild_channel_create(self,channel):
        if channel.category:
            if channel.category.name == wfb_channel[channel.name]:
                await channel.send(f'{wfb_channel[channel.name]}[{channel.category.name}] Fuzzing Start!')
# -------------------------------------------------------------------------


# discord report----------------------------------------------------------
class Report:
    async def __init__(self, name,method,URL,payload):
        self.name=name
        self.method=method
        self.URL=URL
        self.payload=payload
        self.Report()

    #__init__ -> name=self.__class__.__name__ 추가
    async def Report(name,method,URL,payload):
        report = discord.Embed(title=f"{(name)} 취약점 발생!! ",\
            description=f"method : {method}"+"\n"\
                        f"URL : {URL}"+"\n"\
                        f"payload : {payload}"+"\n", color=0x00aaaa)

        await channel.send(embed=report,category=category_id)

# discord message error check---------------------------------------------

# @client.event 
# async def on_error(event, *args, **kwargs):
#     if event == "on_message": 
#         message = args[0]
#         exc = sys.exc_info() 
#         message.channel.send(str(exc[0].__name__) + "" + str(exc[1])) 
# 	return print("error")

# ------------------------------------------------------------------------

Discord_bot()
client.run(Token)