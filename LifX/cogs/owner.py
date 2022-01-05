import asyncio
import datetime
import os 
import aiofiles
import nextcord
import aiosqlite
import sys
import urllib
import random
from nextcord.ext import ipc, commands
from nextcord.ext.commands.cooldowns import BucketType


class Owner(commands.Cog, name="🔒Owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="menu", description="Shows an owner-only menu for the bot.")
    @commands.is_owner()
    async def menu(self, ctx):
        guild = ctx.guild
        author = ctx.author
        

        e = nextcord.Embed(
            title="Authentication",
            description=f"Please enter the administrator password for this bot:",
            color=author.color
        )

        msg = await ctx.reply(embed=e)
    
        # we define a local variable named 'correct_answer'
        correct_answer = 'admin1'   

        
        def check(message : nextcord.Message) -> bool: 
            return message.author == ctx.author and message.content == correct_answer


       
        try:
            message = await self.bot.wait_for('message', timeout = 10, check = check)
    
    # this will be executed if the user took too long to answer
        except asyncio.TimeoutError: 
            await ctx.send("Error: timed out")           

    # this will be executed if the author responded properly
        else: 
            await ctx.channel.purge(limit=1)
            mod_logging = nextcord.utils.get(self.bot.get_all_channels(), name="auto-logging")
            e2 = nextcord.Embed(
                title="Welcome",
                description=f"This is the admin panel for LifX.\nYour ID: {author.id}\nYour name: {author.name}\nThis server: {guild.name}\nCurrent abilities you are able to access:",
                color=author.color
            )
            e2.add_field(name="Leave", value="`menu leave`\nLeaves the server")
            e2.add_field(name="Stop", value="`menu stop`\nStops the bot")
            e2.add_field(name="Auth password", value="`menu auth`\nShows the current password of the authentication")
            e2.add_field(name="Leave", value="`menu leave`\nLeaves the server")

            await ctx.send(embed=e2)

    # this will be executed regardless
        finally: 
            pass

    @menu.command()
    @commands.is_owner()
    async def stop(self, ctx):
        await sys.exit()


    @commands.command(name="update", description="An owner-only command. Updates a cog.", aliases=["u"])
    @commands.is_owner()
    async def update(self, ctx, arg1, arg2=None):
        if arg2 is None:
            self.bot.reload_extension(f'cogs.{arg1}')
            await ctx.send(f"Updated cog `{arg1}`")
        else:
            self.bot.reload_extension(f'cogs.{arg1}')
            self.bot.reload_extension(f'cogs.{arg2}')
            await ctx.send(f"Updated cogs `{arg1}` and `{arg2}`")


def setup(bot):
    bot.add_cog(Owner(bot))