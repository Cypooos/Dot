import discord
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

with open("key.env","r") as f:
    TOKEN = f.read()
with open("guild.env","r") as f:
    GUILD_ID = int(f.read())

GUILD = discord.Object(id=GUILD_ID)
print("TOKEN:",TOKEN[:5].upper())
print("GUILD_ID:",str(GUILD_ID)[:5])

GUILD = None

ZU_EMOGIES = { }


@tree.command(name = "ping", description = "It says pong !",guild=discord.Object(id=GUILD_ID)) 
async def ping(interaction):
    await interaction.response.send_message("pong!")
    
@tree.command(name = "say", description = "Make Dot say something",guild=discord.Object(id=GUILD_ID)) 
async def say(interaction,text:str):
    await interaction.response.send_message(text)

@tree.command(name = "zuify", description = "Translate a text to zu!",guild=discord.Object(id=GUILD_ID)) 
async def zuify(interaction, text:str):
    t = [c.upper() for c in text.strip()]
    out = map(lambda x:str(ZU_EMOGIES.get(x,":question:")),t)
    await interaction.response.send_message("".join(out))


@client.event
async def on_ready():
    global GUILD
    GUILD = client.get_guild(GUILD_ID)
    if GUILD == None:
        print("GUILD NOT JOINED I AM DED")
        quit()
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    

    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        name_ = "zu"+c
        if c == "Q" or c == "K": name_ = "zuKQ"
        if c == "U" or c == "V": name_ = "zuUV"
        ZU_EMOGIES[c] = discord.utils.get(GUILD.emojis, name=name_)
    ZU_EMOGIES[" "] = discord.utils.get(GUILD.emojis, name="zu")

    print("Ready!")

client.run(TOKEN)
