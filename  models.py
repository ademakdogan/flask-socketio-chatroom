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

client = MongoClient("mongodb+srv://admin:admin@cluster0-azjtd.mongodb.net/test?retryWrites=true&w=majority")

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

save_user("user2", "male")
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
    
def rooms_member(room_id, user_id, start_date, end_date):
    new_id = last_id(room_members_collection, "member_id")
    
    
    
#----------
# =============================================================================
# import json
# import random
# roo
# newvalues = { "$set": { "cap": 1 } }
# rooms_collection.update({"room_id": 5}, newvalues)
# 
# aa = rooms_collection.find({"cap": 0}).sort("room_id", -1)
# deneme = []
# for a in aa:
#     deneme.append(a)
#     print(a)
# deneme[3]["room_id"]
# 
# random.randint(0,1)
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
    
    


