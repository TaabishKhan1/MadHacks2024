# Allows a user to connect to the server, send their word choice, and receive the result.

import socket

# Connect to the server
host = '127.0.0.1'
port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Receive welcome message
message = client_socket.recv(1024).decode()
print(message)

# Receive the prompt for the player name
name_prompt = client_socket.recv(1024).decode()
print(name_prompt)

# Send the player's name
player_name = input("Enter your name: ")
client_socket.send(player_name.encode())

# Receive the queue message
queue_message = client_socket.recv(1024).decode()
print(queue_message)

# Receive the prompt for the game choice
game_prompt = client_socket.recv(1024).decode()
print(game_prompt)

# Send the player's choice
player_choice = input("Choose 'rock', 'paper', or 'scissors': ").lower()
client_socket.send(player_choice.encode())

# Receive the result
result = client_socket.recv(1024).decode()
print(result)

client_socket.close()
