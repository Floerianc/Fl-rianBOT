
'''
NOTES FOR ME AND YOU:
- This script is by no means perfect, I am 100,000% sure that there are many ways to improve this code
- Sensitive Information is going to be removed from this codespace
    This includes:
        - Chatbot API KEY
        - MongoDB URI
        - Discord Token
        - MongoDB Key
- New Commands!!1!!!!!!!11!1!!:
    - Steal (money from another user)
    - Upgrade Account (you're less likely to be robbed :D)
    - Roulette
    - A ((very) polite) chatbot!
'''

import os, discord, time, datetime, colorama, random, requests, discord.interactions, asyncio, func.quotes.quote as qut, func.fun.money as money
from dotenv import load_dotenv; from threading import Thread; from discord.ext import commands; from discord import app_commands

from func.dawum_mrs.get_msg_content import *
from func.apis.apis import *
import func.error.catch as error
from func.db.mongodb import *
from func.fun.ohn import *
from func.ai.chatbot import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
INVITE = os.getenv('DISCORD_INVITE')

client = commands.Bot(intents=discord.Intents.all(), command_prefix="$") # creates client
total_messages_read = 0

'''
CHECKS WHETHER OR NOT BOT IS ONLINE
'''

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


'''
IF MESSAGE IS SENT, INCREASE COUNTER
'''
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    total_messages_read += 1 


'''
IF BOT GOES ONLINE, START THREAD AND REFRESH COMMANDS
'''
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


'''
UPDATE DATABASE
'''
def update_db(user, value):
    update_database(user, value) # updates database with user's name and the cash they received/lost
    with open(f"log NEW.txt", "a", encoding="UTF-8") as f:
        f.write(f"{user} change in money:       {value}\n")


def check_if_user_exists(user):
    if user_exists(str(user)):
        return
    else:
        error_message = f"\n{user} has not yet been set up in MongoDB!\nTrying to set up Account..."
        error.catch_error(error_message)
        create_new_user(user)
        return error_message


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


'''
SHOW ALL OHN WEBSITES
'''
@client.hybrid_command(description="Shows all of the websites from the OHN-Staff!")
async def ohn(ctx: commands.Context):
    """
    shows all the websites from the OHN Staff
    The Website's owners and URLs are saved in lists
    and then later inserted into the messages content
    """

    msg_content = ohn_func()

    embed = discord.Embed(title="All OhHellNaw Websites", description=msg_content, color=255)
    await ctx.send(embed=embed)


'''
SENDS INVITE LINK
'''
@client.hybrid_command(description="A invite link to invite this bot into other Servers aswell!")
async def invite(ctx: commands.Context):
    embed = discord.Embed(title="Invite", description=f"Use this invite link to invite the Bot to other servers!\n[Click here!]({INVITE})", color=255)
    await ctx.send(embed=embed)


'''
SENDS IF SOMEONE IS A FEMBOY OR NOT IN PERCENTAGE LOL
'''
@client.hybrid_command(description="Tells you if a person is a femboy")
@app_commands.describe(person="Which person do you want to choose?")
async def femboy(ctx: commands.Context, person: discord.Member):
    try:
        await ctx.send(f"{person.mention} is {random.randint(0,100)}% femboy.", silent=True)
    except Exception as e:
        error.catch_error(e)


'''
SHIPS TWO PEOPLE
'''
@client.hybrid_command(description="Ships two people")
@app_commands.describe(person="Select the first person", person2="Select the second person")
async def ship(ctx: commands.Context, person: discord.Member, person2: discord.Member):
    try:
        await ctx.send(f"{person.mention} is {random.randint(0,100)}% in love with {person2.mention}! <3", silent=True)
    except Exception as e:
        error.catch_error(e)


'''
DISPLAYS TOTAL_MESSAGES_READ
'''
@client.hybrid_command(description="Reveals how many messages the Bot has read so far...")
async def messages(ctx: commands.Context):
    await ctx.send(f"I've read {total_messages_read:,} messages since the last time I have restarted!")


'''
SENDS RANDOM JOKE FROM WITZEDE API
'''
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


'''
SENDS RANDOM MEME FROM REDDIT
'''
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


'''
RANDOM QUOTE FROM OHN
'''
@client.hybrid_command(description="Shows you a random quote from OHN")
async def quote(ctx: commands.Context):
    quote = qut.get_quote()
    await ctx.send(quote)


'''
EARN MONEY
'''
@client.hybrid_command(description="Do very bad things for money!", name="earnmoney")
async def earn_money(ctx: commands.Context):
    # CREATES 3 BUTTONS
    # (no the fuck it doesn't) LG

    button = discord.ui.Button(label="Steal from someone in the Server!", style=discord.ButtonStyle.danger) # adds button(s)
    button2 = discord.ui.Button(label="Break into a house!", style=discord.ButtonStyle.blurple) 
    button3 = discord.ui.Button(label="Play in the Casino", style=discord.ButtonStyle.gray)
    button4 = discord.ui.Button(label="Steal Money from someone in the Server :>", style=discord.ButtonStyle.danger)
    buttons = [button, button2, button3, button4]

    async def steal(interaction):
        """
        gets all users, then chooses a random one to rob, then the steal_from_user()
        function returns the messages content and the money the user
        receives or loses. this will then later be added to the MongoDB Database.
        """
        users = []
        for member in ctx.guild.members:
            users.append(member) # gets all users
        
        try:
            content, money_change = money.steal_from_user(str(ctx.author), users)
            update_db(str(ctx.author), money_change)
            await interaction.response.send_message({content})
        except:
            await interaction.response.send_message(f"{ctx.author} has not yet been set up in MongoDB!\nTrying to set up an Account just for you...")
            check_if_user_exists(str(ctx.author))
    
    async def break_into_house(interaction):
        """
        The break_into_house() function just returns the content of the message (either they succeed in robbing or not)
        and the money they receive or lose during the operation
        this will then later be added to the MongoDB Database.
        """
        try:
            content, money_change = money.break_into_house(ctx.author)
            update_db(str(ctx.author), money_change)
            await interaction.response.send_message(content)
        except:
            await interaction.response.send_message(f"{ctx.author} has not yet been set up in MongoDB!\nTrying to set up an Account just for you...")
            check_if_user_exists(str(ctx.author))

    async def casino(interaction):
        embed = discord.Embed(title="Welcome to the Casino!", description="To play in the casino, you have to choose between either one of three wheels to spin!\n\n**1.** Poor Wheel (max. profit: 500€, costs: 75€, chance: 15%)\n**2.** Normie Wheel (max. profit: 1500€, costs: 120€, chance: 10%)\n**3.** Rich wheel (max. profit: 5000€, costs: 450€, chance: 5%)\n\nType /casino <wheel> to spin a wheel!\n`e.g.: '/casino poor'`", color=255)
        await interaction.response.send_message(embed=embed)
    
    async def steal_from_someone_actually(interaction):
        embed = discord.Embed(title="Steal from someone!", description="To steal money from someone, try the /steal command.\n**Be aware that if you fail to rob the person, you will lose the same amount of money you try to rob them for. Also, you should not rob someone for more money than you own.**\n`/steal <user> 5000`")
        await interaction.response.send_message(embed=embed)

    # DEFINES THE FUNCTIONS THAT WILL BE CALLED ON CLICK
    button.callback = steal
    button2.callback = break_into_house
    button3.callback = casino
    button4.callback = steal_from_someone_actually

    # ADDS BUTTONS TO VIEW
    view = discord.ui.View() # constructs view
    for button in buttons:
        view.add_item(button)

    # Sends message
    await ctx.send("Choose one of the options below to earn some money! >:)", view=view)
    await client.wait_for("button_click")


'''
TRY OUT THE CASINO
'''
@client.hybrid_command(description="Spin a wheel at the Casino!", name="casino")
@app_commands.describe(option="Choose wisely...")
async def roll_casino(ctx: commands.Context, option: str):
    try:
        """
        casino method either gives you money or you lose money depending on a random number.
        the money you receive or lose will later be added to the MongoDB Database.
        """
        
        option = option.lower()
        
        try:
            user_money = find_user(str(ctx.author))
            content, money_change = money.casino(option, ctx.author, user_money)
            update_db(str(ctx.author), money_change)
            await ctx.send(content)
        except:
            check_if_user_exists(str(ctx.author))
        
    except Exception as e:
        await ctx.send(f"{e}!!!")


'''
DISPLAYS YOUR MONEY
'''
@client.hybrid_command(description="See how much money you have :)")
async def mymoney(ctx: commands.Context, person: discord.Member):
    person_money = find_user(str(person.name)) # person.name und ctx.author sind das gleiche

    if person_money != None:
        embed = discord.Embed(title="Your money!", description=f"{person.mention} currently has **{person_money}€**!", color=255)
    else:
        embed = discord.Embed(title="Couldn't find user!", description=f"{person.mention} is not registered in our Database yet!", color=255)
    await ctx.send(embed=embed, silent=True, ephemeral=True)


@client.hybrid_command(description="Debugging stuff...")
async def debug(ctx: commands.Context):
    content = f""
    debugs = [total_messages_read, client, INVITE, ctx.guild.fetch_members()]
    for i in range(len(debugs)):
        content += f"`{debugs[i]}`\n\n"
    await ctx.send(content, ephemeral=True)


'''
DISPLAYS TOP 10 RICHEST MEMBERS AND YOURSELF
'''
@client.hybrid_command(description="Shows a Leaderboard!")
async def leaderboard(ctx: commands.Context):
    message_content = show_leaderboard(str(ctx.author))
    embed = discord.Embed(title="The top 10 richest Users!", description=message_content, color=255)
    await ctx.send(embed=embed)


'''
STEALS MONEY FROM ANOTHER MEMBER
'''
@client.tree.command(description="Steal money from another User!")
async def steal(interaction: discord.Interaction, option: discord.Member, amount: int):
    '''
    With this command you can steal money from another Member

    First, it checks if the person who uses the command is the same person being robbed
    Secondly, it checks if both users exist in the database
    Then, It defers the message so discord does not interupt the interaction
    After thats done a lot of magic happens to determine wheter or not you can rob the other user
    And in the end it updates the database with the results and sends the message.

    Since I had to use discord.Interaction to get the defer thing working I had to completely delete
    the ctx: commands.Context thing in the parameters because otherwise shit would just crash lmao
    So I replaced every ctx with commands.Context, I hope thats not too confusing.
    So, thats why I use commands.Context here instead of ctx.
    '''

    await interaction.response.defer()

    if str(interaction.user.name) == str(option.name):
        await interaction.followup.send("You can not rob yourself, lol")
        return
    
    user_calling_command_exists = find_user(str(interaction.user.name))
    user_option_exists = find_user(str(option.name))

    if user_calling_command_exists is None or user_option_exists is None:
        await interaction.followup.send(f"{interaction.user.name} or {option.name} does not exist, therefore you can not rob them.")
        return
    
    if amount < 1:
        await interaction.followup.send("Bro you won't gain anything from this lmao")
        return

    users = find_all_users()
    successful, message_content = money.steal_from_another_user(users, str(interaction.user.name), str(option.name), amount)

    if successful is True:
        update_db(str(interaction.user.name), amount)
        update_db(str(option.name), (-amount))
    elif successful is False:
        update_db(str(interaction.user.name), (-amount))
        update_db(str(option.name), amount)
    elif successful is None:
        pass
    
    await interaction.followup.send(message_content) # everyone can see message


@client.hybrid_command(description="Buy new upgrades!")
async def upgrade(ctx: commands.Context):
    '''
    This function displays all available upgrades and adds a button for each one.
    After clicking a button, it executes a function which causes something.
    For more information, check the .callback functions.
    This function also uses the MongoDB Database.
    '''

    all_upgrades = ["Upgrade Security Messures (Reduces chance to be robbed from 30% to 20%)", "Earn 20% more money in the Roulette, if you win."]
    embed_content = f""

    for i in range(len(all_upgrades)):
        embed_content += f"**{i+1}.** {all_upgrades[i]}"

    async def buy_chance_upgrade(interaction):
        try:
            message_content = upgrade_chance(str(ctx.author))
            await interaction.response.send_message(message_content)
        except:
            await interaction.response.send_message(f"{ctx.author} has not yet been set up in MongoDB!\nTrying to set up an Account just for you...")
            check_if_user_exists(str(ctx.author))

    button = discord.ui.Button(label="Steal from someone in the Server!", style=discord.ButtonStyle.success) # construct buttons
    button.callback = buy_chance_upgrade

    view = discord.ui.View() # constructs view
    view.add_item(button)

    embed = discord.Embed(title="Upgrades", description=embed_content, color=255)
    await ctx.send(embed=embed, view=view)
    await client.wait_for("button_click")


@client.tree.command(name="roulette", description="Play Roulette to win... or lose money.")
@app_commands.choices(choices=[
    app_commands.Choice(name="Black", value="Black"),
    app_commands.Choice(name="Red", value="Red"),
    app_commands.Choice(name="Even", value="Even"),
    app_commands.Choice(name="Odd", value="Odd"),
    app_commands.Choice(name="0", value="0"),
])
async def roulette(interaction: discord.Interaction, choices: app_commands.Choice[str]):
    '''
    In the Roulette command you can choose between 5 different options.
    Either you bet your money on Black, Red, an Even number, Odd number or the number 0.
    
    First, the program constructs and defines the buttons, then the callback functions
    for each one of the buttons.
    Here I used lambda so I can pass a parameter through the function because it
    wouldn't work otherwise or at least I couldn't find a simpler solution.

    When we get to the button_callback() we can see that we first get the Roulette results
    and after that we try to find the user in the MongoDB. If the user isn't registered there yet,
    we create a new document for the user.
    Now to the most interesting part for the user, depending on the results in the
    money.roulette_decider(arg) function the program decides whether or not you lose or win.
    If you win, the amount of money you spent times the multiplicator will be added to your document.
    If you lose, the amount of money you spent will be lost.
    '''
    await interaction.response.defer()

    thousand_button = discord.ui.Button(label="1,000€", style=discord.ButtonStyle.blurple)
    ten_thousand_button = discord.ui.Button(label="10,000€", style=discord.ButtonStyle.blurple)
    hundred_thousand_button = discord.ui.Button(label="100,000€", style=discord.ButtonStyle.blurple)
    million_button = discord.ui.Button(label="1,000,000€", style=discord.ButtonStyle.blurple)
    buttons = [thousand_button, ten_thousand_button, hundred_thousand_button, million_button]

    async def button_callback(interaction, arg, value):
        await interaction.response.defer()
        user_won, multiplicator = money.roulette_decider(arg)

        try:
            user_score = find_user(str(interaction.user.name))
            if user_score < value:
                await interaction.followup.send("You don't have enough money for this.")
                return
            
            if user_won == True:
                update_user(str(interaction.user.name), value*multiplicator)
                msg_content = f"{interaction.user.name} won {value*multiplicator:,}€ in the Roulette! Congratulations!"
            else:
                update_database(str(interaction.user.name), (-value))
                msg_content = f"{interaction.user.name} lost {value:,}€ in the Roulette!"
        except:
            await interaction.followup.send(f"{interaction.user.name} has not yet been set up in MongoDB!\nTrying to set up an Account just for you...")
            check_if_user_exists(str(interaction.user.name))

        await interaction.followup.send(msg_content)

    thousand_button.callback = lambda interaction: button_callback(interaction, choices.value, 1000)
    ten_thousand_button.callback = lambda interaction: button_callback(interaction, choices.value, 10000)
    hundred_thousand_button.callback = lambda interaction: button_callback(interaction, choices.value, 100000)
    million_button.callback = lambda interaction: button_callback(interaction, choices.value, 1000000)

    view = discord.ui.View()
    for button in buttons:
        view.add_item(button)

    embed = discord.Embed(title="Welcome to Roulette v1.0!", description="In this Roulette you can choose either Black, Red, an Even number, Odd number or the number 0.\nClick one of the buttons below to bet money, just be responsible with your money... :)")
    await interaction.followup.send(embed=embed, view=view)
    await client.wait_for("button_click")


@client.tree.command(description="Talk to a *very polite* Chatbot!", name="chatbot")
# @app_commands.describe(option="What do you want to say?")
async def chatbot(interaction: discord.Interaction, option: str):
    await interaction.response.defer(thinking=True)
    
    message_content = ai_send_response(user_content=option)
    embed = discord.Embed(title=f'User: "{option}"', description=message_content)
    await interaction.followup.send(embed=embed)

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