import discord
import os
import sys

from discord.ext import commands
from collections import Counter

initial_extensions = (
    'cogs.cogsmanagement',
    'cogs.game',
    'cogs.general',
    'cogs.members'
)


class JustGamingBot(commands.AutoShardedBot):

    def __init__(self):
        super().__init__('!', case_insensitive=True)

        # remove default commands
        self.remove_command('help')

        # load extensions
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(
                    f'Failed to load extension {extension}.', file=sys.stderr)
                print(e)

    def run(self):
        super().run(os.getenv('BOT_TOKEN'), reconnect=True)
