import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime
import config


class fun_user(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rand(self, ctx, a: int, b: int, c: int = 1):
        emb = discord.Embed()
        if c == 1:
            r = random.randint(a, b)
            emb.title = "{} выпало {}".format(ctx.author.name, r)
        else:
            s = 0
            for i in range(c):
                r = random.randint(a, b)
                emb.add_field(name="Бросок №{}".format(i + 1), value=str(r))
                s += r
            emb.title = "{} выпало {}".format(ctx.author.name, s)
        emb.colour = discord.Color.green()
        a = await ctx.channel.send(embed=emb)
        await ctx.channel.delete_messages([a, ctx.message])

    @commands.command()
    async def mg_ball(self, ctx):
        emb = discord.Embed()
        emb.title = '{}, {}'.format(ctx.author.name, random.choice(config.magic_ball))
        emb.colour = discord.Color.dark_purple()
        a = await ctx.channel.send(embed=emb)
        await ctx.channel.delete_messages([a, ctx.message])

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member):
        delta_c = datetime.now() - member.created_at
        delta_j = datetime.now() - member.joined_at
        j = delta_j.days
        c = delta_c.days
        emb = discord.Embed(title='Информация о {}'.format(member.name), colour=discord.Color.purple())
        emb.add_field(name='Имя пользователя на сервере : ', value=member.display_name, inline=False)
        emb.add_field(name='Присоединился на сервер : ',
                      value=f'{member.joined_at.strftime("%d.%m.%Y %H:%M")}\n ({j} дней)', inline=False)
        emb.add_field(name='Аккаунт был создан : ',
                      value=f'{member.created_at.strftime("%d.%m.%Y %H:%M")}\n ({c} дней)', inline=False)
        emb.set_thumbnail(url=member.avatar_url)
        emb.set_footer(text='ID : {}'.format(member.id))
        a = await ctx.send(embed=emb)
        await asyncio.sleep(120)
        await ctx.channel.delete_messages([a, ctx.message])

    @commands.command()
    async def avatar(self, ctx, member: discord.Member):
        emb = discord.Embed(title='Аватарка {}'.format(member.name), colour=discord.Color.purple())
        emb.set_image(url=member.avatar_url)
        await asyncio.sleep(120)
        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(fun_user(client))
    print("Cog fun_user работает")
