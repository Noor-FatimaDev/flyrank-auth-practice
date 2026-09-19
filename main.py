from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer
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

security = HTTPBearer()

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

@app.get("/public/info")
def public_info():
    return {"message":"Welcome stranger! This info is public."}

security = HTTPBearer(auto_error=False)

@app.get("/protected/profile")
def protected_profile(credentials = Depends(security)):
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=401, detail={"error": "Access token required"})
    token = credentials.credentials
    try:
        user = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail={"error": "Invalid or expired token"})
    return {
        "id": user.user.id,
        "email": user.user.email,
        "created_at": user.user.created_at,
    }