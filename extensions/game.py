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

    @tasks.loop(seconds=60.0)
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
                                        await guild_history_channel.send('{0.mention} ich habe erkannt, dass du "**{1.name}**" spielst und dir direkt die passende Gruppe zugewiesen.'.format(member, activity))
                            continue

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def gameinfo(self, ctx, member: discord.Member):
        foundGame = False
        for activity in member.activities:
            if activity.type == discord.ActivityType.playing:

                # set found game true
                foundGame = True

                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.blue(),
                    title="Spielinformationen",
                )

                embed.add_field(
                    name='Name',
                    value=f'{activity.name}',
                    inline=False
                )

                embed.add_field(
                    name='ApplicationID',
                    value=f'{activity.application_id}',
                    inline=False
                )

                # send message
                await ctx.send(ctx.author.mention, embed=embed)

        if not foundGame:

            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'Kein Spiel gefunden'
            )
            embed.add_field(
                name="Fehler", value=f'Es konnte kein Spiel bei {member.mention} entdeckt werden.', inline=False)

            # send embed
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Game(bot))
