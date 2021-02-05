import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

TOKEN_ID = os.getenv('TOKEN_ID')
CREDENTIAL_PATH = os.getenv('CREDENTIAL_PATH')
cred = credentials.Certificate(CREDENTIAL_PATH)

firebase = firebase_admin.initialize_app(cred)
db = firestore.client()

extensions = ['bot.command.EventHandler', 'bot.command.AdminController', 'bot.command.RoleCommand']

server_emoji = dict()
server_msg = dict()