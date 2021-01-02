import discord
import time
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
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
	await ctx.send(f"```yaml\nBong! {round(client.latency*1000)}ms```")
@client.command()
async def clear(ctx,amount):
	amount=int(amount)
	await ctx.channel.purge(limit=amount)
	time.sleep(1)
	await ctx.channel.purge(limit=1)

#FOR STORING CREDS
@client.command()
async def set(ctx,event,ename,passwrd,url):
	if(event in creds.keys()):
		embed=discord.Embed(color=12320855)
		embed.add_field(name="**ERROR:(**",value=(f"```HTTP\nEvent name already saved use .show to see creds or try with another username!```"), inline=False)
		await ctx.send(embed=embed)
		#await ctx.send("```Event name already saved use .show to see creds or try with another username!```")
	else:
		credential=ename+":"+passwrd+":"+url
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
			url=str(lst[2])+":"+str(lst[3])
			retStr = str(f"""```yaml\n Username is :- {uname}\n Password is :- {pwd}\n URL is :- {url}```""")
			embed.add_field(name=(f"**Credentials of {event} are**"), value=retStr, inline=False)
			await ctx.send(embed=embed)
			#await ctx.send(f"Username is {uname}\n Password is {pwd}")
	if(flag==0):
		embed=discord.Embed(color=12320855)
		embed.add_field(name=(f"ERROR!!"), value=(f"```css\nNo Credentials saved for {event}.```"), inline=False)
		await ctx.send(embed=embed)

#FOR SCORE
@client.command()
async def score(ctx,team_name,url):
	flag=0
	embed=discord.Embed(color=12320855)
	r=requests.get(url+"/scoreboard")
	soup=BeautifulSoup(r.content,"html.parser")
	all_content=soup.find_all('a',href=True)
	for a in all_content:
		if "/teams/" in a["href"]:
			url_1=f"{url}{a['href']}"
			r_1=requests.get(url_1)
			soup_1=BeautifulSoup(r_1.content,"html.parser")
			name=soup_1.find("h1",id="team-id").text
			if(name==team_name):
				flag=1
				dict_url_name={name:url_1}
				url_2=dict_url_name[team_name]
				r_2=requests.get(url_2)
				soup_2=BeautifulSoup(r_2.content,"html.parser")
				team_place=soup_2.find("h2",id="team-place").text
				team_score=soup_2.find("h2",id="team-score").text
				index=team_place.find("place")
				point=team_score.find("points")
				embed.add_field(name="**Position**",value=(f"```{team_place[1:index]}```"),inline=False)
				embed.add_field(name=("**Points**"),value=(f"```{team_score[1:point]}```"),inline=False)
				await ctx.send(embed=embed)
				break
			else:
				await ctx.send(f"```{name}```")
				continue
			break
	if(flag==0):
		embed.add_field(name="ERROR!",value=f"```No team is registered with {team_name}```")
		await ctx.send(embed=embed)


#FOR HELP
@client.command()
async def help(ctx):
	embed=discord.Embed(color=12320855)
	tmp=str("""Welcome to the CSFNinjas Discord!
	I am CSFNinjas Boi mainly used to store credential for the events""")
	embed.add_field(name=("**CSFNinjas Bot Help**"), value=tmp, inline=False)
	embed.add_field(name=("**.ping**"), value="```Command to check if bot is online and latency.```", inline=False)
	embed.add_field(name=("**.set eventname username password url**"), value="```Saves your username and password and URL for that event. Ex: .set bytecon ashu pwd http://xyz.com```", inline=False)
	embed.add_field(name=("**.remove eventname**"), value="```Delete as much messages from the channel. Ex .clear 5```", inline=False)
	embed.add_field(name=("**.clear amount**"), value="```Delete credentials for that event. Ex: .remove bytecon```", inline=False)
	embed.add_field(name=("**.show eventname**"), value="```Shows credentials for that event. Ex: .show bytecon```", inline=False)
	embed.add_field(name=("**.clear amount**"), value="```Delete as much messages from the channel. Ex .clear 5```", inline=False)
	embed.add_field(name=("**.score team_name URL**"),value="```Shows score and position of the team. PS: It's is quite slow because it depends on data stored in website```", inline=False)
	await ctx.send(embed=embed)
client.run('')
