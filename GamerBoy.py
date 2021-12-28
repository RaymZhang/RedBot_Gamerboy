from redbot.core import commands
from Perudo/Perudo import Perudo



import whoplay

class GamerBoy(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def launch(self, ctx, game):
        """List of available game

        """
        
        if game == "Perudo" :
        	await ctx.send("{0.author} wants to play Perudo".format(ctx.message))
            listofplayer = [ctx.message.author]
            listofplayer.append(whoplay(ctx))

            await Perudo(ctx,listofplayer)
            listofplayer = None


    @commands.command()
    async def Start(self, ctx):
        await 