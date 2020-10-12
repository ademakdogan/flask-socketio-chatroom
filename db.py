#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 18:34:12 2020

@author: A.Akdogan
"""

from pymongo import MongoClient
import pymongo
from werkzeug.security import generate_password_hash
from datetime import datetime
from bson.objectid import ObjectId
import random
import json

with open('key.json', 'r') as fp:
    key = json.load(fp)


client = MongoClient(key["mongo_key"])


    


chat_db = client.get_database("chat_db")
#user_collection = chat_db.get_collection("chat")
users_collection = chat_db.get_collection("users")
rooms_collection = chat_db.get_collection("rooms")
room_members_collection = chat_db.get_collection("room_members")


def last_id(col, name_id):
    try:
        
        new_id = col.find().sort(name_id, -1)[0][name_id] + 1
        return new_id
    except:
        new_id = 1
        return new_id
    
def save_user(username, gender):
    new_id = last_id(users_collection, "user_id")
    users_collection.insert_one({ "user_id": new_id,"username" : username, "gender" : gender })

#save_user("user2", "male")
#last_doc = users_collection.find_one({'_id': 1},sort=[( '_id', pymongo.DESCENDING )])

def all_rooms():
    new_id = last_id(rooms_collection,"room_id")
    room_name = "room_" + str(new_id)
    rooms_collection.insert_one({"room_id" : new_id, "room_name": room_name, "cap": 0 })

# =============================================================================
# for i in range(14):
#     
#     all_rooms()
# =============================================================================


def get_room_name():
    rooms = []
    avaliable_rooms1 = rooms_collection.find({"cap": 1}).sort("room_id", -1)
    if avaliable_rooms1.count() == 0:
        avaliable_rooms0 = rooms_collection.find({"cap": 0}).sort("room_id", -1)
        if avaliable_rooms0.count() == 0:
            return "Full"
        else:
            for room in avaliable_rooms0:
                rooms.append(room)
            random_index = random.randint(0,len(rooms)-1)
            random_room_name = rooms[random_index]["room_name"]
            return random_room_name
    else:
        for room in avaliable_rooms1:
            rooms.append(room)
        random_index = random.randint(0,len(rooms)-1)
        random_room_name = rooms[random_index]["room_name"]
        return random_room_name


def increase(room_name):
    object_1 = rooms_collection.find({"room_name": room_name}).sort("room_id", -1)[0]
    cap = object_1["cap"]
    new_value = { "$set": { "cap": cap + 1 } }
    rooms_collection.update({"room_name": room_name}, new_value)
    
def decrease(room_name):
    object_1 = rooms_collection.find({"room_name": room_name}).sort("room_id", -1)[0]
    cap = object_1["cap"]
    new_value = { "$set": { "cap": cap - 1 } }
    rooms_collection.update({"room_name": room_name}, new_value)
    

def members_room_start(room_name, username, gender):
    if rooms_collection.find({"room_name": room_name})[0]["cap"] == 1:
       room_members_collection.insert_one({"room_name" : room_name, "username_1": username, "gender_1": gender,
                                           "username_2": "", "gender_2" : "","start_date": "", "end_date": ""})
      
    else:
        #object_1 = room_members_collection.find({"room_name": room_name, "username_2" : ""}).sort("room_id", -1)[0]
        start_date = datetime.now()
        new_value = { "$set": { "username_2": username, "gender_2": gender, "start_date": start_date} }
        room_members_collection.update({"room_name": room_name, "username_2" : ""}, new_value)
        
def members_room_end(room_name, username):
    if rooms_collection.find({"room_name": room_name})[0]["cap"] == 0:
        if room_members_collection.find({"room_name": room_name, "username_1" : username, 
                                      "username_2" : ""}).count() > 0:
            trash = room_members_collection.find({"room_name": room_name, "username_1" : username, 
                                      "username_2" : ""})[0]
            room_members_collection.delete_one(trash)
        else:
            pass
        
    else:
        end_date = datetime.now()
        new_value = { "$set": { "end_date" : end_date} }
        room_members_collection.update({"room_name": room_name, "end_date" : ""}, new_value)
        get_user = room_members_collection.find({"room_name": room_name, "end_date" : end_date})[0] #***
        if get_user["username_1"] == username:
            room_members_collection.insert_one({"room_name" : room_name, "username_1": get_user["username_2"],
                                                "gender_1": get_user["gender_2"],
                                                "username_2": "", "gender_2" : "","start_date": "", "end_date": ""})
        else:
            room_members_collection.insert_one({"room_name" : room_name, "username_1": get_user["username_1"],
                                                "gender_1": get_user["gender_1"],
                                                "username_2": "", "gender_2" : "","start_date": "", "end_date": ""})
        
        
#aa = rooms_collection.find({"room_name": "room_2"})[0]
        #rooms_collection.delete_one(aa)
        
#deneme = rooms_collection.find()[0]     
def reset_db():
    rooms = rooms_collection.find()
    new_value = { "$set": { "cap" : 0} }
    for room in rooms:
        rooms_collection.update(room,new_value)
        

#rooms_collection.find({"room_name": "room_2"}).sort("room_id", -1)[0]
