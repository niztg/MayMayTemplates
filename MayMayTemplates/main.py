"""
MIT License

Copyright (c) 2020 nizcomix

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# I didn't know SQL when I created this table.
# So I stored user_id's as strings instead of bigints.
# Forgive me.

import os
import platform

import discord
from asyncpg import create_pool
from discord.ext import commands

from MayMayTemplates import config
from MayMayTemplates.utils.embed import MayMayEmbed


class MayMayTemplates(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=['$', 'mh'], activity=discord.Game('mhhelp or $help'), description=f"The #1 Meme Template Bot")
        self.db = self.loop.run_until_complete(self.create_db_pool())
        self.table = "templates"
        self.loop.create_task(self.ready())
        self.embed = MayMayEmbed
        self.config = {"owner": 350349365937700864}
        self.ext = [ext[:-3] for ext in os.listdir('cogs') if ext.endswith('.py')]
        self.load_extension('jishaku')

    @property
    def owner(self):
        return self.get_user(self.config['owner'])

    async def create_db_pool(self):
        return await create_pool(database=config.DATABASE, user=config.USER, password=config.PASSWORD, port=config.PORT)

    def run(self, *args, **kwargs):
        super().run(config.TOKEN)

    async def ready(self):
        await self.wait_until_ready()
        print(f"LOGGED IN AS: {self.user.name}")
        print(f"DISCRIMINATOR: {self.user.discriminator}")
        print(f"ID: {self.user.id}")
        print(f"DISCORD.py VERSION: {discord.__version__}")
        print(f"PYTHON VERSION: {platform.python_version()}")
        for f in self.ext:
            try:
                self.load_extension(f'cogs.{f}')
            except Exception as error:
                print(f'Could not load {f}: {error}')
        print(f"COGS LOADED")


MayMayTemplates().run()
