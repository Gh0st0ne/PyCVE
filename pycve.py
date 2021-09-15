import os
import discord
import re
import requests

#oauth https://discord.com/api/oauth2/authorize?client_id=886979811648602173&permissions=2064&scope=bot

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
client = commands.Bot(command_prefix='!')

def cveSearch(id):
    r = requests.get("https://services.nvd.nist.gov/rest/json/cve/1.0/{}".format(id))
    data = r.json()
    return data

class initializeBot:
    @client.event
    async def on_ready():
        print(f'{client.user} is online!')

    @client.event
    async def on_guild_join(guild):
        chans = await guild.fetch_channels()
        if 'cve-alerts' in chans:
            return
        else:
            await guild.create_text_channel('cve-alerts', position=0)
            
    @client.command()
    async def cve(ctx, id):
        valid = re.match('(^[A-Za-z]*[-]\d*[-]\d*)', id)
        if valid:
            search = cveSearch(id)
            try:
                result = search['result']['CVE_Items'][0]['cve']
                cve_assigner = result['CVE_data_meta']['ASSIGNER']
                cve_desc = result['description']['description_data'][0]['value']
                cve_url = "https://cve.mitre.org/cgi-bin/cvename.cgi?name={}".format(id)
                await ctx.send('**CVE ID:** {}\n**CVE Assigner:** {}\n**CVE Description:** {}\n**MITRE URL:** {}'.format(id, cve_assigner, cve_desc, cve_url))
            except KeyError:
                await ctx.send('{} not found'.format(id))
        else:
            await ctx.send('You did not give me a valid CVE ID')
  
    client.run(TOKEN)