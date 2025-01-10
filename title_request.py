import discord
import streamlit as st
import asyncio
import threading
import logging
import time
import requests
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

logging.basicConfig(level=logging.INFO)

DISCORD_TOKEN = 'YOUR_VALID_DISCORD_BOT_TOKEN'  # Replace with your actual bot token
CHANNEL_ID = 1269107769462755349

bot_ready_event = threading.Event()

responses = []

class MyClient(discord.Client):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MyClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_initialized'):
            intents = discord.Intents.default()
            intents.messages = True
            intents.message_content = True
            intents.guilds = True
            super().__init__(intents=intents, *args, **kwargs)
            self.channel_id = CHANNEL_ID
            self.channel = None
            self._initialized = True

    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')
        try:
            guild = self.guilds[0]
            for channel in guild.channels:
                logging.info(f"Found channel: {channel.name} (ID: {channel.id})")
                if channel.id == self.channel_id and isinstance(channel, discord.TextChannel):
                    self.channel = channel
                    break
            if self.channel:
                logging.info(f"Connected to text channel: {self.channel.name}")
                bot_ready_event.set()
            else:
                logging.error("Text channel with the specified ID not found!")
        except discord.Forbidden:
            logging.error("The bot doesn't have permission to access the channels! Please check the channel permissions.")
        except discord.HTTPException as e:
            logging.error(f"HTTP error occurred: {e}")

    async def on_message(self, message):
        if message.channel.id == self.channel_id and message.author != self:
            responses.append(message)
            logging.info(f"Response captured: {message.content}")

    async def send_message_async(self, message):
        if self.channel:
            try:
                logging.info(f"Sending message: {message}")
                await self.channel.send(message)
                logging.info("Message sent successfully!")
            except Exception as e:
                logging.error(f"Failed to send message: {e}")
        else:
            logging.error("Text channel not found! Verify the channel ID and permissions.")

    def send_message_sync(self, message):
        if self.channel:
            logging.info(f"Scheduling message: {message}")
            asyncio.run_coroutine_threadsafe(self.send_message_async(message), self.loop)
        else:
            logging.error("Text channel not found! Verify the channel ID and permissions.")

def decrypt_key():
    try:
        with open("private_key.pem", "rb") as private_file:
            private_key = serialization.load_pem_private_key(
                private_file.read(), 
                password=None
            )
        logging.info("Private key loaded successfully.")
    except FileNotFoundError:
        logging.error("private_key.pem file not found.")
        return None
        
    try:
        with open("encrypted_message.bin", "rb") as enc_file:
            encrypted_message = enc_file.read()
        logging.info("Encrypted message loaded successfully.")
    except FileNotFoundError:
        logging.error("encrypted_message.bin file not found.")
        return None

    try:
        decrypted_message = private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        logging.info("Decryption successful.")
    except Exception as e:
        logging.error(f"Failed to decrypt message: {e}")
        return None

    return decrypted_message.decode()

def fetch_latest_messages(bot_token, channel_id):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {"Authorization": f"Bearer {bot_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to fetch messages: {response.status_code} {response.text}")
        return []

def run_bot():
    logging.info("Starting the bot...")
    global client
    if not hasattr(run_bot, '_client_started'):
        run_bot._client_started = True
        client = MyClient()
        decrypted_key = decrypt_key()
        if decrypted_key:
            client.run(decrypted_key)
        else:
            logging.error("Bot failed to start. Check the decryption process.")

def handle_request_title():
    st.title('Request title')

    title = st.selectbox('Choose Title', options=['justice', 'scientist', 'duke', 'architect'])
    hk_lk = st.selectbox('Choose HK or LK', options=['hk', 'lk'])
    x_coord = st.text_input('Enter X Coordinate')
    y_coord = st.text_input('Enter Y Coordinate')

    if st.button('Send Message') and title and hk_lk and x_coord and y_coord:
        message = f"{title} {hk_lk} {x_coord} {y_coord}"

        responses.clear()

        if bot_ready_event.wait(timeout=30):
            client.send_message_sync(message)
            st.success("Message sent successfully!")

            time.sleep(2)  # Delay to allow the first response to be captured

            # Fetch and display the latest messages from the channel
            latest_messages = fetch_latest_messages(DISCORD_TOKEN, CHANNEL_ID)
            
            for msg in latest_messages:
                st.markdown(f"**{msg['author']['username']}**: {msg['content']}")

            logging.info("Messages fetched and displayed successfully!")

        else:
            st.warning("Bot is not ready yet. Try again after a moment.")
    else:
        st.warning("All fields are required.")

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    handle_request_title()





