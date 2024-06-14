import os, discord, time, datetime, colorama, random, requests, discord.interactions, asyncio, func.quotes.quote as qut, pickledb, func.fun.money as money
from dotenv import load_dotenv; from threading import Thread; from threading import Thread; from discord.ext import commands; from discord import app_commands

from func.dawum_mrs.get_msg_content import *
from func.apis.apis import *
import func.error.catch as error

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
INVITE = os.getenv('DISCORD_INVITE')

client = commands.Bot(intents=discord.Intents.all(), command_prefix="$")
total_messages_read = 0
db = []


def check_online(client):
    while True:
        currentDateAndTime = datetime.datetime.now()
        currentTime = currentDateAndTime.strftime("%H\\%M\\%S")
        print(colorama.Fore.LIGHTGREEN_EX + f"{client} IS STILL ONLINE " + colorama.Fore.BLACK + colorama.Back.WHITE + f"{currentTime}" + colorama.Style.RESET_ALL)
        time.sleep(300)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    def total_messages():
        global total_messages_read
        total_messages_read = total_messages_read + 1
    
    total_messages()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    checking_thread = Thread(target=check_online, args=(client.user,))
    checking_thread.start()

    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        error.catch_error(e)



@client.hybrid_command(description="Displays the results of the most recent political surveys in Germany.")
async def mrs(ctx: commands.Context):
    get_current_json()
    with open("cache/message.bot", "r", encoding="UTF-8") as msg:
        msg_content = msg.read()
    
    embed = discord.Embed(title="NEUSTE WAHLERGEBNISSE", description=msg_content, color=255)
    await ctx.send(embed=embed)

    try:
        file_path = "cache\\message.bot"
        os.remove(file_path)
    except Exception as e:
        error.catch_error(e)


@client.hybrid_command(description="Shows all of the websites from the OHN-Staff!")
async def ohn(ctx: commands.Context):
    ohn_association = ["DNA", "Flörian", "Fabix", "Nightwolf", "Matxilla"]
    ohn_websites = ["www.dnascanner.de", "flo.ohhellnaw.de", "bagelxd.de", "nightwolf.ohhellnaw.de", "mat.ohhellnaw.de"]

    msg_content = f""
    for i in range(len(ohn_websites)):
        msg_content += f"\n### {i+1}: [{ohn_association[i]}'s Website](https://{ohn_websites[i]})"
        if ohn_association[i] == "Flörian":
            msg_content += f" *(The creator of this bot hehe :>)*\n"

    embed = discord.Embed(title="All OhHellNaw Websites", description=msg_content, color=255)
    await ctx.send(embed=embed)


@client.hybrid_command(description="A invite link to invite this bot into other Servers aswell!")
async def invite(ctx: commands.Context):
    embed = discord.Embed(title="Invite", description=f"Use this invite link to invite the Bot to other servers!\n[Click here!]({INVITE})", color=255)
    await ctx.send(embed=embed)


@client.hybrid_command(description="Tells you if a person is a femboy")
@app_commands.describe(person="Which person do you want to choose?")
async def femboy(ctx: commands.Context, person: discord.Member):
    try:
        await ctx.send(f"{person.mention} is {random.randint(0,100)}% femboy.", silent=True)
    except Exception as e:
        error.catch_error(e)


@client.hybrid_command(description="Ships two people")
@app_commands.describe(person="Select the first person", person2="Select the second person")
async def ship(ctx: commands.Context, person: discord.Member, person2: discord.Member):
    try:
        await ctx.send(f"{person.mention} is {random.randint(0,100)}% in love with {person2.mention}! <3", silent=True)
    except Exception as e:
        error.catch_error(e)


@client.hybrid_command(description="Reveals how many messages the Bot has read so far...")
async def messages(ctx: commands.Context):
    await ctx.send(f"I've read {total_messages_read:,} messages since the last time I have restarted!")


@client.hybrid_command(description="Tells you a random german joke!")
async def joke(ctx: commands.Context):
    filename = witzede()
    with open(filename, "r", encoding="UTF-8") as f:
        content = f.read()

    embed = discord.Embed(title="Witz", description=content, color=255)
    embed.set_footer(text=f"Witze von: https://witzapi.de/")
    await ctx.send(embed=embed)


@client.hybrid_command(description="Sends a random meme into the chat!")
async def meme(ctx: commands.Context):
    asyncio.sleep(5)
    filename = memeapi()
    with open(filename, "r", encoding="UTF-8") as f:
        content = f.read()
    
    await ctx.send(f"{content}")


@client.hybrid_command(description="Rock, Paper, Scissors.")
@app_commands.describe(option="Choose Wisely...")
async def rps(ctx: commands.Context, option: str):
    options = ["rock", "paper", "scissors"]

    if option.lower() in options:
        bot_choice = random.choice(options)
        await ctx.send(f"I chose **{bot_choice.upper()}** and you chose **{option}**!")
    else:
        await ctx.send(f"{option} is not an available choice! Remember: Rock, Paper or Scissors! >:(")


@client.hybrid_command(description="Shows you a random quote from OHN")
async def quote(ctx: commands.Context):
    quote = qut.get_quote()
    await ctx.send(quote)


@client.hybrid_command(description="Do very bad things for money!", name="earnmoney")
async def earn_money(ctx: commands.Context):
    button = discord.ui.Button(label="Steal from someone in the Server!", style=discord.ButtonStyle.danger) # adds button(s)
    button2 = discord.ui.Button(label="Break into a house!", style=discord.ButtonStyle.blurple) 

    def update_db(user, value):
        if user in db:
            index = db.index(user)
            value_index = index+1
            db[value_index] = db[value_index] + value
        else:
            db.append(user)
            db.append(value)

    async def steal_from_user(interaction):
        users = []
        for member in ctx.guild.members:
            users.append(member)
        
        while True:
            rdm_user = random.choice(users)
            if rdm_user == ctx.author:
                random.choice(users)
            else:
                break
        content, money_change = money.steal_from_user(ctx.author, rdm_user)
        await interaction.response.send_message(content)
        
    
    async def break_into_house(interaction):
        content, money_change = money.break_into_house(ctx.author)
        await interaction.response.send_message(content)
        update_db(ctx.author, money_change)
    
    button.callback = steal_from_user
    button2.callback = break_into_house

    view = discord.ui.View() # constructs view
    view.add_item(button)
    view.add_item(button2)

    await ctx.send("Choose one of the options below to earn some money! >:)", view=view)
    await client.wait_for("button_click")


@client.hybrid_command(description="See how much money you have :)")
async def mymoney(ctx: commands.Context, person: discord.Member):
    if person in db:
        index = db.index(person)
        value_index = index+1
        embed = discord.Embed(title="Your money!", description=f"{person.mention} currently has **{db[value_index]}€**!", color=255)
        await ctx.send(embed=embed, silent=True)
    else:
        embed = discord.Embed(title="User not found!", description=f"{person} was not found in our Database!", color=255)
        await ctx.send(embed=embed, silent=True)

@client.event
async def on_guild_join(guild):
    import colorama
    print(colorama.Fore.GREEN + f"{client.user} has joined {guild.name} successfully." + colorama.Style.RESET_ALL)
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(title="Thank you!", description="Thanks for inviting me to your server!\nTo view all commands try using '**$Help**'!", color=255)
            await channel.send(embed=embed)
            break

client.run(TOKEN)