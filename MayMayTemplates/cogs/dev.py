import discord
from discord.ext import commands


class Developer(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.tick = "☑️"

    async def cog_check(self, ctx):
        return ctx.author.id == 350349365937700864

    @commands.command(help="Reloads Cogs", aliases=['rl'])
    async def reload(self, ctx, *extension):
        if not extension:
            for file in self.bot.ext:
                try:
                    self.bot.reload_extension(f"cogs.{file}")
                except commands.ExtensionNotLoaded:
                    self.bot.load_extension(file)
            await ctx.message.add_reaction(emoji="☑️")

        else:
            cogs = [c for c in self.bot.ext]
            for x in cogs:
                if x in extension:
                    try:
                        self.bot.load_extension(f"cogs.{x}")
                    except Exception as error:
                        print(error)
            await ctx.message.add_reaction(emoji="☑️")

    @commands.command(help="Logs MayMayTemplates out.")
    async def logout(self, ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{self.bot.user.name} logging out. Goodbye World! 🌍",
                                color=self.bot.colour))
        await self.bot.logout()

    @commands.command()
    async def nickname(self, ctx, *, name=None):
        if not name:
            await ctx.guild.me.edit(nick=self.bot.user.name)
        else:
            await ctx.guild.me.edit(nick=f"{name} [{ctx.prefix}]")


def setup(client):
    client.add_cog(Developer(client))