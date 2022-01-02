from redbot.core import commands
from .Perudo.Perudo import Perudo


class GamerBoy(commands.Cog):
	"""My custom cog"""

	def __init__(self, bot):
		self.bot = bot
		self.game_on = 0
		self.gamecog = None

	@commands.command()
	async def ragequit(self, ctx):
		self.game_on = 0
		self.gamecog = None
		self.bot.remove_cog(self.game)


	@commands.command()
	async def launch(self, ctx, game):
		"""
		List of available game
		"""
		self.game = game
		if self.game_on == 0 : 
			if game == "Perudo" :
				await ctx.send("{0.author} wants to play Perudo".format(ctx))
				self.bot.add_cog(Perudo(self.bot,ctx))
				self.gamecog = self.bot.get_cog(game)

				await self.gamecog.wait_for_player()
				await self.gamecog.run_game()

				self.gamecog = None
				self.bot.remove_cog(game)

