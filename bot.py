import time

from imports import *

intents = discord.Intents.default()  # Allow the use of custom intents
intents.members = True

meassage_list = []

globalCtx = ""

token = os.environ['token']
bot = commands.Bot(command_prefix="!", intents=intents)
waitText = False
commandWait = ""
commandAdd = ""

buttons = ButtonsClient(bot)

bot.remove_command("help")


@bot.event
async def on_ready():
    print(f'Вы вошли как {bot.user}, ваш id: 937708581753602048')


@bot.command()
async def test_button(ctx):
    await buttons.send(
        content="It's test",
        channel=ctx.channel.id,
        components=[
            ActionRow(
                Button(
                    label="1",
                    style=ButtonType().Primary,
                    custom_id="one"
                )
            )
        ]
    )


@buttons.click
async def one(ctx):
    print("WORK")
    await ctx.reply("Hello")


@bot.command(name="clear", pass_context=True)
@has_permissions(manage_roles=True, ban_members=True)
async def clear(ctx, amount: int = None):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(colour=0xff9900,
                          title=f"Удалено {amount} сообщений") if amount is not None else discord.Embed(colour=0xff9900,
                                                                                                        title=f"Удалены все сообщения")
    await ctx.send(embed=embed, delete_after=2)


@bot.command()
async def quests(ctx, level=1):
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
async def on_member_join(member):
    id = random.randint(1, 6)
    photoid = f"photo/photo{id}.jpg" if id != 2 and id != 3 else f"photo/photo{id}.gif"
    await member.send(
        f'привет, я приветствую тебя на сервере "Канал Холви"\nМеня создал blastmerder.\nЯ до сих пор программируемый проект\nУдачи тебе освоится {member.name}!',
        file=discord.File(f"{photoid}"))


@bot.event
async def on_member_leave(member):
    await member.send(
        f'Приятно было познокомится с табой, {member.name}.')


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


@bot.command()
async def faq(ctx):
    await ctx.channel.purge(limit=1)
    FaqBot = open("txt files/faq.txt", "r", encoding="UTF-8")
    fb = FaqBot.read()
    await ctx.send(fb)
    FaqBot.close()


@bot.command()
@commands.has_permissions(administrator=True)
async def send_hi(ctx, member: discord.Member):
    id = random.randint(1, 6)
    photoid = f"photo/photo{id}.jpg" if id != 2 and id != 3 else f"photo/photo{id}.gif"
    try:
        await member.send("привет", file=discord.File(f"{photoid}"))
        await ctx.send(f"успешно было прислано приветствие пользователю {member.name}")
    except:
        await ctx.send(f"не удалось прислать приветствие пользователю {member.name}")


@bot.command()
@commands.has_permissions(administrator=True)
async def send(ctx, member: discord.Member, message):
    try:
        await member.send(f"{message}")
        await ctx.send(f"успешно было прислано сообщение пользователю {member.name}")
    except:
        await ctx.send(f"не удалось прислать сообщение пользователю {member}")


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, time_mute=1, model_time_mute="s", reason="Без причины"):
    if time_mute == 1:
        time_mute_text = Translation_singular[model_time_mute]
    else:
        time_mute_text = f"{time_mute} {Translation_plural[model_time_mute]}"
    try:
        emb = discord.Embed(
            colour=0xFF8C00,

            description=
            f"""
                Пользователь {member.name} был замутен на {time_mute_text},
                Пользователем {ctx.message.autor.name}.
                По причине: {reason}
                """
        )
        emb.set_author(name=f'{ctx.message.autor.name}')
        guild = bot.get_guild(ctx.guild.id)
        mute_role = guild.get_role(958658798388662352)
        await member.add_roles(mute_role)
        await ctx.send(embed=emb)
        time.sleep(time_mute * time_multiplier[model_time_mute])
        await member.remove_roles(mute_role)
    except:
        emb = discord.Embed(
            colour=0xFF8C00,

            description=
            f"""
                        Не удолось замутить пользователя {member.name}
                        """
        )
        emb.set_author(name=f'Что-то пошло не так (')
        await ctx.send(embed=emb)


@bot.command()
@commands.has_permissions(administrator=True)
async def send(ctx, member: discord.Member, message=None):
    try:
        if message is None:
            await ctx.send(f"не указанно сообщение")
        else:
            await member.send(f"{message}")
            await ctx.send(f"успешно было прислано приветствие пользователю {member.name}")
    except:
        await ctx.send(f"не удалось прислать приветствие пользователю {member.name}")


@bot.command()
async def Help(ctx):
    await ctx.channel.purge(limit=1)
    FaqBot = open("txt files/helpCommand.txt", "r", encoding="UTF-8")
    fb = FaqBot.read()
    await ctx.send(fb)


@bot.command()
async def sphere(ctx, text=None):
    if text is None:
        await ctx.send(f"не достаточно данных")
    else:
        vc = open("txt files/varebleConten", "r", encoding="UTF-8")
        facts = vc.read().split("\n")

        colour = open("txt files/colour.txt", "r", encoding="UTF-8")
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


@bot.event
async def on_button_click(inter):
    print("событие\n", inter)
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


Thread(target=schedule_checker).start()
bot.run(token)
