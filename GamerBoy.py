from redbot.core import commands
from Perudo.Perudo import Perudo


class GamerBoy(commands.Cog):
	"""My custom cog"""

	def __init__(self, bot):
		self.bot = bot
		self.game_on = 0
		self.gamecogs = None

	@commands.command()
	async def ragequit(self, ctx):
		self.game_on = 0
		self.gamecogs = None


	@commands.command()
	async def launch(self, ctx, game):
		"""
		List of available game
		"""
		if self.game_on == 0 : 
			if game == "Perudo" :
				await ctx.send("{0.author} wants to play Perudo".format(ctx))
				bot.add_cog(Perudo(bot,ctx))
				self.gamecogs = self.bot.get_cog('Perudo')

				await self.gamecogs.wait_for_player()
				await self.gamecogs.run_game()

				self.gamecogs = None
				bot.remove_cog('Perudo')

