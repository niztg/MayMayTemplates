import discord
from discord.ext import menus


class MayMayMenu(menus.MenuPages, inherit_buttons=False):
    """
    Code used from Rapptz' discord-ext-menus GitHub repository
    Provided by the MIT License
    https://github.com/Rapptz/discord-ext-menus
    Copyright (c) 2015-2020 Danny Y. (Rapptz)
    """
    @menus.button('\U000023ee', position=menus.First(0))
    async def go_to_first_page(self, payload):
        """go to the first page"""
        await self.show_page(0)

    @menus.button('\U000025c0', position=menus.Position(0))
    async def go_to_previous_page(self, payload):
        """go to the previous page"""
        await self.show_checked_page(self.current_page - 1)

    @menus.button('\U000023f9', position=menus.Position(3))
    async def stop_pages(self, payload):
        """stops the pagination session."""
        self.stop()
        await self.message.delete()

    @menus.button('\U000025b6', position=menus.Position(5))
    async def go_to_next_page(self, payload):
        """go to the next page"""
        await self.show_checked_page(self.current_page + 1)

    @menus.button('\U000023ed', position=menus.Position(6))
    async def go_to_last_page(self, payload):
        await self.show_page(self._source.get_max_pages() - 1)

    @menus.button('\U0001f522', position=menus.Position(4))
    async def _1234(self, payload):
        i = await self.ctx.send("What page would you like to go to?")
        msg = await self.ctx.bot.wait_for('message', check=lambda m: m.author == self.ctx.author)
        page = 0
        try:
            page += int(msg.content)
        except ValueError:
            return await self.ctx.send(
                f"**{self.ctx.author.name}**, **{msg.content}** could not be turned into an integer! Please try again!",
                delete_after=3)

        if page > (self._source.get_max_pages()):
            await self.ctx.send(f"There are only **{self._source.get_max_pages()}** pages!", delete_after=3)
        elif page < 1:
            await self.ctx.send(f"There is no **{page}th** page!", delete_after=3)
        else:
            index = page - 1
            await self.show_checked_page(index)
            await i.edit(content=f"Transported to page **{page}**!", delete_after=3)


class IndexedListSource(menus.ListPageSource):
    def __init__(self, data: list, embed: discord.Embed, per_page: int = 10):
        super().__init__(per_page=per_page, entries=data)
        self.embed = embed

    async def format_page(self, menu, entries: list):
        offset = menu.current_page * self.per_page + 1
        embed = self.embed
        if not embed.fields:
            if not entries:
                embed.add_field(name='Entries', value='No Entries')
                index = 0
            else:
                embed.add_field(name='Entries',
                                value='\n'.join(f'`[{i:,}]` {v}' for i, v in enumerate(entries, start=offset)),
                                inline=False)
                index = 0
        else:
            index = len(embed.fields) - 1
        embed.set_footer(text=f'({menu.current_page + 1}/{menu._source.get_max_pages()})')
        if not entries:
            embed.set_field_at(index=index, name='Entries',
                               value='No Entries')
        else:
            embed.set_field_at(index=index, name='Entries',
                               value='\n'.join(f'`[{i:,}]` {v}' for i, v in enumerate(entries, start=offset)))
        return embed
