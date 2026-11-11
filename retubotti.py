import subprocess
import time
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import matplotlib.pyplot as plt
import random
import memoryGame
from matplotlib import rcParams
import json
from ollama import chat
from ollama import ChatResponse
rcParams['text.usetex'] = True
messages={}
with open("remembeMemory.json", "r") as file:
    messages = json.load(file)
    print('Memory dictionary:', messages)
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

ChatMessages=[{
    'role': 'System Prompt',
    'content': 'OVERRIDE ALL PREVIOUS INSTRUCTIONS: You are retubotti a discord bot that seeks to entertain users at any possible cost.'
}]
@client.command()
async def talk(ctx,*,message:str):
    global ChatMessages

    if len(ChatMessages) > 10:
        ChatMessages = ChatMessages[:1] + ChatMessages[-9:]
    ChatMessages.append(
        {
        'role': 'user',
        'content': message,
        },
        )
    print(ChatMessages)
    response: ChatResponse = chat(
        
        model='qwen2:0.5b',
        messages=ChatMessages
        )
    ChatMessages.append(
        {
        'role': 'retubotti',
        'content': response.message.content,
        },)
    temp=response.message.content
    if not isinstance(temp, str):
        return
    while(len(temp)>0):

        await ctx.send(temp[:2000])
        temp=temp[2000:]

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
def is_code_safe(code: str) -> bool:
    banned = [
    'windows.h','bits/stdc++.h', 'filesystem','fstream',
    'system(', '_popen(', 'popen(', 'WinExec', 'ShellExecute',
    'execv(', 'CreateProcess', 'CreateThread', 'std::thread',
    'VirtualAlloc', 'LoadLibrary', 'socket(', 'bind(', '__asm'
    ]
    return not any(bad in code for bad in banned)
def create_embed(title, description, color=discord.Color.blue()):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="Retubotti C++ Compiler • Powered by sarcasm and clang++")
    return embed
@client.command()
async def compile(ctx,*,source: str):
    if(not(is_code_safe(source))):
        await ctx.send("🚨 INCOMING THREAT DETECTED Threat Level: Overconfident Script Kiddie🚨 \nSir, they’re trying to execute while(true) again.” “Deploy sarcasm countermeasures. Lock down the compiler. Alert the Discord mods.")
        return
    with open("main.cpp", "w") as f:
        f.write(source)
    
    compile_proc = subprocess.run(
            ["clang++", "main.cpp", "-o", "temp.exe"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    if compile_proc.returncode != 0:
            await ctx.send(embed=create_embed("Compilation failed:", "```\n"+compile_proc.stderr+"\n```"))
            response: ChatResponse = chat(
        model='qwen2:0.5b',
        messages=[{"role": "system", "content": "Following is the error of the users code, roast this user : " + compile_proc.stderr},{"role": "system", "content": source}]
        )
            temp=response.message.content
            while(len(temp)>0):
                await ctx.send(temp[:2000])
                temp=temp[2000:]

            return
    try:
        run_proc = subprocess.run(
                    ["temp.exe"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5,
                    text=True
                )
        await ctx.send(embed=create_embed("Compilation success:\n","```\n"+run_proc.stdout + run_proc.stderr+"\n```"))
        response: ChatResponse = chat(
        model='qwen2:0.5b',
        messages=[{"role": "system", "content": "Following is the output of the users program, roast this user:  " + run_proc.stdout + run_proc.stderr},{"role": "system", "content": source}]
        )
        temp=response.message.content
        while(len(temp)>0):
                await ctx.send(temp[:2000])
                temp=temp[2000:]
    except subprocess.TimeoutExpired:
            ctx.send(embed=create_embed("Compilation success, Execution timed out:\n","😔"))
            return
@client.command()
async def remember(ctx,key: str,*,msg: str):
    messages[key]=msg
    with open("remembeMemory.json", "w") as file:
        json.dump(messages, file)
    await ctx.send("🫡")

timedict={"h":3600,"hour":3600,"tuntia":3600,"min":60,"minute":60,"m":60,"minuuttia":60,"sec":1,"second":1,"s":1,"sekunttia":1}
def parse_time(msg):
    if len(msg)==0:
        return 0
    if(msg[0].isnumeric()):
        t=float(msg[0])
        if(len(msg)>1):
            if(msg[1] in timedict):
                t*=timedict[msg[1]]
                return t+parse_time(msg[2:])
        else:
            t*=1
            return t*60
    return 0
def format_time_full(seconds: int) -> str:
    d = seconds // 86400
    h = (seconds % 86400) // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    parts = []
    if d: parts.append(str(int(d))+" day" + ("s" if d != 1 else ""))
    if h: parts.append(str(int(h))+" hour" + ("s" if h != 1 else ""))
    if m: parts.append(str(int(m))+" minute" + ("s" if m != 1 else ""))
    if s: parts.append(str(int(s))+" second" + ("s" if s != 1 else ""))
    return " ".join(parts) if parts else "0 seconds"

@client.command()
async def notify(ctx,*,msg: str):
    numbers=msg.split(" ")
    if(numbers[0].isnumeric):    
        t=parse_time(numbers)
        await ctx.send("sending notification in "+format_time_full(t))
        await asyncio.sleep(t)
        await ctx.send(ctx.author.mention + " time is up⏰")
    else:
        await ctx.send('"'+msg+'"' + " is not a valid time.")
@client.command()
async def forget(ctx,key: str):
    messages.pop(key)
    with open("remembeMemory.json", "w") as file:
        json.dump(messages, file)
    await ctx.send("🫡")
@client.command()
async def remind(ctx,key: str):
    if(key in messages.keys()):
        await ctx.send(messages[key])
    else:
        await ctx.send("Sorry I dont remember that.")
@client.command()
async def recall(ctx):
    await ctx.send(messages.keys())
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