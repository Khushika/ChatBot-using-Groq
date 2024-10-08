import logging
from aiogram import Bot, Dispatcher, types
from aiogram import run  # Use run for aiogram 3.x
from dotenv import load_dotenv
import os
from groq import Groq 

# Load environment variables from .env file
load_dotenv()
API_TOKEN = os.getenv('TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')  # Add your Groq API key

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def command_start_handler(message: types.Message):
    """
    This handler receives messages with `/start` or `/help` command
    """
    await message.reply("Hi\nI am Legal Advisor Bot!\nCreated by Khushika.")

@dp.message_handler()
async def echo(message: types.Message):
    """
    This will return an echo of the received message.
    """
    user_input = message.text
    print(f">>> USER: \n\t{user_input}")  # Log user input

    # Create a completion request using Groq
    completion = client.chat.completions.create(
        model="llama3-70b-8192",  
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,  # Set stream to False to handle it in one go
    )

    # Process the response
    groq_response = completion['choices'][0]['message']['content']
    print(f">>> Groq: \n\t{groq_response}")
    await message.answer(groq_response)  # Send the response back to the user

if __name__ == "__main__":
    # Start polling updates from Telegram using run
    run(dp, skip_updates=True)  # Use run for aiogram 3.x
