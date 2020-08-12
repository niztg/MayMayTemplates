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
from discord.ext import commands
import os


class Meta(commands.Cog):
    """Meta bot commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Shows you the bot's latency"""
        await ctx.send(f'pong {round(ctx.bot.latency * 1000, 3)}')

    @commands.command()
    async def owner(self, ctx):
        """Shows you the owner of the bot"""
        await ctx.send("♿nizcomix#7532 made me")

    @commands.command()
    async def guide(self, ctx):
        """Shows you how to use the bot"""
        embed = self.bot.embed(title="How to use me")
        at = self.bot.get_command("add_template")
        gt = self.bot.get_command("get_template")
        embed.description = "**How to submit templates**\n"
        embed.description += f"The format for submitting templates is:\n `{ctx.prefix}{at.name} {at.signature}`. Both of these arguments are **required**. (We couldnt fetch your template if you didnt tell us what it was!)\n"
        embed.description += f"\n*While submitting templates, please do...*\n• Be **descriptive!** One word descriptions are discouraged unless it is a very specific thing.\n• Be **original!** Submit your own custom templates that couldnt be found with a quick google search!\n• **Submit the defining words of the template first** - This is mostly because of the way the bot works (see `$algo`) When submitting a template, think about what a normal person would call that template at first glance, or how they would search for that on google. As a rule of thumb, you should put nouns before adjectives or actions. If you were entering a template of a cat with it's arms up, `cat arms up` is considerably better than `arms up cat`, for instance.\n"
        embed.description += f"\n*While submitting templates, please __DO NOT__...*\n• **Submit videos.** Just dont. (gifs are ok)\n• **Submit imgur albums.** They won't process as an embed image. Please get the image url instead.\n• **Submit any NSFW images or descriptions.** Light curses are fine but no pornography or lewd stuff."
        embed.description += f"\n\n**BREAKING ANY OF THESE RULES MAY RESULT IN A WARNING OR BLACKLIST FROM THE BOT DEPENDING ON THE SEVERITY**\n\n"
        embed.add_field(name=f"**How to find a template you need**", value=
        f"The format for getting templates is: `{ctx.prefix}{gt.name} {gt.signature}`. Description is a **required** argument\n\nI am merely a bot, which means I can't read. Therefore, I calculate my matching percentages in a procedural manner, not like a human would (see `$algo`). Because of this, the percentages might sometimes be very off."
        f"\n**HOwever, you can stomp thims!** (sorry, i have a speech impediment.) Simply do not be **too vague** in your descriptions. Being too vague will get you various random results, but maybe not the one you need. However, being to specific might cause you to not get any results. Bottom line, find your balance."
        "\n\nDo `$help` to get to know other commands. If you have any questions, contact ♿nizcomix#7532 or join https://discord.com/invite/2fxKxJH.\nHave fun bb's <:smiley:733042887507443735>")
        embed.set_footer(text='if you\'re reading this you\'re gay')
        await ctx.send(embed=embed)

# https://github.com/niztg/MayMayTemplates

    @commands.command(aliases=["sourcecode", "src", "github"], help="Shows source code for a given command")
    async def source(self, ctx, *, command=None):
        # Lines 55-96 used from niztg's CyberTron5000 GitHub repository provided by the MIT License
        # https://github.com/niztg/CyberTron5000/blob/master/CyberTron5000/cogs/meta.py/#L97-L139
        # Copyright (c) 2020 nizcomix
        if not command:
            embed = self.bot.embed(title="<:star:737736250718421032> Check out the source code on GitHub!", url="https://github.com/niztg/MayMayTemplates")
            embed.description = "Star the GitHub repository to support the bot!"
            embed.add_field(name="<:license:737733205645590639> LICENSE",
                            value=f"GNU AGPL")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_image(
                url='https://media.discordapp.net/attachments/738163422117625876/743146606790049872/Screen_Shot_2020-08-12_at_12.39.08_PM.png')
            return await ctx.send(embed=embed)
        elif command == "help":
            embed = self.bot.embed(title=f"<:star:737736250718421032> Sourcecode for command help/?", url="https://github.com/niztg/MayMayTemplates/blob/master/MayMayTemplates/cogs/help.py/#L8-L77")
            embed.description = "Star the GitHub repository to support the bot!"
            embed.add_field(name="<:license:737733205645590639> LICENSE", value=f"GNU AGPL")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_image(url='https://media.discordapp.net/attachments/738163422117625876/743146606790049872/Screen_Shot_2020-08-12_at_12.39.08_PM.png')
            await ctx.send(embed=embed)
        else:
            cmd = self.bot.get_command(command)
            if not cmd:
                return await ctx.send("Command not found.")
            file = cmd.callback.__code__.co_filename
            location = os.path.relpath(file)
            total, fl = __import__('inspect').getsourcelines(cmd.callback)
            ll = fl + (len(total) - 1)
            url = f"https://github.com/niztg/MayMayTemplates/blob/master/MayMayTemplates/{location}#L{fl}-L{ll}"
            if not cmd.aliases:
                char = '\u200b'
            else:
                char = '/'
            embed = self.bot.embed(title=f"<:star:737736250718421032> Sourcecode for command {cmd.name}{char}{'/'.join(cmd.aliases)}", url=url)
            embed.description = "Star the GitHub repository to support the bot!"
            embed.add_field(name="<:license:737733205645590639> LICENSE",
                            value=f"GNU AGPL")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_image(
                url='https://media.discordapp.net/attachments/738163422117625876/743146606790049872/Screen_Shot_2020-08-12_at_12.39.08_PM.png')
            await ctx.send(embed=embed)

    @commands.command()
    async def support(self, ctx):
        await ctx.send(content='Server: https://discord.com/invite/2fxKxJH\nGithub: https://github.com/niztg/MayMayTemplates\nCyberTron5000: https://cybertron-5k.netlify.app', embed=self.bot.embed(title=f"Support me", description=f"[Git](https://github.com/niztg/cybertron5000)\n[Server](https://cybertron-5k.netlify.app/server)\nCheck out [CyberTron5000](https://cybertron-5k.netlify.app), {self.bot.owner.name}'s **real** bot."))


def setup(bot):
    bot.add_cog(Meta(bot))
