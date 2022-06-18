import os
import discord
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from asyncio import sleep
import json
import random
import datetime
bot = commands.Bot(command_prefix = '.')
waitlist = []
@bot.event
async def on_ready():
  print('Ready!')
  await bot.change_presence(activity=discord.Game(name=".help, .anagrams"))
  await sleep(0)
  await daily_info.start()
  
bot.remove_command('help')

async def add_points(id, amt):
  id = str(id)
  with open('save.json', 'r') as f:
    save = json.load(f)
  if id in save:
    pass
  else:
    save[id] = {"stuybucks":0,"stuyscore":0}
  save[id]['stuyscore'] += amt
  save[id]['stuybucks'] += amt
  with open('save.json', 'w') as f:
    json.dump(save, f)
    
@bot.command()
async def register(ctx):
  id = str(ctx.message.author.id)
  with open('save.json', 'r') as f:
    save = json.load(f)
  if id in save:
    await ctx.reply("You are already registered!")
  else:
    save[id] = {"stuybucks":0,"stuyscore":0}
    await ctx.reply("Successfully registered!")
  with open('save.json', 'w') as f:
    json.dump(save, f)

@bot.command()
async def registercr(ctx, tag):
  id = str(ctx.message.author.id)
  try:
    with open('save.json', 'r') as f:
      save = json.load(f)
    save[id]['tagcr'] = tag
    with open('save.json', 'w') as f:
      json.dump(save, f)
  except:
    await ctx.reply("Please register in the form **.registercr [tag]**!")
    return None
  await ctx.reply("Successfully registered!")

@bot.command()
async def statscr(ctx):
  id = str(ctx.message.author.id)
  try:
    with open('save.json', 'r') as f:
      save = json.load(f)
    tag = save[id]['tagcr']
  except:
    await ctx.reply("Please register first using **.registercr [tag]**!")
    return None
  await ctx.reply(f"https://royaleapi.com/player/{tag}/")

@bot.command()
async def registerbs(ctx, tag):
  id = str(ctx.message.author.id)
  try:
    with open('save.json', 'r') as f:
      save = json.load(f)
    save[id]['tagbs'] = tag
    with open('save.json', 'w') as f:
      json.dump(save, f)
  except:
    await ctx.reply("Please register in the form **.registerbs [tag]**!")
    return None
  await ctx.reply("Successfully registered!")

@bot.command()
async def statsbs(ctx):
  id = str(ctx.message.author.id)
  try:
    with open('save.json', 'r') as f:
      save = json.load(f)
    tag = save[id]['tagbs']
  except:
    await ctx.reply("Please register first using **.registerbs [tag]**!")
    return None
  await ctx.reply(f"https://brawlstats.com/profile/{tag}")
  
@bot.command()
async def lb(ctx):
  with open('save.json', 'r') as f:
    save = json.load(f)
  lb = {}
  for id in save:
    lb[id] = save[id]['stuyscore']
  lb = dict(sorted(lb.items(),key=lambda x:x[1], reverse = True))
  users = list(lb.keys())[:5]
  embed_list = []
  convert = ['A','B','C','D', 'F']
  for user in range(len(users)):
    embed_list.append(f"**{convert[user]}) {(await bot.fetch_user(users[user])).name}** |** {lb[users[user]]}**")
  ranks = "\n".join(embed_list)
  embed = discord.Embed(title = "Here's the current Stuyscore leaderboard:", description = ranks).set_thumbnail(url = "https://cdn.discordapp.com/attachments/946077984559865948/987586698462502942/report-card-featured-image.jpeg")
  await ctx.send(embed = embed)

@bot.command()
async def ss(ctx):
  with open('save.json', 'r') as f:
    save = json.load(f)
  id = str(ctx.message.author.id)
  if id in save:
    lb = {}
    for x in save:
      lb[x] = save[x]['stuyscore']
      lb = dict(sorted(lb.items(),key=lambda x:x[1], reverse = True))
      users = list(lb.keys())[:5]
    convert = ['A','B','C','D', 'F']
    index = users.index(id)
    grade = convert[index]
    if index == -1:
      grade = "F-"
    score = save[id]["stuyscore"]
    user = await bot.fetch_user(id)
    embed = discord.Embed(title = f"{user.name}'s Stuyscore: **{score}**", description = f"**Grade: {grade}**").set_thumbnail(url = user.avatar_url)
    await ctx.reply(embed = embed)
  else:
    await ctx.reply("Please first register using **.register**!")

done = False
@bot.command()
async def anagrams(ctx, opp):
  global done
  global waitlist
  opp = opp.split('@')[1]
  opp = opp.split('>')[0]
  p1 = await bot.fetch_user(ctx.message.author.id)
  p2 = await bot.fetch_user(opp)
  if p1 in waitlist or p2 in waitlist or p1 == p2:
    await ctx.send("One of you already has a pending game!")
    return True
  else:
    pass
  waitlist.append(p1)
  waitlist.append(p2)
  await ctx.send(f"**{p1}** has challenged **{p2}** to an Anagrams battle! Please wait for **{p2}** to accept the challenge by responding to my DM.")
  with open('words.txt') as file:
    words = file.readlines()
    words = [word.rstrip().lower() for word in words if len(word.rstrip()) > 2 and len(word.rstrip()) <= 8]
  eight_letters = [word for word in words if len(word) == 8]
  letters = list(random.choice(eight_letters))
  random.shuffle(letters)
  final = []
  for word in words:
    valid = True
    for letter in word:
      if word.count(letter) <= letters.count(letter):
        pass
      else:
        valid = False
    if valid == True:
      final.append(word)
  final = sorted(final, key=len, reverse=True)
  embed = discord.Embed(title = "You're up first!", description = "Type as many words as you can using the given letters in 1 minute.\nEnter anything to start.\nType 'X' to decline the invitation.").set_thumbnail(url = "https://cdn.discordapp.com/attachments/946077984559865948/987609144120999936/unnamed.webp")
  p1score = 0
  p1words = []
  p1words2 = []
  p2score = 0
  p2words = []
  p2words2 = []
  newline = '\n'
  def check_valid(answer):
    if answer in final:
      return True
    else:
      return False
  await p2.send(embed = embed)
  start = False
  denied = False
  while start == False:
    answer = await bot.wait_for('message')
    if answer.author == p2:
      if answer.content == 'X':
        denied = True
        waitlist.remove(p1)
        waitlist.remove(p2)
        break
      else:
        finishTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
        finishTime = finishTime.time()
        break
  if denied == True:
    await ctx.send(f"**{p2}** has declined the offer.")
    return True
  embed = discord.Embed(title = f'**{" ".join(letters).upper()}**').set_thumbnail(url = "https://cdn.discordapp.com/attachments/946077984559865948/987609144120999936/unnamed.webp").set_footer(text = f"Score: {p2score}")
  await p2.send(embed = embed)
  while datetime.datetime.now().time() < finishTime:
    answer = await bot.wait_for('message')
    if answer.author == p2:
      answer = answer.content
      if answer.upper() not in p2words2:
        correct = check_valid(answer)
      else:
        correct = False
      if correct == True and datetime.datetime.now().time() < finishTime:
        gain = 25 * 2 ** len(answer)
        p2score += gain
        p2words.append(f"**{answer.upper()}** +{gain}")
        p2words2.append(answer.upper())
        p2words = sorted(p2words, key=len, reverse=True)
      else:
        pass
      embed = discord.Embed(title = f'**{" ".join(letters).upper()}**', description = f"{newline.join(p2words)}").set_thumbnail(url = "https://cdn.discordapp.com/attachments/946077984559865948/987609144120999936/unnamed.webp").set_footer(text = f"Score: {p2score}")
      await p2.send(embed = embed)
  waitlist.remove(p2)
  embed = discord.Embed(title = "Time's up! Here were your results:", description = f"Score: **{p2score}**\n\n{newline.join(p2words)}").set_thumbnail(url = "https://cdn.discordapp.com/attachments/946077984559865948/987609144120999936/unnamed.webp").set_footer(text = f"Please wait for {p1}.")
  await p2.send(embed = embed)
  #p1
  embed = discord.Embed(title = f'{p2} has finished!', description = "Type as many words as you can using the given letters in 1 minute.\nEnter anything to start.").set_thumbnail(url = "https://cdn.discordapp.com/attachments/946077984559865948/987609144120999936/unnamed.webp")
  await p1.send(embed = embed)
  start = False
  while start == False:
    answer = await bot.wait_for('message')
    if answer.author == p1:
      finishTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
      finishTime = finishTime.time()
      break
  embed = discord.Embed(title = f'**{" ".join(letters).upper()}**').set_thumbnail(url = "https://cdn.discordapp.com/attachments/946077984559865948/987609144120999936/unnamed.webp").set_footer(text = f"Score: {p2score}")
  await p1.send(embed = embed)
  while datetime.datetime.now().time() < finishTime:
    answer = await bot.wait_for('message')
    if answer.author == p1:
      answer = answer.content
      if answer.upper() not in p1words2:
        correct = check_valid(answer)
      else:
        correct = False
      if correct == True and datetime.datetime.now().time() < finishTime:
        gain = 25 * 2 ** len(answer)
        p1score += gain
        p1words.append(f"**{answer.upper()}** +{gain}")
        p1words2.append(answer.upper())
        p1words = sorted(p1words, key=len, reverse=True)
      else:
        pass
      embed = discord.Embed(title = f'**{" ".join(letters).upper()}**', description = f"{newline.join(p1words)}").set_thumbnail(url = "https://cdn.discordapp.com/attachments/946077984559865948/987609144120999936/unnamed.webp").set_footer(text = f"Score: {p1score}")
      await p1.send(embed = embed)
  waitlist.remove(p1)
  embed = discord.Embed(title = "Time's up! Here were your results:", description = f"Score: **{p1score}**\n\n{newline.join(p1words)}").set_thumbnail(url = "https://cdn.discordapp.com/attachments/946077984559865948/987609144120999936/unnamed.webp")
  await p1.send(embed = embed)
  gain = random.randint(5, 10) * 10
  if p1score > p2score:
    embed = discord.Embed(title = f"{p1} wins with a score of {p1score}!", description = f"**Letters:** {' '.join(letters).upper()}\n\n**All possible words:**\n{', '.join(final)}").set_thumbnail(url = "https://cdn.discordapp.com/attachments/946077984559865948/987609144120999936/unnamed.webp")
    p1m = f"+{gain} SS"
    p2m = f"-{gain} SS"
    await add_points(p1.id, gain)
    await add_points(p2.id, -1 * gain)
  else:
    embed = discord.Embed(title = f"{p2} wins with a score of {p2score}!", description = f"**Letters:** {letters}\n\n**All possible words:**\n{newline.join(final)}").set_thumbnail(url = "https://cdn.discordapp.com/attachments/946077984559865948/987609144120999936/unnamed.webp")
    p2m = f"+{gain} SS"
    p1m = f"-{gain} SS"
    await add_points(p2.id, gain)
    await add_points(p1.id, -1 * gain)
  await ctx.send(embed = embed)
  embed = discord.Embed(title = f"{p1}'s results:", description = f"Score: **{p1score}**\n\n{newline.join(p1words)}").set_thumbnail(url = p1.avatar_url).set_footer(text = p1m)
  await ctx.send(embed = embed)
  embed = discord.Embed(title = f"{p2}'s results:", description = f"Score: **{p2score}**\n\n{newline.join(p2words)}").set_thumbnail(url = p2.avatar_url).set_footer(text = p2m)
  await ctx.send(embed = embed)

@bot.command()
async def wordle(ctx):
    validwords = open("validwords.txt", "r").read().split("\n")
    word_list = open("wordlist.txt", "r").read().split("\n")
    chosen_word = word_list[random.randint(0, len(word_list) - 1)]
    user = ctx.message.author
    embed = discord.Embed(title = "StuyBS presents to you: Brawl Stars Wordle!", description = "Guess any word to begin!")
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/947292794345652225/961836366243704872/60b65fc8668685c9237a3c67_brawlstars3.jpeg')
    await ctx.message.channel.send(embed = embed)
    finished = False
    answered = False
    turns = 6
    green = '🟩'
    yellow = '🟨'
    grey = '⬜'
    black = ':white_square_button:'
    corrects = ''
    guesses = []
    squares = ['⬛','⬛','⬛','⬛','⬛']
    squares2 = [':white_square_button:',':white_square_button:',':white_square_button:',':white_square_button:',':white_square_button:']
    letters = {}
    repeats = {}
    convert = {'A' :'🇦', 'B':'🇧', 'C':'🇨', 'D':'🇩', 'E': '🇪', 'F':'🇫', 'G':'🇬', 'H':'🇭', 'I':'🇮', 'J':'🇯', 'K':'🇰', 'L':'🇱', 'M':'🇲', 'N':'🇳', 'O':'🇴', 'P':'🇵', 'Q':'🇶', 'R':'🇷', 'S':'🇸', 'T':'🇹', 'U':'🇺','V':'🇻',  'W':'🇼', 'X':'🇽', 'Y':'🇾', 'Z':'🇿'}
    for letter in convert:
      letters[letter.lower()] = grey
    while finished == False:
      answered = False
      while answered == False:
        input1 = (await bot.wait_for('message'))
        input = input1.content
        if input.lower() in validwords and len(input) == 5 and input1.author == user:
          guess = input.lower()
          guesss = input.upper()
          answered = True
          conversion = []
          for letter in guesss:
            conversion.append(convert[letter])
          break
      guesslist = []
      for x in guess:
        guesslist.append(x)
      chosenlist = []
      correct = [grey,grey,grey,grey,grey]
      for x in chosen_word:
        chosenlist.append(x)
      let = 0
      for letter in guesslist:
        repeats[letter] = 0
      for letter in guesslist:
        if letter in chosenlist and guesslist[let] == chosenlist[let]:
          correct[let] = green
          if letters[letter] != green:
            letters[letter] = green
          repeats[letter] += 1
        let += 1
      let = 0
      for letter in guesslist:
        if letter in chosenlist and guesslist[let] != chosenlist[let]:
          if repeats[letter] >= chosenlist.count(letter):
            correct[let] = grey
            if letter not in chosenlist:
              letters[letter] = black
          else:
            correct[let] = yellow
            if letters[letter] != green:
              letters[letter] = yellow
            repeats[letter] += 1
        elif letter not in chosenlist:
          correct[let] = grey
          letters[letter] = black
        let += 1
      guesses.append((f"\n{' '.join(conversion)}\n{' '.join(correct)}"))
      guessstring = ''
      for x in range(len(guesses)):
        guessstring += (f"{guesses[x]}")
      for x in range(turns - 1):
        guessstring += f"\n{' '.join(squares)}"
        guessstring += f"\n{' '.join(squares2)}"
      lettersOrg = []
      lettersOrg.append(" ")
      lettersOrg.append(letters['q'])
      lettersOrg.append(letters['w'])
      lettersOrg.append(letters['e'])
      lettersOrg.append(letters['r'])
      lettersOrg.append(letters['t'])
      lettersOrg.append(letters['y'])
      lettersOrg.append(letters['u'])
      lettersOrg.append(letters['i'])
      lettersOrg.append(letters['o'])
      lettersOrg.append(letters['p'])
      lettersOrg.append('\n')
      lettersOrg.append('\t')
      lettersOrg.append(letters['a'])
      lettersOrg.append(letters['s'])
      lettersOrg.append(letters['d'])
      lettersOrg.append(letters['f'])
      lettersOrg.append(letters['g'])
      lettersOrg.append(letters['h'])
      lettersOrg.append(letters['j'])
      lettersOrg.append(letters['k'])
      lettersOrg.append(letters['l'])
      lettersOrg.append('\n')
      lettersOrg.append('\t')
      lettersOrg.append('\t')
      lettersOrg.append(letters['z'])
      lettersOrg.append(letters['x'])
      lettersOrg.append(letters['c'])
      lettersOrg.append(letters['v'])
      lettersOrg.append(letters['b'])
      lettersOrg.append(letters['n'])
      lettersOrg.append(letters['m'])
      
      await ctx.message.channel.send(f"{guessstring}\n\n\n{' '.join(lettersOrg)}")
      corrects += (f"{' '.join(correct)}\n\n")
      correctamt = 0
      for x in range(len(correct)):
        if correct[x] == green:
          correctamt += 1
      
      if correctamt == 5:
        gain = random.randint(5, 10) * 5
        embed = discord.Embed(title = f"{chosen_word.upper()} was the word, you win!", description = f"{corrects}").set_footer(text = f"+{gain} SS")
        await ctx.message.channel.send(embed = embed)
        await add_points(user.id, gain)
        break
        finished = True
      else:
        turns -= 1
      if turns <= 0:
        gain = random.randint(5, 10) * -5
        embed = discord.Embed(title = f"You lose. The word was {chosen_word.upper()}.", description = f"{corrects}").set_footer(text = f"{gain} SS")
        await ctx.message.channel.send(embed = embed)
        await add_points(user.id, gain)
        break
        finished = True
      else:
        finished = False
        pass      

@bot.command()
async def boxodds(ctx):
    await ctx.send("How many standard Brawl Boxes?")
    while True:
      try:
        brawlb = int((await bot.wait_for('message')).content)
        break
      except:
        await ctx.send("Invalid response! Please try again.")
    await ctx.send("How many Big Boxes?")
    while True:
      try:
        bigb = int((await bot.wait_for('message')).content)
        break
      except:
        await ctx.send("Invalid response! Please try again.")
    await ctx.send("How many Mega Boxes?")
    while True:
      try:
        megab = int((await bot.wait_for('message')).content)
        break
      except:
        await ctx.send("Invalid response! Please try again.")
    await ctx.send("What is your percent probability for the desired rarity?")
    while True:
      try:
        prob = float((await bot.wait_for('message')).content)
        break
      except:
        await ctx.send("Invalid response! Please try again.")
    trials = 0
    for x in range(brawlb):
      trials += 1
    for x in range(bigb):
      trials += 3
    for x in range(megab):
      trials += 10
    prob = prob / 100
    final = round(((1 - (1 - prob) ** trials) * 100), 2)
    if final == 100:
      final = 99.99
    await ctx.send(f"Your probability is **{final}%**.")  

@bot.command()
async def help(ctx):
  help = \
  f"""
  ***Account***
  
  **.register:** Register your Discord account into my system.
  **.ss:** View your Stuyscore.
  **.sb:** View your Stuybucks balance.
  **.lb:** View the Stuyscore leaderboard.

  ***Games*** (Coming soon: Battleship)

  **.wordle:** Play a game of Wordle for SS.
  **.anagrams @[opponent]:** Play a game of Anagrams against a friend for SS.

  ***Misc***

  **.registerbs [tag]:** Register your Brawl Stars tag.
  **.registercr [tag]:** Register your Clash Royale tag.
  **.statsbs:** View your Brawl Stars stats.
  **.statscr:** View your Clash Royale stats.
  **.boxodds:** Find your odds of getting a certain rarity of brawler.
  


  
  """
  embed = discord.Embed(title = "Help is on the way!", description = help)
  await ctx.send(embed = embed)

@tasks.loop(hours = 24)
async def daily_info():
  #brawl
  channel = bot.get_channel(987747306361221220)
  await channel.purge(limit=10)
  req = Request('https://brawlify.com/maps/', headers={'User-Agent': 'Mozilla/5.0'})
  site = urlopen(req).read()
  soup = BeautifulSoup(site, 'html.parser')
  maps = soup.find_all(class_ = "map-def col-6 col-md-4 col-lg-3 map-block mb-0")
  for map in maps:
    one = map.find("div", class_ = "img-fluid map-block")
    two = one.find("div", class_="card-img-overlay text-center")
    three = two.find("span", class_ = "badge map-name text-success")
    try:
      if "ACTIVE" in three.get_text():
        four = one.find("img")
        name = four["alt"]
        image = four["src"]
        embed = discord.Embed(title = name)
        embed.set_image(url = image)
        await channel.send(embed = embed)
    except:
      pass
      
  #clash
  channel = bot.get_channel(987747295976108072)
  await channel.purge(limit=10)
  req = Request('https://royaleapi.com/decks/popular', headers={'User-Agent': 'Mozilla/5.0'})
  site = urlopen(req).read()
  soup = BeautifulSoup(site, 'html.parser')
  decks = soup.find_all(class_="ui attached segment deck_segment")
  decks = decks[:5]
  rank = 1
  for deck in decks:
    name = deck.find(class_ = "deck_human_name-mobile").get_text()
    cards = deck.find("div")
    cards = cards.find("div")
    cards = cards["data-deck-name"]
    cards = cards.split(',')
    first = cards[0]
    image = f"https://cdn.royaleapi.com/static/img/cards-150/{first}.png?t=f0eeffa5c"
    for card in range(len(cards)):
      cards[card] = cards[card].title()
      cards[card] = cards[card].replace('-',' ')
    cards = '\n'.join(cards)
    embed = discord.Embed(title = f"{rank}. {name}", description = f"**{cards}**").set_thumbnail(url = image)
    await channel.send(embed = embed)
    rank += 1
    
#https://discord.com/api/oauth2/authorize?client_id=987491513183375370&permissions=8&scope=bot
bot.run(os.environ.get('TOKEN'))
