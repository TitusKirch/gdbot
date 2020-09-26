import discord

from discord.ext import commands
from db import db_session
from models.extension import Extension


class ExtensionsManagement(commands.Cog, name='ExtensionsManagement'):
    def __init__(self, bot):
        self.bot = bot
        self.extensions_dir = 'extensions.'
        self.extensions_blocklist = [
            'extensionsmanagement'
        ]

    @commands.command(aliases=['lade', 'aktiviere'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, extension: str):
        extension = extension.lower()

        # check if extension is not on blocklist
        if extension not in self.extensions_blocklist:

            # try to load extension
            try:
                # load extension
                self.bot.load_extension(self.extensions_dir + extension)

                # check extension in database and update/set
                db_extension = Extension.get(extension)
                if db_extension:
                    db_extension.isLoaded = True
                    db_extension.loadMeta()
                else:
                    extension_object = Extension(extension, True)
                    extension_object.loadMeta()
                    db_session.add(extension_object)

                # commit update
                db_session.commit()

            except Exception as e:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'"{extension}" wurde nicht aktiviert!'
                )
                embed.add_field(name="Fehler", value="{}: {}".format(
                    type(e).__name__, e), inline=False)

                # send embed
                await ctx.send(ctx.author.mention, embed=embed)
            else:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.green(),
                    title=f'"{extension}" wurde erfolgreich aktiviert!'
                )
                # send embed
                await ctx.send(ctx.author.mention, embed=embed)
        else:
            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'"{extension}" wurde nicht aktiviert!'
            )
            embed.add_field(
                name="Fehler", value="Die Erweiterung steht auf der Blockliste und darf nicht aktiviert werden.", inline=False)

            # send embed
            await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(aliases=['deaktiviere'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, extension: str):
        extension = extension.lower()

        # check if extension is not on blocklist
        if extension not in self.extensions_blocklist:

            # try to unload extension
            try:
                # load extension
                self.bot.unload_extension(self.extensions_dir + extension)

                # check extension in database and update/set
                db_extension = Extension.get(extension)
                if db_extension:
                    db_extension.isLoaded = False
                else:
                    extension_object = Extension(extension, False)
                    extension_object.loadMeta()
                    db_session.add(extension_object)

                # commit update
                db_session.commit()

            except Exception as e:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'"{extension}" wurde nicht deaktiviert!'
                )
                embed.add_field(name="Fehler", value="{}: {}".format(
                    type(e).__name__, e), inline=False)

                # send embed
                await ctx.send(ctx.author.mention, embed=embed)
            else:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.green(),
                    title=f'"{extension}" wurde erfolgreich deaktiviert!'
                )
                # send embed
                await ctx.send(ctx.author.mention, embed=embed)
        else:
            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'"{extension}" wurde nicht deaktiviert!'
            )
            embed.add_field(
                name="Fehler", value="Die Erweiterung steht auf der Blockliste und darf nicht deaktiviert werden.", inline=False)

            # send embed
            await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(aliases=['neuladen'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, extension: str):
        extension = extension.lower()

        # check if extension is not on blocklist
        if extension not in self.extensions_blocklist:

            # try to reload extension
            try:
                # load extension
                self.bot.reload_extension(self.extensions_dir + extension)

            except Exception as e:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'"{extension}" wurde nicht neugeladen!'
                )
                embed.add_field(name="Fehler", value="{}: {}".format(
                    type(e).__name__, e), inline=False)

                # send embed
                await ctx.send(ctx.author.mention, embed=embed)
            else:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.green(),
                    title=f'"{extension}" wurde erfolgreich neugeladen!'
                )
                # send embed
                await ctx.send(ctx.author.mention, embed=embed)
        else:
            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'"{extension}" wurde nicht neugeladen!'
            )
            embed.add_field(
                name="Fehler", value="Die Erweiterung steht auf der Blockliste und darf nicht neugeladen werden.", inline=False)

            # send embed
            await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(aliases=['erweiterungen', 'cogs', 'ls'])
    @commands.has_permissions(administrator=True)
    async def extensions(self, ctx):

        # create output embeds
        embed_loaded = discord.Embed(
            colour=discord.Colour.green(),
            title="Aktivierte Erweiterungen:"
        )
        embed_unloaded = discord.Embed(
            colour=discord.Colour.red(),
            title="Deaktivierte Erweiterungen:"
        )

        # get loaded extension
        loaded_extensions = Extension.loaded()
        if loaded_extensions:
            for extension in loaded_extensions:
                embed_loaded.add_field(
                    name=extension.name, value=f'Beschreibung: {extension.description} \n Author: {extension.author}', inline=False)
        else:
            embed_loaded.add_field(
                name="Keine Erweiterungen", value="Es sind keine Erweiterungen aktiviert!", inline=False)

        # get unloaded extension
        unloaded_extensions = Extension.unloaded()
        if unloaded_extensions:
            for extension in unloaded_extensions:
                embed_loaded.add_field(
                    name=extension.name, value=f'Beschreibung: {extension.description} \n Author: {extension.author}', inline=False)
        else:
            embed_unloaded.add_field(
                name="Keine Erweiterungen", value="Es sind keine Erweiterungen deaktiviert!", inline=False)

        # send embeds
        await ctx.send(ctx.author.mention, embed=embed_loaded)
        await ctx.send(ctx.author.mention, embed=embed_unloaded)


def setup(bot):
    bot.add_cog(ExtensionsManagement(bot))
