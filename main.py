from dotenv import load_dotenv
from supabase import Client, create_client
from fastapi import FastAPI
import os

load_dotenv()

supabase: Client = create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_KEY")
)

app = FastAPI()

@app.on_event("startup")
async def startup_check():
    print("Server running and connected to Supabase client")