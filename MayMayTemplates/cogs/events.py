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
        # Traceback code used from Daggy1234's Dagbot GitHub Repository provided by the GNU Affero General Public License v3.0
        # https://github.com/Daggy1234/dagbot/blob/master/dagbot/extensions/errors.py#L38-L42
        # Copyright (C) 2020  Daggy1234
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
        if message.author.id != 350349365937700864 and not message.author.bot and any(item in message.content.lower() for item in ['niz', 'charles', 'python', 'java', 'c++', 'coding', 'nerd']):
            await self.bot.get_user(350349365937700864).send(embed=discord.Embed(description=f'[pinged]({message.jump_url})'))

def setup(bot):
    bot.add_cog(Events(bot))