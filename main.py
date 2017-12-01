import atexit
from signal import *
import csv
import logging
import discord
from discord.ext import commands

logging.basicConfig(level=logging.DEBUG)

class EmotMe:
    """ Bot that edit message to put big smileys """

    def __init__(self, bot):
        self.bot = bot
        self.emots = {}
        self.load_emots()

    @commands.command(no_pm=True, pass_context=True)
    async def emadd(self, context, emot: str, url: str):
        """ Add an emoji """
        if emot is not None and url is not None:
            if emot not in self.emots.keys():
                self.emots[emot] = url.strip("\n")
                
                with open("emots.csv", mode="w", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for key, value in self.emots.items():
                        writer.writerow([key, value])

                await self.bot.say(":white_check_mark:  **" + emot + "** Added !")
            else:
                await self.bot.say(":x: Emoji **" + emot + "** already exist !")
        else:
            await self.bot.say(":x: You must specify your emot and the emoji name !")

    @commands.command(no_pm=True, pass_context=True)
    async def emdel(self, context, *, emot: str):
        """ Delete an emoji """

        if emot is not None:
            if emot in self.emots.keys():
                del self.emots[emot]
                await self.bot.say(":white_check_mark:  **" + emot + "** Deleted !")
            else:
                await self.bot.say(":x: Uknown emoji **" + emot + "**")
        else:
            await self.bot.say(":x: you must specify an emoji !")

    @commands.command(no_pm=True, pass_context=True)
    async def em(self, context, *, emot: str):
        """ Print an emoji """

        if emot is not None:
            if emot in self.emots.keys() :
                await self.bot.delete_message(context.message)
                await self.bot.say(self.emots[emot])
            else:
                await self.bot.say(":x: **" + emot + "** does not exist ! Use **$emadd** to create it !")
        else:
            await self.bot.say(":x: You must specify an emoji !")

    @commands.command(no_pm=False, pass_context=True)
    async def emlist(self, context):
        """ List all available emojis """
        keys = self.emots.keys()

        if len(keys) > 0:
            await self.bot.say("\n".join(keys))
        else:
            await self.bot.send_message(context.message.author, ":x: No emoji found, you can add them with **$emadd**")
        return

    def load_emots(self):
        """ Load emoji directory """
        with open("emots.csv", mode="r", newline='') as csvfile:
            reader = csv.reader(csvfile)
            self.emots = dict(reader)
    


async def my_command_error(exception, context):
    """ Handle error """
    command = context.invoked_with

    await BOT.send_message(context.message.channel, ":x: An error occured.BlockingIOError")
    return

BOT = commands.Bot(command_prefix=commands.when_mentioned_or("$"))
cog = EmotMe(BOT)
BOT.add_listener(my_command_error, "on_command_error")

BOT.add_cog(cog)

# Put your bot token here
BOT.run('token')