import config
import discord
import random
import os
import asyncio
from datetime import datetime


def status(ctx, author):
    roles = [i.id for i in author.roles]
    a = None
    for i in roles:
        if i in config.roles.values():
            a = i
    a = [i.name for i in ctx.guild.roles if i.id == a]
    if len(a) == 0:
        return "Пользователь"
    else:
        return a[0]


async def send_sys(ctx, event, des, colour, gif=None):
    emb = discord.Embed(title=event, description=des + "\n\n{} {}".format(status(ctx, ctx.author), ctx.author.mention),
                        colour=colour)
    file = None
    if gif:
        a = random.choice(os.listdir("./media/{}".format(gif)))
        file = discord.File("./media/{}/{}".format(gif, a), filename=a)
        emb.set_image(url="attachment://{}".format(a))
    a = await ctx.send(embed=emb, file=file)
    await asyncio.sleep(15)
    await ctx.channel.delete_messages([a, ctx.message])


async def send_log(ctx, event, des, colour):
    emb = discord.Embed(title=event, description=des + "\n\n{} {} • {}".format(status(ctx, ctx.author),
                                                                               ctx.author.mention,
                                                                               datetime.now().strftime('%Y-%m-%d '
                                                                                                       '%H:%M:%S')),
                        colour=colour)
    log_channel = config.client.get_channel(896033770954706994)
    a = await log_channel.send(embed=emb)