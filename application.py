import os

from flask import Flask, render_template, session, request, flash, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from forms import RegistrationForm, LoginForm, ChatForm
#from flask_session import Session

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)



#temporary array for users in channel
users = []
users_1 = []
users_2 = []
channels = []

@app.route("/", methods=["GET", "POST"])
def index():
    
    #clear client side cookies and ask for chat name
    session.clear()
    form = ChatForm()
    

    #after entering chat name
    if (request.method == "POST"):
        newUser = request.form.get("username")
        users.append(newUser)
        #assign user a session cookie
        print(users)
        session["user_id"] = newUser
    
    return render_template("index.html", form = form)

@socketio.on("createChannel")
def createChannel(data):
    channelName = data["channelName"]
    #join_room(channelName)
    print("created channel")
    
    emit("new channel", {"newChannel": channelName}, broadcast = True)
    print("backend ok")
    
@socketio.on("submit message")
def messageHandler(data):
    print("message submition")
    print(data["channel"])
    message = data["message"]
    print(message)
    channel = data["channel"]
    if (channel == "all"):
        emit("announce message", {"message": message, "username": session["user_id"]}, broadcast = True)
        print("broadcasting")
    else:
        emit("announce message", {"message": message, "username": session["user_id"]}, room=channel)
        #print("going to room1")

@socketio.on("join")
def roomJoiner(data):
    room = data["room"]
    username = session["user_id"]
    join_room(room)
    #users_1.append(username)
    #print(users_1)
    emit("status", {"msg": username + ' has entered the room.'}, room=room)
    

if __name__ =="__main__":
    socketio.run(app)
