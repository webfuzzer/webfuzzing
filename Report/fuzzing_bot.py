import discord.ext.commands as commands
from tldextract import extract
import discord

token = 'OTEyNTkwNjY4NTU0MjAzMTY3.YZyKSg.CjliMhAs3_n5vGdSJ3lt63gApWQ'

Client = discord.Client()

wfb_channel = {}

category_id = ''

@Client.event
async def on_ready():
    print('fuzzing bot starting')

@Client.event
async def on_message(message):
    global category_id
    global wfb_channel
    if message.content.startswith('!category'):
        content = message.content.split(' ')[1].strip()
        if content:
            category = await message.guild.create_category(content)
            category_id = category
            print(f'create category name is {category.name}')

            await message.channel.send(f'create {category.name} Category Completed')

    if message.content.startswith('!fuzzing'):
        content = message.content.split()[1].strip()
        if content: 
            domain = extract(content).domain
            wfb_channel[domain] = content
            channel = await message.guild.create_text_channel(domain, category=category_id)
            print(f'id of the {channel.name} channel is {channel.id}')
            await message.channel.send(f'Create {channel.name} Channel Completed')

@Client.event
async def on_guild_channel_create(channel):
    global wfb_channel
    if channel.category:
        if channel.category.name == 'fuzzing':
            print(wfb_channel)
            print("channel id : ",channel.id)
            await channel.send(f'{wfb_channel[channel.name]} [{channel.category.name}] : Fuzzing Start!')

Client.run(token)