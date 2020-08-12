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

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# I didn't know SQL when I created this table.
# So I stored user_id's as strings instead of bigints.
# Forgive me.

import os
import random
import platform

import discord
from asyncpg import create_pool
from discord.ext import commands, tasks

from MayMayTemplates import config
from MayMayTemplates.utils.embed import MayMayEmbed


class MayMayTemplates(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=self.get_prefix, description=f"The #1 Meme Template Bot")
        self.db = self.loop.run_until_complete(self.create_db_pool())
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

    async def get_prefix(self, message):
        return commands.when_mentioned_or('mh', '$')(self, message)

    @tasks.loop(minutes=2)
    async def presence(self):
        return await self.change_presence(activity=discord.Game(f"blees's mom's weight: {random.randint(12313414, 120937891)}"))

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
        await self.change_presence(
            activity=discord.Game(f"blees's mom's weight: {random.randint(12313414, 120937891)}"))
        print(f"COGS LOADED")


MayMayTemplates().run()
