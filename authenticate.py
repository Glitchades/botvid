from pymessenger.bot import Bot

import os

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFICATION_TOKEN")
ADMIN = os.environ.get("ADMIN")

import mysql.connector
connection = mysql.connector.connect(user= os.environ.get("DB_USER"),
                                     password= os.environ.get("DB_PASS"),
                                     host= os.environ.get("DB_HOST"),
                                     db= os.environ.get("DB"))

def verify_bot_access():
    return Bot(ACCESS_TOKEN)

def verify_fb_token(request):
    token_sent = request.args.get("hub.verify_token")
    if (token_sent == VERIFY_TOKEN):
        return request.args.get("hub.challenge")
    return ("<h1>Access Denied: No Proper Rights!!<h1>")

def is_admin(user_id):
    return user_id == ADMIN