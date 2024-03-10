from fastapi import APIRouter, HTTPException
from db.database import session, User
from typing import Optional 
from pydantic import BaseModel
from utils.hashPassword import hash_password

# set userInfo for the model with Optional modules
class userInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

# router need to start with users
router = APIRouter(prefix='/users')

@router.put('/{id}/edit')
def edit_a_user(id: int, userInfo: userInfo):     
    # check if can get user, if cannot, return 404 with no this user
    getUser = session.get(User, id)
    if getUser is None:
        raise HTTPException(
                status_code=404,
                detail={'status': 'Fail', 'error-message': 'Cannot found the user'}
            )
    # if related field are all blank or empty, then not overwrite userinfo
    if userInfo.name:
        userInfo.name = userInfo.name.strip()
    if userInfo.email:
        userInfo.email = userInfo.email.strip()
    if userInfo.password:
        userInfo.password = userInfo.password.strip()

    if userInfo.name:
        getUser.name = userInfo.name

    if userInfo.email:
        # check whether the email existed, if existed then refuse the change with bad request error
        result = session.query(User).filter_by(email=userInfo.email).first()
        if result is not None:
            raise HTTPException(
                    status_code=400,
                    detail={'status': 'Fail', 'error-message': 'Email has existed'}
                )
        getUser.email = userInfo.email

    if userInfo.password:
        getUser.password = hash_password(userInfo.password)

    session.add(getUser)
    session.commit()
    # query again to check the data is write in database
    editUser = session.get(User, id)
    return {'status': 'Success', 'user': editUser}

@router.delete('/{id}/delete')
def delete_a_user(id: int):
    # if can's find the user, then return 404 with no this user
    user = session.get(User, id)
    if not user:
        raise HTTPException(
                status_code=404,
                detail={'status': 'Fail', 'error-message': 'Cannot found the user'}
            )
    session.delete(user)
    session.commit()
    return {'status': 'Success',}

@router.post('/create')
def create_a_user(userInfo: userInfo):
    # if fill the blank, need to get rid of it
    userInfo.name = userInfo.name.strip()
    userInfo.email = userInfo.email.strip()
    userInfo.password = userInfo.password.strip()
    # check the field are all fill the string, if not, return 400 bad request for not fill all fields
    if not userInfo.name or not userInfo.email or not userInfo.password:
        raise HTTPException(
                status_code=400,
                detail={'status': 'Fail', 'error-message': 'Please fill all the fields and not fill with blank.'}
            )
    # email need to be unique, so check database has this email or not, if has, return 400 with email existed
    result = session.query(User).filter_by(email=userInfo.email).first()
    print(result)
    if result is not None:
        raise HTTPException(
                status_code=400,
                detail={'status': 'Fail', 'error-message': 'Email has existed'}
            )
    # set the password to hashpassword for security
    new_user = User(
                    name = userInfo.name, 
                    email = userInfo.email, 
                    password =  hash_password(userInfo.password)
                )
    session.add(new_user)
    session.commit()
    newUser = session.get(User, new_user.id)
    return {'status': 'Success', 'user': newUser}

@router.get('/{id}')
def get_a_user(id: int):
    # if cannot find the user, the return 404 with no this user
    user = session.get(User, id)
    if user is None:
        raise HTTPException(
                status_code=404,
                detail={'status': 'Fail', 'error-message': 'Cannot found the user'}
            )
    return {'status': 'Success', 'user': user}

@router.get('')
def get_all_users():
    users = session.query(User).all()
    return {'status': 'Success', 'users': users}