import requests
import json

def update_players():
    assert()

def update_chests_status():
    assert() 

def get_leaderboard(type, timeframe):
    if (type == "Player" or type == "player"):
        response_API = requests.get('https://api.wynncraft.com/public_api.php?action=statsLeaderboard&type=player&timeframe=alltime')
    elif (type == "PVP" or type == "pvp"):
        if timeframe == "alltime":
            response_API = requests.get('https://api.wynncraft.com/public_api.php?action=statsLeaderboard&type=pvp&timeframe=alltime')
        elif timeframe == "weekly":
            response_API = requests.get('https://api.wynncraft.com/public_api.php?action=statsLeaderboard&type=pvp&timeframe=weekly')
    elif (type == "Guild" or type == "guild"):
        response_API = requests.get("https://api.wynncraft.com/public_api.php?action=statsLeaderboard&type=guild&timeframe=alltime")
    else:
        return {}
    data = response_API.text
    parsed_data = json.loads(data)

    return parsed_data


from discord.ext import commands
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Bot connected')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def leaderboard(message, type, scope, timeframe):
    await message.send("Fetching Leaderboard...")
    data = get_leaderboard(type, timeframe)
    if len(data) != 0:
        try:
            int(scope)
        except:
            await message.send("Incorrect usage! \nTo use, format as: !leaderboard string<type> int<scope> string<timeframe>")
            return
        if int(scope) > 30: scope = "30"
        board = ""
        for i in range (0, int(scope)):
            rank = str(i + 1)
            board += rank + ". " + data["data"][i]["name"] + "   "
            if type == "Player" or type == "player":
                board += "combat level/xp: " + str(data["data"][i]["xp"]) + "\n"
            if type == "Pvp" or type == "pvp":
                board += "kills: " + str(data["data"][i]["kills"]) + "\n"
            if type == "Guild" or type == "guild":
                board += "territories:" + str(data["data"][i]["territories"]) + "\n"
        await message.send(board)
    else:
        await message.send("Incorrect usage! \nTo use, format as: !leaderboard string<type> int<scope> string<timeframe>")

bot.run('OTczMzkxMTczMTQ0MTc4NzU4.GGHNIO.TvqNcHEgZ7lNvw4qhYuVYfq3D91I4lLq4bcJdw')