import hashlib



def hash_password(password):
   return hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000).hex()



def verify_password(password:str, password_hash) -> bool:
    return hash_password(password) == password_hash

