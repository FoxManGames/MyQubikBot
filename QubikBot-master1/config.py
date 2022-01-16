import discord
from discord.ext import commands

token = 'NzYyNTk3MzU2MTY3MjMzNTQ2.X3reIg.TnTJQp3fkVTPtA9FZm9ww0FaY1U'
# Мое - Njg1NTI5NTczMjM2MTQ2Mjg0.XmJ_Kg.MuaAd35oJtAnI_Gaw2Bgu8WGjJs
# Некита - NzYyNTk3MzU2MTY3MjMzNTQ2.X3reIg.TnTJQp3fkVTPtA9FZm9ww0FaY1U
log_f = True
prefix = '.'
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)
del_limit = 100
colors = {}

roles = {"admin": 683353413307596832,
         "first_m": 677202146688761886,
         "second_m": 677202145178812454,
         "third_m": 677202142754242564,
         "forth_m": 676337583629926431,
         "dnd_m": 696804545187282995,
         "test_role": 763814005487173663}


def clear_p():
    return commands.has_any_role(roles["admin"], roles["first_m"], roles["second_m"], roles["third_m"],
                                 roles["test_role"])


def kick_p():
    return commands.has_any_role(roles["admin"], roles["first_m"], roles["second_m"], roles["test_role"])


def ban_p():
    return commands.has_any_role(roles["admin"], roles["first_m"], roles["test_role"])


def unban_p():
    return commands.has_any_role(roles["admin"], roles["first_m"], roles["test_role"])


def mute_p():
    return commands.has_any_role(roles["admin"], roles["first_m"], roles["second_m"], roles["third_m"],
                                 roles["test_role"])


def unmute_p():
    return commands.has_any_role(roles["admin"], roles["first_m"], roles["second_m"], roles["third_m"],
                                 roles["test_role"])


def createrole_p():
    return commands.has_any_role(roles["admin"], roles["first_m"], roles["second_m"], roles["third_m"],
                                 roles["test_role"])


def addrole_p():
    return commands.has_any_role(roles["admin"], roles["first_m"], roles["second_m"], roles["third_m"],
                                 roles["test_role"])


def removerole_p():
    return commands.has_any_role(roles["admin"], roles["first_m"], roles["second_m"], roles["third_m"],
                                 roles["test_role"])


def fight():
    return commands.has_any_role(roles["dnd_m"], roles["test_role"])


magic_ball = ["бесспорно!", "предрешено!", "никаких сомнений!", "определённо да!", "можешь быть уверен в этом!",
              "мне кажется - да", "вероятнее всего", "хорошие перспективы!", "знаки говорят - да!", "да!",
              "пока не ясно...", "попробуй снова...", "спроси позже...", "лучше тебе не знать...",
              "сейчас не могу предсказать...", "сконцентрируйся и спроси опять...", "даже не думай!",
              "Артур не одобряет!", "мой ответ - нет!", "по моим данным - нет!", "перспективы не очень хорошие",
              "весьма сомнительно"]

dnd_info = (("Оружие",
             {"👊": "кулак",
              "⚔": "меч",
              "🗡": "кинжал",
              "🦯": "копье",
              "🏹": "лук",
              "🔨": "молот",
              "🪓": "топор",
              "🥏": "меткость"}),
            ("Магия",
             {"⚡": "молния",
              "🔥": "огонь",
              "🌱": "жизнь",
              "👁": "иллюзия",
              "🧠": "внушение",
              "☄": "душа",
              "💫": "перемещение"}),
            ("Разное",
             {"🕵": "скрытность",
              "🍽": "кулинария",
              "🧣": "шитье",
              "🤸": "акробатика",
              "🍀": "удача"}))
