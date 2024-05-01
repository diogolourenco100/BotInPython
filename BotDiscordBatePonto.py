import os
import platform
import time
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)

# Dicionário para armazenar os horários em que os pontos foram abertos
pontos_abertos = {}

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")

@bot.command()
async def ping(ctx: commands.Context):
    user = ctx.author
    await ctx.reply(f"Hello, {user.display_name}.")

@bot.command()
async def apagar(ctx, quantidade: int):
    if ctx.message.author.guild_permissions.manage_messages:
        messages = []
        async for message in ctx.channel.history(limit=quantidade + 1):
            messages.append(message)

        for message in messages:
            await message.delete()

        await ctx.send(f"{quantidade} mensagens apagadas.", ephemeral=True)
    else:
        await ctx.send("Você não tem permissão para executar este comando.", ephemeral=True)

@bot.command()
async def painel_bp(ctx):
    embed = discord.Embed(title="ℹ️ BATE-PONTO!",
                          description="Esse servidor possui sistema de BATE-PONTO. "
                                      "Uma maneira fácil, prática e rápida de registrar suas horas.",
                          color=discord.Color.purple())

    embed.add_field(name="COMO UTILIZAR:",
                    value="Clique em ``ABRIR`` para iniciar a contagem de horas no bate-ponto.\n\n"
                          "Clique em ``FECHAR`` para interromper sua contagem de horas.\n\n"
                          "Você também pode consultar o total de horas obtidas, clicando em ``HORAS.``",
                    inline=False)
    
    embed.add_field(name="⚠️ Alerta:",
                    value="``FORJAR`` bate-ponto resultará em ``PUNIÇÃO!``",
                    inline=False)
    
    async def response_button(interact: discord.Interaction):
        await interact.response.send_message('Botao!', ephemeral=True)

    async def abrir_ponto(interact: discord.Interaction):
        # Verifica se o autor do comando está em uma das calls principais
        call_principal_ids = [1234409418947297340, 1234409577441792021, 1234409590678880286, 1234410445125714001, 1234410504546549791]
        if interact.user.id not in call_principal_ids:
            await interact.response.send_message("Você precisar estar em alguma call de PTR para abrir o ponto.", ephemeral=True)
            return

        # Salva o horário em que o ponto foi aberto associado ao autor do comando
        pontos_abertos[interact.user.id] = time.time()

        await interact.response.send_message('Ponto aberto.', ephemeral=True)

    async def fechar_ponto(interact: discord.Interaction):
        # Verifica se o autor do comando tinha um ponto aberto
        if interact.user.id not in pontos_abertos:
            await interact.response.send_message("Você não tem um ponto aberto para fechar.", ephemeral=True)
            return

        # Calcula o tempo decorrido desde que o ponto foi aberto
        horario_abertura = pontos_abertos.pop(interact.user.id)
        tempo_decorrido = time.time() - horario_abertura

        # Exibe o tempo decorrido formatado
        await interact.response.send_message(f"Seu ponto foi aberto por {tempo_decorrido:.2f} segundos.", ephemeral=True)

    view = discord.ui.View()
    abrir = discord.ui.Button(label='Abrir', style=discord.ButtonStyle.green)
    fechar = discord.ui.Button(label='Fechar', style=discord.ButtonStyle.red)
    horas = discord.ui.Button(label='Horas', style=discord.ButtonStyle.blurple)

    abrir.callback = abrir_ponto
    fechar.callback = fechar_ponto
    horas.callback = response_button

    view.add_item(abrir)
    view.add_item(fechar)
    view.add_item(horas)

    await ctx.send(view=view, embed=embed)

@bot.event
async def on_ready():
    clear()
    print("Logged as Atom!")

bot.run("TOKEN")
