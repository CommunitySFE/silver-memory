from .utilbot import UtilBot

class CustomCommand:
    """
    Utility class for fetching and storing custom commands.
    """

    @staticmethod
    async def fetch_custom_commands(bot: UtilBot):
        custom_commands = []

        async for cmd in await bot.db.commands.find({}):
            custom_commands += CustomCommand.from_dict(bot, cmd)

    @staticmethod
    def from_dict(bot, dict):
        return CustomCommand(
            bot,
            dict.get("user"),
            dict.get("name"),
            dict.get("whitelisted"),
            dict.get("fmt")
        )

    def __init__(self, bot: UtilBot, user, name, whitelisted, fmt):
        self.bot = bot
        self.user = user
        self.name = name
        self.whitelisted = whitelisted
        self.fmt = fmt

    def whitelist(user):
        """
        Whitelist a user.
        """
        self.whitelisted += user
