import os, discord, time, datetime, colorama, random, requests, discord.interactions, asyncio, func.quotes.quote as qut, func.fun.money as money
from dotenv import load_dotenv; from threading import Thread; from threading import Thread; from discord.ext import commands; from discord import app_commands

from func.dawum_mrs.get_msg_content import *
from func.apis.apis import *
import func.error.catch as error
from func.db.mongodb import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
INVITE = os.getenv('DISCORD_INVITE')

client = commands.Bot(intents=discord.Intents.all(), command_prefix="$") # creates client
total_messages_read = 0


def check_online(client):
    while True:
        """
        this little guy just refreshes every 5 Minutes to give me 
        an update whether or not the bot is still active or not
        """
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


def update_db(user, value):
    update_database(user, value) # updates database with user's name and the cash they received/lost
    with open(f"log NEW.txt", "a", encoding="UTF-8") as f:
        f.write(f"{user} change in money:       {value}\n")


@client.hybrid_command(description="Displays the results of the most recent political surveys in Germany.")
async def mrs(ctx: commands.Context):
    """
    
    I know this might not be the best solution to getting all the content for the message
    but its much more consistant than creating a file and then reading from it because
    1. it's faster and 2. I don't have inconsistancies with the path of the file
    for example, on my Raspberry PI, creating the file, reading from it and then deleting it
    after using it just does not work for some reason ._.

    """

    data = get_current_json()
    MRS = most_recent_survey(data)
    date, surveyed_people, parliament_name, institute_name, abbreviations, percentages, parties, parliament_ID, institute_ID = get_values(MRS, data)
    content = full_message(data, date, surveyed_people, parliament_name, institute_name, abbreviations, percentages, parties, parliament_ID, institute_ID)

    embed = discord.Embed(title="NEUSTE WAHLERGEBNISSE", description=content, color=255)
    await ctx.send(embed=embed)


@client.hybrid_command(description="Shows all of the websites from the OHN-Staff!")
async def ohn(ctx: commands.Context):
    """
    shows all the websites from the OHN Staff
    The Website's owners and URLs are saved in lists
    and then later inserted into the messages content
    """

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
    """
    This requests a random joke from the witzede API
    The witzede() function returns the joke as a string
    which then can be used in the embed.
    """
    joke = witzede()
    embed = discord.Embed(title="Witz", description=joke, color=255)
    embed.set_footer(text=f"Witze von: https://witzapi.de/")
    await ctx.send(embed=embed)


@client.hybrid_command(description="Sends a random meme into the chat!")
async def meme(ctx: commands.Context):
    """
    Same thing as with the joke() function but
    this time it sends a link which will embed a meme
    asyncio.sleep(5) is used so the interaction between
    user and bot will not be interrupted.
    """
    asyncio.sleep(5)
    meme = memeapi()
    
    await ctx.send(f"{meme}")



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

    # CREATES 3 BUTTONS
    button = discord.ui.Button(label="Steal from someone in the Server!", style=discord.ButtonStyle.danger) # adds button(s)
    button2 = discord.ui.Button(label="Break into a house!", style=discord.ButtonStyle.blurple) 
    button3 = discord.ui.Button(label="Play in the Casino", style=discord.ButtonStyle.gray)

    async def steal_from_user(interaction):
        """
        gets all users, then chooses a random one to rob, then the steal_from_user()
        function returns the messages content and the money the user
        receives or loses. this will then later be added to the MongoDB Database.
        """
        users = []
        for member in ctx.guild.members:
            users.append(member) # gets all users
        
        while True:
            rdm_user = random.choice(users)
            if rdm_user == ctx.author:
                random.choice(users)
            else:
                break
        content, money_change = money.steal_from_user(ctx.author, rdm_user)
        await interaction.response.send_message(content)
        update_db(str(ctx.author), money_change)
    
    async def break_into_house(interaction):
        """
        The break_into_house() function just returns the content of the message (either they succeed in robbing or not)
        and the money they receive or lose during the operation
        this will then later be added to the MongoDB Database.
        """
        content, money_change = money.break_into_house(ctx.author)
        await interaction.response.send_message(content)
        update_db(str(ctx.author), money_change)

    async def casino(interaction):
        embed = discord.Embed(title="Welcome to the Casino!", description="To play in the casino, you have to choose between either one of three wheels to spin!\n\n**1.** Poor Wheel (max. profit: 500€, costs: 75€, chance: 15%)\n**2.** Normie Wheel (max. profit: 1500€, costs: 120€, chance: 10%)\n**3.** Rich wheel (max. profit: 5000€, costs: 450€, chance: 5%)\n\nType /casino <wheel> to spin a wheel!\n`e.g.: '/casino poor'`", color=255)
        await interaction.response.send_message(embed=embed)

    # DEFINES THE FUNCTIONS THAT WILL BE CALLED ON CLICK
    button.callback = steal_from_user
    button2.callback = break_into_house
    button3.callback = casino

    # ADDS BUTTONS TO VIEW
    view = discord.ui.View() # constructs view
    view.add_item(button)
    view.add_item(button2)
    view.add_item(button3)

    # Sends message
    await ctx.send("Choose one of the options below to earn some money! >:)", view=view)
    await client.wait_for("button_click")


@client.hybrid_command(description="Spin a wheel at the Casino!", name="casino")
@app_commands.describe(option="Choose wisely...")
async def roll_casino(ctx: commands.Context, option: str):
    try:
        """
        casino method either gives you money or you lose money depending on a random number.
        the money you receive or lose will later be added to the MongoDB Database.
        """
        option = option.lower()
        content, money_change = money.casino(option, ctx.author)
        await ctx.send(content)
        update_db(str(ctx.author), money_change)
    except Exception as e:
        await ctx.send(f"{e}!!!")


@client.hybrid_command(description="See how much money you have :)")
async def mymoney(ctx: commands.Context, person: discord.Member):
    person_money = find_user(person.name) # person.name und ctx.author sind das gleiche

    if person_money != None:
        embed = discord.Embed(title="Your money!", description=f"{person.mention} currently has **{person_money}€**!", color=255)
    else:
        embed = discord.Embed(title="Couldn't find user!", description=f"{person.mention} is not registered in our Database yet!", color=255)
    await ctx.send(embed=embed, silent=True)


@client.hybrid_command(description="Debugging stuff...")
async def debug(ctx: commands.Context):
    content = f""
    debugs = [total_messages_read, client, INVITE, ctx.guild.fetch_members()]
    for i in range(len(debugs)):
        content += f"`{debugs[i]}`\n\n"
    await ctx.send(content)


@client.hybrid_command(description="Shows a Leaderboard!")
async def leaderboard(ctx: commands.Context):
    message_content = show_leaderboard()
    embed = discord.Embed(title="The top 10 richest Users!", description=message_content, color=255)
    await ctx.send(embed=embed)

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