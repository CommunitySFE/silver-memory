import discord
import logging

from discord.ext import commands

from .env import MAINTAINERS

def is_maintainer():
    """Check whether the context was created by a maintainer."""
    async def predicate(ctx):
        for id in MAINTAINERS:
            if id == str(ctx.author.id):
                return True
        return False

    return commands.check(predicate)


def is_in_guild(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id
    return commands.check(predicate)


class CommandPermissionError(commands.CommandError):
    def __init__(self, message, required_permission):
        self.message = message
        self.required_permission = required_permission


def perm_level(permission):
    """A check to test whether a user can run a command based on their permission level."""
    async def predicate(ctx):
        if type(ctx.author) is discord.Member:
            logging.getLogger("utils").debug(
                f"Checking permission for '{ctx.author.id}' - requires {permission}.")

            if await ctx.bot.permissions.has_permission(ctx.author, permission):
                return True
        raise CommandPermissionError(
            f"Lacking permission for command '{ctx.command.name}' - requires {permission}.",
            permission
        )

    return commands.check(predicate)