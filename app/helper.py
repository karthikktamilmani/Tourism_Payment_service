import math as m
import random as r
from app import mailTrigger
from cryptography.fernet import Fernet

# function to generate OTP
def OTPgen():
    # Declare a string variable
    # which stores all alpha-numeric characters
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    varlen = len(string)
    for i in range(6):
        OTP += string[m.floor(r.random() * varlen)]

    return OTP

def sendOTPMail(email):
    otp = OTPgen()
    mailTrigger.sendEmail(email, "OTP for accessing our App", "OTP is : " + otp)
    return otp

def encryptValue(value):
    return cipher_suite.encrypt(value.encode())

def decryptValue(value):
    return cipher_suite.decrypt(value).decode()

# def getItemFromUsers(tableObj,)