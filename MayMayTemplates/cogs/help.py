from itertools import groupby

import discord
import asyncio
from discord.ext import commands


class MayMayHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={"help": "Shows info about the bot, a command, or category."})

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            fmt = f'{command.name}'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{self.clean_prefix}{alias} {command.signature}'

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot

        def key(c):
            return c.cog_name or "\u200bUncategorized Commands\n"

        entries = await self.filter_commands(bot.commands, sort=True, key=key)
        embed: discord.Embed = bot.embed()
        embed.set_author(name=f"{ctx.me.name} Help", icon_url=ctx.me.avatar_url)
        embed.set_footer(text=embed.footer.text + f" • Do {self.clean_prefix}help <command> for more info!")
        embed.description = bot.description or ''
        for ext, cmds in groupby(entries, key=key):
            if str(ext).lower() == "jishaku":
                continue
            embed.description += f"\n**{ext}**\n" + "\n".join(
                [f'> `{self.get_command_signature(cmd)}` - {cmd.help or "No help provided."}' for cmd in cmds])

        embed_dict = {
            "ℹ️": bot.embed(description="<argument> - This means the argument is **required.**\n[argument] - This means the argument is **optional.**\n[A|B] - This means that it can be either **A or B.**\n[argument...] - This means you can have **multiple arguments.**\nNow that you know the basics, it should be noted that...\n**You do not type in the brackets!**"),
            "↩️": embed
        }
        valid_reactions = [*embed_dict.keys()] + ['⏹']
        msg = await ctx.send(embed=embed)
        for i in valid_reactions:
            await msg.add_reaction(i)
        try:
            while True:
                # I am aware that I can use ext menus here
                # whatevs
                done, pending = await asyncio.wait([bot.wait_for('reaction_add', timeout=300, check=lambda re, us: str(re.emoji) in valid_reactions and us == ctx.author and re.message.id == msg.id), bot.wait_for('reaction_remove', timeout=300, check=lambda re, us: str(re.emoji) in valid_reactions and us == ctx.author and re.message.id == msg.id)], return_when=asyncio.FIRST_COMPLETED)
                data = done.pop().result()
                if str(data[0].emoji) == '⏹':
                    await msg.delete()
                    await ctx.message.add_reaction(emoji="☑️")
                else:
                    e = embed_dict.get(str(data[0].emoji))
                    await msg.edit(embed=e)
        except asyncio.TimeoutError:
            pass

    async def send_command_help(self, command):
        embed = self.context.bot.embed()
        embed.title = self.get_command_signature(command)
        embed.description = command.help or "No help provided"
        if command.aliases:
            embed.add_field(name=f"Aliases", value=f"{', '.join([f'`{command}`' for command in command.aliases])}")
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = self.context.bot.embed()
        embed.title = self.get_command_signature(group)
        embed.description = group.help or "No help provided"
        if group.aliases:
            embed.add_field(name=f"Aliases", value=f"{', '.join([f'`{command}`' for command in group.aliases])}")
        if isinstance(group, commands.Group):
            embed.add_field(name=f"Subcommands", value=f"{', '.join([f'`{command}`' for command in group.commands])}")
        await self.context.send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = MayMayHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(Help(bot))
