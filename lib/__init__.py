from . import react
from . import games

game_commands = {
    "heist": games.heist,
}


async def startgame(self, ctx, *args):
    game = args[0]
    if game in game_commands:
        await game_commands[game](ctx, *args)
    else:
        ctx.send("/me Game does not exist.")