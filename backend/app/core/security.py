from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

PWD_CONTEXT = CryptContext(schemes=["argon2"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "1987_KESSEL_SECRET")

def get_password_hash(password: str): return PWD_CONTEXT.hash(password)
def verify_password(plain, hashed): return PWD_CONTEXT.verify(plain, hashed)
def create_token(subject: str):
    return jwt.encode({"exp": datetime.utcnow() + timedelta(hours=24), "sub": str(subject)}, SECRET_KEY, algorithm="HS256")
