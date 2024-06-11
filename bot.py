import os, discord, json, time, datetime, colorama, random
from dotenv import load_dotenv
from threading import Thread
from discord.ext import commands
from discord import app_commands

from func.dawum_mrs.get_msg_content import *
from func.xmsg.xmsgbox import *
import func.error.catch as error

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
INVITE = os.getenv('DISCORD_INVITE')

client = commands.Bot(intents=discord.Intents.all(), command_prefix="/")
total_messages_read = 0


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


@client.hybrid_command(description="Displays a message directly on my Screen")
@app_commands.describe(message="What do you want the message to say?")
async def msg(ctx: commands.Context, message: str):
    user_msg = f"{message}"
    try:
        write_vbs(user_msg)
        time.sleep(1)

        file_path = "cache\\msg_from_user.vbs"
        os.remove(file_path)
        await ctx.send("Message was sent!")
    except Exception as e:
        await ctx.send("Message couldn't be delivered :(")
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