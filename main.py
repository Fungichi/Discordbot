import discord
import sqlite3

TOKEN = "MTI1OTEyODA3OTI5NzgxMDQ1NA.Gk5uIH.RRRN6bibP-UGT0dACmqr_NrGnA9cXVDe05jTe8"  
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
        await message.channel.send('Here is a list of commands: ```*help - Displays this message\n *ping - Pings the bot\n```')
        
    elif message.content.lower() == '*ping':
        await message.channel.send('Aura is online')
        
    elif message.content.lower().startswith('*'):
        await message.channel.send('Invalid command. Use ```*help``` to see a list of available commands.')
    elif message.content.lower() == '*register':
        username = str(message.author)
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user is already registered
        cursor.execute('SELECT * FROM user_stats WHERE username = ?', (username,))
        result = cursor.fetchone()

        if result:
            await message.send(f'{username}, you are already registered.')
        else:
            # Register the user with default aura of 0
            cursor.execute('INSERT INTO user_stats (username, aura) VALUES (?, ?)', (username, 0))
            conn.commit()
            await message.send(f'{username}, you have been successfully registered!')

        conn.close()
    

client.run(TOKEN)
