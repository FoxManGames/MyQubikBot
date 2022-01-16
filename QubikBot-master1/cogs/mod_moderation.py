import discord
from discord.ext import commands
import config
import util_func
import random
import asyncio
from datetime import timedelta
from datetime import datetime


class moderation_mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @config.clear_p()
    async def clear(self, ctx, *inp):
        form = "%d.%m.%y%H:%M"
        args = [1, None, ctx.guild.created_at, ctx.message.created_at]
        if len(inp) == 1:
            if inp[0].isdigit():
                args[0] = int(inp[0])
            else:
                args[0] = 100
                args[2] = datetime.strptime(datetime.now().strftime("%d.%m.%y") + inp[0], form) - timedelta(hours=2)
        elif len(inp) == 2:
            if inp[0].isdigit():
                args[0] = int(inp[0])
                args[1] = inp[1].replace("!", "")
            else:
                args[0] = 100
                args[2] = datetime.strptime(inp[0] + inp[1], form) - timedelta(hours=2)
        elif len(inp) == 3:
            args[0] = 100
            args[2] = datetime.strptime(inp[0] + inp[1], form) - timedelta(hours=2)
            args[3] = datetime.strptime(datetime.now().strftime("%d.%m.%y") + inp[2], form) - timedelta(hours=2)
        elif len(inp) == 4:
            args[0] = 100
            args[2] = datetime.strptime(inp[0] + inp[1], form) - timedelta(hours=2)
            args[3] = datetime.strptime(inp[2] + inp[3], form) - timedelta(hours=2)
        elif len(inp) != 0:
            raise commands.BadArgument
        amount = args[0]

        def check(m):
            if args[0] == 0 or m.created_at < args[2]:
                return False
            if args[1]:
                if m.author.mention == args[1] and m != ctx.message and args[2] < m.created_at < args[3]:
                    args[0] -= 1
                    return True
            elif m != ctx.message and args[2] < m.created_at < args[3]:
                args[0] -= 1
                return True
            return False

        await ctx.channel.purge(limit=config.del_limit, check=check)
        await util_func.send_log(ctx, 'УДАЛЕНИЕ СООБЩЕНИЙ из #{}'.format(ctx.channel.name),
                                 'Удалено {} из {}'.format(amount - args[0], amount), discord.Color.green())
        await util_func.send_sys(ctx, 'Удаление сообщений из #{}'.format(ctx.channel.name),
                                 'Удалено {} из {}'.format(amount - args[0], amount), discord.Color.green(), "clear")

    @commands.command()
    @config.kick_p()
    async def kick(self, ctx, member: discord.Member, *, reason="плохое поведение"):
        await util_func.send_log(ctx, 'КИК!',
                                 "{} {} был кикнут за **{}**!".format(util_func.status(ctx, member), member.mention,
                                                                      reason),
                                 discord.Color.orange())
        await util_func.send_sys(ctx, 'Кик с сервера!',
                                 "{} {} был кикнут за **{}**!".format(util_func.status(ctx, member), member.mention,
                                                                      reason),
                                 discord.Color.orange(), "kick")
        await member.kick(reason=reason)

    @commands.command()
    @config.ban_p()
    async def ban(self, ctx, member: discord.Member, *, time: int = None, reason="плохое поведение"):
        if time:
            await util_func.send_log(ctx, 'БАН!',
                                     "{} {} был забанен на **{} часов** за **{}**!".format(util_func.status(ctx, member),
                                                                           member.mention, time, reason),
                                     discord.Color.red())
            await util_func.send_sys(ctx, 'Бан!',
                                     "{} {} был забанен на **{} часов** за **{}**!".format(util_func.status(ctx, member),
                                                                           member.mention, time, reason),
                                     discord.Color.red(), "ban")
            await member.ban(reason=reason)
            await asyncio.sleep(time * 3600)
            await ctx.guild.unban(member)
            await util_func.send_log(ctx, 'РАЗБАН!',
                                     "{} был успешно разбанен!".format(member),
                                     discord.Color.green())
            await util_func.send_sys(ctx, 'Ты снова в законе!',
                                     "{} был успешно разбанен!".format(member.name),
                                     discord.Color.green())
        else:
            await util_func.send_log(ctx, 'БАН!',
                                     "{} {} был забанен без срока за **{}**!".format(util_func.status(ctx, member),
                                                                           member.mention, reason),
                                     discord.Color.red())
            await util_func.send_sys(ctx, 'Бан!',
                                     "{} {} был забанен без срока за **{}**!".format(util_func.status(ctx, member),
                                                                           member.mention, reason),
                                     discord.Color.red(), "ban")
            await member.ban(reason=reason)

    @commands.command()
    @config.unban_p()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await util_func.send_log(ctx, 'РАЗБАН!',
                                     "{} был успешно разбанен!".format(user),
                                     discord.Color.green())
            await util_func.send_sys(ctx, 'Ты снова в законе!',
                                     "{} был успешно разбанен!".format(user.name),
                                     discord.Color.green())
            return

    @commands.command()
    @config.mute_p()
    async def mute(self, ctx, member: discord.Member, time: int = None):
        mute_role = discord.utils.get(ctx.message.guild.roles, name='mute')
        if mute_role in member.roles:
            await util_func.send_sys(ctx, 'Небольшая ошибочка...',
                                     "{} {} уже лишён возможности говорить!".format(util_func.status(ctx, member),
                                                                                    member.mention),
                                     discord.Color.orange())
        else:
            await member.add_roles(mute_role)
            if time:
                await util_func.send_log(ctx, 'МЬЮТ!',
                                         "{} {} был замьючен\n на **{} минут**!".format(util_func.status(ctx, member),
                                                                                      member.mention, time),
                                         discord.Color.orange())
                await util_func.send_sys(ctx, 'Немота!',
                                         "{} {} был замьючен\n на **{} минут**!".format(util_func.status(ctx, member),
                                                                                      member.mention, time),
                                         discord.Color.orange(), "mute")
                await asyncio.sleep(time * 60)
                await self.unmute(ctx, member)
            else:
                await util_func.send_log(ctx, 'МЬЮТ!',
                                         "{} {} был замьючен без срока!".format(util_func.status(ctx, member), member.mention),
                                         discord.Color.orange())
                await util_func.send_sys(ctx, 'Немота!',
                                         "{} {} был замьючен без срока!".format(util_func.status(ctx, member), member.mention),
                                         discord.Color.orange(), "mute")

    @commands.command()
    @config.unmute_p()
    async def unmute(self, ctx, member: discord.Member):
        mute_role = discord.utils.get(ctx.message.guild.roles, name='mute')
        if mute_role not in member.roles:
            await util_func.send_sys(ctx, 'Небольшая ошибочка...',
                                     "{} {} не был замьючен!".format(util_func.status(ctx, member), member.mention),
                                     discord.Color.orange())
        else:
            await member.remove_roles(mute_role)
            await util_func.send_log(ctx, 'РАЗМЬЮТ!',
                                     "{} {} был размьючен!".format(util_func.status(ctx, member), member.mention),
                                     discord.Color.green())
            await util_func.send_sys(ctx, 'Получен пропуск на трындеж!',
                                     "{} {} был размьючен!".format(util_func.status(ctx, member), member.mention),
                                     discord.Color.green())


def setup(client):
    client.add_cog(moderation_mod(client))
    print("Cog moderation_mod работает")