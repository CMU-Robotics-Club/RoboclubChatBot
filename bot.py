import discord
import re

with open("apikey.txt") as f:
    API_KEY = f.read().strip()

DO_24HR_CONVERSION = True

class RoboClient(discord.Client):
    async def on_ready(self):
        print("Logged on as {}!".format(self.user))

    async def on_message(self, msg):
        if msg.author == self.user:
            return

        if DO_24HR_CONVERSION:
            msg_txt = msg.clean_content

            if msg_txt[0] == "/":
                msg_txt = msg_txt[0] + " " + msg_txt[1:]

            time_strs = re.findall("(\d+\d:?\d\d+)", msg_txt)
            corrections = []
            for time_str_raw in time_strs:
                time_str = time_str_raw
                if ":" not in time_str:
                    time_str = time_str[:2] + ":" + time_str[2:]
                if len(time_str) != 5:
                    #print("Found bad string: '{}'".format(time_str))
                    continue

                time_hr,time_min = map(int, time_str.split(":"))
                if time_hr > 23 or time_hr < 0 or time_min > 59 or time_min < 0:
                    #print("Found close but not real time: {}".format(time_str))
                    continue

                if ":" in time_str_raw and time_str[0] != "0":
                    continue

                fmt_hr = str(time_hr - 12) if time_hr > 12 else (str(time_hr) if time_hr != 0 else "12")
                fmt_min = "0" + str(time_min) if time_min < 10 else str(time_min)
                fmt_ampm = "PM" if time_hr > 11 else "AM"
                time_12hr = "{}:{} {}".format(fmt_hr, fmt_min, fmt_ampm)
                corrections.append((time_str_raw, time_12hr))

            if len(corrections) > 0:
                msg_trans = msg_txt
                for (incorr, corr) in corrections:
                    msg_trans = msg_trans.replace(incorr, corr)
                await msg.reply("Translation:\n> " + msg_trans)

intents = discord.Intents.default()
intents.message_content = True

client = RoboClient(intents=intents)
client.run(API_KEY)
