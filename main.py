from twitchio.ext import commands
from auth import client_id, irc_token, bot_nick, owner
from random import choice, randint
import games

from lib import db

gamescmds = {
    "guess" : games.guess_run,
    "heist" : games.heist_run,
}

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=irc_token, client_id=client_id, nick=bot_nick, prefix='!', initial_channels=[owner])
        db.build()


    async def event_ready(self):
         print(f'Ready | {self.nick}')


    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)



    # Commands use a decorator...
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')


    ######################
    # COINFLIP
    ######################
    @commands.command(name='coinflip')
    async def coinflip(self, ctx, side=None, *args):
        if side is None:
            await ctx.send("You need to guess which side the coin will land!")
        elif (side := side.lower()) not in (opt := ("h", "t", "heads", "tails")):
            await ctx.send("Enter one of the following as the side: " + ", ".join(opt))

        else:
            result = choice(("heads", "tails"))

            if side[0] == result[0]:
                await ctx.send(f"It landed on {result}! You won 50 coins!")

            else:
                await ctx.send(f"Too bad - it landed on {result}. You didn't win anything!")


    ######################
    # START GAME
    ######################
    @commands.command(name='startgame')
    async def startgame(self, ctx, *args):
        if args is not None:
            if args[0] in gamescmds:
                await gamescmds[args[0]](self, ctx, *args)

    @commands.command(name='bet')
    async def add_user(self, ctx, *args):
        user = ctx.author.name
        await games.add_user(self, ctx, user, *args)

    @commands.command(name='getgameusers')
    async def read_users(self, ctx, *args):
        await games.read_users(self, ctx, *args)
 
   
if __name__ == "__main__":
    bot = Bot()
    bot.run()
