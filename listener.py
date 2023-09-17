import socket

host2_ip = ''  # Replace with the actual IP of Host 2
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host2_ip, port))
    server_socket.listen()

    print("Waiting for a connection from Host 1...")
    connection, address = server_socket.accept()

    with connection:
        print("Connected by:", address)
        message = connection.recv(1024).decode()
        print("Message received from Host 1:", message)
        # Forward the message to Inspector (Host 3)
        inspector_ip = '10.0.0.3'  # Replace with the actual IP of Inspector (Host 3)
        inspector_port = 54321  # Choose a port number for communication with Inspector
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as inspector_socket:
            inspector_socket.connect((inspector_ip, inspector_port))
            inspector_socket.send(message.encode())
            connection.close()