from .GamerBoy import GamerBoy


def setup(bot):
    bot.add_cog(GamerBoy(bot))