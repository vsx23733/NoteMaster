from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# user database
users_db = {
    "Axel": {
        "username": "Axel",
        "email": "axel@example.com",
        "hashed_password": "$2b$12$d3bKqqAwZ96pz9GMfZwuv.013wQZNQ8QKAE6HO92fgDY3we8zngI2"
    }
}
