from twitchio.ext import commands
from random import choice, randint
from time import time
import asyncio

from lib import db

gameObj = None


#####################
# COMMON GAME METHODS
#####################


async def add_user(self, ctx, user, *args):
	if gameObj is not None:
		if gameObj.running == True:
			await gameObj.add_user(ctx, user, *args)


async def read_users(self, ctx):
	print(gameObj.game_users)
	await ctx.send(gameObj.game_users)



########################
# GUESSING GAME
########################

class Guess(object):
	def __init__(self):
		self.maxNum = 2
		self.answer = randint(1, self.maxNum)
		self.collection_time = time() + 20
		self.bet_multiplier = 1.5
		self.game_users = {}
		self.running = False

	async def add_user(self, ctx, user, *args):
		bet = args[0]
		uguess = args[1]

		if bet.isdigit() and uguess.isdigit():
			
			bet = int(bet)
			if bet > int((coins := db.field("SELECT Coins FROM users WHERE UserID = ?", user["id"]))):
				await ctx.send(f"You don't have that much to bet - you only have {coins:,} coins.")

			else:
				db.execute("UPDATE users SET Coins = Coins - ? WHERE UserID = ?", bet, user["id"])
				db.commit()
				self.game_users[user["name"]] = [bet, uguess]

				await ctx.send(f"@{user['name']} - Bet submitted")

		else:
			await ctx.send("!bet error")
	
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
	#
	#Start game from here. Create a new game object using Guess class. Starts running state.
	#
	global gameObj

	if gameObj is None:

		gameObj = Guess()
		gameObj.running = True
		await ctx.send("EVENT: Guessing Game! Enter your bets: !bet <bet amount> <guess>")
		await guess_start(self, ctx)

	else:	
		await ctx.send("A game is currently in session")


async def guess_start(self, ctx):
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
			await asyncio.sleep(1)
			winner_message = winner_message + " | " + winner + "  $" + str(winners[winner])
			db.execute("UPDATE users SET Coins = Coins + ? WHERE UserName = ?", winners[winner], winner)
			db.commit()
		await ctx.send(winner_message)
	else:
		await ctx.send("EVENT: No winners!")

	await ctx.send("EVENT: Ending game")

	gameObj = None


######################
#HEIST GAME
######################

class Heist(object):
	def __init__(self):
		self.collection_time = 0
		self.collection_state = False
		self.start_time = 0
		self.bet_multiplier = 1.5
		self.succeeded = []
		self.game_users = {}
		self.running = False
		self.messages = {
			"success" : [
				"@{} fought off the guards, and got their haul!",
				"@{} sneaked out of the back entrance with their share!",
				"@{} got in and out seemlessly with their money!",
			],
			"fail" : [
				"@{} got caught by the guards!",
				"@{} was injured by a gunshot!",
				"@{} got lost!",
			]
		}

	

	async def add_user(self, ctx, user, *args):
		if self.collection_state:
			bet = int(args[0])
			if user in self.game_users:
				await ctx.send(f"@{user} You're already good to go.")

			else:
				self.game_users[user] = bet
				db.execute("UPDATE users SET Coins = Coins - ? WHERE UserID = ?", bet, user["id"])
				db.commit()
				await ctx.send(f"@{user} You're all suited and ready to go! Stand by for showtime...")
		else:
			await ctx.send("Heist is in progress. Not taking bets.")

	
	async def collect(self, ctx):
		await ctx.send("EVENT: Hiest is on! Enter your bets: !bet <bet amount>")
		self.running = True
		self.collection_state = True
		self.collection_time = time() + 30
		while True:
			await asyncio.sleep(1)
			if self.collection_time <= time():
				await self.start(ctx)
				break

	async def start(self, ctx):
		await ctx.send("The heist has started! Standby for results...")
		self.collection_state = False
		self.start_time = time() + randint(10, 20)
		while True:
			await asyncio.sleep(1)
			if self.start_time <= time():
				await self.end(ctx)
				break



	async def end(self, ctx):
		
		for user in self.game_users:
			await asyncio.sleep(1)
			bet = self.game_users[user]
			if randint(0, 1):
				self.succeeded.append((user, int(bet)*1.5))
				db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?", int(bet)*1.5 , user["id"])
				db.commit()
				await ctx.send(choice(self.messages["success"]).format(user))
			else:
				await ctx.send(choice(self.messages["fail"]).format(user))
		
	
		await asyncio.sleep(1)
		if len(self.succeeded) > 0:
			await ctx.send("The heist is over! The winners: " + ", ".join([f"{user} ({coins:,} coins)" for user, coins in self.succeeded]))
		else:
			await ctx.send("The heist was a failure! No one got out!")

		await asyncio.sleep(1)
		self.running = False




async def heist_run(self, ctx, *args):
	global gameObj

	if gameObj is None:

		gameObj = Heist()
		gameObj.running = True
		await gameObj.collect(ctx)

		while True:
			await asyncio.sleep(1)
			if gameObj.running == False:
				await heist_end(self, ctx)
				break
	else:	

		await ctx.send("A game is currently in session")


async def heist_end(self, ctx):
	global gameObj
	gameObj = None