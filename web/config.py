import os

class Config(object):
    DEBUG = False #Disable Debug
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'db') #MySQL Host
    MYSQL_USER = os.getenv('MYSQL_USER', 'myuser') #MySQL username
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'verysecure') #MySQL password
    MYSQL_DB = os.getenv('MYSQL_DB', 'electric_mon') #MySQL DB name
    MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://root:password@mongo:27017/?authSource=admin') #MongoDB Connection String
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey') #your secret key
    SESSION_COOKIE_HTTPONLY = True #Cookie can access from HTTP Only
    REMEMBER_COOKIE_HTTPONLY = True #Cookie can access from HTTP Only
    ALLOW_REGISTER = True #Allow user to register
    LOGIN_ONLY = True #Enable Login to all page and API
    TIME_ZONE = "Asia/Bangkok" #Time zone for check room schedule
    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI') #Recaptcha V2 public key from https://www.google.com/recaptcha
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', 'vFI1TnRWxMZNFuojJ4WifJWe') #Recaptcha V2 private key from https://www.google.com/recaptcha