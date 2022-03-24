import random
import discord
from discord.ext import commands
from discord.utils import get
from dislash import InteractionClient, ActionRow, Button, ButtonStyle, has_permissions
import time
from discord.ext.commands import has_permissions, MissingPermissions
from discord_components import DiscordComponents, Button
from discord_components import DiscordComponents, Button, ButtonStyle
import discord
from discord.ext import commands
from discord.utils import get

token = "OTQ5MjMyNzQ1NzUyNjk4OTEw.YiHX4g.cZS_ZB0cC1CX5FwgUKZs35lHV4w"
bot = commands.Bot(command_prefix="!")


Gguild = ""


@bot.command()
async def members(ctx):
    for guild in ctx.g:
        for member in guild.members:
            await ctx.send(member)


@bot.event
async def on_button_click(inter):
    guild = bot.get_guild(inter.guild)
    message = inter.message
    ctx = discord.utils.get(message.author.guild.text_channels, id=message.channel.id)
    member = inter.author


@bot.command()
async def MyChatCreate(ctx, name=None, *members: discord.Member):
    guild = ctx.guild
    member = ctx.author
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        member: discord.PermissionOverwrite(read_messages=True)
    }

    for memb in members:
        overwrites[memb] = discord.PermissionOverwrite(read_messages=True)

    try:
        mod_logs = await guild.create_text_channel(name=name, overwrites=overwrites)
    except:
        print("couldn't create a mod-logs channel, maybe it exists, or the bot/user doesn't have permissions")

