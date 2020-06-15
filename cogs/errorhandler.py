import sys
import traceback

import discord
from discord.ext import commands

from utils import CommandPermissionError


"""
If you are not using this inside a cog, add the event decorator e.g:
@bot.event
async def on_command_error(ctx, error)
For examples of cogs see:
Rewrite:
https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
Async:
https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5
This example uses @rewrite version of the lib. For the async version of the lib, simply swap the places of ctx, and error.
e.g: on_command_error(self, error, ctx)
For a list of exceptions:
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#errors
"""


class CommandErrorHandler(commands.Cog):
    """Handles errors in a standard fashion."""

    def __init__(self, bot):
        self.bot = bot
        self.bot.logger.info('ErrorHandler loaded!')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

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
            # await ctx.message.add_reaction('❌')
            # @callidus is this a bad idea to do?
            return await ctx.send(f":x: {ctx.command} is missing required argument {error.param}.")

        elif isinstance(error, commands.BadArgument):
            # await ctx.message.add_reaction('❌')
            return await ctx.send(f":x: {ctx.command} {error}")

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f':x: {ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f':x: {ctx.command} can not be used in Private Messages.')
            except Exception:
                pass

        # commented out because I am not sure what it does
        # # For this error example we check to see where it came from...
        # elif isinstance(error, commands.BadArgument):
        #     if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
        #         return await ctx.send(':x: I could not find that member. Please try again.')

        elif isinstance(error, commands.NotOwner):
            return await ctx.send(error)

        # All other Errors not returned come here... And we can just print the default TraceBack.
        self.bot.logger.exception('Ignoring exception in command {}:'.format(
            ctx.command)
        )
        error = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        self.bot.logger.exception(error)

        channel = self.bot.get_channel(623247355575009331)
        if channel:
            await channel.send(
                f"```py\n{error[-1950:]}\n```"
            )

    # """Below is an example of a Local Error Handler for our command do_repeat"""
    # @commands.command(name='repeat', aliases=['mimic', 'copy'])
    # async def do_repeat(self, ctx, *, inp: str):
    #     """A simple command which repeats your input!
    #     inp  : The input to be repeated"""

    #     await ctx.send(inp)

    # @do_repeat.error
    # async def do_repeat_handler(self, ctx, error):
    #     """A local Error Handler for our command do_repeat.
    #     This will only listen for errors in do_repeat.

    #     The global on_command_error will still be invoked after."""

    #     # Check if our required argument inp is missing.
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         if error.param.name == 'inp':
    #             await ctx.send("You forgot to give me input to repeat!")


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))