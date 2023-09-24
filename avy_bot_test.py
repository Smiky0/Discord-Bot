import discord
import os
import random
import requests
from webserver import keep_alive

client = discord.Client()


# food list
def show_food():
    food_gif = [
        "PUT A LIST OF FOOD GIFS WHICH ARE PRESENT IN YOUR LOCAL DIRECTORY"]
    food = random.choice(food_gif)
    return food


# restricted words
restricted_words = ["PUT A LIST OF BAD WORDS HERE"]


#exclude this func if you dont want to know those user names..
# write bad_words user name in file
def write_on_file(user, word):
    try:
        file = open('direct_msg.txt', 'a+')
        user = str(user)
        word = str(word)
        file.write(user + " : " + word + "\n")
    except Exception as e:
        print(e)
        print(user, word)
    finally:
        file.close()


# prints logged in after connecting
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("avy help"))
    print("Logged in as {0.user}".format(client))


# to ignore bots own messages.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

# interaction commands work under this if statement
# posts message anonymously
    if (message.channel.id == "CHANNEL ID"):
        await message.channel.purge(limit=1)
        color = 0xbdbdbd
        # check for bad words
        for msg in restricted_words:
            if (msg in (message.content).lower()):
                #write_on_file(message.author, message.content)
                message.content = "WARNING:\nYou are not allowed to use bad words here."
                color = 0xff0000
        # make variable value change globally
        global user
        # user contains prev user id.. if current and prev user doesnt match
        if (message.author != user):
            # embed color change
            color = 0x0ebcb7
            # user value changes to current
            user = message.author
        # if message content is a gif this will post it as normal msg instead of embeded
        if (message.content.startswith("https://tenor.com")):
            await message.channel.send(message.content)
        # else embed them
        else:
            if (message.content.startswith("/")):
                message.content = str(message.content[1:])
                embedMessage = discord.Embed(description=message.content,
                                             color=color)
                await message.channel.send(embed=embedMessage)

    # DM message reply (in case someone dms ur bot)
    elif not message.guild:
        # sends to the user
        try:
            write_on_file(message.author, message.content)
            await message.channel.send("I don't talk in DM sorryy ^.^ ")
        except discord.errors.Forbidden:
            pass

    # other channels
    else:
        # make it lowercase
        message.content = message.content.lower()
        # reply to hello message
        if message.content.startswith("hello avy"):
            await message.channel.send(
                "Hello, <:wave:926004643656515594> hope you are doing well... <:coolthumbsup:927913013976117278>"
            )

        # check for bad words
        for ew in restricted_words:
            if message.content.startswith(ew):
                warning_msg = "**WARNING:** \nYou aren't allowed to use that word in this server. "
                embedMessage = discord.Embed(description=warning_msg,
                                             color=0xff0000)
                await message.channel.send(embed=embedMessage)

    # reply to happy_new_year_msg
        if message.content.startswith("happy new year"):
            await message.channel.send(
                "HAPPY NEW YEAR :star2: !!")

    # reply to avy jokes
        if message.content.startswith("avy joke"):
            response_joke = requests.get(
                'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,racist&type=twopart'
            )
            await message.channel.send(response_joke.json().get("setup"))
            await message.channel.send(response_joke.json().get("delivery"))

    # reply to bored message
        bored_list = [
            "avy im bored", "avy i'm bored", "avy i am bored",
            "avy im still bored"
        ]
        for msg in bored_list:
            if message.content.startswith(msg):
                response_bored = requests.get(
                    "https://www.boredapi.com/api/activity/")
                await message.channel.send(
                    response_bored.json().get("activity"))

"""
#no need to include lol
# reply to avy is boring message
        boring_lst = ["avy is boring", "avy you are boring", "avy boring"]
        for msg in boring_lst:
            if message.content.startswith(msg):
                await message.channel.send("Heh? Then have some water..  ^_-")
                await message.channel.send(file=discord.File('give-water.gif'))
"""
    # replies to shush avy
        if message.content.startswith("shush avy"):
            await message.channel.send(
                "Sorry Senpai")

    # sends gif to rickroll message
        if message.content.startswith("avy rickroll"):
            try:
                await message.channel.send(
                    file=discord.File('rickroll-roll.gif'))
            except:
                await message.channel.send("Failed to send gif!")

    # sends gif to show food
        food = show_food()
        if message.content.startswith("avy food"):
            try:
                await message.channel.send(file=discord.File(food))
            except:
                await message.channel.send("Failed to send gif!")

    # adds emoji to message
        if ("sadge") in message.content:
            await message.add_reaction("<'EMOJI'>")
    # for laughing
        laugh_lst = ['gagi', 'haha', 'gago', 'hehe']
        for laugh in laugh_lst:
            if (laugh) in message.content:
                await message.add_reaction("<'EMOJI'>")
    # for noice
        if ("noice") in message.content:
            await message.add_reaction("<'EMOJI'>")

    # help embed message
        if message.content.startswith("avy help"):
            embedMessage = discord.Embed(
                description="**Support Yuji's Garden at-**\nTop.gg - [Vote or review us on top.gg.](https://top.gg/servers/918183414824329226) \nDisboard - [Vote or review us on disboard.](https://disboard.org/server/918183414824329226)\n\n**Avy's commands:**\n-hello avy\n-avy joke\n-avy im bored\n-avy boring\n-avy rickroll\n-avy food\n\t~*no special character needed*",
                color=0x00b7eb)
            await message.channel.send(embed=embedMessage)


my_secret = "SECRET_KEY"
# keep_alive()
client.run(my_secret)
