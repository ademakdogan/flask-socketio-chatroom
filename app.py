#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 01:13:18 2020

@author: A.Akdogan
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room
from db import get_room_name, increase, decrease, members_room_start, members_room_end, reset_db

#reset_db()

app = Flask(__name__)
socketio = SocketIO(app)
deneme = []


@app.route("/", methods = ["GET"])
def home():
    return render_template("index.html")

@app.route("/chat")
def chat():
    username = request.args.get("username")
    #room = request.args.get("room")
    gender = request.args.get("gender") #***
    room = get_room_name()
    if username and gender:
        return render_template("chat.html", username = username, room = room, gender = gender)
    else:
        return redirect(url_for("home"))

@socketio.on("join_room")
def hande_join_room_event(data):
    app.logger.info(("{} has joined room {}").format(data["username"], data["room"]))
    print("{} has joined room {}".format(data["username"], data["room"]))
    join_room(data["room"])
    socketio.emit("join_room_ann", data, room = data["room"])
    increase(data["room"])
    members_room_start(data["room"], data["username"], data["gender"])

@socketio.on("send_message")
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {} ,gender : {}".format(data["username"],
                                                                                 data["room"],
                                                                                 data["message"],
                                                                                 data["gender"]))
    socketio.emit("receive_message", data, room = data["room"])

# =============================================================================
# @socketio.on("sample_disconnect")
# def disconnect(data):
#      app.logger.info(" {} client disconnected".format(data["username"]))
#      socketio.emit("sample_disconnect", data)
# =============================================================================
    
@socketio.on('client_disconnecting')
def disconnect_details(data):
    print("{data['username']} user disconnected.")
    app.logger.info( "{} user disconnected.".format(data["username"]))
    socketio.emit("left_room_ann", data, room = data["room"]) #***
    decrease(data["room"])
    members_room_end(data["room"], data["username"])


if __name__ == "__main__":
    socketio.run(app, debug = True, port = 5001)