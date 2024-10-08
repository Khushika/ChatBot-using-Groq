import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from groq import AsyncGroq

# Load environment variables from .env file
load_dotenv()
API_TOKEN = os.getenv('TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the Groq client
client = AsyncGroq(api_key=GROQ_API_KEY)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start", "help"))
async def command_start_handler(message: types.Message):
    """Handler for /start and /help commands."""
    await message.reply("Hello! I'm your Legal Advisor bot\n Created by Khushika.")

@dp.message(F.text)
async def echo_handler(message: types.Message):
    """Echo the received message and respond using Groq."""
    user_input = message.text
    print(f">>> USER: \n\t{user_input}")  # Log user input

    # Create a completion request using Groq
    response = await client.chat.completions.create(
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
        stream=True,
        stop=None,
    )

    # Process the response
    groq_response = ""
    async for chunk in response:
        if chunk.choices[0].delta.content is not None:
            groq_response += chunk.choices[0].delta.content

    print(f">>> Groq: \n\t{groq_response}")
    await message.answer(groq_response)  # Send the response back to the user

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

'''
For debugging :

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

# Print to verify that the key is loaded correctly
print("Groq API Key:", groq_api_key)  # For debugging purposes
'''
