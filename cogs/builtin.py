from discord.ext import commands
from discord import Member

from utils.checks import perm_level

class BuiltinCommands(commands.Cog):
    """
    Built-in fun commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hug")
    @perm_level(0)
    async def hug_command(self, ctx, member: Member):
        await ctx.message.delete()

        if not member:
            return await ctx.send(
                "<@{a}> tried to hug nobody, but the **V O I D** was unable to do anything, and could only stare back in return.".format(
                    a=event.author.id)
            )

        else:
            message = random.choice(self.config.hug_phrases)
            return await ctx.send(message.format(
                a=str(ctx.author.id),
                b=str(member.id)
            ))

    @commands.command(name="fight")
    @perm_level(0)
    async def fight_command(self, ctx, person: Member):
        message = random.choice(self.config.fight_phrases)
        await ctx.send(message.format(
            a=str(ctx.author.id),
            b=str(person.id)
        ))


    @commands.command(name="pat")
    async def pat(self, ctx, member=None):
        await ctx.message.delete()

        if not member:
            self.config.pat_dissipation_count += 1
            return await ctx.reply(
                "<@{a}> tried to give nobody a pat, but the energy was dissipated into the **V O I D.** (`{b}` wasted pats)"
                .format(a=ctx.author.id, b=self.config.pat_dissipation_count)
            )
    
        elif member.id == ctx.author.id:
            return await ctx.reply(
                ":negative_squared_cross_mark: You can't pat yourself, you fool."
            )
        else:
            pat_amount = self.config.pat_records.get(member.id)
            if not pat_amount:
                pat_amount = 1
                self.config.pat_records[member.id] = 1

            self.config.pat_records[member.id] += 1

            if self.config.pat_ping_records.get(member.id) or self.config.pat_ping_records.get(member.id) is None:
                return await ctx.reply(
                    "<@{a}> gave <@{b}> a pat! (`{c}`)"
                    .format(a=ctx.author.id, b=member.id, c=pat_amount)
                )
            else:
                return await ctx.reply(
                    "<@{a}> gave {b} a pat! (`{c}`)"
                    .format(a=ctx.author.id, b=member.tag, c=pat_amount)
                )

    @commands.command(name="poptart", aliases=["cat"])
    @perm_level(0)
    async def poptart(self, ctx, ping=None, noun=str):
        """This is the poptart command - Given to Poptart for most messages in a giveaway. Move to CC?"""

        if ping and ctx.author.id == 116757237262843906:
            if ping == 1:
                await ctx.message.delete()
                self.config.cat_should_ping = False
                await ctx.send(":ok_hand: Disabled pings. Enjoy your day, you fine cat.")
                return
            elif ping == 2:
                await ctx.message.delete()
                self.config.cat_should_ping = True
                await ctx.send(":ok_hand: Enabled pings. Enjoy your day, you fine cat.")
                return
            elif ping == 3:
                if noun:
                    await ctx.message.delete()
                    self.config.cat_noun = noun
                    await ctx.send(":ok_hand: Noun set to {a}. Enjoy your day, you fine cat.".format(
                        a=str(self.config.cat_noun)))
                else:
                    await ctx.send(":negative_squared_cross_mark: Expecting a string.")
                return
            elif ping == 4:
                await ctx.message.delete()
                if "@everyone" in noun or "@here" in noun:
                    await ctx.send("no can do")
                await ctx.send("**PSA: {a}**".format(a=str(noun)))
                return
            elif ping == 5:
                await ctx.message.delete()
                if not noun.isdigit():
                    await ctx.send(":no_entry_sign: invalid user id")
                    return
                cat_ids = self.config.cat_ids
                cat_ids.append(int(noun))
                self.config.cat_ids = cat_ids
                await ctx.send(":ok_hand: added {user_id} to whitelisted cat IDs".format(user_id=noun))
            elif ping == 6:
                await ctx.message.delete()
                if not noun.isdigit():
                    await ctx.send(":no_entry_sign: invalid user id")
                    return
                self.config.cat_ids.remove(int(noun))
                await ctx.send(":ok_hand: removed {user_id} from whitelisted cat IDs".format(user_id=noun))
            else:
                return await ctx.send(":negative_squared_cross_mark: Expecting 1-6.")

        if ctx.author.id not in self.config.cat_ids:
            return

        await ctx.message.delete()

        if self.config.cat_should_ping:
            await ctx.send(
                "**PSA: <@116757237262843906> is the {a} here.**".format(a=str(self.config.cat_noun)))
        else:
            await ctx.send(
                "**PSA: Cat is the {a} here.**".format(a=str(self.config.cat_noun)))

def setup(bot):
    bot.add_cog(BuiltinCommands(bot))
