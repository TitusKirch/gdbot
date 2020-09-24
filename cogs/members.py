import discord
import os

from discord.ext import commands


class Members(commands.Cog, name='Members'):
    def __init__(self, bot):
        self.bot = bot

        self.guild_history_channel_id = os.getenv('GUILD_HISTORY_CHANNEL')
        if isinstance(self.guild_history_channel_id, str):
            self.guild_history_channel_id = int(self.guild_history_channel_id)

    @commands.Cog.listener()
    async def on_member_join(self, member):

        if self.guild_history_channel_id > 0:
            guild_history_channel = member.guild.get_channel(
                self.guild_history_channel_id)
            if guild_history_channel != None:
                await guild_history_channel.send('**Willkommen {0.mention} :tada:**'.format(member))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.guild_history_channel_id > 0:
            guild_history_channel = member.guild.get_channel(
                self.guild_history_channel_id)
            if guild_history_channel != None:
                await guild_history_channel.send('*Bye {0.mention} :sleepy:*'.format(member))


def setup(bot):
    bot.add_cog(Members(bot))
