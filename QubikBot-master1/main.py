import discord
from discord.ext import commands
import os
import config


@config.client.command()
async def load(ctx, extension):
    if ctx.author.id == 396741075739607062 or 378974831330328586:
        config.client.load_extension(f"cogs.{extension}")
        await ctx.send("Cog загружен!")
    else:
        await ctx.send("Вы не разработчик бота!")


@config.client.command()
async def unload(ctx, extension):
    if ctx.author.id == 396741075739607062 or 378974831330328586:
        config.client.unload_extension(f"cogs.{extension}")
        await ctx.send("Cog разгружен!")
    else:
        await ctx.send("Вы не разработчик бота!")


@config.client.command()
async def reload(ctx, extension):
    if ctx.author.id == 396741075739607062 or 378974831330328586:
        config.client.unload_extension(f"cogs.{extension}")
        config.client.load_extension(f"cogs.{extension}")
        await ctx.send("Cog разгружен!")
    else:
        await ctx.send("Вы не разработчик бота!")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        config.client.load_extension(f"cogs.{filename[:-3]}")

config.client.run(config.token)
