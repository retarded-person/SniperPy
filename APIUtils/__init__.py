import requests
import time
import discord
from discord.ext import commands
import random
from fake_useragent import UserAgent
ua = UserAgent()



class Generator:
    def user_agent(headers=None):
        if headers == None:
            return ua.random
        
            
        headers["user_agent"] = ua.random
        return headers

class Discord:
    def __init__(self, token):
        self.token = token
        
    base_url = 'https://discord.com/api/v9'
    
    def url(self, t):
        return Discord.base_url + t
    
    def headers(self):
        header = {
            "authorization": self.token
        }
        return header
    
        
        


