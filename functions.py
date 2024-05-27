# generate random number
# function definition,takes no argument
def gen_ramdom():
    import random
    # random is used to generate random numbers and make random selection
    import string
    # it provides a collection of string constants, including digits, letters
    # initiallize the size of 
    N=6
    # N is set to 6, specifies the length of string
    # generate a random string
    res = ''.join(random.choices(string.digits, k=N))
    # ''.join() it concatitnates the random strings to single string
    # print the result
    print("The generated string is: "+str(res))
    return str(res)
# gen_ramdom()

# check phone validity
import re
# its a module that provides support for working with regular expressions.
def check_phone(phone):
    # the function takes one argument phone
    regex = "^\+254\d{9}"
    # ^ it asserts the start of the string
    #\+254 it matches the literal string +254
    #\d{9} it matches a exactly nine digits
    if not re.match(regex,phone)or len(phone) != 13:
        print("Phone is not valid")
        return False
    else:
        print("Phone is Valid, OK")
        return True
    
# check_phone ("+254114373702")
    
# check password validity+
import re
def password_validity(password):
    if len(password) < 8:
        return("Password is too short")
    elif not re.search("[A-Z]",password):
        return("Password must contain atleast an uppercase letter")
    elif not re.search("[a-z]",password):
        return("Password must contain atleast a lowercase letter")
    elif not re.search("[0-9]",password):
        return("Password must contain atleast a digit")
    elif not re.search("[@#$%&]",password):
        return("Password must contain atleast a special character")
    else:
        return True
    
# password_validity(input("Enter your password: "))
    
# sending an sms
import africastalking
africastalking.initialize(
username="joe2022",
api_key="aab3047eb9ccfb3973f928d4ebdead9e60beb936b4d2838f7725c9cc165f0c8a"
#justpaste.it/1nua8
)
sms = africastalking.SMS
def send_sms(phone,message):
    recipients = [phone]
    sender = "AFRICASTALKING"
    try:
        response = sms.send(message,recipients)
        print(response)
    except Exception as error:
        print("Error is :",error)

# send_sms("+254114373701", "This is my message")


# hash password
import bcrypt
# bcrypt is a module for hashing and checking passwords
# it is very secure
def hash_password(password):
    bytes = password.encode("utf-8")
    # password is encoded into bytes 
    # it is necessary because bcrypt library works well with byte data
    # print(bytes)
    salt = bcrypt.gensalt()
    # using a unique salt for each password ensures that even if two users have same passwords, their hashed password will be different
    # print(salt)
    hash = bcrypt.hashpw(bytes,salt)
    # print(hash)
    return hash.decode()

# hash_password(input("Enter your password: "))

# verify password
def hash_verify(password,hash_password):
    bytes = password.encode("utf-8")
    result = bcrypt.checkpw(bytes,hash_password.encode("utf-8"))
    print(result)
    return result

# hash_verify("1234","$2b$12$i40MHuWDL6IMDZGzKcEBUesUmF6quGCkvqAqdKuMiMJ3rok7P53t6")

# encrypt data
from cryptography.fernet import Fernet
# we import fernet class
# the module is used for encryption and decryption
def generate_key():
    # its a function used to generate a new encryption key
    key = Fernet.generate_key()
    # print(key)
    with open("key.key", "wb") as key_file:
    # with open it opens a new file if it exists
    # creates a new file if it doesnt exist
    # wb(write binary) ensures the file is properly closed after writing on it
        key_file.write(key)

# generate_key()
# load key
def load_key():
    return open("key.key", "rb").read()
# it reads the entire content of the file

# load_key()

# encrypt data
def encypt(data):
    key = load_key()
    fernet = Fernet(key)
    # print(fernet)
    # this creates a fernet object for encryption
    encypt_data = fernet.encrypt(data.encode())
    print (encypt_data.decode())
# encypt("1234") 


# decrypt data
def decrypt(encrypted_data):
    key = load_key()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data.encode())
    print(decrypted_data.decode())

decrypt("gAAAAABmUELDvvXXgXB97jGaB26jhrWLAFf7nj_Fnq39BCfaXVYbFZr5SsG9_KwrORzW8g6XIueYiuZ5H2OOCwNwgPvFScDE7w==")