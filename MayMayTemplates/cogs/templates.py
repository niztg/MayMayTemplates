import random
import re
from typing import Union

import discord
from discord.ext import commands

from MayMayTemplates.utils.menu import IndexedListSource, MayMayMenu


async def fetch_appropriate_user(user_id: int, bot: commands.Bot):
    return bot.get_user(user_id) or await bot.fetch_user(user_id)


class MayMayMaker(commands.Converter):
    async def convert(self, ctx, argument):
        if not argument.isdigit() or not (await fetch_appropriate_user(int(argument), ctx.bot)):
            raise commands.BadArgument('That is not a valid user!')
        return await fetch_appropriate_user(int(argument), ctx.bot)


class Templates(commands.Cog):
    """Templates commands"""

    def __init__(self, bot):
        self.bot = bot
        self.db_table = "templates"

    async def templates_dict(self, values: bool = False):
        data = await self.bot.db.fetch("SELECT user_id, array_agg(template_url) FROM %s GROUP BY user_id" % self.db_table)
        if not values:
            return {int(key): len(value) for key, value in dict(data).items()}
        if values:
            return {int(key): value for key, value in dict(data).items()}

    async def fetch_template(self, query: str):
        data = await self.bot.db.fetch("SELECT * FROM %s" % self.db_table)
        query1 = self.compress_string(query)
        templates = []
        for item in data:
            percent = 0
            query2 = self.compress_string(str(item['query']))
            for _1, _2 in zip(query1, query2):
                if _1 == _2:
                    percent += 1
            if (total := round(percent / len(query) * 100, 3)) > 50:
                templates.append({'query': str(item['query']), 'percent': total, 'author': int(item['user_id']),
                                  'template': item['template_url']})
        return templates

    async def get_desc_by_url(self, url):
        return (await self.bot.db.fetch("SELECT query FROM %s WHERE template_url = $1" % self.db_table, url))[0][0]

    async def get_user_by_url(self, url):
        return int((await self.bot.db.fetch("SELECT user_id FROM %s WHERE template_url = $1" % self.db_table, url))[0][0])

    def validate_url(self, image_url):
        # NOTE: i did not write this regex
        # stole it from stack o.
        regex = re.compile(
            r"^(?:http|ftp)s?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$", re.IGNORECASE)
        if not re.match(regex, image_url) is not None:
            return False
        else:
            if not any(a in image_url for a in ['.png', '.jpg', '.jpeg', '.webp', '.gif']):
                return False
        return True

    def compress_string(self, string: str):
        for x in string:
            if x in ("'", '.', '!', '"', ',', '-', '?'):
                string = string.replace(x, '')
        return string.strip().lower().replace(' ', '')

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx):
        """Shows you the template leaderboard"""
        async with ctx.typing():
            templates_dict = await self.templates_dict()
            templates_dict = sorted(templates_dict.items(), key=lambda x: x[1], reverse=True)
            try:
                my_rank = [a[0] for a in templates_dict].index(ctx.author.id) + 1
            except ValueError:
                my_rank = "You are not ranked!"
            format = [f'{await fetch_appropriate_user(item[0], self.bot)} - {item[1]} templates' for item in
                      templates_dict]
        source = IndexedListSource(data=format, embed=self.bot.embed(title="Meme Leaderboard",
                                                                     description=f"Your rank: **{my_rank}**"))
        await MayMayMenu(source=source).start(ctx)

    @commands.command(aliases=['stats'])
    async def statistics(self, ctx, user: Union[MayMayMaker, discord.Member] = None):
        """Shows you how many templates you have submitted"""
        user = user or ctx.author
        user_id = str(user.id)
        resp = await self.bot.db.fetch("SELECT * FROM %s WHERE user_id = $1" % self.db_table, user_id)
        await ctx.send(embed=self.bot.embed(description=f"**{str(user.name)}** has submitted `{len(resp)}` templates."))

    @commands.command()
    async def total(self, ctx):
        """The total amount of templates in the database."""
        data = await self.templates_dict()
        await ctx.send(embed=self.bot.embed(
            description=f"*I found `{sum(data.values())}` templates contributed by `{len(data)}` users!*"))

    @commands.command(aliases=['gt'])
    async def get_template(self, ctx, *, query):
        """Get a specified template from the Database"""
        async with ctx.typing():
            data = await self.fetch_template(query)
            embed = self.bot.embed(title=f"Results ({len(data)})",
                                   description="Here are the results which matched your query.")
            data = sorted(data, key=lambda x: x['percent'], reverse=True)
            for x in data:
                try:
                    embed.add_field(
                        name=f"Result #{data.index(x)+1}:\n> {x.get('query')}\n{(await fetch_appropriate_user(x.get('author'), self.bot))}\n`{x.get('percent')}%`",
                        value=f"[Click Here]({x.get('template')})")
                except Exception:
                    break
        await ctx.send(embed=embed)

    @commands.command(aliases=['at', 'add-template', 'add-temp', 'add-format', 'submit', 'add'])
    async def add_template(self, ctx, image_url, *, description):
        """Adds a template to the db"""
        if await self.bot.db.fetch("SELECT template_url FROM %s where query = $1" % self.db_table, description):
            return await ctx.send("A template with that exact description already exists! Try changing it up a bit.")
        if not self.validate_url(image_url):
            raise commands.BadArgument('That is not a valid image url!')
        await self.bot.db.execute("INSERT INTO %s (template_url, user_id, query) VALUES ($1, $2, $3)" % self.db_table, image_url, str(ctx.author.id), description)
        await ctx.send("MEME DATABSE HAS BEEN UPDATED")

    @commands.command(aliases=['aa', 'adda'])
    async def add_attachment(self, ctx, *, description):
        """Adds an attachment to the db"""
        if not ctx.message.attachments:
            return await ctx.send(f"You didnt add any images!")
        if await self.bot.db.fetch("SELECT template_url FROM templates where query = $1", description):
            return await ctx.send("There is already a template with this exact query!")
        for attachment in ctx.message.attachments:
            await self.bot.db.execute(
                "INSERT INTO %s (template_url, user_id, query) VALUES ($1, $2, $3)" % self.db_table, str(attachment.url),
                str(ctx.author.id), description)
        await ctx.send("MEME DATABSE HAS BEEN UPDATED")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, *, template):
        """Delete a template from the DB"""
        await self.bot.db.execute("DELETE FROM %s WHERE query = $1" % self.db_table, template)
        await ctx.send("Done")

    @commands.command(aliases=['tf'])
    async def template_from(self, ctx, user: Union[MayMayMaker, discord.Member] = None):
        """Shows you a random template from a specific user"""
        user = user or ctx.author
        data = await self.templates_dict(values=True)
        if not (urls := data.get(user.id)):
            return await ctx.send("That user has not submitted any templates :(")
        random.shuffle(urls)
        url = random.choice(urls)
        count = 0
        while self.validate_url(url) is False:
            url = random.choice(urls)
            count += 1
            if count == 15:
                return await ctx.send("This user doesnt have any valid url templates :(")
        embed = self.bot.embed(title=f'Random Template from {user}', url=url)
        embed.description = await self.get_desc_by_url(url)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['r', 'rand'])
    async def random_template(self, ctx):
        """Gives you a random template."""
        templates = []
        for item in (await self.templates_dict(values=True)).values():
            templates += item
        random.shuffle(templates)
        template = random.choice(templates)
        counter = 0
        while self.validate_url(template) is False:
            template = random.choice(templates)
            counter += 1
            if counter == 30:
                return await ctx.send("An error occured. Try again.")
        author = await self.get_user_by_url(template)
        author = await fetch_appropriate_user(author, self.bot)
        description = await self.get_desc_by_url(template)
        embed = self.bot.embed(title='Random Template', description=f'{description}\nBy {author}', url=template)
        embed.set_image(url=template)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Templates(bot))