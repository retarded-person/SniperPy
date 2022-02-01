from re import L
import re
import sys
import requests
from APIUtils import Discord
from configparser import ConfigParser
from colorama import Fore
import colorama, os, requests, time, discord
from discord import Webhook
from discord.ext import commands
import discum     
import random
from fake_useragent import UserAgent
import io 
import json
ua = UserAgent()

def set_title(title):
    os.system(f"title {title}")



colorama.init(True)
set_title('Giveaway Sniper')
config = ConfigParser()
config.read('config.ini')

z = open('dm_messages.json')
dm_messages = json.load(z)
all_arrays = []
for arrays in dm_messages:
    all_arrays.append(arrays)

token = config["settings"]["token"]
webhook = config["settings"]["webhook"]
scrape_previous_giveaways = config["settings"]["scrape_previous_giveaways"]
giveaway_join_delay = config["settings"]["giveaway_join_delay"]

bot = discum.Client(token=token, log=False, user_agent=ua.random)

invite_links = []
total_snipes = 0


print(f"""{Fore.LIGHTMAGENTA_EX}  ▄████  ██▓ ██▒   █▓▓█████ ▄▄▄       █     █░ ▄▄▄     ▓██   ██▓        ██████  ███▄    █  ██▓ ██▓███  ▓█████  ██▀███  
 ██▒ ▀█▒▓██▒▓██░   █▒▓█   ▀▒████▄    ▓█░ █ ░█░▒████▄    ▒██  ██▒      ▒██    ▒  ██ ▀█   █ ▓██▒▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
▒██░▄▄▄░▒██▒ ▓██  █▒░▒███  ▒██  ▀█▄  ▒█░ █ ░█ ▒██  ▀█▄   ▒██ ██░      ░ ▓██▄   ▓██  ▀█ ██▒▒██▒▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
░▓█  ██▓░██░  ▒██ █░░▒▓█  ▄░██▄▄▄▄██ ░█░ █ ░█ ░██▄▄▄▄██  ░ ▐██▓░        ▒   ██▒▓██▒  ▐▌██▒░██░▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄  
░▒▓███▀▒░██░   ▒▀█░  ░▒████▒▓█   ▓██▒░░██▒██▓  ▓█   ▓██▒ ░ ██▒▓░      ▒██████▒▒▒██░   ▓██░░██░▒██▒ ░  ░░▒████▒░██▓ ▒██▒
 ░▒   ▒ ░▓     ░ ▐░  ░░ ▒░ ░▒▒   ▓▒█░░ ▓░▒ ▒   ▒▒   ▓▒█░  ██▒▒▒       ▒ ▒▓▒ ▒ ░░ ▒░   ▒ ▒ ░▓  ▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
  ░   ░  ▒ ░   ░ ░░   ░ ░  ░ ▒   ▒▒ ░  ▒ ░ ░    ▒   ▒▒ ░▓██ ░▒░       ░ ░▒  ░ ░░ ░░   ░ ▒░ ▒ ░░▒ ░      ░ ░  ░  ░▒ ░ ▒░
░ ░   ░  ▒ ░     ░░     ░    ░   ▒     ░   ░    ░   ▒   ▒ ▒ ░░        ░  ░  ░     ░   ░ ░  ▒ ░░░          ░     ░░   ░ 
      ░  ░        ░     ░  ░     ░  ░    ░          ░  ░░ ░                 ░           ░  ░              ░  ░   ░     
                 ░                                      ░ ░                                                            """)
print(f"""{Fore.LIGHTWHITE_EX}using webagent: {ua.random}\n""")

class Channel(Discord):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        super().__init__(token=token)
    
    def get_messages(self):
        req = requests.get(self.url(f'/channels/{self.id}/messages'), headers=self.headers())
        return req.json()

class Guild(Discord):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        super().__init__(token=token)


    def channels(self):
        req = requests.get(self.base_url + f'/guilds/{self.id}/channels', headers=self.headers())
        return req.json()


class Sniper(Discord):
    def get_guilds(self):
        req = requests.get(self.base_url + "/users/@me/guilds", headers=self.headers())
        return req.json()
    
    
    def get_id(self):
        try:
            user = requests.get(self.base_url + "/users/@me", headers=self.headers()).json()
            return user["id"]
        except:
            return 400
        
        
    def check_invite(self, invite):
        code = invite.replace('https://discord.gg/', '')
        x = requests.get('https://discord.com/api/v9/invites/' + code, headers=self.headers())
        return x
    
    def run(self):
        print(f"{Fore.LIGHTWHITE_EX}>>> This sniper was made by Mythxcal, modified by Lunar | Blast <<<")
        
        id = self.get_id()
        if id != 400:
            print(f"{Fore.LIGHTCYAN_EX}[*] Sniper Started (ID: {id}) (Method: 1)")
        else:
            print(f"{Fore.LIGHTRED_EX}[*] Improper Token Has Been Passed")
            time.sleep(5)
            exit()
            
        print(f"{Fore.LIGHTBLUE_EX}[!] Sniping Giveaways")
        for g in self.get_guilds():
            count = 0
            guild_id = g["id"]
            guild_name = g["name"]
            guild = Guild(id=guild_id, name=guild_name)
            for c in guild.channels():
                channel = Channel(id=c["id"], name=c["name"])
                
                if ('giveaway' in channel.name) or ('drop' in channel.name) or ('leave' in channel.name) or (c["position"] < 3) or ('req' in channel.name) or ('special' in channel.name) or ('gw' in channel.name) or ('ad' in channel.name) or ('🎉' in channel.name) or ('🎁' in channel.name) or ('here' in channel.name) or ('set' in channel.name) or ('godly' in channel.name) or ('gem' in channel.name) or ('💎' in channel.name):
                    for message in channel.get_messages():
                        try:
                            author_id = message["author"]["id"]
                            content = message["content"]
                            message_id = message["id"]
                            if author_id == '294882584201003009':
                                if "**GIVEAWAY**" in content:
                                    x = requests.put(self.url(f'/channels/{channel.id}/messages/{message_id}/reactions/%F0%9F%8E%89/@me'), headers=self.headers())    
                                    count += 1
                                    global total_snipes
                                    total_snipes += 1             
                                    time.sleep(3)

                            for word in content.split():
                                if 'https://discord.gg/' in word:
                                    invite_links.append(word)
                                    
                        except Exception as e:            
                            pass
            if count != 0:
                print(f"{Fore.LIGHTYELLOW_EX}[!] Sniped {count} giveaway(s) in {guild_name}") 

                
                
        

sniper = Sniper(token=token)    

if config.getboolean('settings', 'scrape_previous_giveaways') == True:
    sniper.run()
else:
    print(f"{Fore.LIGHTWHITE_EX}>>> This sniper was made by Mythxcal, modified by Lunar | Blast <<<")
    
print(f"{Fore.LIGHTYELLOW_EX}[!] Joined {total_snipes} Giveaways")


def send_webhook(msg):
    payload = {"content": msg}
    x = requests.post(webhook, json=payload)

def send_embed_webhook(title, description, color):
    payload = {"embeds": [
            {
                "title": title,
                "description": description,
                "color": color
            }
        ]
    }

    x = requests.post(webhook, json=payload)

for invite in invite_links:
    if sniper.check_invite(invite).status_code == 200:
        send_webhook(invite)    
    else:
        invite_links.remove(invite)
        
        
print(f"{Fore.LIGHTBLUE_EX}[!] Sent requirement servers to webhook")
print(f"{Fore.LIGHTBLUE_EX}[!] Scraping previous snipes complete!")

base_url = 'https://discord.com/api/v9'
header = {
    "authorization": 'MzAxNTI5MTM2NDM3MDAyMjQw.YfYkPg.vqqzXecNkWJfpowD3XEbhcZAanM'
}
json = {}
json2 = {}

@bot.gateway.command
def a(resp):
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print(f"{Fore.LIGHTCYAN_EX}[*] Sniper Started (ID: {user['id']}) (Method: 2)")
        print(f"{Fore.LIGHTBLUE_EX}[!] Awaiting for new giveaways and nitro...")

    if resp.event.message:
        m = resp.parsed.auto()
        user = bot.gateway.session.user
        guildID = m['guild_id'] if 'guild_id' in m else None #because DMs are technically channels too
        channelID = m['channel_id']
        username = m['author']['username']
        discriminator = m['author']['discriminator']
        content = m['content']
        if "discord.gift" in content or "discord.com/gifts" in content or "discordapp.com/gifts" in content:
            content = content.replace("https://", "")
            content = content.replace("discord.gift/", "")
            content = content.replace("discord.com/gifts/", "")
            content = content.replace("discordapp.com/gifts/", "")
            if len(content) == 16:
                r = requests.post(
                    f"https://discordapp.com/api/v7/entitlements/gift-codes/{content}/redeem",
                    headers=header,
                ).text

                if "subscription_plan" in r:
                    print(Fore.GREEN + f"[!] Sucessfully sniped nitro! - Code: {content}")
                    send_webhook("<@325849904570302469>")
                    send_embed_webhook("Nitro Snipe", f"Code: {content}", 5814783)
                else:
                    print(Fore.RED + f"[!] Invalid Nitro Code - Code: {content}")
            else:
                print(Fore.RED + f"[!] Fake Nitro Code - Code: {content}")
        if username == "GiveawayBot" and discriminator == "2381" or "giveaway" in username.lower():
            if "Hosted by:" in m['embeds'][0]['description']:
                target_str = m['embeds'][0]['description']
                buf = io.StringIO(target_str)
                res_str = buf.readlines()
                res_str = res_str[len(res_str)-1]
                res_str = res_str.replace("Hosted by:", "")
                res_str = res_str.replace("<@", "")
                res_str = res_str.replace(">", "")
                res_str = res_str.replace(" ", "")
                res_str = res_str.replace("\n", "")
                json.update({f'{guildID}':res_str})
                json2.update({f'{guildID}':m['embeds'][0]['author']['name']})

            if "GIVEAWAY" in content:
                if config.getboolean('settings', 'giveaway_join_delay') == False:
                    requests.put(base_url + f'/channels/{channelID}/messages/{m["id"]}/reactions/%F0%9F%8E%89/@me', headers=header)
                else:
                    if config.getboolean('settings', 'giveaway_join_delay') == True:
                        time.sleep(30) 
                        requests.put(base_url + f'/channels/{channelID}/messages/{m["id"]}/reactions/%F0%9F%8E%89/@me', headers=header)
                    try:
                        tmp = int(giveaway_join_delay)
                        time.sleep(giveaway_join_delay)
                        requests.put(base_url + f'/channels/{channelID}/messages/{m["id"]}/reactions/%F0%9F%8E%89/@me', headers=header)
                    except:
                        time.sleep(30)
                        requests.put(base_url + f'/channels/{channelID}/messages/{m["id"]}/reactions/%F0%9F%8E%89/@me', headers=header)

                req = requests.get(base_url + "/users/@me/guilds", headers=header)
                for guild in req.json():
                    if str(guild["id"]) == str(guildID):
                        guild_name = guild["name"]
                
                if config.getboolean('settings', 'giveaway_join_delay') == False:
                    print(Fore.LIGHTYELLOW_EX + f"[!] Sniped new giveaway in {guild_name}")
                else:
                    if config.getboolean('settings', 'giveaway_join_delay') == True:
                        print(Fore.LIGHTYELLOW_EX + f"[!] Sniped new giveaway in {guild_name} and waited 30s")
                    try:
                        tmp = int(giveaway_join_delay)
                        print(Fore.LIGHTYELLOW_EX + f"[!] Sniped new giveaway in {guild_name} and waited {giveaway_join_delay}s")
                    except:
                        print(Fore.LIGHTYELLOW_EX + f"[!] Sniped new giveaway in {guild_name} and waited 30s")

                send_webhook("<@325849904570302469>")
                send_embed_webhook(f"Sniped giveaway in {guild_name}", f"Prize: {json2[guildID]}\nHost: {json[guildID]}", 5814783)
            if f"<@{user['id']}>!" in content:
                wait = random.randrange(45,75)
                req = requests.get(base_url + "/users/@me/guilds", headers=header)
                for guild in req.json():
                    if str(guild["id"]) == str(guildID):
                        guild_name = guild["name"]
                print(Fore.LIGHTYELLOW_EX + f"[!] We won {json2[guildID]} from a giveaway in {guild_name}!")
                send_webhook("<@325849904570302469>")
                send_embed_webhook(f"Won giveaway in {guild_name}", f"Prize: {json2[guildID]}\nHost: {json[guildID]}", 5814783)
                print(Fore.GREEN + f"[!] Sending DM to {json[guildID]} in {wait}s")
                array = random.choice(all_arrays)
                time.sleep(wait)
                newDM = bot.createDM([str(json[guildID])]).json()["id"] 
                time.sleep(random.randrange(1,2))
                bot.typingAction(newDM)
                time.sleep(0.5)
                for sentence in dm_messages[array]:
                    time.sleep(random.randrange(2,3))
                    bot.sendMessage(newDM, str(sentence))

                print(Fore.LIGHTCYAN_EX + f"[!] Sent DM to {json[guildID]}")
                send_webhook("<@325849904570302469>")
                send_embed_webhook(f"AutoDM | Giveaway Won | {guild_name}", f"Prize: {json2[guildID]}\nHost: {json[guildID]}\nDM Message: {dm_messages[array]}", 5814783)
                
    
bot.gateway.run(auto_reconnect=True)
