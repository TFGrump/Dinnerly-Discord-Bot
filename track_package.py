import urllib.request
import urllib.error
import json
from time import sleep
from discord.ext.commands import Bot
import discord.ext.commands

bot = Bot(command_prefix="_food_")
TOKEN = '' # Token for the discord bot would go here

tracking_numbers = []


async def find_package(ctx, tracking_number):
    json_url = 'http://www.lasership.com/track/' + tracking_number + '/json'
    try:
        with urllib.request.urlopen(json_url) as url:
            data = json.loads(url.read().decode())
            if data["Events"][0]["EventType"] == "Miscellaneous":
                if data["Events"][1]["EventType"] == "Delivered":
                    tracking_numbers.remove(tracking_number)
                    await ctx.send("You food box has been delivered")
            elif data["Events"][0]["EventType"] == "Delivered":
                tracking_numbers.remove(tracking_number)
                await ctx.send("You food box has been delivered")
            else:
                print("not here yet")
    except urllib.error.HTTPError:
        await ctx.send("There was an error finding the tracking number")


@bot.command(description='Sends a message if a package has arrived',
             breif='Sends a message if a package has arrived',
             pass_context=True)
async def track_package(ctx, arg):
    if tracking_numbers.count(arg) == 0:
        tracking_numbers.append(arg)
    while len(tracking_numbers) > 0:
        if tracking_numbers.count(arg) > 0:
            for tracking_number in tracking_numbers:
                print("checking for package")
                await find_package(ctx, tracking_number)
        if len(tracking_numbers) > 0:
            sleep(1800)
    print('finished tracking')


@bot.command(description='Stops tracking a certain package',
             brief='Stops tracking a certain package')
async def stop_tracking(arg):
    tracking_numbers.remove(arg)


@bot.command(description='Shows what packages are being tracked',
             brief='Shows what packages are being tracked',
             pass_context=True)
async def show_tracking_numbers(ctx):
    # Create some kind of embed to make the list look nice
    print('does nothing for now')


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

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name='for your box'))


bot.run(TOKEN)
