###Data format design

#Plugin
keep a record of a hash of blocks data to see if the chunk data has hanged
on update check how many blocks have changed i > then threshold send to server


Spark processing

For each data

-------------------------------------------------------------------------------------

##Database design
Mongo

Collections:
    ServerID_Events: Will contain all documents relating to events such as player move, block place etc,
    ServerID_Meta
    ServerID_Worlds
    ServerID_Chunks



Server Meta -> update

Server Worlds -> Update

NC                  DC

From NC check with oldC