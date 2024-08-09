import discord
import sqlite3
import os

TOKEN = os.environ['TOKEN']
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
        await message.channel.send('Here is a list of commands:\n `*help` - Displays this message\n `*aura` - Used to give or take someones aura\n`*ping` - Pings the bot\n `*stats` - Displays your stats\n `*register`- Registers you as a user of the aura system')
        
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
    elif message.content.lower().startswith('*aura'):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            sender = str(message.author)
            receiver = message.content.split(' ')[1]
            amount = int(message.content.split(' ')[2])
            reason = ' '.join(message.content.split(' ')[3:])
            
            
        except(ValueError,IndexError):
            print('Invalid command format')
            await message.channel.send('Invalid command format. Use the command in the following format:\n `*aura <receiver> <amount> <reason>`')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                rstats = find_stats(receiver)
                sstats = find_stats(sender)
                print(rstats)
                print(sstats)
                if rstats is not None and sstats is not None and reason !="" and rstats != sstats:
                    if rstats[1] >= amount:
                        cursor.execute('UPDATE user_stats SET tokens = tokens - ? WHERE username = ?', (abs(amount), sender))
                        cursor.execute('UPDATE user_stats SET aura = aura + ? WHERE username = ?', (amount, receiver))
                        cursor.execute('INSERT INTO transaction_logs (sender_name, receiver_name, amount, description) VALUES (?, ?, ?, ?)',(sender, receiver, amount, reason))
                        await message.channel.send(f'{sender} gave {amount} aura to {receiver} because:\n {reason}')    
                    
                    else:
                        await message.channel.send(f'{sender}, you do not have enough tokens')
                    
                elif sstats == rstats:
                    await message.channel.send('You cannot give yourself aura')
                elif rstats is None:
                    await message.channel.send(f'{receiver} is not registered. Use the command `*register` to register.')

                elif reason == "":
                    await message.channel.send('Invalid command format. Use the command in the following format:\n `*aura <receiver> <amount> <reason>`')
                else:
                    await message.channel.send(f'{sender} is not registered. Use the command `*register` to register.')

                conn.commit()
            finally:
                conn.close()
    elif message.content.lower().startswith('*'):
        await message.channel.send('Invalid command. Use ```*help``` to see a list of available commands.')

client.run(TOKEN)


#TO DO:

