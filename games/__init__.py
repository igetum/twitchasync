from twitchio.ext import commands
from random import choice, randint
from time import time
import asyncio


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
	def __init__(self):
		self.answer = randint(1,10)
		self.collection_time = time() + 60
		self.bet_multiplier = 2


	async def get_results(self, ctx, *args):
		await asyncio.sleep(1)
		winners = {}
		for user in self.game_users:
			
			bet = int(self.game_users[user][0])
			uguess = int(self.game_users[user][1])

			if uguess == self.answer:
				winners[user] = bet * self.bet_multiplier

		return winners




async def guess_run(self, ctx, *args):
	global gameObj

	if gameObj is None:

		gameObj = Guess()
		gameObj.running = True
		await ctx.send("EVENT: Guessing Game! Enter your bets: !bet <bet amount> <guess>")
		await guess_start(self, ctx)

	else:	
		await ctx.send("A game is currently in session")


async def guess_start(self, ctx):
	global gameObj

	while True:
		await asyncio.sleep(1)
		if gameObj.collection_time <= time():
			await guess_end(self, ctx)
			break


async def guess_end(self, ctx):
	global gameObj
	await ctx.send(f"EVENT: The correct guess is {gameObj.answer}")
	winners = await gameObj.get_results(self, ctx)
	winner_message = "EVENT: Winners"

	if bool(winners):
		for winner in winners:
			winner_message = winner_message + " | " + winner + "  $" + str(winners[winner])
		await ctx.send(winner_message)
	else:
		await ctx.send("EVENT: No winners!")

	await ctx.send("EVENT: Ending game")
	gameObj = None



######################
#HEIST GAME
######################