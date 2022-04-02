from email import message
from http import client
import discord
import time
import typing
import asyncio
from discord.ext import commands
import os
import json
from datetime import datetime
import aiosqlite
import functools
import itertools
import math
import random
import youtube_dl
from async_timeout import timeout
from dotenv import load_dotenv
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
from discord import TextChannel
from youtube_dl import YoutubeDL
from discord import Intents
import re
import aiohttp
from discord import FFmpegPCMAudio
import atexit
import uuid
import datetime
import aiofiles
from datetime import datetime
from discord import Embed
from discord_components import *
from discord.ext.commands.cooldowns import BucketType
import sqlite3
from os import listdir
from os.path import isfile, join
import sys, traceback
from time import time
from inspect import getsource
from typing import Optional
from math import floor
from typing import List
from discord_components import Button, ButtonStyle













bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())










db = sqlite3.connect("BankAccounts.db")
cur = db.cursor()
START_BALANCE = 1000
START_WALLET = 1000



players = {}


cmdsettings = {}







load_dotenv()





@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command()
@commands. has_permissions(ban_members=True)
async def ban(ctx, members: commands.Greedy[discord.Member],
                   delete_days: typing.Optional[int] = 0, *,
                   reason: str):
    """Mass bans members with an optional delete_days parameter"""
    for member in members:
        await member.ban(delete_message_days=delete_days, reason=reason)

@bot.command() 
async def add(ctx, *nums):
    operation = " + ".join(nums)
    await ctx.send(f'{operation} = {eval(operation)}')

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked from the server.')

@bot.command()
@commands.has_permissions(manage_roles=True) # Check if the user executing the command can manage roles
async def create_role(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'Role `{name}` has been created')


@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx , amount=5):
  await ctx.channel.purge(limit=amount + 1)

@bot.command()
async def create_channel(ctx, channel_name):
	guild = ctx.guild
	channel = await guild.create_text_channel(channel_name)

@bot.command()
async def say(ctx, *, text):
    await ctx.send(text)

@bot.command()
@commands.has_permissions(manage_channels = True)
async def create_category(ctx , arg2):
  await ctx.guild.create_category(arg2)

##### START LEVEL COMMAND #####
 
with open("users.json", "ab+") as ab:
    ab.close()
    f = open('users.json','r+')
    f.readline()
    if os.stat("users.json").st_size == 0:
      f.write("{}")
      f.close()
    else:
      pass
 
with open('users.json', 'r') as f:
  users = json.load(f)
 
@bot.event    
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)
        await add_experience(users, message.author)
        await level_up(users, message.author, message)
        with open('users.json', 'w') as f:
            json.dump(users, f)
            await bot.process_commands(message)
 
async def add_experience(users, user):
  if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 0
  users[f'{user.id}']['experience'] += 6
  print(f"{users[f'{user.id}']['level']}")
 
async def level_up(users, user, message):
  experience = users[f'{user.id}']["experience"]
  lvl_start = users[f'{user.id}']["level"]
  lvl_end = int(experience ** (1 / 4))
  if lvl_start < lvl_end:
    await message.channel.send(f':tada: {user.mention} has reached level {lvl_end}. Congrats! :tada:')
    users[f'{user.id}']["level"] = lvl_end
 
@bot.command()
async def rank(ctx, member: discord.Member = None):
  if member == None:
    userlvl = users[f'{ctx.author.id}']['level']
    await ctx.send(f'{ctx.author.mention} You are at level {userlvl}!')
  else:
    userlvl2 = users[f'{member.id}']['level']
    await ctx.send(f'{member.mention} is at level {userlvl2}!')
 
##### END LEVEL COMMAND #####


@bot.command()
async def ticket(ctx, *, args = None):

    await bot.wait_until_ready()

    if args == None:
        message_content = "Please wait, we will be with you shortly!"
    
    else:
        message_content = "".join(args)

    with open("data.json") as f:
        data = json.load(f)

    ticket_number = int(data["ticket-counter"])
    ticket_number += 1

    ticket_channel = await ctx.guild.create_text_channel("ticket-{}".format(ticket_number))
    await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

    for role_id in data["valid-roles"]:
        role = ctx.guild.get_role(role_id)

        await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
    
    await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    em = discord.Embed(title="New ticket from {}#{}".format(ctx.author.name, ctx.author.discriminator), description= "{}".format(message_content), color=0x00a8ff)

    await ticket_channel.send(embed=em)

    pinged_msg_content = ""
    non_mentionable_roles = []

    if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
            role = ctx.guild.get_role(role_id)

            pinged_msg_content += role.mention
            pinged_msg_content += " "

            if role.mentionable:
                pass
            else:
                await role.edit(mentionable=True)
                non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
            await role.edit(mentionable=False)
    
    data["ticket-channel-ids"].append(ticket_channel.id)

    data["ticket-counter"] = int(ticket_number)
    with open("data.json", 'w') as f:
        json.dump(data, f)
    
    created_em = discord.Embed(title="Auroris Tickets", description="Your ticket has been created at {}".format(ticket_channel.mention), color=0x00a8ff)
    
    await ctx.send(embed=created_em)

@bot.command()
async def close(ctx):
    with open('data.json') as f:
        data = json.load(f)

    if ctx.channel.id in data["ticket-channel-ids"]:

        channel_id = ctx.channel.id

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

        try:

            em = discord.Embed(title="Auroris Tickets", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0x00a8ff)
        
            await ctx.send(embed=em)
            await bot.wait_for('message', check=check, timeout=60)
            await ctx.channel.delete()

            index = data["ticket-channel-ids"].index(channel_id)
            del data["ticket-channel-ids"][index]

            with open('data.json', 'w') as f:
                json.dump(data, f)
        
        except asyncio.TimeoutError:
            em = discord.Embed(title="Auroris Tickets", description="You have run out of time to close this ticket. Please run the command again.", color=0x00a8ff)
            await ctx.send(embed=em)

        

@bot.command()
async def addaccess(ctx, role_id=None):

    with open('data.json') as f:
        data = json.load(f)
    
    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass
    
    if valid_user or ctx.author.guild_permissions.administrator:
        role_id = int(role_id)

        if role_id not in data["valid-roles"]:

            try:
                role = ctx.guild.get_role(role_id)

                with open("data.json") as f:
                    data = json.load(f)

                data["valid-roles"].append(role_id)

                with open('data.json', 'w') as f:
                    json.dump(data, f)
                
                em = discord.Embed(title="Auroris Tickets", description="You have successfully added `{}` to the list of roles with access to tickets.".format(role.name), color=0x00a8ff)

                await ctx.send(embed=em)

            except:
                em = discord.Embed(title="Auroris Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title="Auroris Tickets", description="That role already has access to tickets!", color=0x00a8ff)
            await ctx.send(embed=em)
    
    else:
        em = discord.Embed(title="Auroris Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
        await ctx.send(embed=em)

@bot.command()
async def delaccess(ctx, role_id=None):
    with open('data.json') as f:
        data = json.load(f)
    
    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass

    if valid_user or ctx.author.guild_permissions.administrator:

        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("data.json") as f:
                data = json.load(f)

            valid_roles = data["valid-roles"]

            if role_id in valid_roles:
                index = valid_roles.index(role_id)

                del valid_roles[index]

                data["valid-roles"] = valid_roles

                with open('data.json', 'w') as f:
                    json.dump(data, f)

                em = discord.Embed(title="Auroris Tickets", description="You have successfully removed `{}` from the list of roles with access to tickets.".format(role.name), color=0x00a8ff)

                await ctx.send(embed=em)
            
            else:
                
                em = discord.Embed(title="Auroris Tickets", description="That role already doesn't have access to tickets!", color=0x00a8ff)
                await ctx.send(embed=em)

        except:
            em = discord.Embed(title="Auroris Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
            await ctx.send(embed=em)
    
    else:
        em = discord.Embed(title="Auroris Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
        await ctx.send(embed=em)

@bot.command()
async def addpingedrole(ctx, role_id=None):

    with open('data.json') as f:
        data = json.load(f)
    
    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass
    
    if valid_user or ctx.author.guild_permissions.administrator:

        role_id = int(role_id)

        if role_id not in data["pinged-roles"]:

            try:
                role = ctx.guild.get_role(role_id)

                with open("data.json") as f:
                    data = json.load(f)

                data["pinged-roles"].append(role_id)

                with open('data.json', 'w') as f:
                    json.dump(data, f)

                em = discord.Embed(title="Auroris Tickets", description="You have successfully added `{}` to the list of roles that get pinged when new tickets are created!".format(role.name), color=0x00a8ff)

                await ctx.send(embed=em)

            except:
                em = discord.Embed(title="Auroris Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)
            
        else:
            em = discord.Embed(title="Auroris Tickets", description="That role already receives pings when tickets are created.", color=0x00a8ff)
            await ctx.send(embed=em)
    
    else:
        em = discord.Embed(title="Auroris Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
        await ctx.send(embed=em)

@bot.command()
async def delpingedrole(ctx, role_id=None):

    with open('data.json') as f:
        data = json.load(f)
    
    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass
    
    if valid_user or ctx.author.guild_permissions.administrator:

        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("data.json") as f:
                data = json.load(f)

            pinged_roles = data["pinged-roles"]

            if role_id in pinged_roles:
                index = pinged_roles.index(role_id)

                del pinged_roles[index]

                data["pinged-roles"] = pinged_roles

                with open('data.json', 'w') as f:
                    json.dump(data, f)

                em = discord.Embed(title="Auroris Tickets", description="You have successfully removed `{}` from the list of roles that get pinged when new tickets are created.".format(role.name), color=0x00a8ff)
                await ctx.send(embed=em)
            
            else:
                em = discord.Embed(title="Auroris Tickets", description="That role already isn't getting pinged when new tickets are created!", color=0x00a8ff)
                await ctx.send(embed=em)

        except:
            em = discord.Embed(title="Auroris Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
            await ctx.send(embed=em)
    
    else:
        em = discord.Embed(title="Auroris Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
        await ctx.send(embed=em)


@bot.command()
@commands.has_permissions(administrator=True)
async def addadminrole(ctx, role_id=None):

    try:
        role_id = int(role_id)
        role = ctx.guild.get_role(role_id)

        with open("data.json") as f:
            data = json.load(f)

        data["verified-roles"].append(role_id)

        with open('data.json', 'w') as f:
            json.dump(data, f)
        
        em = discord.Embed(title="Auroris Tickets", description="You have successfully added `{}` to the list of roles that can run admin-level commands!".format(role.name), color=0x00a8ff)
        await ctx.send(embed=em)

    except:
        em = discord.Embed(title="Auroris Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
        await ctx.send(embed=em)

@bot.command()
@commands.has_permissions(administrator=True)
async def deladminrole(ctx, role_id=None):
    try:
        role_id = int(role_id)
        role = ctx.guild.get_role(role_id)

        with open("data.json") as f:
            data = json.load(f)

        admin_roles = data["verified-roles"]

        if role_id in admin_roles:
            index = admin_roles.index(role_id)

            del admin_roles[index]

            data["verified-roles"] = admin_roles

            with open('data.json', 'w') as f:
                json.dump(data, f)
            
            em = discord.Embed(title="Auroris Tickets", description="You have successfully removed `{}` from the list of roles that get pinged when new tickets are created.".format(role.name), color=0x00a8ff)

            await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title="Auroris Tickets", description="That role isn't getting pinged when new tickets are created!", color=0x00a8ff)
            await ctx.send(embed=em)

    except:
        em = discord.Embed(title="Auroris Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
        await ctx.send(embed=em)

@bot.command()
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog') # Make a request
      dogjson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Doggo!", color=discord.Color.purple()) # Create embed
   embed.set_image(url=dogjson['link']) # Set the embed image to the value of the 'link' key
   await ctx.send(embed=embed) # Send the embed



@bot.event
async def on_message_delete(message):
    bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@bot.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = bot.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)





@bot.command()
async def balance(ctx):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    async with aiosqlite.connect("BankAccounts.db") as db:
        cur = await db.cursor()
        await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
        await cur.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        result_userID = await cur.fetchone()

    if result_userID is None:
        async with aiosqlite.connect("BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute('insert into Accounts(user_name, user_id, balance, wallet) values(?,?,?,?)', (USER_NAME, USER_ID, START_BALANCE, START_WALLET))
            await db.commit()
        await ctx.send('We gave you 2000c. you now have 1kc in your bank and other half in wallet')
    else:   
        async with aiosqlite.connect("BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
            #SQL.execute(f'select wallet from Accounts where user_id="{USER_ID}"')
            result_userbal = await cur.fetchone()
            await cur.execute(f'select wallet from Accounts where user_id="{USER_ID}"')
            result_userwallet = await cur.fetchone()
        emb = discord.Embed(title='Bank')
        emb.add_field(name='Wallet: ', value=f'{result_userbal[0]}$', inline=False)
        emb.add_field(name='Bank: ', value=f'{result_userwallet[0]}$', inline=False)
        await ctx.send(embed=emb)

@bot.command()
async def beg(ctx):

    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    async with aiosqlite.connect("BankAccounts.db") as db:
        cur = await db.cursor()
        await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
        await cur.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        result_userID =await cur.fetchone()

    if result_userID is None:
        await ctx.send(f'{ctx.message.author.mention} please create an account using balance command')
    else:
        #db.commit()
        random_amount = random.randint(0,100)
        async with aiosqlite.connect("BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute(f'UPDATE Accounts SET balance = balance + {random_amount} where user_id={USER_ID}')
            await db.commit()
        await ctx.send(f'Daddy gave you {random_amount}')

@bot.command()
async def deposite(ctx, amount:int):
    USER_ID = ctx.message.author.id
    async with aiosqlite.connect("BankAccounts.db") as db:
        cur = await db.cursor()
        await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
        await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
        result_userID = await cur.fetchone()
    if result_userID is None:
        await ctx.send('🖕Please create an account using balance command before you deposite')  
    elif result_userID:      
        wallet_balance = int(result_userID[0])
    if amount > wallet_balance:
        await ctx.send('You do not have enough money to do that')
    elif str(amount) <= str(wallet_balance):
        async with aiosqlite.connect("BankAccounts.db") as db:    
            cur = await db.cursor()
            await cur.execute(f'UPDATE Accounts SET wallet = wallet + {int(amount)} where user_id={USER_ID}')
            await db.commit()
            await cur.execute(f'UPDATE Accounts SET balance = balance - {int(amount)} where user_id={USER_ID}')
            await db.commit()
        await ctx.send(f'Successfully transfered {amount} to your bank') 
    else:
        await ctx.send(f"{ctx.message.author.mention} That's why yo mama dead")    

@bot.command()
async def withdraw(ctx, amount:int):
    USER_ID = ctx.message.author.id
    async with aiosqlite.connect("BankAccounts.db") as db:
        cur = await db.cursor()
        await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
        await cur.execute(f'select wallet from Accounts where user_id="{USER_ID}"')
        result_userID = await cur.fetchone()
    if result_userID is None:
        await ctx.send('🖕Please create an account using balance command before you deposite')
    elif result_userID:
        bank_balance = int(result_userID[0])
    if amount > bank_balance:
        await ctx.send('You do not have enough money to do that')
    elif str(amount) <= str(bank_balance):
        async with aiosqlite.connect("BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute(f'UPDATE Accounts SET wallet = wallet - {int(amount)} where user_id={USER_ID}')
            await db.commit()
            await cur.execute(f'UPDATE Accounts SET balance = balance + {int(amount)} where user_id={USER_ID}')
            await db.commit() 
        await ctx.send(f'Successfully withdrawn {amount}')
    else:
        await ctx.send(f"{ctx.message.author.mention} That's why yo mama dead")                     


@deposite.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(f"{ctx.message.author.mention} That's why yo mama dead") 

@bot.command()
async def search(ctx):
    USER_ID = ctx.message.author.id
    async with aiosqlite.connect("BankAccounts.db") as db:
        cur = await db.cursor()
        await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
        result_userID = await cur.fetchone()
    if result_userID is None:
        await ctx.send('Mofo Create an account first using balance command')    
    else:
        options = ['Socks', 'Hell', 'Toilet', 'Dog', 'Lawn', 'Couch', 'Sex house']
        option1 = random.choice(options)
        options.remove(option1)
        option2 = random.choice(options)
        options.remove(option2)
        option3 = random.choice(options)

        embed1 = discord.Embed(title='Disclaimer',description='What do you want to search', color=0xfcba03)
        embed1.add_field(name='search', value=f"``{option1}``,``{option2}``, ``{option3}`` ")
        await ctx.send(embed=embed1)

        def msg_check(m):
            return m.author == ctx.message.author and m.channel == ctx.channel

        try:
            response = await bot.wait_for('message', check=msg_check, timeout=10.0)
            if str(response) == option1.lower() or option2.lower() or option3.lower():
                random_money = random.randint(0,2000)
                async with aiosqlite.connect("BankAccounts.db") as db:
                    cur = await db.cursor()
                    await cur.execute(f'UPDATE Accounts SET balance = balance + {random_money} where user_id={USER_ID}')
                    await db.commit()
                await ctx.send(f'``You searched {response.content} and found {random_money}$ ``')
            else:
                await ctx.send('Bruh')    
        except asyncio.TimeoutError:
            await ctx.send('Dumbass you ran out of time')







@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user
  
  if (user.name, user.discriminator) == (member_name, member_discriminator):
    await ctx.guild.unban(user)
    await ctx.send(f"{user} have been unbanned sucessfully")
    return



def sub(x:float ,y: float): #Used for subtractiom
	return x-y

def add(x:float ,y: float): #used for Addition
	return x+y

def div(x:float ,y: float): #usef for division
	return x/y

def mul(x:float ,y: float): #used for multiplication
	return x*y

def rando(x:int ,y: int):
	return random.randint(x,y) #returns the random integer between these two arguments

def sqrt(x:float):
	return math.sqrt(x)


#All commands are over now



@bot.command()
async def mathsub(ctx,x:float,y:float):
	res=sub(x,y)
	await ctx.send(res)

@bot.command()
async def mathdiv(ctx,x:float,y:float):
	res=div(x,y)
	await ctx.send(res)

@bot.command()
async def mathmul(ctx,x:float,y:float):
	res=mul(x,y)
	await ctx.send(res)

@bot.command()
async def mathrandom(ctx,x:float,y:float):
	res=rando(x,y)
	await ctx.send(res)

@bot.command()
async def mathsqrt(ctx,x:float):
	res=sqrt(x)
	await ctx.send(res)

# End of Functions


# music starts

# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
@bot.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


# command to play sound from a youtube URL
@bot.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Bot started playing music')

# check if the bot is already playing
    else:
        await ctx.send("Bot already plays music")
        return


# command to resume voice if it is paused
@bot.command()
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Music has been resumed')


# command to pause voice if it is playing
@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Music has been paused')


# command to stop voice
@bot.command()
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Stopping.....')


# music stop


@bot.command()
async def create_embed(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send('Waiting for a title')
    title = await bot.wait_for('message', check=check)
  
    await ctx.send('Waiting for a description')
    desc = await bot.wait_for('message', check=check)

    embed = discord.Embed(title=title.content, description=desc.content, color=0x72d345)
    await ctx.send(embed=embed)





@bot.command()
@commands.has_permissions(manage_roles=True) #permissions
async def giverole(ctx, user : discord.Member, *, role : discord.Role):
  if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
    return await ctx.send('**:x: | That role is above your top role!**') 
  if role in user.roles:
      await user.remove_roles(role) #removes the role if user already has
      await ctx.send(f"Removed {role} from {user.mention}")
  else:
      await user.add_roles(role) #adds role if not already has it
      await ctx.send(f"Added {role} to {user.mention}") 



@bot.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

@bot.command()
@commands.has_permissions(administrator=True)
async def react(ctx, Message: discord.Message, *,  emoji):
    await Message.add_reaction(emoji)

       



@bot.command()
async def cat(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat')
      catjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/cat')
      catfact = await request2.json()

   embed = discord.Embed(title="cat!", color=discord.Color.purple())
   embed.set_image(url=catjson['link'])
   embed.set_footer(text=catfact['fact'])

   await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="meme", description="here a meme for you!")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def nsfw(ctx):
    embed = discord.Embed(title="nsfw!")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/nsfw/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)




@bot.event
async def on_ready():
    activity = discord.Game(name="!help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
print("im online")










bot.run("NopE")

 
