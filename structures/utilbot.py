import logging
import motor.motor_asyncio

from discord.ext import commands

from utils.env import LOG_LEVEL, DATABASE_URI
from utils.permissions import PermissionsManager

class UtilBot(commands.Bot):
    """
    Wrapper class for SFE Utilities.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI).sfe_utilities

        self.logger = logging.getLogger("utils")
        self.logger.setLevel(int(LOG_LEVEL))

        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter(
            '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(sh)

        self.permissions = PermissionsManager(self)
