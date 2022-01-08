from redbot.core import commands
from .Perudo.Perudo import Perudo


class GamerBoy(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        self.game_on = 0
        self.gamecog = None
        self.gamelist = ["perudo"]

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
        if self.game_on == 0 and :
            if self.game.lower() in self.gamelist:
                self.game_on = 1
                if game.lower() == "perudo":
                    self.game = "Perudo"
                    await ctx.send("{0.author} wants to play Perudo".format(ctx))
                    self.bot.add_cog(Perudo(self.bot, ctx))
                    self.gamecog = self.bot.get_cog(self.game)

                    await self.gamecog.wait_for_player()
                    self.game_on = 2
                    await self.gamecog.run_game()

                    self.gamecog = None
                    self.bot.remove_cog(self.game)   
                    self.game_on = 0  
            else :
                await ctx.send("This game is not yet coded")                    
        else :
            await ctx.send("Another instance of {0} is already running".format(self.game))
               
