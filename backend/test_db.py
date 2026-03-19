import asyncio
import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

async def test_conn():
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("DATABASE_URL not found!")
        return
    
    if url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql+asyncpg://", "postgres://", 1)
        
    print(f"Connecting to: {url}")
    try:
        conn = await asyncpg.connect(url)
        print("Connection successful!")
        await conn.close()
    except Exception as e:
        print(f"Connection failed: {type(e).__name__} - {e}")

if __name__ == "__main__":
    asyncio.run(test_conn())
