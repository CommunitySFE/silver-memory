from discord.ext import commands
from discord import Member, Message

from structures.utilbot import UtilBot
from utils.checks import perm_level

class CustomCommands(commands.Cog):
    """
    Cog for the creation of custom commands.
    """
    def __init__(self, bot: UtilBot):
        self.bot = bot
        self.db = bot.db
        self.logger = bot.logger

        self.custom_commands = []

    async def get_active_custom_commands(self):
        """
        Find active custom commands.
        """
        custom_commands = []
        active_command_objects = await self.db.commands.find({
            'active': True
        })

        for command in active_command_objects:
            custom_commands.append(command)

        return custom_commands

    async def reload_custom_commands(self):
        # Reset the custom command storage
        self.custom_commands = []
        # Fetch active custom commands from database
        self.custom_commands = await self.get_active_custom_commands()

        self.logger.debug("Custom commands reloaded.")

    def is_donator(self, member):
        return self.config.donator_plus_role in member.roles

    @commands.group("cc")
    @perm_level(0)
    async def cc(self, ctx: commands.Context):
        await ctx.send("Valid sub-commands: `none uwu`")

    @cc.command(name="create")
    @perm_level(0)
    async def create_command(self, ctx: commands.Context):
        if ctx.guild is None:
            return

        if not self.is_donator(ctx.member):
            await ctx.send(':no_entry_sign: Sorry, but you must have Donator+ to use this command. Please get Donator+ at ' +
                '<https://www.paypal.com/pools/c/8iCBNxzoRJ> to get custom command permissions for SFE.')
            return

        if len(name) < 3:
            await ctx.send(':no_entry_sign: please make a longer name.')
            return

        previous_custom_command = await self.db.commands.find_one({
            '$or': [{
                'name': name
            }, {
                'author': ctx.author.id
            }]
        })

        if previous_custom_command is not None:
            await ctx.send(':no_entry_sign: you either already have a custom command or have created a custom command before.')
            return
        
        await self.db.commands.insert_one({
            'active': False,
            'name': name,
            'content': '[content not set]',
            'author': event.msg.author.id
        })

        await ctx.send(':ok_hand: custom command created successfully. you can change the content using `.cc setcontent <content>`')
    
    @cc.command(name="setcontent")
    @perm_level(0)
    async def set_command_content(self, ctx: commands.Context, *, content: str):
        if ctx.guild is None:
            return

        if not self.is_donator(event.msg.member):
            await ctx.send(':no_entry_sign: Sorry, but you must have Donator+ to use this command. Please get Donator+ at ' +
                '<https://www.paypal.com/pools/c/8iCBNxzoRJ> to get custom command permissions for SFE.')
            return

        if len(content) <= 2:
            await ctx.send(':no_entry_sign: you need at least 3 characters of content.')
            return

        previous_custom_command = await self.db.commands.find_one({
            'author': event.msg.author.id
        })

        if previous_custom_command is None:
            await ctx.send(':no_entry_sign: you don\'t have an inactive custom command. you can create one using `.cc create <name>`.')
            return
        
        if '@everyone' in content or '@here' in content:
            await ctx.send(':no_entry_sign: do not attempt to mention everyone in your command content.')
            return
        
        await self.db.commands.update_one({
            '_id': previous_custom_command['_id']
        }, {
            '$set': {
                'content': content
            }
        })

        if not previous_custom_command['active']:
            await ctx.send(':ok_hand: content updated. for your command to go live, you\'ll have to ask for approval.')
        else:
            self.reload_custom_commands()
            await ctx.send(':ok_hand: command content updated successfully.')

    @cc.command(name="setactive")
    @perm_level(3)
    async def set_command_active(self, event, name: str):
        custom_command = await self.db.commands.find_one({
            'name': name
        })

        if custom_command is None:
            await ctx.send(':no_entry_sign: could not find custom command with that name.')
            return
        
        await self.db.commands.update_one({
            '_id': custom_command['_id']
        }, {
            '$set': {
                'active': True
            }
        })

        self.reload_custom_commands()
        
        await ctx.send(':ok_hand: command is now active.')
    
    @cc.command(name="blacklist")
    @perm_level(0)
    async def blacklist_user_from_command(self, ctx: commands.Context, user: Member):
        custom_command = await self.db.commands.find_one({
            'author': event.msg.author.id
        })

        if custom_command is None:
            await ctx.send(":no_entry_sign: you don't have a custom command.")
            return

        if custom_command['author'] == user.id:
            await ctx.send(":no_entry_sign: you cannot blacklist yourself.")
            return
        
        blacklist = []

        if custom_command.get('blacklisted_users') is not None:
            blacklist = custom_command['blacklisted_users']
        
        if user.id in blacklist:
            blacklist.remove(user.id)
        else:
            blacklist.append(user.id)

        await self.db.commands.update_one({
            '_id': custom_command['_id']
        }, {
            '$set': {
                'blacklisted_users': blacklist
            }
        })

        self.reload_custom_commands()

        await ctx.send(':ok_hand: blacklist toggled for {user} (`{id}`).'.format(user=str(user), id=user.id))
    
    @cc.command(name="whitelist")
    @perm_level(0)
    async def whitelist_user_for_command(self, ctx: commands.Context, user: Member):
        custom_command = await self.db.commands.find_one({
            'author': event.msg.author.id
        })

        if custom_command is None:
            await ctx.send(":no_entry_sign: you don't have a custom command.")
            return
        
        if custom_command['author'] == user.id:
            await ctx.send(":no_entry_sign: you cannot whitelist yourself.")
            return
        
        whitelist = []

        if custom_command['whitelisted_users'] is not None:
            if custom_command['whitelisted_users'] == 'all':
                await ctx.send(':no_entry_sign: whitelist is not enabled. please enable it using `.cc togglewhitelist`.')
                return
            whitelist = custom_command['whitelisted_users']
        
        if user.id in whitelist:
            whitelist.remove(user.id)
        else:
            whitelist.append(user.id)

        await self.db.commands.update_one({
            '_id': custom_command['_id']
        }, {
            '$set': {
                'whitelisted_users': whitelist
            }
        })

        await self.reload_custom_commands()
        await ctx.send(':ok_hand: whitelist toggled for {user} (`{id}`).'.format(user=str(user), id=user.id))
    
    @cc.command(name="togglewhitelist")
    @perm_level(0)
    async def toggle_command_whitelist(self, ctx: commands.Context):
        custom_command = await self.db.commands.find_one({
            'author': ctx.author.id
        })

        if custom_command is None:
            await ctx.send(":no_entry_sign: you don't have a custom command.")
            return

        whitelist = None

        if custom_command.get('whitelisted_users') is None or type(custom_command.get('whitelisted_users')) == str:
            whitelist = [ctx.author.id]
        else:
            whitelist = 'all'

        await self.db.commands.update_one({
            '_id': custom_command['_id']
        }, {
            '$set': {
                'whitelisted_users': whitelist
            }
        })

        self.reload_custom_commands()
        await ctx.send(':ok_hand: whitelist successfully toggled.')

    @cc.command(name="forcereload")
    @perm_level(3)
    async def force_custom_command_reload(self, ctx):
        await self.reload_custom_commands()
        await ctx.send(':ok_hand: custom commands reloaded.')
    
    @cc.command(name="delete")
    @perm_level(0)
    async def delete_custom_command(self, ctx):
        custom_command = await self.db.commands.find_one({
            'author': ctx.author.id
        })

        if custom_command is None:
            return await ctx.send(":no_entry_sign: you don't have a custom command.")

        was_active = custom_command['active']
        await self.db.commands.delete_one({
            '_id': custom_command['_id']
        })

        if was_active:
            self.reload_custom_commands()

        await ctx.send(':ok_hand: custom command removed successfully.')
    
    @cc.command(name="forcedelete")
    async def force_delete_custom_command(self, ctx, name: str):
        custom_command = await self.db.commands.find_one({
            'name': name
        })

        if custom_command is None:
            return await ctx.send(":no_entry_sign: couldn't find a custom command with that name.")

        was_active = custom_command['active']
        await self.db.commands.delete_one({
            '_id': custom_command['_id']
        })

        if was_active:
            self.reload_custom_commands()

        await ctx.send(':ok_hand: custom command removed successfully.')

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.guild is None:
            return

        if message.author.bot:
            return
        
        if not message.content.startswith('.'):
            return
        
        for command in self.custom_commands:
            if command.get("name") is None or command.get("content") is None:
                self.logger.warn("WARNING: Custom commands must have a name and content value.")
                continue
            if not message.content.lower().startswith(".%s" % command.get("name").lower()):
                continue
            if command.get('whitelisted_users') is not None:
                if type(command.get('whitelisted_users')) is str:
                    if not command.get('whitelisted_users') == 'all':
                        break
                else:
                    if not message.author.id in command.get('whitelisted_users') and not message.member.permissions.can("ADMINISTRATOR"):
                        break
            if command.get('blacklisted_users') is not None:
                if message.author.id in command.get('blacklisted_users') and not message.member.permissions.can("ADMINISTRATOR"):
                    break
            content = command.get("content")
            command_name_length = len(command.get("name").split(" "))
            split_command = message.content.split(" ")
            for i in range(command_name_length - 1, len(split_command)):
                if '@everyone' in split_command[i] or '@here' in split_command[i]:
                    message.channel.send(":no_entry_sign: cannot mention everyone/here in command arguments.")
                    return
                content = content.replace("${%s}" % (i), split_command[i])
            if '${...}' in content:
                split_command.pop(0)
                content = content.replace('${...}', ' '.join(split_command))
                if '@everyone' in content or '@here' in content:
                    message.channel.send(":no_entry_sign: cannot mention everyone/here in command arguments.")
                    return
            if self.command_cooldowns.get(command.get('name'), 0) + 20 > time.time():
                await message.add_reaction('⏱')
                return
            self.command_cooldowns[command.get('name')] = time.time()
            await message.channel.send(content)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.reload_custom_commands()

def setup(bot):
    bot.add_cog(CustomCommands(bot))
