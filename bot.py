import discord
import requests
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

headers = {
    'User-Agent': 'RuneXchange',
    'From': 'Meme25327#4475'
}

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(msg):
    if msg.author == client.user: #ignores the message if it comes from the bot
        return
   

    #splits the message to find the arguments. stored in the format of a list
    splitMsg = msg.content.split(' ')
    args = splitMsg[1:]

    if msg.content.startswith("%rs"):
        if msg.content.startswith("%rs latest"):
            name = ' '.join(args[1:])
            id_list = requests.get('https://rsbuddy.com/exchange/names.json', headers = headers)
            ids = id_list.json()
            for i in ids:
                global item_id
                item_name = (ids[i]['name'])
                if item_name.lower() == name.lower():
                    break
            item_id = str(i)
            print(item_id)
            print("got to item_id")
            url = "https://prices.runescape.wiki/api/v1/osrs/latest?id=" + item_id + ".json"
            print("got to url")
            price_json = requests.get(url, headers=headers)
            data = price_json.json()
            high_price = data['data'][item_id]['high']
            low_price = data['data'][item_id]['low']
            result = "The current highest price of " + name + " is " + str(high_price) + ", and the current lowest price is " + str(low_price)
            print("got to result")
            await msg.channel.send(result)
        elif msg.content.startswith("%rs help"):
            await msg.channel.send("RuneXchange's help menu can be found at: https://meme25327.github.io/RuneXchange/index.html")
            

# PRICE EXAMPLE {'data': {'4151': {'high': 2482752, 'highTime': 1616508592, 'low': 2478103, 'lowTime': 1616508582}}}
# NAME EXAPLE 2:{'name': 'Cannonball', 'store': 5}

client.run(TOKEN)
