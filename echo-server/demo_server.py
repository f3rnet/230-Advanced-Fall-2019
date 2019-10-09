import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

address = ('127.0.0.1', 20000)

server_socket.bind(address)
server_socket.listen(1)

connection, client_address = server_socket.accept()

buffer_size = 4096

connections = []

while True:
    try:
        connection, client_address = server_socket.accept()
        connections.append(connection)
    except BlockingIOError:
        pass

    received_messages = []
    for connection in connections:
        try:
            received_message = connection.recv(4096)
        except BlockingIOError:
            received_message = None

        if received_message:
            print("Client says: {}".format(received_message.decode()))
            received_message.append(received_message)

        for connection in connections:
            for received_message in received_message:
                connection.sendall(received_message)
                
time.sleep(1)

