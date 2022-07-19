"""
discord events : 
    on_ready : lance une bulle pour signaler que discord est ouvert
    on_message : lance une bulle message discord

methods : 
    get_messages : renvoie les "n" derniers messages (avant "depart") du "channel"
    get_channels : renvoie les channels disponibles.
"""

import discord
from interfaces.utilities import JsonInterface

def get_token():
    return "ODY4NTQ4NDI3Mzc2NjI3NzYy.YPxQwQ.oHaOrqROdEyghD85S8M8dlEFeHg" #a planquer dans un fichier d'environnement

class DiscordInterface():
    """
    etats des calls (en attente...) sera sauvegarde via pickle
    """
    def __init__(self, meep, token=None): #mettre la recherche des messages a ce niveau la est surement inutile => boucler asyncio au niveau du fichier processes
        if token:
            self.token = token
        else:
            self.token = get_token()
        self.meep = meep

        self.events = {'new messages':True} #accessible par dehors

        self.identifiers = JsonInterface("interfaces\data\discord_ids.json") #accessible par dehors
        self.client = discord.Client(loop=meep.loop)

        self.temporary_message_history = []

        self.events = {}
        self.update_events()

    #events

        @self.client.event
        async def on_ready():
            print('discord ON READY EVENT')

        @self.client.event 
        async def on_message(message):
            print("discord ON MESSAGE EVENT")
            author = message.author.name + '#' + message.author.discriminator
            if not author == "Meep#3221":

                self.temporary_message_history.append({'date':message.created_at, 'author':author, 'content':message.content})
                
                for event in self.events["message recu"]: #CASCADE
                    self.meep.cascade(event)

                self.identifiers.update('users', message.author.id, author)

    #get

    def get_messages(self, channel_id): #accessible par dehors
        print('bwo')

    def can_write_in(self):
        channel_list = []
        for guild in self.client.guilds:
            for channel in guild.text_channels:
                name = guild.name + '#' + channel.name
                channel_list.append(name)
        return channel_list

    #internal

    def update_events(self):
        meta = JsonInterface("meta.json").get()
        for interface in meta["interfaces"]:
            if interface["name"] == "Discord":
                self.events = interface["events"]

    def update_ids(self):
        #channel scrapping
        for guild in self.client.guilds:
            self.identifiers.update('guilds', guild.id, guild.name)

            for channel in guild.text_channels:
                name = guild.name + '#' + channel.name
                self.identifiers.update('text channels', channel.id, name)

            for channel in guild.voice_channels:
                name = guild.name + '#' + channel.name
                self.identifiers.update('voice channels', channel.id, name)

            for user in guild.members:
                name = user.name + '#' + user.discriminator
                self.identifiers.update('users', user.id, name)

        self.identifiers.save()

    async def send(self, id, message, userid=False):
        print("discord :: send FUNCTION TRIGGERED w "+message+" ; "+id)
        if userid:
            user = await self.client.fetch_user(int(id)) #cree un objet discord user (qui a une method send) pour envoyer le msg en DM
            channel = user
        else: #is channel id
            channel = await self.client.fetch(int(id))
        await channel.send(message)

    async def start(self): #rendre asynchrone ===
        await self.client.start(self.token)