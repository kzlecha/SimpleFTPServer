from socket import AF_INET, SOCK_STREAM, socket

def get(sock, filename):
    '''
    Send the file with @param: filename from the client directory to server
    '''
    print("Recieved File: "+filename)
    try:
        # get data and write to file until recieve end signal
        data = sock.recv(1024).decode("utf-8")
        with open(filename, 'w') as outfile:
            while(data):
                outfile.write(data)
                data = sock.recv(1024).decode("utf-8")
                # if the data contains the end signal, stop
                if "EOF-STOP" in data:
                    stop_point = data.find("EOF-STOP")
                    outfile.write(data[:stop_point])
                    return data[stop_point+8:]
    except Exception as e:
        print(e)
        error_message = "There has been an error recieving the requested file."
        sock.sendall(error_message.encode('utf-8'))


def put(sock, filename):
    '''
    Read the file with @param: filename from the server and save it in the client directory
    '''
    try:
        # ensure space to separate filename
        sock.send(" ".encode('utf-8'),1024)
        # send the data in the file
        with open(filename, 'r') as infile:
            for line in infile:
                sock.sendall(line.encode('utf-8'))
        # send signal to stop reading
        end_message = "EOF-STOP"
        sock.sendall(end_message.encode('utf-8'))
    except Exception as e:
        print(e)
        error_message = "There has been an error sending the requested file. " + filename + " might not exist"
        sock.sendall(error_message.encode('utf-8'))


command_list = ["QUIT","CLOSE", "OPEN", "GET","PUT"]

HOST = '127.0.0.1'
PORT = 12000

# set up the tcp socket
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((HOST, PORT))

while (True):
    # read command from user and send to server
    s = input("Message: ")
    sock.sendall(s.encode("utf-8"))
    command = s.split(' ')[0].upper()

    if command in command_list:
        if command == "QUIT":
            # end the client connection.
            print("Goodbye :)")
            break

        if command == "CLOSE":
            # close the connection to the server but don't quit yet
            print("Server is disconnecting. Please connect to a different server")
            continue

        if command == "OPEN":
            # ensure request has been recieved
            data = sock.recv(1024).decode('utf-8')
            print(data)

            # create a new socket open on the port number and connect to server
            port = int(s.split(' ')[1])
            sock2 = socket(AF_INET, SOCK_STREAM)
            sock2.connect((HOST, port))

            # replace the old socket
            sock = sock2
            continue

        if command == "GET":
            filename = s.split(' ')[1]
            remainder = get(sock, filename)

        if command == "PUT":
            filename = s.split(' ')[1]
            put(sock, filename)

    else:
        # if its not a command just print the capitalized respose from the server
        data = sock.recv(1024).decode("utf-8")
        print ("Received: ", data)

sock.close()