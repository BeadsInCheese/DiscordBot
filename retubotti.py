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
    def get_params(self,s):
        s2=s.split(",")
        return s2
    async def on_message(self, message):
        mess=message.content.split("$")
        if(1<len(mess)):
            mess=mess[1]
            mess=self.get_params(mess)
        if(mess[0]==("StartMemoryGame")):
            self.tg=memoryGame.tileGame()
            await message.channel.send(memoryGame.printTiles(self.tg.grid))
        if(mess[0]==("roll")):
            print(mess)
            p=mess[1]

            if (int(p)):
                await message.channel.send(random.randint(1,int(p)))
        if(mess[0]==("MemoryGamePM")):
            try:

                x1=int(mess[1])
                print(x1)
                y1=int(mess[2])
                print(y1)
                x2=int(mess[3])
                print(x2)
                y2=int(mess[4])
                print(y2)
                await message.channel.send(memoryGame.openTilePair([[x1,y1],[x2,y2]],self.tg.grid))
            except Exception as e:
                print(e)
        if(mess[0]==("Hello")):
            await message.channel.send("Hello world!")


        if(mess[0]==("clearPool")):
            self.clear_pool()
            await message.channel.send("user-pool cleared")



        if(mess[0]==("selectUser")):
            if(len(self.pool)>0):
                w=random.randint(0,len(self.pool)-1)
                for user in range(len(self.pool)):
                    if(w==user):
                        print(self.pool[user])
                        await self.pool[user].send("You were selected")
                    else:
                        print(self.pool[user])
                        await self.pool[user].send("You were NOT selected")
        if(mess[0]==("$addMe")):
            self.pool.append(message.author)
        print('Message from {0.author}: {0.content}'.format(message))
        print(mess[0])
        #await self.process_commands(message)


client = MyClient(intents=discord.Intents.default())
tokenFile = open("token.txt", "r")
token=tokenFile.read()
tokenFile.close()
client.run(token)
#client = commands.Bot(command_prefix = "$",intents=discord.Intents.default())
client.run(token)
@client.command()
async def MemoryGamePM(ctx,  x1: int,  y1: int,  x2: int,  y2: int):
  await ctx.send(memoryGame.openTilePair([[x1,y1],[x2,y2]]))