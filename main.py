import discord
from discord.ext import commands
from asyncio import sleep
import os

client = commands.Bot(command_prefix = ".", self_bot = True, help_command = None)
token = os.getenv("TOKEN")
@client.event
async def on_ready():
  print("hi")
@client.command()
async def abuse(ctx):
  for _ in range(10):
    await ctx.send("$wa")
    await sleep(0.5)
  
client.run(token, bot = False)
