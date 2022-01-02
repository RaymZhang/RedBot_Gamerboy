from redbot.core import commands 

class Coggameinstance(commands.Cog):
	"""
	Classe containing general function to play a game
	

	Commands :
		-[p]start start the game
		-[p]whoplay send the list of players

	attributes : 
		-player : list of players
		-game_on : state of the game, 0 game finished, 1 looking for player, 2 game playing 
	"""

	def __init__(self, bot, ctx):
		self.bot = bot
		self.players = []
		self.ctx = ctx

	def check_start(self):
		return lambda m: m.content == "!start"


	async def wait_for_player(self):
		await self.ctx.send("Say 'me' to play and '!start' to start the game")
		await self.bot.wait_for('message', check = self.check_start())


	@commands.Cog.listener(name = "on_message")
	async def add_player(self, message):
		if self.game_on == 1 and message == "me" and message.author not in self.players:
			self.players.append(message.author)
			await self.ctx.send("{0}, you are registered".format(message.author.mention))
		elif self.game_on == 1 and message == "me" and message.author in self.players:
			await self.ctx.send("{0}, you are already registered".format(message.author.mention))

	
	@commands.command()
	async def whoplay(self, ctx):
		string = ""
		for player in self.players:
			string += "{0.mention} ".format(player)
		string +=  " are playing."
		await ctx.send(string)



