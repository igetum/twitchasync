
from collections import defaultdict
from datetime import datetime, timedelta
from random import randint
from re import search
from time import time

from lib import db

welcomed = []
messages = defaultdict(int)

async def process(message):
	ctx = message.channel
	user = {"name": message.author.name, "id": message.author.id}
	
	await update_records(ctx, user)
	await check_activity(ctx, user)
	await add_user(user)
		


async def update_records(ctx, user):
	db.execute("UPDATE users SET UserName = ?, MessagesSent = MessagesSent + 1 WHERE UserID = ?",
		user["name"].lower(), user["id"])
	db.commit()

async def add_user(user):
	db.execute("INSERT OR IGNORE INTO users (UserID, UserName, Coins) VALUES (?, ?, ?)", user["id"], user["name"].lower(), 100)
	db.commit()

async def say_goodbye(ctx, user):
	await ctx.send(f"See ya later {user['name']}!")
	welcomed.remove(user["id"])


async def check_activity(ctx, user):
	messages[user["id"]] += 1

	if (count := messages[user["id"]]) % 20 == 0:
		ctx.send(f"Thanks for being active in chat {user['name']} - you've sent {count:,} messages! Keep it up!")


async def thank_for_cheer(ctx, user, match):
	await ctx.send(f"Thanks for the {match.group[5:]:,} bits {user['name']}! That's really appreciated!")