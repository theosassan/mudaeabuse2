import discord
from discord.ext import commands
from asyncio import sleep

client = commands.Bot(command_prefix = ".", self_bot = True, help_command = None)


token = "NDU3NTQ1MTA4MTk2MTYzNTg0.GFBzQo.YDLPTMddvl4ZB2QEWNoqFbBJSbLZPVk2ya6b3I"

@client.event
async def on_ready():
  print("hi")
@client.command()
async def abuse(ctx):
  for _ in range(10):
    await ctx.send("$wa")
    await sleep(0.5)
  
client.run(token, bot = False)
