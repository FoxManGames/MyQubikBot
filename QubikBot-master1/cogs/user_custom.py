import discord
from discord.ext import commands
import util_func


class custom_user(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def записаться(self, ctx):
        member = ctx.message.author
        role = member.guild.get_role(801800618615635999)
        await member.add_roles(role)
        await util_func.send_sys(ctx, 'Успешно!',
                                 "Теперь ты записан на ивент!", discord.Color.green())


def setup(client):
    client.add_cog(custom_user(client))
    print("Cog custom_user работает")