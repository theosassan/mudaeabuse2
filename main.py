import discord
from discord.ext import commands, tasks
from asyncio import sleep
import os

client = commands.Bot(command_prefix = "%", self_bot = True, help_command = None)

token = os.getenv("TOKEN")

@client.event
async def on_ready():
  print("hi")
  #await sleep(1800)
  await rolls.start()
  
@client.command()
async def abuse(ctx):
  for _ in range(10):
    await ctx.send("$wa")
    await sleep(1)

@client.event
async def on_message(message):
    if message.author.id == 432610292342587392:
      try:
        async for message in message.channel.history(limit=1):
          embed = message.embeds[0]
          msgdict = embed.to_dict()
          name = msgdict['author']['name']
          claims = msgdict['description']
          claims = claims.split('Claims: #')[1]
          claims = int(claims.split('\n')[0])
          print(name, claims)
          emoji = '❤️'
          if name == 'Kaori Miyazono':
            await message.add_reaction(emoji)
      except:
        pass

@tasks.loop(hours = 1)
async def rolls():
  channel = client.get_channel(766491456885227550)
  for _ in range(10):
    await channel.send("$wa")
    await sleep(1)
    async for message in channel.history(limit=1):
      try:
        embed = message.embeds[0]
        msgdict = embed.to_dict()
        print(msgdict)
        name = msgdict['author']['name']
        claims = msgdict['description']
        claims = claims.split('Claims: #')[1]
        claims = int(claims.split('\n')[0])
        print(name, claims)
        emoji = '❤️'
        if name == "Kaori Miyazono":
          await message.add_reaction(emoji)
          await channel.send('@294184126343282690 HOLY SHIT FINALLY')
        elif claims <= 500:
          await message.add_reaction(emoji)
        elif claims <= 2000:
          ask = await channel.send('<@294184126343282690> should I claim?')
          await ask.add_reaction(emoji)
          await sleep(15)
          async for ask in channel.history(limit=1):
            reactions = await ask.reactions[0].users().flatten()
            if len(reactions) >= 2:
              await ask.delete()
              await sleep(1)
              async for message in channel.history(limit=1):
                await message.add_reaction(emoji)
      except:
        pass
    await sleep(2)
    
        
client.run(token, bot = False)
