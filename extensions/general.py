import discord

from discord.ext import commands
from db import db_session, db_engine, Session


class General(commands.Cog, name='General'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['i', 'info'])
    async def information(self, ctx):
        # create output embed
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="Informationen",
            description="Ein Discord-Bot für unseren Gaming-Discord"
        )
        embed.add_field(name="GitHub Repository",
                        value="https://github.com/TitusKirch/justgamingbot", inline=False)

        # send message
        await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(aliases=['h', 'hilfe'])
    async def help(self, ctx):
        # create output embed
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="Hilfe",
            description="Hier findest du eine Übersicht aller aktiven Befehle."
        )
        embed.add_field(
            name="!games|spiele", value="Zeigt dir alle unterstützten Spiele an.", inline=False)
        embed.add_field(
            name="!h|help|hilfe", value="Zeigt diesen Text hier an.", inline=False)
        embed.add_field(name="!i|info|information",
                        value="Zeigt alle Informationen über den Bot an.", inline=False)
        embed.add_field(
            name="!stats|stat", value="Zeigt eine Statistik an", inline=False)

        # send message
        await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(aliases=['stat'])
    async def stats(self, ctx):
        # create output embed
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="Stats",
        )

        members_total = len(self.bot.users)
        members_online = 0
        for member in self.bot.get_all_members():
            if member.status == discord.Status.online:
                members_online += 1

        embed.add_field(name='Mitglieder',
                        value=f'{members_online} von {members_total} online', inline=False)

        embed.add_field(name='Shards',
                        value=f'Shard {ctx.guild.shard_id + 1} von {len(self.bot.shards)} (ID: {ctx.guild.shard_id})', inline=False)

        # send message
        await ctx.send(ctx.author.mention, embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
