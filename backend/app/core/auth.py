from jose import jwt, JWTError
from backend.app.core.auth_config import SUPABASE_JWT_SECRET

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except JWTError:
        raise ValueError("Invalid or expired token")