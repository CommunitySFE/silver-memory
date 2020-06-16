import logging
import os
import signal
import traceback

from discord.ext import commands

import motor.motor_asyncio
from utils.env import DATABASE_URI, LOG_LEVEL
from utils.permissions import PermissionsManager


class UtilBot(commands.Bot):
    """
    Wrapper class for SFE Utilities.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = logging.getLogger("utils")
        self.logger.setLevel(int(LOG_LEVEL))

        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter(
            '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(sh)

        self.logger.debug("Setting up database...")
        self.db = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI).sfe_utilities

        self.logger.debug("Setting up permissions...")
        self.permissions = PermissionsManager(self)

    async def on_ready():
        # Console write when bot starts
        self.logger.info(
            f'\n\nLogged in as: {self.user.name} - {self.user.id}\n')

        # load cogs
        cog_count = 0
        self.logger.debug(f"Cogs to load: {','.join(os.listdir('./cogs'))}")

        for cog in os.listdir('./cogs'):
            if cog.startswith('__'):
                continue
            else:
                ext = "cogs." + cog.replace(".py", "")
                try:
                    self.logger.info(f"Loading {ext}...")
                    self.load_extension(ext)
                    cog_count += 1
                except Exception as e:
                    error = "".join(traceback.format_exception(
                        type(e), e, e.__traceback__))
                    self.logger.exception(f'Failed to load ext {ext}.\n{error}')

        self.logger.debug(f"Successfully loaded {cog_count} cogs.")

        self.logger.info("Init complete.")
        self.logger.info('------')

    async def on_command_error(self, ctx, error):
        """
        The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # commands.UserInputError
        ignored = (commands.CommandNotFound)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error, CommandPermissionError):
            try:
                return await ctx.send(embed=discord.Embed(
                    description=":x: You don't have permission to run this command.",
                    color=discord.Color(0xff5555)
                ))
            except Exception:
                pass

        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f":x: {ctx.command} is missing required argument {error.param}.")

        elif isinstance(error, commands.BadArgument):
            return await ctx.send(f":x: {ctx.command} {error}")

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f':x: {ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f':x: {ctx.command} can not be used in Private Messages.')
            except Exception:
                pass

        elif isinstance(error, commands.NotOwner):
            return await ctx.send(error)

        # All other Errors not returned come here... And we can just print the default TraceBack.
        self.logger.exception('Ignoring exception in command {}:'.format(
            ctx.command)
        )
        error = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        self.logger.exception(error)


def signal_handler(sig, frame):
    """
    Gracefully shut down the bot when SIGINT signal is received. Not sure if this actually
    makes a difference lol.
    """
    bot.logger.info("Exit request received - shutting down...")
    run_coroutine_threadsafe(bot.logout(), bot.loop)
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
