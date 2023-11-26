#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# mc-server-stat.py

import os
import socket

from mcstatus import JavaServer
from discord.ext import commands, tasks
from discord import Intents
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
STATUS_CHANNEL = os.getenv('STATUS_CHANNEL')
PLAYERS_CHANNEL = os.getenv('PLAYERS_CHANNEL')
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = os.getenv('SERVER_PORT')

intents = Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

@tasks.loop(seconds=1.5)
async def change_channel_names():
    status_channel = client.get_channel(int(STATUS_CHANNEL))
    players_online = client.get_channel(int(PLAYERS_CHANNEL))
    server = JavaServer(SERVER_IP, int(SERVER_PORT))

    try:
        status = server.status()
        if 'Online' in status_channel.name:
            pass
        else:
            await status_channel.edit(name='Server Status: Online')
        players = status.raw['players']['online']
        if not str(players) in players_online.name:
            await players_online.edit(name=f'Players Online: {str(players)}')

    except socket.gaierror:
        if 'OFFLINE' not in status_channel.name:
            await status_channel.edit(name='Server Status: OFFLINE')
        if 'OFFLINE' not in players_online.name:
            await players_online.edit(name=f'Players Online: SERVER OFFLINE')

@client.command(name='ping')
async def get_ping(ctx):
    server = JavaServer(SERVER_IP, int(SERVER_PORT))

    try:
        ping = server.ping()
        await ctx.send(f'The server replied in {ping} ms.')
    except socket.gaierror:
        await ctx.send('Server is not online.')

@client.command(name='players')
async def get_players(ctx):
    server = JavaServer(SERVER_IP, int(SERVER_PORT))

    try:
        status = server.status()
        player_list_dict = status.raw['players']['sample']

        player_list = []
        for pldict in player_list_dict:
            player_list.append(pldict['name'])

        if len(player_list) == 0:
            await ctx.send('No players are online.')
        else:
            await ctx.send(f'Players online: {", ".join(player_list)}')

    except socket.gaierror:
        await ctx.send('Server is not online.')

@client.listen()
async def on_ready():
    change_channel_names.start()

client.run(TOKEN)
