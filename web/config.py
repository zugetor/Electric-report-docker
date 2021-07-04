import os

class Config(object):
    DEBUG = (os.getenv("DEBUG", 'False').lower() in ('true', '1', 't')) #Disable Debug
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'db') #MySQL Host
    MYSQL_USER = os.getenv('MYSQL_USER', 'myuser') #MySQL username
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'verysecure') #MySQL password
    MYSQL_DB = os.getenv('MYSQL_DB', 'electric_mon') #MySQL DB name
    MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://root:password@mongo:27017/?authSource=admin') #MongoDB Connection String
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey') #your secret key
    SESSION_COOKIE_HTTPONLY = (os.getenv("SESSION_COOKIE_HTTPONLY", 'True').lower() in ('true', '1', 't')) #Cookie can access from HTTP Only
    REMEMBER_COOKIE_HTTPONLY = (os.getenv("REMEMBER_COOKIE_HTTPONLY", 'True').lower() in ('true', '1', 't')) #Cookie can access from HTTP Only
    ALLOW_REGISTER = (os.getenv("ALLOW_REGISTER", 'True').lower() in ('true', '1', 't')) #Allow user to register
    LOGIN_ONLY = (os.getenv("LOGIN_ONLY", 'True').lower() in ('true', '1', 't')) #Enable Login to all page and API
    TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Bangkok') #Time zone for check room schedule
    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI') #Recaptcha V2 public key from https://www.google.com/recaptcha
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe') #Recaptcha V2 private key from https://www.google.com/recaptcha