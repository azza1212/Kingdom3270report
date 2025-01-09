import streamlit as st
import discord
import asyncio
import threading
import logging
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import time  # Import time module for adding delay

# Configure logging
logging.basicConfig(level=logging.INFO)

# Use your verified TextChannel ID
CHANNEL_ID = 1269107089894263259  # Correct TextChannel ID

# Global event to track when the bot is ready
bot_ready_event = threading.Event()

# Global list to store bot responses
bot_responses = []

class MyClient(discord.Client):
    _instance = None  # Singleton instance to ensure only one bot runs

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MyClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_initialized'):
            intents = discord.Intents.default()
            intents.messages = True  # Ensure the bot can receive message events
            super().__init__(intents=intents, *args, **kwargs)
            self.channel_id = CHANNEL_ID
            self.channel = None  # To store the channel once fetched
            self._initialized = True

    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')
        try:
            guild = self.guilds[0]  # Assumes the bot is only in one guild
            for channel in guild.channels:
                logging.info(f"Found channel: {channel.name} (ID: {channel.id}) - Type: {type(channel)}")
                if channel.id == self.channel_id and isinstance(channel, discord.TextChannel):
                    self.channel = channel
                    break
            if self.channel:
                logging.info(f"Connected to text channel: {self.channel.name}")
                bot_ready_event.set()
            else:
                logging.error("Text channel with the specified ID not found!")
        except discord.Forbidden:
            logging.error("Bot doesn't have permission to access the channels! Please check the channel permissions.")
        except discord.HTTPException as e:
            logging.error(f"HTTP error occurred: {e}")

    async def on_message(self, message):
        if message.author == self.user:
            # Capture bot's own messages and store in global list
            bot_responses.append(message.content)
            logging.info(f"Bot response captured: {message.content}")  # Log the captured response

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
            logging.error("Text channel not found! Please verify the channel ID and permissions.")

    def send_message_sync(self, message):
        """Send a message synchronously (blocking)"""
        if self.channel:
            logging.info(f"Scheduling message: {message}")
            asyncio.run_coroutine_threadsafe(self.send_message_async(message), self.loop)
        else:
            logging.error("Text channel not found! Please verify the channel ID and permissions.")

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
        )
    )

    return decrypted_message.decode()

# Create and run the bot only once
def run_bot():
    logging.info("Starting the bot...")
    global client
    if not hasattr(run_bot, '_client_started'):
        run_bot._client_started = True
        client = MyClient()
        client.run(decrypt_key())  # This runs the bot and manages its event loop

def handle_request_title():
    """Handle Streamlit UI for title requests."""
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
        # Clear previous responses
        bot_responses.clear()

        # Wait for the bot to be ready before sending the message
        if bot_ready_event.wait(timeout=30):  # Wait up to 30 seconds for the bot to be ready
            client.send_message_sync(message)
            st.success("Message sent successfully!")

            # Add a slight delay for the bot's response to be captured
            time.sleep(2)  # Adjust the delay as needed

            # Display bot response
            if bot_responses:
                st.markdown(f"**Bot Response**: {bot_responses[-1]}")
            else:
                st.warning("No response from the bot yet.")
        else:
            st.warning("Bot is not ready yet. Try again after a moment.")
    elif message == "":
        st.warning("Message cannot be empty.")

# Entry point to run the bot and Streamlit app
if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    handle_request_title()
