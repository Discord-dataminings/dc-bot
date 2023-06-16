import re, discord, asyncio, json
from discord.ext import commands
import os, random, requests
from keep_alive import keep_alive

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


async def send(content, embeds=None):
  channel_id = 1107053249548267590
  c = client.get_channel(channel_id)
  a = await c.send(content, embeds=embeds)
  return a


description = """
![](https://cdn.discordapp.com/attachments/964562087365972109/1106684769703571526/image.png)
"""
roles = {
  "screenshot": "<@&1107041903901409394>",
  "strings": "<@&1107041647377789090>",
  "experiment": "<@&1107042029306912955>"
}
regex_images = r"!\[.*\]\(.*\)"
regex_experiment = r"(?i)experiment"
regex_strings = r"(?i)strings"


@client.event
async def on_ready():
  print("Ready!")


@client.event
async def on_message(msg):
  if msg.channel.id == 1103068776678826014 and msg.author.bot:
    description = msg.embeds[0].description
    if re.search(regex_images, description):
      await msg.reply(roles["screenshot"])
    elif re.search(regex_experiment, description):
      await msg.reply(roles['experiment'])
    elif re.search(regex_strings, description):
      await msg.reply(roles["strings"])
    else:
      pass
  if msg.channel.id == 1103291176339124224 and msg.author.bot:
    cc = client.get_channel(1103276235074830376)
    m = await cc.send(msg.content, embeds=msg.embeds)
    await m.publish()
    await m.reply(
      '<@&1107042029306912955> (Source: https://discord.gg/datamining)')
  if msg.channel.id == 1118626181181345892 and msg.author.bot:
    cc = client.get_channel(1118580285454438490)
    m = await cc.send(
      "<@&1118579427446628352> (Source: https://discord.gg/discord-603970300668805120)",
      embeds=msg.embeds)
    await m.publish()
    await m.reply('<@&1107042029306912955>')
  await client.process_commands(msg)


keep_alive()

import discord
from discord.ext import commands


@client.command()
async def giveaway_winner(ctx, winner: discord.User, message_link):
  # Extracting the message ID from the link
  message_id = int(message_link.split('/')[-1])

  # Retrieving the message from the same server
  try:
    message = await ctx.fetch_message(message_id)
  except discord.NotFound:
    await ctx.send("The provided message could not be found.")
    return

  # Checking if the message is from the same server
  if message.guild.id != ctx.guild.id:
    await ctx.send("The provided message is not from this server.")
    return

  # Extracting the prize from the message content
  prize = message.content.split('[prize=')[1].split(']')[0]

  embed = discord.Embed(title=f"**{winner.name} WON**",
                        description="You won the giveaway!",
                        color=0x5562EA)
  embed.add_field(name="**Prize:**", value=prize)
  embed.add_field(name="**Winner:**", value=winner.mention)
  embed.set_footer(text="Bot by discord dataminings!")
  await ctx.send(
    f'**<a:tada_:1112789550016774224> Giveaway winner: {winner.mention}**',
    embed=embed)


@client.event
async def on_message_delete(message):
  if message.channel.id == 1108696126359609435:
    if message.author.bot:
      # Update the counter
      with open('stats.json', 'r') as file:
        stats = json.load(file)
        stats['clyde_servers'] -= 1
      with open('stats.json', 'w') as file:
        json.dump(stats, file)


client.run(os.getenv('token'))
