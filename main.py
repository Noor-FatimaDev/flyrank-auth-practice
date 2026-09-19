from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from supabase import Client, create_client
from pydantic import BaseModel
import os

load_dotenv()

supabase: Client = create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_KEY")
)

class SignupRequest(BaseModel):
    email: str
    password: str
    
app = FastAPI()

@app.on_event("startup")
async def startup_check():
    print("Server running and connected to Supabase client")
    
@app.post("/auth/signup", status_code=201)
def signup(body: SignupRequest):
    if not body.email or not body.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    return supabase.auth.sign_up({"email": body.email, "password": body.password})
        
@app.post("/auth/login", status_code=200)
def login(body: SignupRequest):
    if not body.email or not body.password:
        raise HTTPException(status_code=401, detail={ "error": "Invalid login credentials" })
    return supabase.auth.sign_in_with_password({"email": body.email, "password": body.password})