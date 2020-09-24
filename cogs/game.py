import discord
import json
import os

from discord.ext import commands, tasks


class Game(commands.Cog, name='Game'):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = os.getenv('GUILD_ID')
        if isinstance(self.guild_id, str):
            self.guild_id = int(self.guild_id)

        self.guild_history_channel_id = os.getenv('GUILD_HISTORY_CHANNEL')
        if isinstance(self.guild_history_channel_id, str):
            self.guild_history_channel_id = int(self.guild_history_channel_id)

        if self.guild_id > 0:
            if os.path.isfile('games.json'):
                with open('games.json') as json_file:
                    self.games = json.load(json_file)

                self.check_for_games.start()

    def cog_unload(self):
        self.check_for_games.cancel()

    @tasks.loop(seconds=5.0)
    async def check_for_games(self):

        if (not hasattr(self, 'guild') or not self.guild):
            self.guild = self.bot.get_guild(self.guild_id)
        else:
            for member in self.bot.get_all_members():
                if member.status != discord.Status.offline:
                    for activity in member.activities:
                        if activity.type == discord.ActivityType.playing:

                            if str(activity.application_id) in self.games:

                                # get game role
                                game_role = self.guild.get_role(
                                    self.games[str(activity.application_id)]['roleID'])
                                guild_history_channel = self.guild.get_channel(
                                    self.guild_history_channel_id)

                                # check if member has not therole
                                if (game_role and game_role not in member.roles):
                                    await member.add_roles(game_role)

                                    if guild_history_channel:
                                        await guild_history_channel.send('{0.mention} ich habe erkannt, dass du "{1.name}" spielst und dir direkt die passende Gruppe zugewiesen.'.format(member, activity))
                            continue


def setup(bot):
    bot.add_cog(Game(bot))
