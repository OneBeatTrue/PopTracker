import smtplib
from addition import TOKEN, SENDER_EMAIL, REC_EMAIL, EMAIL_PASSWORD
import discord
import asyncio
import time
import json, requests


TOKEN = TOKEN
HIST = []
ISWRITE = False


class YLBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} has connected to chat:\n'
                f'{guild.name}(id: {guild.id})'
                f'I am ready to to track students.')

    # async def on_member_join(self, member):
    #     await member.create_dm()
    #     # global ISWRITE, HIST
    #     # if ISWRITE:
    #     #     HIST.append(member.name + ' ' + time.asctime().split()[3])
    #     await member.dm_channel.send(
    #         f'Hello, {member.name}!'
    #     )

    async def on_group_join(self, channel, user):
        print(channel, user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.author.mention
            return
        if "set_timer" in message.content.lower():
            a = message.content.lower().split()
            lesson = {}
            dop = []
            for i in a:
                if i.isdigit():
                    dop.append(int(i))
            if not (0 <= dop[0] <= 23 and 0 <= dop[1] <= 60):
                await message.channel.send('You are trying to set th wrong time!')
                return
            await message.channel.send(f'The lesson should start at {dop[0]} hours {dop[1]} minutes and lasts {dop[2]} minutes.') #!!!
            # global ISWRITE
            # ISWRITE = True
            now = [int(i) for i in str(time.asctime().split()[3]).split(':')]
            if now[0] > dop[0] or now[0] == dop[0] and now[1] > dop[1]:
                dop[0] += 24
            await asyncio.sleep((dop[0] - now[0]) * 3600 + (dop[1] - now[1]) * 60) #!!!
            await message.channel.send("The lesson starts!") #!!!
            lesson['At the beginning of the lesson, there were:'] = []
            for guild in client.guilds:
                for member in guild.voice_channels[0].members:
                    lesson['At the beginning of the lesson, there were:'].append(member.name)
                    print(member.name)
            await asyncio.sleep(dop[2] * 60)
            await message.channel.send("The lesson is ended!")
            letter = f'Report on the lesson that started at {dop[0]}:{dop[1]}'
            print(letter)
            for key in lesson.keys():
                print(key)
                print('\n'.join(lesson[key]))
            # await guild.text_channels[0].send(guild.voice_channels[0].members)
            # voice_channel = discord.utils.get(ctx.message.server.channels, name="channelname",
            #                                   type=discord.ChannelType.voice)
            # finds the members
            # members = voice_channel.voice_members
            # print(members)
            # global HIST
            # print('\n'.join(HIST))
            # HIST = []
            # ISWRITE = False

            # letter = 'hello'
            # SERVER = smtplib.SMTP('smtp.gmail.com', 587)
            # SERVER.starttls()
            # SERVER.login(SENDER_EMAIL, EMAIL_PASSWORD)
            # SERVER.sendmail(SENDER_EMAIL, REC_EMAIL, letter)
            return

        # if "member" in message.content.lower():
        #     vch = discord.VoiceChannel
        #     print(vch.members)
        #     for guild in self.guilds:
        #         print(guild.VoiceChannel.members)

        # if "кот" in message.content.lower():
        #     await message.channel.send(requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url'])
        #     return
        # if "собак" in message.content.lower():
        #     await message.channel.send(requests.get('https://dog.ceo/api/breeds/image/random').json()['message'])
        #     return
        # await message.channel.send("Спасибо за сообщение")

        # if "member" in message.content.lower():
        #     voice_channel = discord.utils.get(ctx.message.server.channels, name="channelname", type=discord.ChannelType.voice)
        #     print(111111111)
        #     # finds the members
        #     members = voice_channel.voice_members
        #     memids = []
        #     for member in members:
        #         memids.append(member.id)
        #     print(memids)
        #     return


client = YLBotClient()
client.run(TOKEN)




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
