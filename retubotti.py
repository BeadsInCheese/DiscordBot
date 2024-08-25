import discord
from discord.ext.commands import Bot
from discord.ext import commands
import matplotlib.pyplot as plt
import random
import memoryGame
from matplotlib import rcParams
rcParams['text.usetex'] = True
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

intent =  intents=discord.Intents.all()
intent.members = True
intent.message_content = True
#client = MyClient(intents=intent)
client = commands.Bot(command_prefix='$', description="Just chilling", intents=intent)
tokenFile = open("token.txt", "r")
token=tokenFile.read()
tokenFile.close()
#client = commands.Bot(command_prefix = "$",intents=discord.Intents.default())
tg=None
@client.command()
async def StartMemoryGame(ctx):
    """Initializes the memory game*"""
    global tg 
    tg=memoryGame.tileGame()
    await ctx.channel.send(memoryGame.printTiles(tg.grid))
@client.command()
async def MemoryGamePM(ctx,  x1: str,  y1: str,  x2: str,  y2: str):
  """MemoryGamePM x1 y1 x2 y2-->open two tiles in the memory game"""
  global tg 
  await ctx.send(memoryGame.openTilePair([[int(x1),int(y1)],[int(x2),int(y2)]],tg.grid))

@client.command()
async def roll(ctx,dice: str):
    """usage- roll num -->Rolls a number between 1 and num"""
    try:
        x=int(dice)
        if (x<1):
            await ctx.send("╭∩╮(≖_≖ )╭∩╮")
        else:
            await ctx.send(random.randint(1,x))
    except:
        await ctx.send(dice+" is not a number dingus.")
@client.command()
async def latex(ctx,txt: str):
    plt.text(0.5,0.5, r"$%s$" %(txt),fontsize=30,va="center",ha="center")
    
    fig = plt.gca()
    fig.frameon=False
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    fig.axes.axis('off')
    plt.savefig("latex.png")
    await ctx.send( file=discord.File("latex.png"))
    plt.clf()
    
client.run(token)