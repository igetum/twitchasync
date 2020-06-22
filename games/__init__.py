from twitchio.ext import commands
from random import choice, randint


gameObj = None

class Game(object):
	running = False
	game_users = {}

#####################
# COMMON GAME METHODS
#####################


async def add_user(self, user, *args):
	if gameObj is not None:
		if gameObj.running == True:
			gameObj.game_users[user] = [args[0], args[1]]


async def read_users(self, ctx):
	print(gameObj.game_users)



########################
# GUESSING GAME
########################


class Guess(Game):
	pass
      

async def guess_run(self, ctx, *args):

	global gameObj

	if gameObj is None:

		gameObj = Guess()
		gameObj.running = True

	else:	
		await ctx.send("A game is currently in session")


