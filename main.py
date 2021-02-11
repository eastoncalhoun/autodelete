import discord
from discord.ext import commands
global channels

prefix = "%"
bot = commands.Bot(command_prefix=prefix)
client = discord.Client()
channels = []
token = "Put token here"

def notPinned(message):
    if not message.pinned:
        return True
    

class AutoChannel:
    def __init__(self, channelId, limit):
        self.channelId = channelId
        self.limit = limit
        self.messages = []

    def addMessage(self, messageId):
        self.messages.append(messageId)

    def getFirst(self):
        s = self.messages[0]
        del(self.messages[0])
        return s

    def timeToDelet(self):
        if len(self.messages) > self.limit:
            return True
        else:
            return False

    async def delet(self, link):
        try:
            channel = bot.get_channel(self.channelId)
            toDelet = await channel.fetch_message(link)
            if not toDelet.pinned:
                await channel.delete_messages([toDelet])
        except:
            print("an exception occured")


@bot.command()
async def ping(ctx):
    await ctx.channel.send("Pong!")

@bot.command()
@commands.has_any_role("Mod", "Admin")
async def disableauto(ctx):
    for ch in channels:
        if ch.channelId == ctx.channel.id:
            del(ch)
            return await ctx.channel.send("Auto delete has been disabled...")
        else:
            return await ctx.channel.send("This channel doesn't have autodelete enabled!")

@bot.command()
@commands.has_any_role("Mod", "Admin")
async def enableauto(ctx, limit):
    for ch in channels:
        if ch.channelId == ctx.channel.id:
            if ch.limit == int(limit):
                return await ctx.channel.send("That is the limit already!")
            else:
                ch.limit = int(limit)
    channels.append(AutoChannel(ctx.channel.id, int(limit)))
    await ctx.channel.send("Auto delete enabled with limit " + str(limit))

@bot.event
async def on_message(message):
    if message.content.startswith(prefix):
        return await bot.process_commands(message)
    for c in channels:
        if message.channel.id == c.channelId:
            c.addMessage(message.id)
            if c.timeToDelet():
                a = c.getFirst()
                await c.delet(a)
            

@bot.event
async def on_ready():
    print("Client logged in...")


bot.run(token)
