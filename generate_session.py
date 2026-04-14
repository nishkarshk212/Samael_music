import asyncio
from pyrogram import Client

async def generate_session():
    print("Pyrogram Session String Generator")
    print("---------------------------------")
    
    api_id = input("Enter your API_ID: ")
    api_hash = input("Enter your API_HASH: ")
    
    async with Client(":memory:", api_id=int(api_id), api_hash=api_hash) as app:
        session_string = await app.export_session_string()
        print("\nYour SESSION_STRING is:")
        print("-----------------------")
        print(f"\n{session_string}\n")
        print("-----------------------")
        print("Copy the string above and paste it into your .env file.")

if __name__ == "__main__":
    asyncio.run(generate_session())
