import bcrypt

def hash_password(password: str) -> str:
    # use encode to change password to byte, after hash with salt, decode with utf-8 and get hashPassword
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt(10))
    return hashed_password.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    # use encode to change password, hashpassword to byte, check and return test result
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes) 