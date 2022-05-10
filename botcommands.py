import requests
import json
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

#Every minute, update which players are online or offline
def update_players():
    assert()
#Every minute, check all online players for whether their looted chests count has gone up, the location, 
#and record who looted chests in which location
def update_chests_status():
    assert() 

#Returns a dictionary of the top 100 in a specific leaderboard
def get_leaderboard(type, timeframe):
    #If the user entered player for the type of leaderboard, GET the player leaderboard api data
    if (type.lower() == "player"):
        response_API = requests.get('https://api.wynncraft.com/public_api.php?action=statsLeaderboard&type=player&timeframe=alltime')
    #If the user entered pvp for the type of leaderboard, GET pvp data
    elif (type.lower() == "pvp"):
        #If the user entered alltime, get alltime pvp data
        if timeframe.lower() == "alltime":
            response_API = requests.get('https://api.wynncraft.com/public_api.php?action=statsLeaderboard&type=pvp&timeframe=alltime')
        #GET weekly pvp data
        elif timeframe.lower() == "weekly":
            response_API = requests.get('https://api.wynncraft.com/public_api.php?action=statsLeaderboard&type=pvp&timeframe=weekly')
    #If the user entered guild for the type of leaderboard, GET the guild data
    elif (type.lower() == "guild"):
        response_API = requests.get("https://api.wynncraft.com/public_api.php?action=statsLeaderboard&type=guild&timeframe=alltime")
    #If player, pvp, or guild was not entered, the user mispelled or used the command improperly. 
    #Return an empty dictionary for error handling.
    else:
        return {}
    #convert api GET request to a python dictionary
    data = response_API.text
    parsed_data = json.loads(data)

    #return the dictionary
    return parsed_data

#Every command you type into discord must be prefixed with the .
bot = commands.Bot(command_prefix='.')

#When the python code has connected to the bot and activiated the bot online, print this statement
@bot.event
async def on_ready():
    print('Bot connected')

#Makes sure the bot reads all messages for possible commands
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

#Test function. Returns whatever string argument is passsed. 
@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

#This command, when invoked, makes the bot return a leaderboard list
#Type = type of leaderboard, player, pvp, or guild
#Scope = how far the leaderbaord goes, top 5, top 10, e.t.c. Current limit has been placed at 30
#Timeframe = either alltime or weekly. This only matters for pvp, which has these two options
@bot.command()
async def leaderboard(message, type, scope, timeframe):
    #Whenever this command is invoked, print out this statement
    await message.send("Fetching Leaderboard...")
    #Calls the get_leaderboard function to get the api data
    data = get_leaderboard(type, timeframe)
    #Checks that the data dictionary has contents within it to print
    if len(data) != 0:
        #checks if scope has been passed as an integer, not a word
        try:
            int(scope)
        except:
            await message.send("Incorrect usage! \nTo use, format as: !leaderboard string<type> int<scope> string<timeframe>")
            return #empty return statement, exits this entire function
        #sets the scope maximum limit to 30
        if int(scope) > 100: scope = "100"
        #initializes the embedded discord text which will store the leaderboard
        board = discord.Embed(
                title = type.lower().capitalize() + "Leaderboard",
                color = discord.Color.green()
        )
        #loops through the top <scope> players, storing their information in the string
        for i in range (0, int(scope)):
            #creates the rank (arrays start at index 0, so index 0 is no. 1)
            rank = str(i + 1)
            #stores different stats depending on which type of leaderboard it is
            if type.lower() == "player":
                board.add_field(name= rank + ". " + data["data"][i]["name"], value = "combat level/xp: " + str(data["data"][i]["xp"]))
            if type == "PVP" or type == "pvp":
                board.add_field(name = rank + ". " + data["data"][i]["name"], value = "kills: " + str(data["data"][i]["kills"]))
            if type == "Guild" or type == "guild":
                board.add_field(name = rank + ". " + data["data"][i]["name"], value = "territories:" + str(data["data"][i]["territories"]))
        #prints the leaderboard onto the discord channel 
        await message.send(embed=board)
    #If the dictionary returned by the function is empty, we know the command has been misused and simply exit with an error message
    else:
        await message.send("Incorrect usage! \nTo use, format as: !leaderboard string<type> int<scope> string<timeframe>")

#Connects the python script to the discord bot and keeps the bot running until the code terminates. 
bot.run(DISCORD_TOKEN)