"""
MayMayTemplates Discord Bot
Copyright (C) 2020  nizcomix

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
"""
import traceback

import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.x_r = ":warning:727013811571261540"
        self.channel = self.bot.get_channel(727277234666078220)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Lines 29-50 used from niztg's CyberTron5000 GitHub Repository provided by the MIT License
        # https://github.com/niztg/CyberTron5000/blob/master/CyberTron5000/cogs/events.py/#L25-L48
        # Copyright (C) 2020  nizcomix
        et = type(error)
        tb = error.__traceback__
        v = 4
        lines = traceback.format_exception(et, error, tb, v)
        traceback_text = "".join(lines)
        known_errors = [commands.BadArgument, commands.MissingRequiredArgument, commands.MissingPermissions, commands.BotMissingPermissions, commands.CommandOnCooldown, commands.NSFWChannelRequired, commands.NotOwner]
        pass_errors = [commands.CommandNotFound, commands.CheckFailure, commands.BadUnionArgument]
        if type(error) in pass_errors:
            return
        elif type(error) in known_errors:
            await ctx.message.add_reaction(self.x_r)
            await ctx.send(f'<{self.x_r}> **{ctx.author.name}**, {(str(error))}')
        else:
            embed = discord.Embed(title="Unkown Error Occured!", description=f"Error on `{ctx.command}`: `{error.__class__.__name__}`\n```py\n{traceback_text}```\n**Server:** {ctx.guild}\n**Author:** {ctx.author}\n[URL]({ctx.message.jump_url})")
            await ctx.message.add_reaction(self.x_r)
            await self.channel.send(embed=embed)
            # await ctx.send(content="The error has been sent to my creator! It will be fixed as soon as possible!",
            #                embed=embed)

    @commands.Cog.listener(name='on_message')
    async def maymayhelper_mention(self, message):
        if "<@&710880987168505898>" in message.content:
            for i in ["<:upvote:700689655607197746>", "<:downvote:700689654906880063>", "<:yes:719841750788866060>", "<:pepesquint:700692817789321269>"]:
                await message.add_reaction(i)
        if message.author.id != 350349365937700864 and not message.author.bot and any(item in message.content.lower() for item in ['niz']):
            await self.bot.get_user(350349365937700864).send(embed=discord.Embed(description=f'[pinged]({message.jump_url})'))

def setup(bot):
    bot.add_cog(Events(bot))