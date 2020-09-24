import discord
from discord.ext import commands


class CogsManagement(commands.Cog, name='CogsManagement'):
    def __init__(self, bot):
        self.bot = bot
        self.cogs_dir = 'cogs.'
        self.cogs_blocklist = [
            'cogsmanagement'
        ]

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, cog: str):
        cog = cog.lower()

        # check if cog is not on blocklist
        if cog not in self.cogs_blocklist:

            # try to load cog
            try:
                # load cog
                self.bot.load_extension(self.cogs_dir + cog)

            except Exception as e:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'"{cog}" wurde nicht geladen!'
                )
                embed.add_field(name="Fehler", value="{}: {}".format(
                    type(e).__name__, e), inline=False)

                # send embed
                await ctx.send(embed=embed)
            else:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.green(),
                    title=f'"{cog}" wurde erfolgreich geladen!'
                )
                # send embed
                await ctx.send(embed=embed)
        else:
            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'"{cog}" wurde nicht geladen!'
            )
            embed.add_field(
                name="Fehler", value="Die Erweiterung steht auf der Blockliste und darf nicht geladen werden.", inline=False)

            # send embed
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, cog: str):
        cog = cog.lower()

        # check if cog is not on blocklist
        if cog not in self.cogs_blocklist:

            # try to unload cog
            try:
                # load cog
                self.bot.unload_extension(self.cogs_dir + cog)

            except Exception as e:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'"{cog}" wurde nicht deaktiviert!'
                )
                embed.add_field(name="Fehler", value="{}: {}".format(
                    type(e).__name__, e), inline=False)

                # send embed
                await ctx.send(embed=embed)
            else:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.green(),
                    title=f'"{cog}" wurde erfolgreich deaktiviert!'
                )
                # send embed
                await ctx.send(embed=embed)
        else:
            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'"{cog}" wurde nicht deaktiviert!'
            )
            embed.add_field(
                name="Fehler", value="Die Erweiterung steht auf der Blockliste und darf nicht deaktiviert werden.", inline=False)

            # send embed
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, cog: str):
        cog = cog.lower()

        # check if cog is not on blocklist
        if cog not in self.cogs_blocklist:

            # try to unload cog
            try:
                # load cog
                self.bot.unload_extension(self.cogs_dir + cog)

            except Exception as e:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'"{cog}" wurde nicht deaktiviert!'
                )
                embed.add_field(name="Fehler", value="{}: {}".format(
                    type(e).__name__, e), inline=False)

                # send embed
                await ctx.send(embed=embed)
            else:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.green(),
                    title=f'"{cog}" wurde erfolgreich deaktiviert!'
                )
                # send embed
                await ctx.send(embed=embed)
        else:
            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'"{cog}" wurde nicht deaktiviert!'
            )
            embed.add_field(
                name="Fehler", value="Die Erweiterung steht auf der Blockliste und darf nicht deaktiviert werden.", inline=False)

            # send embed
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, cog: str):
        cog = cog.lower()

        # check if cog is not on blocklist
        if cog not in self.cogs_blocklist:

            # try to reload cog
            try:
                # load cog
                self.bot.reload_extension(self.cogs_dir + cog)

            except Exception as e:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'"{cog}" wurde nicht neugeladen!'
                )
                embed.add_field(name="Fehler", value="{}: {}".format(
                    type(e).__name__, e), inline=False)

                # send embed
                await ctx.send(embed=embed)
            else:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.green(),
                    title=f'"{cog}" wurde erfolgreich neugeladen!'
                )
                # send embed
                await ctx.send(embed=embed)
        else:
            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'"{cog}" wurde nicht neugeladen!'
            )
            embed.add_field(
                name="Fehler", value="Die Erweiterung steht auf der Blockliste und darf nicht neugeladen werden.", inline=False)

            # send embed
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CogsManagement(bot))
