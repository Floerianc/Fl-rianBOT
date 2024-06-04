# bot.py
import os, discord, json, time, datetime, colorama, random
from dotenv import load_dotenv
from threading import Thread

from func.dawum_mrs.get_msg_content import *
from func.xmsg.xmsgbox import *
import func.error.catch as error

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
INVITE = os.getenv('DISCORD_INVITE')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)


def check_online(client):
    while True:
        currentDateAndTime = datetime.datetime.now()
        currentTime = currentDateAndTime.strftime("%H\\%M\\%S")
        print(colorama.Fore.LIGHTGREEN_EX + f"{client} IS STILL ONLINE " + colorama.Fore.BLACK + colorama.Back.WHITE + f"{currentTime}" + colorama.Style.RESET_ALL)
        time.sleep(300)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    checking_thread = Thread(target=check_online, args=(client.user,))
    checking_thread.start()



@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return
        
        if message.content.startswith('$MRS'):
            get_current_json()
            with open("cache/message.bot", "r", encoding="UTF-8") as msg:
                msg_content = msg.read()
            
            embed = discord.Embed(title="NEUSTE WAHLERGEBNISSE", description=msg_content, color=255)
            await message.channel.send(embed=embed)

            file_path = "cache\\message.bot"
            os.remove(file_path)
        

        elif message.content.startswith('$MSG'):
            user_msg = message.content.replace("$MSG", " ")
            write_vbs(user_msg)
            time.sleep(1)

            file_path = "cache\\msg_from_user.vbs"
            os.remove(file_path)
        
        elif message.content.startswith('$OHN'):
            ohn_association = ["Matxilla", "Nightwolf", "Flörian", "DNAScanner"]
            ohn_websites = ["mat.", "nightwolf.", "flo.", "dnascanner.de"]

            msg_content = f""
            msg_content += f"### 1: [DNAScanner's Website](https://www.dnascanner.de)\n"
            for i in range(len(ohn_websites)-1):
                msg_content += f"\n### {i+2}: [{ohn_association[i]}'s Website](https://{ohn_websites[i]}ohhellnaw.de)"
                if ohn_association[i] == "Flörian":
                    msg_content += f" *(The creator of this bot hehe :>)*\n"

            embed = discord.Embed(title="All OhHellNaw Websites", description=msg_content, color=255)
            await message.channel.send(embed=embed)
        
        elif message.content.startswith('$Help'):
            with open("commands.json", encoding="UTF-8") as file:
                commands = json.load(file)
            msg_content = f""
        
            for i in range(len(commands["Commands"])):
                msg_content += f'**{commands["Commands"][f"{i+1}"]["name"]}** *{commands["Commands"][f"{i+1}"]["desc"]}*\n'
            msg_content += "\n### Developers\n"
            
            for j in range(len(commands["Developer"])):
                msg_content += f'**{commands["Developer"][f"{j+1}"]["name"]}** - *{commands["Developer"][f"{j+1}"]["job"]}*'
            
            embed = discord.Embed(title="Help", description=msg_content, color=255)
            await message.channel.send(embed=embed)
    
        elif message.content.startswith('$Invite'):
                embed = discord.Embed(title="Invite", description=f"Use this invite link to invite the Bot to other servers!\n[Click here!]({INVITE})", color=255)
                await message.channel.send(embed=embed)

        elif message.content.startswith('$Femboy'):
            humans = []
            async for member in message.guild.fetch_members():
                humans.append(member)
            user = random.choice(humans)
            await message.channel.send(f"{user.mention} is {random.randint(0,100)}% femboy.")
        
        elif message.content.startswith('$Ship'):
            humans = []
            async for member in message.guild.fetch_members():
                humans.append(member)
            await message.channel.send(f"{(random.choice(humans)).mention} is {random.randint(0,100)}% in love with {(random.choice(humans)).mention}! <3")

    except Exception as ex:
        error.catch_error(ex)



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