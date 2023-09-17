import socket

#host2_ip = '10.0.0.2'  # Replace with the actual IP of Host 2 (Mininet)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect(('10.0.0.2', 12345))
    message = "banned1"
    message2= "UNION SELECT username, password FROM users--"
    message3="SELECT * from table where id = 123"
    message4="SELECT * FROM Users WHERE UserId = 105 OR 1=1;"
    message5="admin"
    message6='emir2001'
    client_socket.send(message.encode())
    
