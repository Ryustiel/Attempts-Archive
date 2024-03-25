"""
methods to interact with discord : sending messages, fetching data
"""
import discord
import asyncio
from os import environ

def send(message: str, id: str, userid: bool):
    """
    (test) boots up discord very fast and sends a single message, then shuts down
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = discord.Client(loop = loop)

    @client.event
    async def on_ready():
        """
        behavior once it's running
        """
        while client == None:
            asyncio.sleep(1) # waiting

        if userid:
            user = await client.fetch_user(int(id)) #cree un objet discord user (qui a une method send) pour envoyer le msg en DM
            channel = user
        else: #is channel id
            channel = await client.fetch(int(id))
        await channel.send(message)

        await client.close()

    client.run(environ.get("DiscordToken"))

    

