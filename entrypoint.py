import os
import signal
import traceback

from asyncio import run_coroutine_threadsafe

from structures.utilbot import UtilBot
from utils.env import TOKEN

bot = UtilBot(command_prefix="!",
              description="Utility commands & sthuff idk don't @ me")


@bot.event
async def on_ready():
    # Console write when bot starts
    bot.logger.info(
        f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\n')

    # load cogs
    cog_count = 0
    bot.logger.debug(f"Cogs to load: {','.join(os.listdir('./cogs'))}")

    for cog in os.listdir('./cogs'):
        if cog.startswith('__'):
            continue
        else:
            ext = "cogs." + cog.replace(".py", "")
            try:
                bot.logger.info(f"Loading {ext}...")
                bot.load_extension(ext)
                cog_count += 1
            except Exception as e:
                error = "".join(traceback.format_exception(
                    type(e), e, e.__traceback__))
                bot.logger.exception(f'Failed to load extension {ext}.\n{error}')

    bot.logger.debug(f"Successfully loaded {cog_count} cogs.")


    bot.logger.info("Initialization complete.")
    bot.logger.info('------')


def signal_handler(sig, frame):
    bot.logger.info("Exit request received - shutting down...")
    run_coroutine_threadsafe(bot.logout(), bot.loop)
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    bot.run(TOKEN, bot=True, reconnect=True)
except InterruptedError as e:
    bot.logger.exception("Failed to initialize bot:")
    raise e
