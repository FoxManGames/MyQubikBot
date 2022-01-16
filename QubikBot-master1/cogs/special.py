import discord
from discord.ext import commands
import config
import util_func


class start(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        config.colors = {i.split()[0].lower(): [int(i.split()[1]), int(i.split()[2]), int(i.split()[3])]
                         for i in open('./data/colors.txt').readlines()}
        await config.client.change_presence(status=discord.Status.online, activity=discord.Game('имитацию'))
        print('Опять работа?')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        role = member.guild.get_role(903683830282608680)
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole) or isinstance(error, commands.MissingPermissions):
            await util_func.send_sys(ctx, 'Ошибка', 'У вас недостаточно прав', discord.Color.red())
        elif isinstance(error, commands.BadArgument):
            await util_func.send_sys(ctx, 'Ошибка', 'Неверный порядок или тип параметров', discord.Color.red())
        elif isinstance(error, commands.MissingRequiredArgument):
            await util_func.send_sys(ctx, 'Ошибка', 'Укажите все аргументы', discord.Color.red())
        else:
            print(error)
            await util_func.send_sys(ctx, 'Ошибка', 'Неизвестный код ошибки', discord.Color.red())


def setup(client):
    client.add_cog(start(client))
    print("Cog special работает")
