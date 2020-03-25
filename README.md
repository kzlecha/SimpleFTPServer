# SimpleFTPServer
Simple FTP server using socket programming written in Python.
The client can upload files to the server or pull files from the server.

## To Run
In a terminal run the server.
```
python server/tcp_server.py
```
Then in a new terminal let the client ping the server.
```
python client/tcp_client.py
```
## File Structure
### Client
Contains the client socket and any local files to the client
### Server
Contains the server socket and any files on the server
