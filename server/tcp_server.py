from socket import AF_INET, SOCK_STREAM, socket

def get(conn, filename):
    '''
    Read the file with @param: filename from the client and save it in the
    server directory
    '''
    try:
        # send the data in the file
        with open(filename, 'r') as infile:
            for line in infile:
                conn.sendall(line.encode('utf-8'))    
        # send signal to stop reading
        end_message = "EOF-STOP"
        conn.sendall(end_message.encode('utf-8'))
    except Exception as e:
        print(e)
        error_message = ("There has been an error sending the requested file. "
                         + filename + " might not exist")
        conn.sendall(error_message.encode('utf-8'))


def put(conn, data):
    '''
    Send the file with @param: filename from the server directory to client
    '''
    filename = data.split(' ')[1]
    print("Recieved File: "+filename)

    try:
        # get data and write to file until recieve end signal
        data = conn.recv(1024).decode("utf-8")
        with open(filename, 'w') as outfile:
            while(data):
                outfile.write(data)
                data = conn.recv(1024).decode("utf-8")
                # if the data contains the end signal, stop
                if "EOF-STOP" in data:
                    stop_point = data.find("EOF-STOP")
                    outfile.write(data[:stop_point])
                    return data[stop_point+8:]
    except Exception as e:
        print(e)
        error_message = "There has been an error recieving the requested file."
        conn.sendall(error_message.encode('utf-8'))
        return ""


command_list = ["QUIT","CLOSE", "OPEN", "GET","PUT"]

HOST = '127.0.0.1'
PORT = 12000

# set up the tcp socket
sock = socket(AF_INET, SOCK_STREAM)
sock.bind((HOST, PORT))

# continuously listen for a connection in TCP welcome socket
while True:
    sock.listen()

    # accept request and create new socket for connection
    # This is where multithreading would occur if I wasn't too busy
    conn, addr = sock.accept()
    print("Connected to " , addr)

    remainder = ""
    while (True):
        command = ""
        if remainder == "":
            # if there's no leftover message, recieve a new one
            data = conn.recv(1024).decode("utf-8")
            command = data.split(' ')[0].upper()
        else:
            # if there is a leftover message then execute it
            data = remainder
            space = remainder.find(' ')
            command = remainder[:space].upper()
            remainder = ""

        if command in command_list:
            if command == "QUIT":
                # close the connection
                print("Client quitting")
                conn.sendall(command.encode("utf-8"))
                conn.close()
                # server stays alive because it makes no sense for the client
                # to be able to kill it
                break
            
            if command == "CLOSE":
                # close the connection
                print("Client disconnecting")
                conn.sendall(command.encode("utf-8"))
                conn.close()
                break

            if command == "OPEN":
                port = int(data.split(' ')[1])
                
                # achknowledge request
                message = "Binding to Port " + str(port)
                conn.sendall(message.encode('utf-8'))

                # create new socket to replace the old one
                sock2 = socket(AF_INET, SOCK_STREAM)
                sock2.bind((HOST, port))
                sock2.listen(1)
                conn2, addr2 = sock2.accept()
                print("Connected to " , addr2)

                # replace the old socket
                sock = sock2
                conn = conn2
                continue

            if command == "GET":
                filename = data.split(' ')[1]
                get(conn, filename)

            if command == "PUT":
                remainder = put(conn, data)

        else:
            # if its not a command just capitalize and return
            print(data)
            conn.sendall(data.upper().encode("utf-8"))

    # If loop exitted, have disconnected
    print("Disconnected from:", addr)

# close the server   
sock.close()