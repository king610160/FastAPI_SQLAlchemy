from fastapi import APIRouter, HTTPException
from db.database import session, User
from pydantic import BaseModel

from utils.hashPassword import check_password

class userInfo(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.post('/login')
def login(userInfo: userInfo):
    # find the user with email, if there is not email in database, return 400 with email or password not correct
    user = session.query(User).filter_by(email=userInfo.email).first()
    if user is None:
        raise HTTPException(
                status_code=400,
                detail={'status': 'Fail', 'error-message': 'Email or password is not correct'}
            )
    # check input password is correspond to password in database with hash method
    result = check_password(userInfo.password, user.password)
    # if password not correct, return 400 with email or password not correct
    if result is False:
        raise HTTPException(
                status_code=400,
                detail={'status': 'Fail', 'error-message': 'Email or password is not correct'}
            )
    return {'status': 'Success','user': user}