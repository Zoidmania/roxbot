import random
import checks
import requests
from discord.ext.commands import bot

class NFSW():
	def __init__(self, bot_client):
		self.bot = bot_client

	def gelbooru_clone(self, base_url, tags):
		# Maybe a page randomiser
		limit = 100
		url = base_url + '/index.php?page=dapi&s=post&q=index&json=1&tags=' + tags + '&limit=' + str(limit)
		req = requests.get(url, headers={'User-agent': 'RoxBot Discord Bot'})
		if str(req.content) == "b''": # This is to catch any errors if the tags don't return anything because I can't do my own error handling in commands.
			post = None
			return post
		post = random.choice(req.json())
		return post

	@bot.command(pass_context=True)
	@checks.is_nfsw_enabled()
	async def e621(self, ctx, *, tags):
		"""
		Returns an image from e621.com and can use tags you provide.
		"""
		base_url = "https://e621.net/"
		limit = 150
		url = base_url + 'post/index.json?tags=' + tags + '&limit=' + str(limit)
		req = requests.get(url, headers = {'User-agent': 'RoxBot Discord Bot'})
		if str(req.content) == "b'[]'": # This is to catch any errors if the tags don't return anything because I can't do my own error handling in commands.
			return await ctx.send("Nothing was found. *psst, check the tags you gave me.*")
		post = random.choice(req.json())
		return await ctx.send(post["file_url"])

	@bot.command(pass_context=True)
	@checks.is_nfsw_enabled()
	async def rule34(self, ctx, *, tags):
		"""
		Returns an image from rule34.xxx and can use tags you provide.
		"""
		base_url = "https://rule34.xxx"
		post = self.gelbooru_clone(base_url, tags)
		if not post:
			return await ctx.send("Nothing was found. *psst, check the tags you gave me.*")
		url = "https://img.rule34.xxx/images/" + post["directory"] + "/" + post["image"]
		return await ctx.send(url)

	@bot.command(pass_context=True)
	@checks.is_nfsw_enabled()
	async def gelbooru(self, ctx, *, tags):
		"""
		Returns an image from gelbooru.com and can use tags you provide.
		"""
		base_url = "https://gelbooru.com"
		post = self.gelbooru_clone(base_url, tags)
		if not post:
			return await ctx.send("Nothing was found. *psst, check the tags you gave me.*")
		url = "https://simg3.gelbooru.com/images/" + ''.join(post["directory"].split("\\")) + "/" + post["image"]
		return await ctx.send(url)


def setup(bot_client):
	bot_client.add_cog(NFSW(bot_client))