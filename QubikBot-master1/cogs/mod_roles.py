import discord
from discord.ext import commands
import config
import util_func
import random


class roles_mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @config.createrole_p()
    async def createrole(self, ctx, color, *, name: str):
        role = 0
        for i in ctx.guild.roles:
            if i.name == name and i.color == discord.Color.from_rgb(config.colors[color][0], config.colors[color][1],
                                                                    config.colors[color][2]):
                role = i
        if color not in config.colors:
            color = random.choice(list(config.colors.keys()))
        color = color.lower()
        if role == 0:
            role = await ctx.guild.create_role(name=name, permissions=ctx.guild.roles[0].permissions,
                                               colour=discord.Color.from_rgb(config.colors[color][0],
                                                                             config.colors[color][1],
                                                                             config.colors[color][2]))
        await util_func.send_log(ctx, 'РОЛЬ СОЗДАНА!',
                                 'Роль {} успешно создана!'.format(name), discord.Color.green())
        await util_func.send_sys(ctx, 'Создание роли!',
                                 'Роль {} успешно создана!'.format(name), discord.Color.green())

    @commands.command()
    @config.addrole_p()
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):
        if role in member.roles:
            await util_func.send_sys(ctx, 'НЕ добавление роли',
                                     "{} {} не может быть **{}** дважды\nТакие вещи случаюся только раз в жизни)"
                                     .format(util_func.status(ctx, member), member.mention, role),
                                     discord.Color.orange())
        elif role in ctx.guild.roles:
            await member.add_roles(role)
            await util_func.send_log(ctx, 'РОЛЬ ДОБАВЛЕНА!',
                                     '{} {} теперь **{}**!'.format(util_func.status(ctx, member), member.mention, role),
                                     discord.Color.green())
            await util_func.send_sys(ctx, 'Добавление роли!',
                                     "{} {} теперь **{}**!\nПоздравляю! ... наверное"
                                     .format(util_func.status(ctx, member), member.mention, role),
                                     discord.Color.green())

    @commands.command()
    @config.removerole_p()
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        if role not in member.roles:
            await util_func.send_sys(ctx, 'НЕ свержение с роли',
                                     "{} {} не является **{}**...\nНу, приятель, ты ничего не потерял!)"
                                     .format(util_func.status(ctx, member), member.mention, role),
                                     discord.Color.orange())
        elif role in ctx.guild.roles:
            await member.remove_roles(role)
            await util_func.send_log(ctx, 'РОЛЬ ЗАБРАНА!',
                                     '{} {} теперь НЕ **{}**!'
                                     .format(util_func.status(ctx, member), member.mention, role),
                                     discord.Color.orange())
            await util_func.send_sys(ctx, 'Свержение с роли',
                                     "{} {} теперь НЕ **{}**\nНЕ поздравляю! ... наверное"
                                     .format(util_func.status(ctx, member), member.mention, role),
                                     discord.Color.orange())


def setup(client):
    client.add_cog(roles_mod(client))
    print("Cog roles_mod работает")
