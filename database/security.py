import jwt
from datetime import datetime, timedelta

SECRET_KEY = "AnalSex_With_niggasAndFellas/2332.-minf9emf0e,mfjt8mujtf-utu-8kt-uvjktvu-kj"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.isoformat()})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(payload=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return 'Error'
