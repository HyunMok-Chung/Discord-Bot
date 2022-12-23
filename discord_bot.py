import discord
from discord.ext import commands
import json
import riot

class ChatBot(discord.Client):
    async def on_ready(self):
        game = discord.Game("도지 1달러")
        await bot.change_presence(status=discord.Status.online, activity=game)
        print("Ready")
        
    async def on_message(self,message):
        if message.author.bot: #메시지 보낸 곳이 봇이면 어떠한 작업도 하지 않음
            return None
        
        if message.content == "!제작자":
            channel = message.channel
            msg = "정현목\n홍지민"
            await channel.send(msg)
            return None
        if message.content == "!로테이션":
            rotation = riot.RiotData().getChampRotation() #추후 수정
            channel = message.channel
            print(rotation)
            await channel.send(rotation)
            return None
    
    def runBot(self):
        with open('key.json') as json_file:
            json_data = json.load(json_file)
        Discord_Key = json_data['Discord_Key']
        bot.run(Discord_Key)

if __name__ == "__main__":
    bot = ChatBot()
    bot.runBot()