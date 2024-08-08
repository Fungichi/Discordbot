import discord
import sqlite3

TOKEN = ""
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.guilds = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)
def get_db_connection():
    conn = sqlite3.connect('stats.sql')
    return conn
def find_stats(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_stats WHERE username = ?', (username,))
    result = cursor.fetchone()
    if result:
        aura, tokens = result[1], result[2]
        return aura, tokens
    else:
        return None

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    try:
        channel = client.get_channel(1259126694757929042)
        if channel:
            await channel.send("ONLINE")
            print("[Starting sequence]:COMPLETE")
        else:
            print("Channel not found or bot has no access to the channel")
    except Exception as e:
        print(f"An error occurred: {e}")

@client.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")  
    if message.author == client.user:
        return
    if message.content.lower() == '*help':
        await message.channel.send('Here is a list of commands:\n `*help` - Displays this message\n `*ping` - Pings the bot\n `*stats` - Displays your stats\n `*register`- Registers you as a user of the aura system')
        
    elif message.content.lower() == '*ping':
        await message.channel.send('Aura is online')
        
    
    elif message.content.lower() == '*register':
        username = str(message.author)
        conn = get_db_connection()
        cursor = conn.cursor()

        
        cursor.execute('SELECT * FROM user_stats WHERE username = ?', (username,))
        result = cursor.fetchone()

        if result:
            await message.channel.send(f'{username}, you are already registered.')
        else:
            
            cursor.execute('INSERT INTO user_stats (username, aura, tokens) VALUES (?, ?, ?)', (username, 0, 500))
            conn.commit()
            await message.channel.send(f'{username}, you have been successfully registered!')

        conn.close()
    elif message.content.lower() == "*stats":
        username = str(message.author)
        
        stats = find_stats(username)
        if stats is not None:
            aura, tokens = stats
            await message.channel.send(f'{username}, your stats:\n Aura: `{aura}`\n Tokens: `{tokens}`')
        else:
            await message.channel.send(f'{username}, you are not registered. Use the command `*register` to register.')

    elif message.content.lower().startswith('*stats'):
        username = message.content.split(' ')[1]
        stats = find_stats(username)
        if stats is not None:
            aura, tokens = stats
            await message.channel.send(f'{username}, stats:\n Aura: `{aura}`\n Tokens: `{tokens}`')
        else:
            await message.channel.send(f'{username}, is not registered. Use the command `*register` to register.')
        
    elif message.content.lower().startswith('*'):
        await message.channel.send('Invalid command. Use ```*help``` to see a list of available commands.')

client.run(TOKEN)
