from discord.ext import commands
from discord import Member

from utils.checks import perm_level

class BuiltinCommands(commands.Cog):

    pat_dissipation_count = 0
    pat_records = {}
    pat_ping_records = {}
    noot_record = 0

    cat_ids = [
        116757237262843906,  # Poptart
        137919409644765184,  # Jess
        150662786257518592,  # Zach
        156670353282695168,  # Critiql
        210118905006522369,  # Ori
        210540648128839680,  # Guffuffle
        249462738257051649,  # Lost
        303502679089348608,  # 1A3
        390906358259777536,  # CustomName
        436481695617777665   # Tiller
    ]

    cat_should_ping = True

    cat_noun = "coolest cat"

    hug_phrases = [
        "<@{a}> gave <@{b}> a big big hug!",
        "With a great big hug from <@{a}>\nand a gift from me to you\nWon't you say you love me too <@{b}>?",
        "<@{a}> dabbed on <@{b}> haters and gave them a hug.",
        "<@{b}> unexpectedly received a big hug from <@{a}>",
        "<@{a}> reached out their arms, wrapped them around <@{b}> and gave them a giant hug!"
    ]
    fight_phrases = [
        "<@{a}> fought with <@{b}> with a large fish.",
        "<@{a}> tried to fight <@{b}>, but it wasn't very effective!",
        "<@{a}> fought <@{b}>, but they missed.",
        "<@{a}> fought <@{b}> with a piece of toast.",
        "<@{a}> and <@{b}> are fighting with a pillow.",
        "<@{a}> aimed but missed <@{b}> by an inch.",
        "<@{b}> got duck slapped by <@{a}>",
        "<@{a}> tried to dab on <@{b}> but they tripped, fell over, and now they need @ someone",
        "<@{b}> was saved from <@{a}> by wumpus' energy!",
        "Dabbit dabbed on <@{b}> from a request by <@{a}>!",
        "CustomName banned <@{a}> for picking a fight with <@{b}>!",
        "<@{a}> joined the game.\n<@{a}>: That's not very cash money of you.\n<@{b}>: What\nCONSOLE: <@{b}> was banned by an operator.\n<@{b}> left the game.",
        "<@{b}> tied <@{a}>’s shoelaces together, causing them to fall over.",
        "You are the Chosen One <@{a}>. You have brought balance to this world. Stay on this path, and you will do it again for the galaxy. But beware your heart said master <@{b}>",
        "<@{a}> used 'chat flood'. It wasn't very effective, so <@{b}> muted them."
    ]

    donator_plus_role = 627562670303739905

    custom_commands = []
    
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
            message = random.choice(self.hug_phrases)
            return await ctx.send(message.format(
                a=str(ctx.author.id),
                b=str(member.id)
            ))

    @commands.command(name="fight")
    @perm_level(0)
    async def fight_command(self, ctx, person: Member):
        message = random.choice(self.fight_phrases)
        await ctx.send(message.format(
            a=str(ctx.author.id),
            b=str(person.id)
        ))


    @commands.command(name="pat")
    async def pat(self, ctx, member: Member):
        await ctx.message.delete()

        if not member:
            self.pat_dissipation_count += 1
            return await ctx.send(
                "<@{a}> tried to give nobody a pat, but the energy was dissipated into the **V O I D.** (`{b}` wasted pats)"
                .format(a=ctx.author.id, b=self.pat_dissipation_count)
            )
    
        elif member.id == ctx.author.id:
            return await ctx.send(
                ":negative_squared_cross_mark: You can't pat yourself, you fool."
            )
        else:
            pat_amount = self.pat_records.get(member.id)
            if not pat_amount:
                pat_amount = 1
                self.pat_records[member.id] = 1

            self.pat_records[member.id] += 1

            if self.pat_ping_records.get(member.id) or self.pat_ping_records.get(member.id) is None:
                return await ctx.send(
                    "<@{a}> gave <@{b}> a pat! (`{c}`)"
                    .format(a=ctx.author.id, b=member.id, c=pat_amount)
                )
            else:
                return await ctx.send(
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
                self.cat_should_ping = False
                await ctx.send(":ok_hand: Disabled pings. Enjoy your day, you fine cat.")
                return
            elif ping == 2:
                await ctx.message.delete()
                self.cat_should_ping = True
                await ctx.send(":ok_hand: Enabled pings. Enjoy your day, you fine cat.")
                return
            elif ping == 3:
                if noun:
                    await ctx.message.delete()
                    self.cat_noun = noun
                    await ctx.send(":ok_hand: Noun set to {a}. Enjoy your day, you fine cat.".format(
                        a=str(self.cat_noun)))
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
                cat_ids = self.cat_ids
                cat_ids.append(int(noun))
                self.cat_ids = cat_ids
                await ctx.send(":ok_hand: added {user_id} to whitelisted cat IDs".format(user_id=noun))
            elif ping == 6:
                await ctx.message.delete()
                if not noun.isdigit():
                    await ctx.send(":no_entry_sign: invalid user id")
                    return
                self.cat_ids.remove(int(noun))
                await ctx.send(":ok_hand: removed {user_id} from whitelisted cat IDs".format(user_id=noun))
            else:
                return await ctx.send(":negative_squared_cross_mark: Expecting 1-6.")

        if ctx.author.id not in self.cat_ids:
            return

        await ctx.message.delete()

        if self.cat_should_ping:
            await ctx.send(
                "**PSA: <@116757237262843906> is the {a} here.**".format(a=str(self.cat_noun)))
        else:
            await ctx.send(
                "**PSA: Cat is the {a} here.**".format(a=str(self.cat_noun)))

def setup(bot):
    bot.add_cog(BuiltinCommands(bot))
