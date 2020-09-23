import discord
import os

from discord.ext import commands
from collections import Counter


class JustGamingBot(commands.AutoShardedBot):

    def __init__(self):
        super().__init__('!', case_insensitive=True)

    def run(self):
        super().run(os.getenv('BOT_TOKEN'), reconnect=True)
