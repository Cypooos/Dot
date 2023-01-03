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
COLOR_ROLES = { }


@tree.command(name = "color", description = "Give you a color role! See available with /colors. Use `/color remove` to remove your color.", guilds=GUILDS_PRIORITARY) 
async def color(interaction,color:str):
    color = color.lower().strip()
    if color == "remove":
        for x in COLOR_ROLES[interaction.guild_id].values() :
            if color in x.name: continue
            await interaction.user.remove_roles(x)
        await interaction.response.send_message("You are brand new!", ephemeral=True)
    if COLOR_ROLES[interaction.guild_id] == {}:
        await interaction.response.send_message("This server doesn't have color roles, sorry !", ephemeral=True)
    else:
        r = COLOR_ROLES[interaction.guild_id].get(color,None)
        if r == None:
            await interaction.response.send_message("I did not find color `"+color+"`, use `/colors` to see a list of colors", ephemeral=True)
        else:
            await interaction.user.add_roles(r)
            for x in COLOR_ROLES[interaction.guild_id].values() :
                if color in x.name: continue
                await interaction.user.remove_roles(x)
            await interaction.response.send_message("Done!", ephemeral=True)


@tree.command(name = "reload", description = "**ADMINISTRATOR ONLY**: will reload this server informations.", guilds=GUILDS_PRIORITARY) 
async def reload(interaction):
    if interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Reloading...", ephemeral=True)
        await reload_guild(interaction.guild)
    else:
        await interaction.response.send_message("It doesn't seems like you have the necessary permission to use this command, sorry!", ephemeral=True)


@tree.command(name = "colors", description = "Print the list of color roles available in this server", guilds=GUILDS_PRIORITARY) 
async def colors(interaction):
    if COLOR_ROLES[interaction.guild_id] == {}:
        await interaction.response.send_message("This server doesn't have color roles, sorry !", ephemeral=True)
    else:
        c = "\n - ".join([key+": <@&"+str(r.id)+">" for key,r in COLOR_ROLES[interaction.guild_id].items() if key != "remove"])
        await interaction.response.send_message("The list of available colors is :\n - "+c+"\nUse `/color remove` to remove your color role.", ephemeral=True)

@tree.command(name = "ping", description = "It says pong !", guilds=GUILDS_PRIORITARY) 
async def ping(interaction):
    await interaction.response.send_message("pong!", ephemeral=True)
    
@tree.command(name = "say", description = "Make Dot say something", guilds=GUILDS_PRIORITARY) 
async def say(interaction,text:str):
    if len(text) > 100:
        await interaction.response.send_message("Your text was too long for me, sorry :(\n(limit is 100 characters)", ephemeral=True)
    else:
        await interaction.response.send_message(text)

@tree.command(name = "zuify", description = "Translate a text to zu!", guilds=GUILDS_PRIORITARY) 
async def zuify(interaction, text:str):
    if len(text) > 100:
        await interaction.response.send_message("Your text was too long for me, sorry :(\n(limit is 100 characters)", ephemeral=True)
    else:
        t = [c.upper() for c in text.replace("\\n","\n").strip()]
        out = map(lambda x:str(ZU_EMOGIES[interaction.guild_id].get(x,":question:")),t)
        await interaction.response.send_message("".join(out))

@client.event
async def on_message(message):
    if message.guild == None:
        if isinstance(message.channel,discord.DMChannel):
            if message.channel.recipient == None:
                g = "DM@?"+str(message.channel.id)
            else:
                g = "DM@"+ message.channel.recipient.name
        elif isinstance(message.channel,discord.GroupChannel):
            g = "GROUP@"+ message.channel.name
        else:
            g = "Unknow#"+ message.channel.name
    else:
        g = message.guild.name+"#"+ message.channel.name
    print(g,message.author,":",message.content)
    #await client.process_commands(message)


async def reload_guild(guild):
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
    print("Adding color roles for",guild.name)
    COLOR_ROLES[guild.id] = {}

    for role in guild.roles:
        to_test = role.name.lower().strip()
        if not ("color" in to_test or "colour" in to_test): continue
        for col in ["blue","cyan","red","black","green","white","pink","orange","yellow","gray","purple","magenta"]:
            if col in to_test:
                COLOR_ROLES[guild.id][col] = role
    
    print("Syncing tree for",guild.name)
    await tree.sync(guild=guild)



@client.event
async def on_ready():
    global GUILD

    for guild in client.guilds:
        await reload_guild(guild)

    print("Ready!")

client.run(TOKEN)
