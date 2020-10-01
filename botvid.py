from flask import Flask, request, render_template
from pymessenger.bot import Bot
import authenticate, user_database, state_database

app = Flask(__name__)
bot = authenticate.verify_bot_access()


def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "Message Sent!"

def get_message():
    response = state_database.get_tabulated_data()
    return response


def get_sudo_message(message):
    if message == "sudo gtu":
        response = user_database.get_total_users()
    elif message == "sudo gu":
        response = user_database.get_users()
    elif message == "sudo status":
        response = "Hey! botvid is working great! :)"
    else:
        response = "unrecognized admin command"
    return response

def get_swear_response():
    response = ["Science says swearing is good for you. Well, fuck science!",
                "When angry, count to four. When very angry, swear :D",
                "'Swearing is industry language. For as long as we're alive, it's not going to change.' - Ramsay",
                "Sorry! I forgot to add that you're stupid as well!!",
                "01010111 01100101 01101100 01101100 00101100 00100000 01100110 01110101 01100011 01101011 00100000 01111001 01101111 01110101 00100001"]

    import random
    return random.choice(response)
                


@app.route("/webhook", methods = ["GET", "POST"])
def receive_message():
    if request.method == "GET":
        return authenticate.verify_fb_token(request)
    else:
        output = request.get_json()
        message = "DEFAULT MESSAGE"
        try:
            message = output["entry"][0]["messaging"][0]["message"]["text"].lower()
        except:
            pass
        user_id = int(output["entry"][0]["messaging"][0]["sender"]["id"])
        print("The user id is: ", user_id)
        if message == "DEFAULT MESSAGE":
            send_message(user_id, "Sorry! I cannot currently handle non-text messages")
            send_message(user_id, "Send 'subscribe' to subscribe for periodic notifications, 'update' to get updates about COVID-19, and 'unsubscribe' to unsubscribe from periodic notifications")
        elif message in ["hi", "hello", "hey", "hola", "namaste"]:
            send_message(user_id, message.capitalize() + " there!")
        elif message == "subscribe": 
            subscribe(user_id)
        elif message == "unsubscribe":
            unsubscribe(user_id)
        elif message == "update":
            response = get_message()
            send_message(user_id, response)
            send_message(user_id, "Above data was scraped from https://www.worldometers.info/coronavirus/country/us/")
        elif message.split()[0] == "sudo" and authenticate.is_admin(user_id):
            response = get_sudo_message(message)
            send_message(user_id, response)
        elif "fuck" in message.split():
            response = get_swear_response()
            send_message(user_id, response)
        else:
            send_message(user_id, "Sorry! I am a dumb bot, and I didn't quite understand what you just said.")
            send_message(user_id, "Send 'subscribe' to subscribe for periodic notifications, 'update' to get updates about COVID-19, and 'unsubscribe' to unsubscribe from periodic notifications")
            
        return "Message Processed"

def is_user_subscribed(user_id):
    return user_database.is_user_subscribed(user_id)

def subscribe(user_id):
    if not (is_user_subscribed(user_id)):
        user_database.add_user(user_id)
        send_message(user_id, "Success! I will now send you periodic messages :)")
        print("User added to the database!") 
        print("Total users in database: " , user_database.get_total_users())
    else:
        send_message(user_id, "You are already a subscriber!")
        print("User already in the database!")
        print("Total users in database: " , user_database.get_total_users())

        
def unsubscribe(user_id):
    if (not is_user_subscribed(user_id)):
        send_message(user_id, "Sorry! You are not a subscriber")
        send_message(user_id, "send me 'subscribe' to subscribe for notifications from me")
    else:
        user_database.remove_user(user_id)
        send_message(user_id, "I won't send you updates anymore")
        send_message(user_id, "Sorry to see you go :(")

        print("User removed from the database!")
        print("Total users in database: " , user_database.get_total_users())
        
        
        
@app.route("/privacy-policy")
def privacy():
    return render_template("privacy_policy.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    app.run(threaded=True)