import discord
import time
from discord.ext import commands

creds={}
client = commands.Bot(command_prefix='.')
client.remove_command('help')

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.online,activity=discord.Game("Storing Creds| .help"))
	print("Bot Is Ready")
@client.command()
async def ping(ctx):
	await ctx.send(f"```yaml\nPong! {round(client.latency*1000)}ms```")
@client.command()
async def clear(ctx,amount):
	amount=int(amount)
	await ctx.channel.purge(limit=amount)
	time.sleep(1)
	await ctx.channel.purge(limit=1)

#FOR STORING CREDS
@client.command()
async def set(ctx,event,credential):
	if(event in creds.keys()):
		embed=discord.Embed(color=12320855)
		embed.add_field(name="**ERROR:(**",value=(f"```HTTP\nEvent name already saved use .show to see creds or try with another username!```"), inline=False)
		await ctx.send(embed=embed)
		#await ctx.send("```Event name already saved use .show to see creds or try with another username!```")
	else:
		creds[event]=credential
		#await ctx.send("""**```HTTP\nCredentials Saved!!```**""")
		embed=discord.Embed(color=12320855)
		embed.add_field(name="**Credentials Saved!!**",value=(f"""```HTTP\n{event} Username and Password are stored```"""), inline=False)
		await ctx.send(embed=embed)

#FOR REMOVING CREDS
@client.command()
async def remove(ctx,event):
	if(event in creds.keys()):
		removed_event=creds.pop(event)
		embed=discord.Embed(color=12320855)
		retStr=str(f"""**```{event} creds  Deleted!!```**""")
		embed.add_field(name="PURGE TIME!!",value=retStr, inline=False)
		await ctx.send(embed=embed)
		#await ctx.send(f"""**```{event} creds  Deleted!!```**""")
	else:
		embed=discord.Embed(color=12320855)
		embed.add_field(name="ERROR:(",value=(f"**```yaml\nNo Credentials stored for {event}```**"), inline=False)
		await ctx.send(embed=embed)
		#await ctx.send(f"**```No Credentials found of {event}```**")

#FOR DISPLAYING CREDS
@client.command()
async def show(ctx,event):
	flag=0
	for key,value in creds.items():
		if(key==event):
			flag=1
			#await ctx.send(f"Credentials of {event} are \n")
			embed=discord.Embed(color=12320855)
			sub=str(creds.get(event))
			lst=sub.split(':')
			uname=str(lst[0])
			pwd=str(lst[1])
			retStr = str(f"""```yaml\n Username is :- {uname}\n Password is :- {pwd}```""")
			embed.add_field(name=(f"**Credentials of {event} are**"), value=retStr, inline=False)
			await ctx.send(embed=embed)
			#await ctx.send(f"Username is {uname}\n Password is {pwd}")
	if(flag==0):
		embed=discord.Embed(color=12320855)
		embed.add_field(name=(f"ERROR!!"), value=(f"```css\nNo Credentials saved for {event}.```"), inline=False)
		await ctx.send(embed=embed)
#FOR HELP
@client.command()
async def help(ctx):
	embed=discord.Embed(color=12320855)
	tmp=str("""Welcome to the CSFNinjas Discord!
	I am CSFNinjas Bot mainly used to store credential for the event""")
	embed.add_field(name=("**CSFNinjas Bot Help**"), value=tmp, inline=False)
	embed.add_field(name=("**.ping**"), value="```Command to check if bot is online and latency.```", inline=False)
	embed.add_field(name=("**.set eventname username:password**"), value="```Saves your username and password for that event.Enter creds in uname:pass format Ex: .set bytecon ashu:pwd```", inline=False)
	embed.add_field(name=("**.remove eventname**"), value="```Delete as much messages from the channel. Ex .clear 5```", inline=False)
	embed.add_field(name=("**.clear amount**"), value="```Delete credentials for that event. Ex: .remove bytecon```", inline=False)
	embed.add_field(name=("**.show eventname**"), value="```Shows credentials for that event. Ex: .show bytecon```", inline=False)
	embed.add_field(name=("**.clear amount**"), value="```Delete as much messages from the channel. Ex .clear 5```", inline=False)
	await ctx.send(embed=embed)
client.run('your_token')
