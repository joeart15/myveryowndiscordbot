import discord
import os
from ec2_metadata import ec2_metadata

# Get the bot token from environment variables
TOKEN = os.getenv('TOKEN')

# Configure intents to listen for messages
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Command: "hello"
    if message.content.lower() == 'hello':
        await message.channel.send('Hello! How can I assist you?')

    # Command: "!serverinfo"
    elif message.content.lower() == '!serverinfo':
        try:
            # Fetch EC2 metadata
            region = ec2_metadata.region
            availability_zone = ec2_metadata.availability_zone
            public_ipv4 = ec2_metadata.public_ipv4

            # Format the response
            response = (
                f"**EC2 Instance Metadata:**\n"
                f"Region: {region}\n"
                f"Availability Zone: {availability_zone}\n"
                f"Public IPv4: {public_ipv4}"
            )
        except Exception as e:
            # Handle errors when retrieving EC2 metadata
            response = f"An error occurred while retrieving EC2 metadata: {str(e)}"

        # Send the response to Discord
        await message.channel.send(response)

    # Command: "!ping"
    elif message.content.lower() == '!ping':
        await message.channel.send('Pong!')

    # Command: "!uptime"
    elif message.content.lower() == '!uptime':
        try:
            # Fetch uptime from the EC2 instance
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                hours, remainder = divmod(uptime_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                response = f"EC2 Uptime: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
        except Exception as e:
            # Handle errors when retrieving uptime
            response = f"An error occurred while retrieving uptime: {str(e)}"

        await message.channel.send(response)

    # Handle unknown commands
    else:
        await message.channel.send("Sorry, I didn't understand that command. Try `hello`, `!serverinfo`, `!ping`, or `!uptime`.")

# Run the bot
client.run(TOKEN)
