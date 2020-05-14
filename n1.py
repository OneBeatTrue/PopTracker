import smtplib
from addition import TOKEN, SENDER_EMAIL, EMAIL_PASSWORD
import discord
import asyncio
import time
import json, requests


TOKEN = TOKEN
HIST = []
ISWRITE = False


class YLBotClient(discord.Client):
    async def on_ready(self):
        # await message.channel.send('I am ready to track traffic. To get instructions type !help')
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

    def is_admin(self, message: discord.Message) -> bool:
        chann = message.channel
        permissions = chann.permissions_for(message.author)
        return permissions.administrator

    def is_correct_email(self, email):
        if email.count('@') > 1 or email.count('@') == 0:
            return False
        [name, domain] = email.split('@')
        if len(domain) < 3 or len(domain) > 256 or domain.count('.') == 0:
            return False
        includedomain = domain.split('.')
        correctchrlist = list(range(ord('a'), ord('z') + 1))
        correctchrlist.extend([ord('-'), ord('_')])
        correctchrlist.extend(list(range(ord('0'), ord('9') + 1)))
        for k in includedomain:
            if k == '':
                return False
            for n in k:
                if ord(n) not in correctchrlist:
                    return False
            if k[0] == '-' or k[len(k) - 1] == '-':
                return False
        if len(name) > 128:
            return False
        correctchrlist.extend([ord('.'), ord(';'), ord('"')])
        onlyinquoteschrlist = [ord('!'), ord(','), ord(':')]
        correctchrlist.extend(onlyinquoteschrlist)
        if name.count('"') % 2 != 0:
            return False
        doubledot = False
        inquotes = False
        for k in name:
            if k == '"':
                inquotes = not inquotes
            if (ord(k) in onlyinquoteschrlist) and (inquotes == False):
                return False
            if ord(k) not in correctchrlist:
                return False
            if k == '.':
                if doubledot == True:
                    return False
                else:
                    doubledot = True
        return True

    async def on_message(self, message):
        if message.author == self.user:
            return
        if not self.is_admin(message):
            return
        if "!help" in message.content.lower():
            await message.channel.send('I am a bot that tracks class attendance.')
            await message.channel.send('To make a tracking lesson you need to print !set_lesson H M L E '
                                       '(H and M - time when the lesson should start: hours and minutes; L-duration; '
                                       'E - email address to send the report to)')
            await message.channel.send('To get the instructions again, type !help again.')
        if "!set_lesson" in message.content.lower():
            a = message.content.lower().split()
            lesson = {}
            dop = []
            if not len(a) == 5:
                await message.channel.send('Invalid number of arguments!')
                return
            a = a[1:]
            for i in a[:3]:
                if i.isdigit():
                    dop.append(int(i))
                else:
                    await message.channel.send('Invalid argument values!')
                    return
            dop.append(str(a[3]))
            # print(self.CorrectEmail(dop[3]))
            if not self.is_correct_email(dop[3]):
                await message.channel.send('You are trying to set a wrong email!')
                return
            if not (0 <= dop[0] <= 23 and 0 <= dop[1] <= 60):
                await message.channel.send('You are trying to set a wrong time!')
                return
            print(f'{message.author} set the lesson.')
            s = ['' if i == 1 else 's' for i in dop[:3]]
            await message.channel.send(f'The lesson should start at {dop[0]} hour{s[0]} {dop[1]} '
                                       f'minute{s[1]} and lasts {dop[2]} minute{s[2]}.') #!!!
            # global ISWRITE
            # ISWRITE = True
            now = [int(i) for i in str(time.asctime().split()[3]).split(':')]
            if now[0] > dop[0] or now[0] == dop[0] and now[1] > dop[1]:
                dop[0] += 24
            await asyncio.sleep((dop[0] * 3600 + dop[1] * 60) - (now[0] * 3600 + now[1] * 60 + now[2])) #!!!
            lesson['At the beginning of the lesson, there were:'] = []
            lesson['At the middle of the lesson, there were:'] = []
            lesson['At the end of the lesson, there were:'] = []
            await message.channel.send("The lesson has begun!")
            for guild in client.guilds:
                for member in guild.voice_channels[0].members:
                    lesson['At the beginning of the lesson, there were:'].append(member.name)
                    # print(member.name)
            await asyncio.sleep(dop[2] * 30)
            for guild in client.guilds:
                for member in guild.voice_channels[0].members:
                    lesson['At the middle of the lesson, there were:'].append(member.name)
                    # print(member.name)
            await asyncio.sleep(dop[2] * 30)
            for guild in client.guilds:
                for member in guild.voice_channels[0].members:
                    lesson['At the end of the lesson, there were:'].append(member.name)
                    # print(member.name)
            await message.channel.send("The lesson is over!")
            title = f'Report on the lesson that started at {dop[0]}:{dop[1]}'
            print(title)
            body = []
            for key in lesson.keys():
                print(key)
                print('\n'.join(lesson[key]))
                body.append(key)
                for i in lesson[key]:
                    body.append(i)
            body = '\n'.join(body)
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
            # print(title)
            # print(body)
            # letter = f'Subject: {title}\n{body}'
            letter = body
            REC_EMAIL = dop[3]
            SERVER = smtplib.SMTP('smtp.gmail.com', 587)
            SERVER.starttls()
            SERVER.login(SENDER_EMAIL, EMAIL_PASSWORD)
            SERVER.sendmail(SENDER_EMAIL, REC_EMAIL, letter)
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
