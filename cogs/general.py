import discord
from discord.ext import commands


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

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        # create output embed
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="Hilfe",
            description="Hier findest du eine Übersicht aller aktiven Befehle."
        )
        embed.add_field(name="!i|info|information",
                        value="Zeigt alle Informationen über den Bot an.", inline=False)
        embed.add_field(
            name="!h|help", value="Zeigt diesen Text hier an.", inline=False)

        # send message
        await ctx.send(ctx.author.mention, embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
