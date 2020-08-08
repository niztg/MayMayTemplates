import discord


class MayMayEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colour = kwargs.get('color') or kwargs.get('colour') or 0x299ffa
        self.set_footer(text=f"Developped by ♿nizcomix#7532")
