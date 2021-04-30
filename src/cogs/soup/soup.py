# General
import asyncio
import datetime
import logging
import pytz
import json
local_timezone = pytz.timezone("Europe/Oslo")

# Discord
import discord
from discord import channel
from discord.ext import commands, tasks

# Custom

logger = logging.getLogger(__name__)


class Soup(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.name = type(self).__name__
        self.delta = datetime.timedelta(minutes=10)
        with open("src/cogs/soup/codes.json", "r", encoding="utf") as f:
            self.codes = json.load(f)
        print(f"Cog {self.name} loaded")
        logger.info(f"Cog {self.name} loaded")

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.client.guilds[0]
        self.channelId = discord.utils.get(self.client.get_all_channels(), guild=self.guild, name='suppekjøkkenet').id
        self.channel = self.client.get_channel(self.channelId)
        logger.info(f"Deploying cleaner to Channel: {self.channelId}")
        self.cleanup.start()


    @commands.command()
    async def kok(self, ctx:commands.Context, code:str, info:str, extra_info:str=""):
        message:discord.Message = ctx.message
        attachments = message.attachments
        name:str = self.codes[code]


        if len(attachments) < 1:
            await ctx.send("Did you forget to attach a file?")
            return
        elif len(attachments) > 1:
            await ctx.send("Oh no, I can't handle all those files at once")
            return
        
        kok:str = f"**{code}** : {name}\n{info}\n{extra_info}"
        await self.channel.send(kok, file = await attachments[0].to_file())

    @kok.error
    async def kok_error(self, ctx, error):
        await ctx.send("I don't understand. Did you maybe forget to close you quotes?")


    @tasks.loop(hours=1)
    async def cleanup(self):
        for message in await self.channel.history(limit=123).flatten():
            if (len(message.attachments) < 1) and (datetime.datetime.now(tz=local_timezone) > local_timezone.localize(message.created_at) + datetime.timedelta(hours=12)):
                await message.delete()
    


def setup(client):
    client.add_cog(Soup(client))