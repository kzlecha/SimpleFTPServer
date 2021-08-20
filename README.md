# SimpleFTPServer
Simple FTP server using socket programming written in Python.
The client can upload files to the server or pull files from the server.

## How To Run
In a terminal run the server.
```shell
cd server
python tcp_server.py
```
Then in a new terminal let the client ping the server.
```shell
cd client
python tcp_client.py
```
From here the client can send requests to the server

### Features

#### Simple Message Response
The server will respond to any message from the client by capitalization.
```
Message: hi :)
Received:  HI :)
```
#### OPEN Port
The OPEN command will change the connection to the specified port number.
Input Command is `OPEN <port number>`

#### QUIT
Will quit out of the client connection. Client socket is closed and cannot connect to anything else, server is only left with welcome socket.
Command: `QUIT`


#### CLOSE
Similar to QUIT - Will close the connection between the client and the server, so the server is listening to receive connections and the client is free to make other connections.
Command: `CLOSE`

#### PUT
Will upload a file from the client directory to the server.
I know you can do this with the FTP library in python but I just used socket.
Command: `PUT <filename>`

#### GET
Will retrieve a file from the server and save it in the client directory
Command: `GET <filename>`

Note that these can be combined to download and upload together.
