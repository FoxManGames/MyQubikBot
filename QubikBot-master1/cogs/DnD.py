import discord
from discord.ext import commands
import config
import random


fight = {}
fight_flag = False
info_message = discord.Message
window = []


class DnD(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @config.fight()
    async def start(self, ctx: commands.Context):
        fight.clear()
        await ctx.channel.purge(limit=None, check=(lambda b: True))
        dnd_info = discord.Embed(title="Активированно", colour=discord.Colour.blue())
        for i in config.dnd_info:
            dnd_info.add_field(name=i[0], value="\n".join([' - '.join([k, v]) for k, v in i[1].items()]))
        global info_message
        info_message = await ctx.channel.send(embed=dnd_info)
        global fight_flag
        fight_flag = True
        for i in config.dnd_info:
            for j in i[1].keys():
                await info_message.add_reaction(j)

    async def on_message(self, message: discord.Message):
        if fight_flag and message.channel == info_message.channel and message.author.id != config.client.user.id:
            await self.ctrl_window(message)
        await config.client.process_commands(message)

    async def ctrl_window(self, message: discord.Message):
        window.append(message)
        while len(window) > 5:
            try:
                await window[0].delete()
            except discord.NotFound:
                pass
            window.pop(0)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id != config.client.user.id and payload.message_id == info_message.id:
            await self.emoji_roll(payload)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.user_id != config.client.user.id and payload.message_id == info_message.id:
            await self.emoji_roll(payload)

    async def emoji_roll(self, payload: discord.RawReactionActionEvent):
        n = ""
        v = ""
        for i in config.dnd_info:
            if payload.emoji.name in i[1]:
                n = i[0]
                v = i[1][payload.emoji.name]
        if n == "" and v == "":
            return
        guild = config.client.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        member = await guild.fetch_member(payload.user_id)
        await self.dnd_roll(12, 1, v, member.name, channel)

    async def ctrl_fight(self, member_n: str, par: str, r: int):
        if member_n in fight:
            fight[member_n]['0'] += 1
            if par in fight[member_n]:
                fight[member_n][par] += r
            else:
                fight[member_n][par] = r
        else:
            fight[member_n] = {'0': 1, par: r}

    async def dnd_roll(self, dice: int, num: int, par: str, member_n: str, channel: discord.TextChannel):
        emb = discord.Embed()
        if num != 1:
            s = 0
            for i in range(num):
                r = random.randint(1, dice)
                emb.add_field(name="Бросок №{}".format(i + 1), value=str(r))
                s += r
                await self.ctrl_fight(member_n, '1', r)
            emb.colour = discord.Color.green()
            emb.title = "{} выпало {}".format(member_n, s)
            m = await channel.send(embed=emb)
            await self.ctrl_window(m)
        else:
            r = random.randint(1, dice)
            emb.title = "{} выпало {}/{}".format(member_n, r, dice)
            if par:
                emb.description = "на {}".format(par)

            if r < (dice - 1) / 4 + 1:
                emb.colour = discord.Colour.dark_red()
            elif r < (dice - 1) / 2 + 1:
                emb.colour = discord.Colour.orange()
            elif r < (dice - 1) * 3 / 4 + 1:
                emb.colour = discord.Colour.gold()
            else:
                emb.colour = discord.Colour.green()

            m = await channel.send(embed=emb)

            if fight_flag:
                await self.ctrl_window(m)
                await self.ctrl_fight(member_n, par, r)

                if (par in config.dnd_info[0][1].values() and r in [1, 7]) or (par == "меткость" and r in [1, 2, 7, 8]):
                    await self.dnd_roll(100, 1, "", member_n, channel)

    @commands.command()
    async def d(self, ctx: commands.Context, b: int, *args):
        if len(args) == 0:
            await self.dnd_roll(b, 1, "", ctx.author.name, ctx.channel)
        elif len(args) == 1 and args[0].isdigit():
            await self.dnd_roll(b, int(args[0]), "", ctx.author.name, ctx.channel)
        elif len(args) == 1 and args[0].isalpha():
            await self.dnd_roll(b, 1, args[0], ctx.author.name, ctx.channel)
        elif len(args) > 1 and args[0].isdigit():
            await self.dnd_roll(b, int(args[0]), ' '.join(args[1:]), ctx.author.name, ctx.channel)
        else:
            await self.dnd_roll(b, 1, ' '.join(args[1:]), ctx.author.name, ctx.channel)

    @commands.command()
    @config.fight()
    async def end(self, ctx: commands.Context):
        await ctx.channel.purge(limit=None, check=(lambda b: True))
        for i in fight:
            emb = discord.Embed(title=i, colour=discord.Colour.blue())
            a = 0
            for j in fight[i]:
                if j != '0':
                    a += fight[i][j]
                    if j not in ['1', ""]:
                        emb.add_field(name=j, value=fight[i][j])
            emb.description = "{:.1f}".format(a / fight[i]['0'])
            await ctx.channel.send(embed=emb)
        fight.clear()
        global fight_flag, info_message
        fight_flag = False
        info_message = discord.Message


def setup(client):
    client.add_cog(DnD(client))
    print("Cog DnD работает")
