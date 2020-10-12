# ChatRoom - Socketio


The chatroom application was made with flask-socketio in this work. There is no need for any registration process to chat. The rooms are designed for only two people. The information of the rooms and the information of the users connected to the rooms (username, gender, start date, end date) are stored in mongodb.


### How to Work

* __Mongo Connection__:  First of all, the key must be obtained for remote connection to mongo. I used MongoDB-Atlas in this work. This key should be saved in the key.json file ("mongo_key": key).

* __Create Room__:  It is necessary to determine how many rooms will be in app. For example, if you want to use only 15 rooms in your application, you should run  `"python create_room.py -r 15"` from command line.

And run to start the app;

```
  python app.py
```  

_Note: The default port is 5001_



