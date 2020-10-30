import urllib.request
import urllib.error
import json
from time import sleep
from discord.ext.commands import Bot
import discord.ext.commands
bot = Bot(command_prefix="_food_")
TOKEN = ''  # Token for the discord bot

tracking_numbers = []


async def find_package(ctx, tracking_number):
    json_url = 'http://www.lasership.com/track/' + tracking_number + '/json'
    try:
        with urllib.request.urlopen(json_url) as url:
            data = json.loads(url.read().decode())
            if data["Events"][0]["EventType"] == "Delivered":
                tracking_numbers.remove(tracking_number)
                await ctx.send("You food box has been delivered")
    except urllib.error.HTTPError:
        await ctx.send("There was an error finding the tracking number")


@bot.command(description='Sends a message if a package has arrived',
             pass_context=True)
async def track_package(ctx, arg):
    if tracking_numbers.count(arg) == 0:
        tracking_numbers.append(arg)
    while len(tracking_numbers) > 0:
        if tracking_numbers.count(arg) > 0:
            for tracking_number in tracking_numbers:
                await find_package(ctx, tracking_number)

        sleep(1800)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("You are missing your tracking number")


@bot.event
async def on_ready():
    print('Bot logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(TOKEN)
