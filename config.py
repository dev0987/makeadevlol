import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
    TEST_TWILIO_ACCOUNT_SID = os.environ.get('TEST_TWILIO_ACCOUNT_SID')
    TEST_TWILIO_AUTHTOKEN = os.environ.get('TEST_TWILIO_AUTHTOKEN')
    MAGIC_NUMBER = os.environ.get('MAGIC_NUMBER')
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTHTOKEN = os.environ.get('TWILIO_AUTHTOKEN')
    NUMBER = os.environ.get('NUMBER')
