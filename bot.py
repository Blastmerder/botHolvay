import os
import random
from threading import Thread
from asyncio import sleep
import discord
from discord.ext import commands
from discord.utils import get
from dislash import InteractionClient, ActionRow, Button, ButtonStyle, has_permissions
import time
from discord.ext.commands import has_permissions, MissingPermissions
from discord_components import DiscordComponents, Button
from discord_components import DiscordComponents, Button, ButtonStyle
from quests import questses

intents = discord.Intents.default()  # Allow the use of custom intents
intents.members = True

meassage_list = []

globalCtx = ""

token = os.environ['token']
bot = commands.Bot(command_prefix="!", intents=intents)
waitText = False
commandWait = ""
commandAdd = ""

bot.remove_command("help")


@bot.event
async def on_ready():
    print(f'Вы вошли как {bot.user}, ваш id: 937708581753602048')


@bot.command(name="clear", pass_context=True)
@has_permissions(manage_roles=True, ban_members=True)
async def clear(ctx, amount: int = None):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(colour=0xff9900,
                          title=f"Удалено {amount} сообщений") if amount is not None else discord.Embed(colour=0xff9900,
                                                                                                        title=f"Удалены все сообщения")
    await ctx.send(embed=embed, delete_after=2)


@bot.command()
async def quests(ctx, level = 1):

    if isinstance(level, int):
        await ctx.send(f'Неправельный формат Уровня.\nУказаный вами уровень равен {level}')

    quest = questses(level)

    emb = discord.Embed(
        colour=0xFF8C00,

        description=
        f"""
                        {quest["text"]}
                        """
    )

    row = [
        [Button(
            style=ButtonStyle.gray,
            label=f'{quest["B1"]}',
            custom_id='True3' if quest['IsTrue'] == 3 else "False3"
        ),
            Button(
                style=ButtonStyle.gray,
                label=f'{quest["B2"]}',
                custom_id='True2' if quest['IsTrue'] else "False2"
            ),
            Button(
                style=ButtonStyle.gray,
                label=f'{quest["B3"]}',
                custom_id='True1' if quest['IsTrue'] else "False1"
            )]
    ]
    emb.set_author(name='Задачки!')
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=emb, components=row)



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


@bot.event
async def on_message(message):
    text = str(message.content).lower()
    textlist = text.split()
    ltl = len(textlist)
    ctx = discord.utils.get(message.author.guild.text_channels, id=message.channel.id)
    member = message.author

    global globalCtx
    globalCtx = ctx

    global waitText
    if waitText and message.author.id == 776122179486089227:
        if textlist[0] == "!chatMessage" and commandWait == "!chatMessage":
            global commandAdd
            if ltl != 1:
                commandAdd = commandAdd + "\tawait ctx."
            else:
                waitText = False
    elif textlist[0] == "привет" or textlist[0] == "hi" \
            or textlist[0] == "hello":
        if message.author.id != 937708581753602048:
            await ctx.send(textlist[0])
    elif textlist[0] == "инфа":
        FaqBot = open("faq.txt", "r", encoding="UTF-8")
        fb = FaqBot.read()
        await ctx.send(fb)
        FaqBot.close()
    else:
        await bot.process_commands(message)
        await bot.event(message)


@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.event
async def on_member_join(member):
    members = open("members", "a", encoding="UTF-8")
    members.write(f"\n{member}")
    members.close()


@bot.event
async def on_member_leave(member):
    members = str(open("members", "r", encoding="UTF-8")).split("\n")
    newMembers = ""
    for memb in members:
        if memb != member:
            newMembers = f"{newMembers}\n{memb}"
    members = open("members", "w", encoding="UTF-8")
    members.write(newMembers)
    members.close()


@bot.command()
async def survay_you_can(ctx):
    emb = discord.Embed(
        colour=0xFF8C00,

        description=
        f"""
        что ты умеешь?
        """
    )

    row = [
        [Button(
            style=ButtonStyle.gray,
            label='строить',
            custom_id='building'
        ),
            Button(
                style=ButtonStyle.gray,
                label='програмировать командный блоки',
                custom_id='progamicCommandBlock'
            ),
            Button(
                style=ButtonStyle.gray,
                label='рисовать текстуры',
                custom_id='paintTexturs'
            )]
    ]

    emb.set_author(name='Привет, это не большой опрос!')
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=emb, components=row)


@bot.command()
async def survayMe(ctx):
    emb = discord.Embed(
        colour=0xFF8C00,

        description=
        f"""
    Мои создатили **Holvay** и **Blastmerder**
    """
    )

    row = [
        [Button(
            style=ButtonStyle.gray,
            label='классно!',
            custom_id='cool'
        ),
            Button(
                style=ButtonStyle.gray,
                label='норм',
                custom_id='normal'
            ),
            Button(
                style=ButtonStyle.gray,
                label='плохо!',
                custom_id='bad'
            )]
    ]

    emb.set_author(name=f'КАК ВАМ МОЯ РАБОТА❔')
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=emb, components=row)


@bot.event
async def on_button_click(inter):
    guild = bot.get_guild(inter.guild.id)
    message = inter.message
    ctx = discord.utils.get(message.author.guild.text_channels, id=message.channel.id)
    member = inter.author

    if inter.component.id == "cool":
        await inter.send(f"Спасибо за поддержку {member.name}!", delete_after=2)
    elif inter.component.id == "normal":
        await inter.send(f"Что {member.name} не понравилось?", delete_after=2)
    elif inter.component.id == "bad":
        await inter.send(f"Я чем то вам {member.name} не угодил?\n"
                         "Я буду стараться быть лучше,\n"
                         "но только скажите что именно вам не понравилось.", delete_after=2)
    elif inter.component.id == "True1" or inter.component.id == "True2" or inter.component.id == "True3":
        await inter.send(f"Воу а вы {inter.author.name} математик!", delete_after=2)
        msg = await message.channel.fetch_message(message.id)
        await msg.delete()
    elif inter.component.id == "False1" or inter.component.id == "False2" or inter.component.id == "False3":
        msg = await message.channel.fetch_message(message.id)
        await msg.delete()
        await inter.send(f"Неа! 😂", delete_after=2)
    elif inter.component.id == "building":
        building = guild.get_role(949308605100884018)
        await member.add_roles(building)
        await inter.send(f"Вы были добавлены в строители.\nУдачного вам дня {member.name}!")
    elif inter.component.id == "progamicCommandBlock":
        commandBlock = guild.get_role(949308709522268161)
        await member.add_roles(commandBlock)
        await inter.send(f"Вы были добавлены в Кбешеры.\nУдачного вам дня {member.name}!")
    elif inter.component.id == "paintTexturs":
        commandBlock = guild.get_role(949308780057874502)
        await member.add_roles(commandBlock)
        await inter.send(f"Вы были добавлены в ресурспакеры.\nУдачного вам дня {member.name}!")


@bot.command()
async def faq(ctx):
    await ctx.channel.purge(limit=1)
    FaqBot = open("faq.txt", "r", encoding="UTF-8")
    fb = FaqBot.read()
    await ctx.send(fb)
    FaqBot.close()


@bot.command()
async def send_hi(ctx, member: discord.Member):
    """id = random.randint(1, 6)
    photoid = f"photo{id}.jpg" if id != 2 and id != 3 else f"photo{id}.gif"""
    """FaqBot = open(f"photo2.gif", "r", encoding="UTF-8")
    fb = FaqBot.read()"""
    await member.send("привет", file=discord.File("photo2.gif"))


@bot.command()
async def Help(ctx):
    await ctx.channel.purge(limit=1)
    FaqBot = open("helpCommand.txt", "r", encoding="UTF-8")
    fb = FaqBot.read()
    await ctx.send(fb)


@bot.command()
async def sphere(ctx, text=None):
    if text is None:
        await ctx.send(f"не достаточно данных")
    else:
        vc = open("varebleConten", "r", encoding="UTF-8")
        facts = vc.read().split("\n")

        colour = open("colour.txt", "r", encoding="UTF-8")
        colours = colour.read().split("\n")

        emb = discord.Embed(
            colour=0xFF9C11
        )

        emb.set_author(name=f"{facts[random.randint(0, 7)]}")

        await ctx.send(embed=emb)
        vc.close()


def schedule_checker():
    while True:
        time.sleep(30)
        print("time proccesing")


Thread(target=schedule_checker).start()
bot.run(token)