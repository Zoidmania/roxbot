#!/usr/env python3

import time
import logging
import os.path
import datetime
import discord
from discord.ext import commands

import Roxbot
from Roxbot import guild_settings as gs

# Sets up Logging that discord.py does on its own
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(
	command_prefix=Roxbot.command_prefix,
	description=Roxbot.__description__,
	owner_id=Roxbot.owner,
	activity=discord.Game(name="v{}".format(Roxbot.__version__), type=0),
	case_insensitive=True
)


@bot.event
async def on_ready():
	# Load Roxbots inbuilt cogs and settings
	bot.load_extension("Roxbot.settings.settings")
	bot.load_extension("Roxbot.err_handle")
	bot.load_extension("Roxbot.logging")
	bot.settings = gs.get_all(bot.guilds)

	print("Discord.py version: " + discord.__version__)
	print("Client logged in\n")

	# Load Extension Cogs
	print("Cogs Loaded:")
	for cog in Roxbot.cogs:
		bot.load_extension(cog)
		print(cog.split(".")[2])
	print("")

	print("Servers I am currently in:")
	for server in bot.guilds:
		print(server)
	print("")

# In the next two functions, I was gunna user bot.settings for something but I don't think it's possible.
# So while I don't use it, the function still will do their jobs of adding and removing the settings.


@bot.event
async def on_guild_join(guild):
	gs.add_guild(guild)


@bot.event
async def on_guild_remove(guild):
	gs.remove_guild(guild)


@bot.event
async def on_message(message):
	"""
	Checks if the user is blacklisted, if not, process the message for commands as usual.
	:param message:
	:return:
	"""
	if Roxbot.blacklisted(message.author):
		return
	return await bot.process_commands(message)


@bot.command()
async def about(ctx):
	"""
	Outputs info about RoxBot, showing uptime, how to report issues, what settings where set in prefs.ini and credits.
	"""
	owner = bot.get_user(Roxbot.owner)
	em = discord.Embed(title="About Roxbot", colour=Roxbot.EmbedColours.pink, description=Roxbot.__description__)
	em.set_thumbnail(url=bot.user.avatar_url)
	em.add_field(name="Command Prefix", value=Roxbot.command_prefix)
	em.add_field(name="Owner", value=str(owner))
	em.add_field(name="Owner ID", value=Roxbot.owner)
	em.add_field(name="Bot Version", value=Roxbot.__version__)
	em.add_field(name="Author", value=Roxbot.__author__)
	em.add_field(name="Discord.py version", value=discord.__version__)
	em.set_footer(text="RoxBot is licensed under the MIT License")

	# Do time calc late in the command so that the time returned is closest to when the message is received
	uptimeflo = time.time() - start_time
	uptime = str(datetime.timedelta(seconds=uptimeflo))
	em.add_field(name="Current Uptime", value=str(uptime.split(".")[0]))

	return await ctx.channel.send(embed=em)

if __name__ == "__main__":
	# Pre-Boot checks
	if not os.path.isfile("Roxbot/settings/preferences.ini"):
		print(
			"PREFERENCE FILE MISSING. Something has gone wrong. Please make sure there is a file called 'preferences.ini' in the settings folder")
		exit(0)

	if not os.path.isfile("Roxbot/settings/servers.json"):
		with open("Roxbot/settings/servers.json", "w") as fp:
			fp.write("{}")

	start_time = time.time()
	bot.run(Roxbot.token)
