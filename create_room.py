#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 15:10:46 2020

@author: A.Akdogan
"""

from pymongo import MongoClient
import json
from db import last_id
import warnings
warnings.filterwarnings("ignore")
import argparse


class CreateRoom():
    
    def __init__(self,room_count):
        with open('key.json', 'r') as fp:
            self.key = json.load(fp)
        self.room_count = room_count

    def get_collection(self):
        client = MongoClient(self.key["mongo_key"])
        chat_db = client.get_database("chat_db")
        rooms_collection = chat_db.get_collection("rooms")
        return rooms_collection

    
    def create_room(self, rooms_collection):
        def all_rooms():
            new_id = last_id(rooms_collection,"room_id")
            room_name = "room_" + str(new_id)
            rooms_collection.insert_one({"room_id" : new_id, "room_name": room_name, "cap": 0 })
            
        for i in range(self.room_count):
            all_rooms()
            
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--room_count", type = int, required = True, 
    	help="room count")
    args = vars(ap.parse_args())
    create_room = CreateRoom(room_count = args["room_count"])
    rooms_collection = create_room.get_collection()
    create_room.create_room(rooms_collection)