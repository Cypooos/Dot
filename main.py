import discord
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

with open("./key.env","r") as f:
    TOKEN = f.read()
    
print("TOKEN:",TOKEN[:5].upper())

GUILDS_PRIORITARY = [ discord.Object(id=x) for x in [1059253745906622545,1057772277967638538,959879578019577887] ]
ZU_EMOGIES = { }


@tree.command(name = "ping", description = "It says pong !", guilds=GUILDS_PRIORITARY) 
async def ping(interaction):
    await interaction.response.send_message("pong!")
    
@tree.command(name = "say", description = "Make Dot say something", guilds=GUILDS_PRIORITARY) 
async def say(interaction,text:str):
    await interaction.response.send_message(text)

@tree.command(name = "zuify", description = "Translate a text to zu!", guilds=GUILDS_PRIORITARY) 
async def zuify(interaction, text:str):
    t = [c.upper() for c in text.replace("\\n","\n").strip()]
    out = map(lambda x:str(ZU_EMOGIES[interaction.guild_id].get(x,":question:")),t)
    await interaction.response.send_message("".join(out))

@client.event
async def on_message(message):
    print(message.guild.name+"#"+message.channel.name,message.author,":",message.content)
    #await client.process_commands(message)

@client.event
async def on_ready():
    global GUILD

    for guild in client.guilds:
        print("Adding zu alphabet for",guild.name)
        ZU_EMOGIES[guild.id] = {}
        for x in "\n\t,'\"#~*_-:?;.$^1234567890+=|`}{()[]&µ!²\\":
            ZU_EMOGIES[guild.id][x] = x
        for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            name_ = "zu"+c
            if c == "Q" or c == "K": name_ = "zuKQ"
            if c == "U" or c == "V": name_ = "zuUV"
            ZU_EMOGIES[guild.id][c] = discord.utils.find(lambda m: m.name.lower().replace("_","") == name_.lower(), guild.emojis)
            if ZU_EMOGIES[guild.id][c] == None:
                ZU_EMOGIES[guild.id][c] = ":question:"
        ZU_EMOGIES[guild.id][" "] = discord.utils.get(guild.emojis, name="zu")

        print("Syncing tree for",guild.name)
        await tree.sync(guild=guild)
    

    print("Ready!")

client.run(TOKEN)
