# -------------------------------------------------------
# RUN THE BOT
import os
import platform

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    clear()
    print("Logged as...")

bot.run(TOKEN)

# -------------------------------------------------------
# BASICS COMMANDS
@bot.command()
async def hello(ctx):
  await ctx.send("Hello, World!")

# -------------------------------------------------------
