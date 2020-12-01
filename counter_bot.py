import discord
import pendulum
import json
from pathlib import Path

STORAGE_PATH = Path('storage.json')

# persistent storage
try:
    storage = json.loads(STORAGE_PATH.read_text())
except FileNotFoundError:
    storage = dict()
    STORAGE_PATH.write_text(json.dumps(storage))
    

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/counter help'):
        # TODO
        return

    elif message.content.startswith('/counter timezone'):
        try:
            tz = message.content.split(' ')[2]
            if tz not in pendulum.timezones:
                # TODO
                return

            if message.author.id not in storage:
                storage[message.author.id] = {'timezone': tz}
            else:
                storage[message.author.id]['timezone'] = tz

            STORAGE_PATH.write_text(json.dumps(storage))

        except IndexError:
            return
    
    elif message.content.startswith('/counter delete'):
        if message.author.id in storage:
            del storage[message.author.id]
        STORAGE_PATH.write_text(json.dumps(storage))


    elif message.content.startswith('/counter'):

        if message.author.id in storage:
            tz = storage[message.author.id]['timezone']
        else:
            # TODO: error message that you should run `/counter timezone` first
            return

        try:
            _, date = message.content.split(' ')
            year, month, day = (int(i) for i in date.split('-'))

            dt = pendulum.datetime(year, month, day, tz=tz)
            delta = pendulum.now(tz) - dt

            storage[message.author.id]['date'] = f'{year}-{month}-{day}'
            
            STORAGE_PATH.write_text(json.dumps(storage))

            # TODO: remove this
            await message.channel.send(f'{delta.days} days recorded.')

        except Exception:
            return
        


if __name__ == '__main__':
    token = Path('token.txt').read_text()
    client.run(token)