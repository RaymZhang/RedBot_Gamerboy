from redbot.core import commands 

class Coggameinstance(commands.cog):
	"""
	Classe containing general function to play a game
	

	Commands :
		-[p]start start the game
		-[p]whoplay send the list of players

	attributes : 
		-player : list of players
		-game_on : state of the game, 0 game finished, 1 looking for player, 2 game playing 
	"""

	def __init__(self, bot):
		self.bot = bot
		self.players = []
		self.game_on = 0
		self.ctx = ctx

	def check_start(self, message):
		if message.content == "!start":
			return True
		else :
			return False


	async def wait_for_player():
		ctx.send("Say 'me' to play and '!start' to start the game")
		await self.wait_for('message', check = self.check_start(message))
		

	@commands.Cog.listener("on_message")
	async def add_player(message):
		if self.game_on == 1 and message == "me" and message.author not in self.players:
			self.players.append(message.author)
			await message.channel.send("{0}, you are registered".format(message.author.mention))
		elif self.game_on == 1 and message == "me" and message.author in self.players:
			await message.channel.send("{0}, you are already registered".format(message.author.mention))

	
	@commands.command()
	async def whoplay(self, ctx):
		string = ""
		for player in self.players:
			string += "{0.mention} ".format(player)
		string +=  " are playing."
		await ctx.send(string)



