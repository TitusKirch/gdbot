import discord
import os
import sys
import logging

from discord.ext import commands
from collections import Counter
from models.extension import Extension
from db import db_session, db_engine, Session

log = logging.getLogger(__name__)


class JustGamingBot(commands.AutoShardedBot):

    def __init__(self):
        super().__init__('!', case_insensitive=True)

        # remove default commands
        self.remove_command('help')

        # try to load extensions management extension
        try:
            self.load_extension('extensions.extensionsmanagement')
        except Exception:
            log.exception(
                "Bot failed to load \"extensionsmanagement\"-extension exception")
            sys.exit()

        # get loaded extension and try to load them
        extensions = Extension.loaded()
        for extension in extensions:
            try:
                self.load_extension('extensions.' + extension.name)
            except Exception:
                extension.isLoaded = False
                db_session.commit()
                log.exception(
                    "Bot failed to load the extension \"" + extension.name + "\"")

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(
            name="Rechnen im Binärsystem",
            type=discord.ActivityType.playing
        ))

    def run(self):
        super().run(os.getenv('BOT_TOKEN'), reconnect=True)
