from time import time
from random import randint, choice
import asyncio

from . import db

gameObj = None


async def bet(ctx, user, *args):
    if gameObj is not None:
        if gameObj.running == True:
            await gameObj.add_user(ctx, user, *args)
    else:
        await ctx.send("There is not game in session")


async def coinflip(ctx, *args):
    print(args[0])


################
# HEIST
################

class Heist:
    def __init__(self):
        self.running = False
        self.collection_time = time() + 60
        self.collection_state = False
        self.run_time = time()
        self.bet_multiplier = 1.5
        self.playerSucceeded = []
        self.playerList = {}

        self.messages = {
            "success": [
                "@{} fought off the guards, and got their haul!",
                "@{} sneaked out of the back entrance with their share!",
                "@{} got in and out seemlessly with their money!",
            ],
            "fail": [
                "@{} got caught by the guards!",
                "@{} was injured by a gunshot!",
                "@{} got lost!",
            ]
        }

    async def run(self, ctx):
        await ctx.send("HIEST is ready to begin. Enter your bets: !bet <bet amount>")
        self.running = True
        self.collection_state = True

        while True:
            await asyncio.sleep(1)
            if self.collection_time <= time():
                await self.start(ctx)
                break

    async def start(self, ctx):
        await ctx.send("The heist has started! Let's see who escapes...")
        self.collection_state = False
        self.run_time = time() + randint(10, 30)

        while True:
            await asyncio.sleep(1)
            if self.run_time <= time():
                await self.end(ctx)
                break

    async def end(self, ctx):
        if len(self.playerList) > 0:
            for player in self.playerList:
                await asyncio.sleep(1)
                bet = self.playerList[player]['bet']
                if randint(0, 1):
                    self.playerSucceeded.append((player, int(bet) * 1.5))
                    db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?", int(bet) * 1.5,
                               self.playerList[player]['id'])
                    db.commit()
                    await ctx.send(choice(self.messages["success"]).format(player))
                else:
                    await ctx.send(choice(self.messages["fail"]).format(player))
        else:
            await ctx.send("We all feared to do the heist....")


async def heist(ctx):
    global gameObj
    gameObj = Heist()
    await gameObj.run(ctx)

    while True:
        await asyncio.sleep(1)
        if gameObj.running is False:
            gameObj = None
