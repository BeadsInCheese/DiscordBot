import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import memoryGame
class MyClient(discord.Client):
    pool=[]
    tg=None
    async def on_ready(self):

        print('Logged on as {0}!'.format(self.user))

    async def args(ctx, arg1, arg2):
        await ctx.send('You sent {} and {}'.format(arg1, arg2))

    def clear_pool(self):
        self.pool=[]
    async def on_message(self, message):
        
        if(message.content.startswith("$StartMemoryGame")):
            tg=memoryGame.tileGame()
            await message.channel.send(memoryGame.printTiles(tg.grid))
        if(message.content.startswith("$MemoryGamePM")):
            memoryGame.openTilePair(message.content)

        if(message.content.startswith("$Hello")):
            await message.channel.send("Hello world!")


        if(message.content.startswith("$clearPool")):
            self.clear_pool()
            await message.channel.send("user-pool cleared")



        if(message.content.startswith("$selectUser")):
            if(len(self.pool)>0):
                w=random.randint(0,len(self.pool)-1)
                for user in range(len(self.pool)):
                    if(w==user):
                        print(self.pool[user])
                        await self.pool[user].send("You were selected")
                    else:
                        print(self.pool[user])
                        await self.pool[user].send("You were NOT selected")
        if(message.content.startswith("$addMe")):
            self.pool.append(message.author)
        print('Message from {0.author}: {0.content}'.format(message))


client = MyClient()
tokenFile = open("token.txt", "r")
token=tokenFile.read()
tokenFile.close()
client.run(token)
client2 = commands.Bot(command_prefix = "$")
@client2.command()
async def MemoryGamePM(ctx,  x1: int,  y1: int,  x2: int,  y2: int):
  await ctx.send(memoryGame.openTilePair([[x1,y1],[x2,y2]]))