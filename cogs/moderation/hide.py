import discord
from discord.ext import commands
from discord import ui

class HideUnhideView(ui.View):
    def __init__(self, channel, author, ctx):
        super().__init__(timeout=120)
        self.channel = channel
        self.author = author
        self.ctx = ctx 
        self.message = None  

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message("You are not allowed to interact with this!", ephemeral=True)
            return False
        return True

    async def on_timeout(self):
        for item in self.children:
            if item.label != "Delete":
                item.disabled = True
        if self.message:
            try:
                await self.message.edit(view=self)
            except Exception:
                pass

    @ui.button(label="Unhide", style=discord.ButtonStyle.success)
    async def unhide(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.channel.set_permissions(interaction.guild.default_role, read_messages=True)
        await interaction.response.send_message(f"{self.channel.mention} has been unhidden.", ephemeral=True)

        embed = discord.Embed(
            description=f"<:RomelChannel:1297340969137471650> **Channel**: {self.channel.mention}\n<:RomelReason:1295595129809141812> **Status**: Unhidden\n<:RomelArrow:1297341001341599797> **Reason:** Unhide request by {self.author}",
            color=0x000000
        )
        embed.add_field(name="<:Romel_staff:1228227884481515613> **Moderator:**", value=self.ctx.author.mention, inline=False)
        embed.set_author(name=f"Successfully Unhidden {self.channel.name}", icon_url="https://cdn.discordapp.com/emojis/1222750301233090600.png")
        await self.message.edit(embed=embed, view=self)

        for item in self.children:
            if item.label != "Delete":
                item.disabled = True
        await self.message.edit(view=self)

    @ui.button(style=discord.ButtonStyle.gray, emoji="<:Romel_bin:1254336650075701308>")
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()


class Hide(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(0, 0, 0)

    @commands.hybrid_command(
        name="hide",
        help="Hides a channel from the default role (@everyone).",
        usage="hide <channel>",
        aliases=["hidechannel"])
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def hide_command(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel 
        if not channel.permissions_for(ctx.guild.default_role).read_messages:
            embed = discord.Embed(
                description=f"**<:RomelChannel:1297340969137471650> Channel**: {channel.mention}\n<:RomelReason:1295595129809141812> **Status**: Already Hidden",
                color=self.color
            )
            embed.set_author(name=f"{channel.name} is Already Hidden", icon_url="https://cdn.discordapp.com/emojis/1294218790082711553.png")
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            view = HideUnhideView(channel=channel, author=ctx.author, ctx=ctx) 
            message = await ctx.send(embed=embed, view=view)
            view.message = message
            return

        await channel.set_permissions(ctx.guild.default_role, read_messages=False)

        embed = discord.Embed(
            description=f"<:RomelChannel:1297340969137471650> **Channel**: {channel.mention}\n<:RomelReason:1295595129809141812> **Status**: Hidden\n<:RomelArrow:1297341001341599797> **Reason:** Hide request by {ctx.author}",
            color=self.color
        )
        embed.add_field(name="<:Romel_staff:1228227884481515613> **Moderator:**", value=ctx.author.mention, inline=False)
        embed.set_author(name=f"Successfully Hidden {channel.name}", icon_url="https://cdn.discordapp.com/emojis/1222750301233090600.png")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        view = HideUnhideView(channel=channel, author=ctx.author, ctx=ctx) 
        message = await ctx.send(embed=embed, view=view)
        view.message = message


"""
@Author: Sonu Jana
    + Discord: me.sonu
    + Community: https://discord.gg/odx (Romel Development)
    + for any queries reach out Community or DM me.
"""