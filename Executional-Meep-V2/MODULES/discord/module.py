"""
gere la commande du bot Meep sur discord, 
permet d'envoyer et de recevoir des messages sur discord.
"""
import discord
import asyncio
from os import environ
from utilities import JsonInterface

# ================================================================= DISCORD CLIENT

identifiers = JsonInterface("MODULES/discord/ids.json") #accessible par dehors

global client, message_history
message_history = ""
client = None

def MODULE_INIT(meep):

    global client
    client = discord.Client(loop=meep.loop)

    #events

    @client.event
    async def on_ready():
        meep.EXECUTE("talker : say", "DISCORD BOT RUNNING")

    @client.event 
    async def on_message(message):
        author = message.author.name + '#' + message.author.discriminator
        if author == "Meep#3221":
            return 
        s = f"'date':{message.created_at}, 'author':{author}, content:{message.content}"

        meep.EXECUTE("input_matcher : matcher", message.content)

        global message_history
        message_history += "\n" + s
        identifiers.update('users', message.author.id, author)

    meep.RUN(client.start, get_token())

# ================================================================= INTERACT

async def send(meep, id, message, userid=False):
    """
    action
    sends the message to the specified channel
    """
    while client == None:
        asyncio.sleep(1)

    if userid:
        user = await client.fetch_user(int(id)) #cree un objet discord user (qui a une method send) pour envoyer le msg en DM
        channel = user
    else: #is channel id
        channel = await client.fetch(int(id))
    await channel.send(message)

async def easy_send(meep, message):
    """
    action
    sends a message to raphael
    """
    if client == None:
        print('COULD NOT SEND "%s" (waiting for discord to boot up)' % message)
        while client == None:
            asyncio.sleep(1)

    await send(meep, 361438727492337664, message, userid=True)

# ================================================================= GET

async def get_messages(meep, channel_id): #accessible par dehors
    """
    getter
    returns the history of the latest messages
    """
    while client == None:
        asyncio.sleep(1)
    return message_history

async def channel_list(meep):
    """
    getter
    return the list of the available channels 
    """
    while client == None:
        asyncio.sleep(1)

    c_list = []
    for guild in client.guilds:
        for channel in guild.text_channels:
            name = guild.name + '#' + channel.name
            c_list.append(name)
    return c_list

# ================================================================= INTERNAL

def update_ids():
    #channel scrapping
    for guild in client.guilds:
        identifiers.update('guilds', guild.id, guild.name)

        for channel in guild.text_channels:
            name = guild.name + '#' + channel.name
            identifiers.update('text channels', channel.id, name)

        for channel in guild.voice_channels:
            name = guild.name + '#' + channel.name
            identifiers.update('voice channels', channel.id, name)

        for user in guild.members:
            name = user.name + '#' + user.discriminator
            identifiers.update('users', user.id, name)

    identifiers.save()

def get_token():
    return environ.get("DiscordToken")