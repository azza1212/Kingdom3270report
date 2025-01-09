import streamlit as st
import discord
import asyncio
import threading
import logging
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Configure logging
logging.basicConfig(level=logging.INFO)

# Replace with your channel ID
CHANNEL_ID = 1269107769324077255  # Ensure this ID is correct

# Global event to track when the bot is ready
bot_ready_event = threading.Event()

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        super().__init__(intents=intents, *args, **kwargs)
        self.channel_id = CHANNEL_ID
        self.channel = None  # To store the channel once fetched

    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')
        # Print all available channels for debugging
        for guild in self.guilds:
            for channel in guild.channels:
                logging.info(f'Channel: {channel.name} (ID: {channel.id})')

        try:
            self.channel = await self.fetch_channel(self.channel_id)
            logging.info(f"Connected to channel: {self.channel.name}")
            bot_ready_event.set()
        except discord.NotFound:
            logging.error("Channel not found! Please verify the channel ID.")
        except discord.Forbidden:
            logging.error("Bot doesn't have permission to access the channel! Please check the channel permissions.")
        except discord.HTTPException as e:
            logging.error(f"HTTP error occurred: {e}")

    async def send_message_async(self, message):
        """Send a message asynchronously"""
        if self.channel:
            try:
                logging.info(f"Sending message: {message}")
                await self.channel.send(message)
                logging.info("Message sent successfully!")
            except Exception as e:
                logging.error(f"Failed to send message: {e}")
        else:
            logging.error("Channel not found! Please verify the channel ID and permissions.")

    def send_message_sync(self, message):
        """Send a message synchronously (blocking)"""
        if self.channel:
            logging.info(f"Scheduling message: {message}")
            asyncio.run_coroutine_threadsafe(self.send_message_async(message), self.loop)
        else:
            logging.error("Channel not found! Please verify the channel ID and permissions.")

def decrypt_key():
    # Load private key from file
    with open("private_key.pem", "rb") as private_file:
        private_key = serialization.load_pem_private_key(
            private_file.read(),
            password=None,
        )

    # Load the encrypted message from file
    with open("encrypted_message.bin", "rb") as enc_file:
        encrypted_message = enc_file.read()

    # Decrypt the message
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return decrypted_message.decode()

# Create and run the bot in a separate thread
def run_bot():
    global client
    client = MyClient()
    client.run(decrypt_key())  # This runs the bot and manages its event loop

def handle_request_title():
    # Streamlit UI
    st.title('Request title')

    # Get message input from the user
    st.text('Please input: <title> <hk/lk> <x> <y>')
    st.text('Example:')
    st.text('justice lk 1533 547')
    st.text('scientist lk 1533 547')
    st.text('duke lk 1533 547')
    st.text('architect lk 1533 547')
    message = st.text_input('')

    if st.button('Send Message') and message:
        # Wait for the bot to be ready before sending the message
        if bot_ready_event.wait(timeout=30):  # Wait up to 30 seconds for the bot to be ready
            client.send_message_sync(message)
            st.success("Message sent successfully!")
        else:
            st.warning("Bot is not ready yet. Try again after a moment.")
    elif message == "":
        st.warning("Message cannot be empty.")
