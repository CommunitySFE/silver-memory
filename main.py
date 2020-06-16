import os

from structures.utilbot import UtilBot
from utils.env import TOKEN

bot = UtilBot(command_prefix="!",
              description="Utility commands & sthuff idk don't @ me")

try:
    bot.run(TOKEN, bot=True, reconnect=True)
except InterruptedError as e:
    bot.logger.exception("Failed to initialize bot:")
    raise e
