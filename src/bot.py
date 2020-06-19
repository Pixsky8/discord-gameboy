import discord
import asyncio
import config
import os
import io
from pyboy import PyBoy, WindowEvent
from pyboy.botsupport import BotSupportManager

class Game:
    gb = None
    bot_supp = None
    channel = None
    pause = True


print("Bot is starting...")

client = discord.Client()
config = config.Config()
### Uncomment the next line if you do not want to use docker.
#config.is_docker = False
game = Game()
input_list = {'a': WindowEvent.PRESS_BUTTON_A,
         'b': WindowEvent.PRESS_BUTTON_B,
         'up': WindowEvent.PRESS_ARROW_UP,
         'down': WindowEvent.PRESS_ARROW_DOWN,
         'left': WindowEvent.PRESS_ARROW_LEFT,
         'right': WindowEvent.PRESS_ARROW_RIGHT,
         'start': WindowEvent.PRESS_BUTTON_START,
         'select': WindowEvent.PRESS_BUTTON_SELECT}


def tick_times(game, n):
    for i in range(n):
        game.gb.tick()

async def timer(client, game):
    await client.wait_until_ready()
    while True:
        if game.gb and not game.pause:
            tick_times(game, 60)

            game.gb.send_input(WindowEvent.RELEASE_BUTTON_START)
            game.gb.send_input(WindowEvent.RELEASE_BUTTON_SELECT)
            game.gb.send_input(WindowEvent.RELEASE_BUTTON_B)
            game.gb.send_input(WindowEvent.RELEASE_BUTTON_A)
            game.gb.send_input(WindowEvent.RELEASE_ARROW_DOWN)
            game.gb.send_input(WindowEvent.RELEASE_ARROW_LEFT)
            game.gb.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
            game.gb.send_input(WindowEvent.RELEASE_ARROW_UP)

            arr = io.BytesIO()
            game.bot_supp.screen().screen_image().save(arr, format='PNG')
            arr.seek(0)
            file = discord.File(arr, "image.png")
            await game.channel.send("", file=file)
        await asyncio.sleep(1)

@client.event
async def on_ready():
    if config.is_docker:
        os.system("echo \"We have logged in as {0.user}\"".format(client))
    else:
        print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.startswith(config.prefix):
            text = message.content[config.prefix_len:]
            
            if text.startswith("run"):
                game.gb = PyBoy("data/PokemonRouge.gb")
                game.bot_supp = game.gb.botsupport_manager()
                game.gb.set_emulation_speed(4)
                game.channel = message.channel
                game.pause = False
                await message.channel.send("Starting: " + game.gb.cartridge_title())

            elif text.startswith("stop"):
                game.gb.stop()
                game.channel = None
                game.bot_supp = None
                game.gb = None
                game.pause = True

            elif text.startswith("pause"):
                game.gb.send_input(WindowEvent.PAUSE)
                game.pause = True
            elif text.startswith("unpause"):
                game.gb.send_input(WindowEvent.PAUSE)
                game.pause = False

            elif text.startswith("name"):
                await message.channel.send("Running: " + game.gb.cartridge_title())

            elif text in input_list.keys() and message.channel == game.channel:
                game.gb.send_input(input_list[text])

client.loop.create_task(timer(client, game))
client.run(config.token)
