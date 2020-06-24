from abc import ABC

from twitchio.ext import commands
from auth import client_id, irc_token, bot_nick, owner

import lib

welcomed = []


class Bot(commands.Bot, ABC):

    def __init__(self):
        super().__init__(irc_token=irc_token, client_id=client_id, nick=bot_nick, prefix='!', initial_channels=[owner])

    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.channel.send(f'Hello {ctx.author.name}!')

    @commands.command(name="startgame")
    async def startgame(self, ctx, *args):
        await lib.startgame(self, ctx, *args)


if __name__ == "__main__":
    bot = Bot()
    bot.run()
