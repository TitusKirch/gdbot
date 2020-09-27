import discord
import json
import os

from discord.ext import commands, tasks
from models.game import Game as GameModel
from models.application import Application
from models.applicationGame import ApplicationGame
from db import db_session, Session


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
            # if os.path.isfile('games.json'):
            #    with open('games.json') as json_file:
            #        self.games = json.load(json_file)
            #    self.check_for_games.start()
            pass

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

    @commands.command(aliases=['spiele'])
    async def games(self, ctx):
        output = ctx.author.mention + " derzeit unterstütze ich folgende Spiele:\n"
        output += '```'
        for game in GameModel.all():
            output += f'{game.key} => {game.name}'

        output += '```'
        output += "Das erste ist immer der \"key\" gefolgt von dem Namen des Spiels. Mit `!join` gefolgt von eienr Auflistung von Keys (Separiert durch Leerzeichen) kannst du dir selbst Spiele zuweisen."

        # send output
        await ctx.send(output)

    @commands.command()
    async def join(self, ctx, *game_keys: str):
        success = []
        has = []
        failed = []
        roles = []
        for game_key in game_keys:
            game = GameModel.getByKey(game_key)
            if (game and game.roleID):
                role = ctx.guild.get_role(game.roleID)

                if role in ctx.author.roles:
                    has.append(game_key)
                else:
                    roles.append(role)
                    success.append(game_key)
            else:
                failed.append(game_key)

        await ctx.author.add_roles(*roles)

        # create output embeds
        embed_success = discord.Embed(
            colour=discord.Colour.green(),
            title='Erfolgreich'
        )
        embed_has = discord.Embed(
            colour=discord.Colour.blue(),
            title='Schon in Gruppen'
        )
        embed_failed = discord.Embed(
            colour=discord.Colour.red(),
            title='Fehler'
        )

        if success:
            embed_success.add_field(
                name='Zugewiesene Spiele:',
                value=', '.join(success), inline=False)

            # send embeds
            await ctx.send(ctx.author.mention, embed=embed_success)

        if has:
            embed_has.add_field(
                name='Schon zugewiesene Spiele:',
                value=', '.join(has), inline=False)

            # send embeds
            await ctx.send(ctx.author.mention, embed=embed_has)

        if failed:
            embed_failed.add_field(
                name='Nicht zugewiesene Spiele:',
                value=', '.join(failed), inline=False)

            # send embeds
            await ctx.send(ctx.author.mention, embed=embed_failed)

    @commands.command()
    async def leave(self, ctx, *game_keys: str):
        success = []
        hasNot = []
        failed = []
        roles = []
        for game_key in game_keys:
            game = GameModel.getByKey(game_key)
            if (game and game.roleID):
                role = ctx.guild.get_role(game.roleID)

                if role in ctx.author.roles:
                    roles.append(role)
                    success.append(game_key)
                else:
                    hasNot.append(game_key)
            else:
                failed.append(game_key)

        await ctx.author.remove_roles(*roles)

        # create output embeds
        embed_success = discord.Embed(
            colour=discord.Colour.green(),
            title='Erfolgreich'
        )
        embed_hasNot = discord.Embed(
            colour=discord.Colour.blue(),
            title='Nicht in Gruppen'
        )
        embed_failed = discord.Embed(
            colour=discord.Colour.red(),
            title='Fehler'
        )

        if success:
            embed_success.add_field(
                name='Verlassene Spiele:',
                value=', '.join(success), inline=False)

            # send embeds
            await ctx.send(ctx.author.mention, embed=embed_success)

        if hasNot:
            embed_hasNot.add_field(
                name='Nicht vorhandene Spiele:',
                value=', '.join(hasNot), inline=False)

            # send embeds
            await ctx.send(ctx.author.mention, embed=embed_hasNot)

        if failed:
            embed_failed.add_field(
                name='Nicht verlassene Spiele:',
                value=', '.join(failed), inline=False)

            # send embeds
            await ctx.send(ctx.author.mention, embed=embed_failed)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def gameadd(self, ctx, key: str, *name: str):
        # check if game with key exist
        db_game = GameModel.getByKey(key)
        if not db_game:
            gameName = '{}'.format(' '.join(name))
            db_game = GameModel()
            db_game.key = key
            db_game.name = gameName
            db_session.add(db_game)

            # commit update
            db_session.commit()

            gameRole = await ctx.guild.create_role(
                name=gameName,
                mentionable=True,
            )

            # get role
            db_game.roleID = gameRole.id
            db_session.commit()

            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.green(),
                title=f'Spiel angelegt'
            )

            Session.close_all()

            # send embed
            await ctx.send(ctx.author.mention, embed=embed)

        else:

            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'Spiel gefunden'
            )
            embed.add_field(
                name="Fehler", value=f'Es wurde das Spiel "{db_game.name}" mit dem Key "{db_game.key}" gefunden.', inline=False)

            # send embed
            await ctx.send(ctx.author.mention, embed=embed)

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

                if hasattr(activity, 'application_id'):
                    embed.add_field(
                        name='ApplicationID',
                        value=f'{activity.application_id}',
                        inline=False
                    )

                # send message
                await ctx.send(ctx.author.mention, embed=embed)
                break

        if not foundGame:

            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'Kein Spiel gefunden'
            )
            embed.add_field(
                name="Fehler", value=f'Es konnte kein Spiel bei {member.mention} entdeckt werden.', inline=False)

            # send embed
            await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(aliases=['gameapp'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def gameapplication(self, ctx, key: str, member: discord.Member):
        # check if game with key exist
        db_game = GameModel.getByKey(key)
        if db_game:
            foundGame = False
            for activity in member.activities:
                if activity.type == discord.ActivityType.playing:

                    # set found game true
                    foundGame = True

                    db_application = Application.getByID(
                        activity.application_id)
                    if not db_application:
                        db_application.id = activity.id
                        db_application.name = activity.name
                        db_session.add(db_application)
                        db_session.commit()

                    db_application_game = ApplicationGame.getByID(
                        db_application.id,
                        db_game.id
                    )
                    if not db_application_game:
                        db_application_game.applicationID = db_application.id
                        db_application_game.gameID = db_game.id
                        db_session.add(db_application_game)
                        db_session.commit()

                        # create output embed
                        embed = discord.Embed(
                            colour=discord.Colour.green(),
                            title="Application hinzugefügt",
                        )

                    else:
                        # create output embed
                        embed = discord.Embed(
                            colour=discord.Colour.red(),
                            title="Application wurde schon hinzugefügt",
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

                    embed.add_field(
                        name='Spiel',
                        value=f'{db_game.name}',
                        inline=False
                    )

                    embed.add_field(
                        name='SpielID',
                        value=f'{db_game.id}',
                        inline=False
                    )

                    Session.close_all()

                    # send message
                    await ctx.send(ctx.author.mention, embed=embed)
                    break

            if not foundGame:

                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'Kein Spiel gefunden'
                )
                embed.add_field(
                    name="Fehler", value=f'Es konnte kein Spiel bei {member.mention} entdeckt werden.', inline=False)

                # send embed
                await ctx.send(ctx.author.mention, embed=embed)

        else:

            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'Spiel nicht gefunden'
            )
            embed.add_field(
                name="Fehler", value=f'Es wurde kein Spiel mit dem Key "{key}" gefunden.', inline=False)

            # send embed
            await ctx.send(ctx.author.mention, embed=embed)


def setup(bot):
    bot.add_cog(Game(bot))
