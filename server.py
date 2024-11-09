# Manages the queue of users, pairs them, and handles the game logic.

import socket
import threading
from collections import deque

# Handle client communication
def handle_client(client_socket, player_name):
    client_socket.send("Welcome to the game Mad Matchups!\n".encode())
    client_socket.send(f"{player_name}, you are in the queue.\n".encode())
    
    queue.append(client_socket)
    # Wait for pairing
    if len(queue) >= 2:
        # Pair the first two clients in the queue
        player1_socket = queue.popleft()
        player2_socket = queue.popleft()
        player1_socket.send("You are paired with another player. Please choose 'rock', 'paper', or 'scissors':\n".encode())
        player2_socket.send("You are paired with another player. Please choose 'rock', 'paper', or 'scissors':\n".encode())

        player1_choice = player1_socket.recv(1024).decode().strip()
        player2_choice = player2_socket.recv(1024).decode().strip()

        # Validate choices
        if player1_choice not in ['rock', 'paper', 'scissors'] or player2_choice not in ['rock', 'paper', 'scissors']:
            player1_socket.send("Invalid input. Please choose from 'rock', 'paper', or 'scissors'.\n".encode())
            player2_socket.send("Invalid input. Please choose from 'rock', 'paper', or 'scissors'.\n".encode())
            return
        
        # Determine the winner
        result = determine_winner(player1_choice, player2_choice)
        player1_socket.send(f"Your choice: {player1_choice}\n".encode())
        player2_socket.send(f"Your choice: {player2_choice}\n".encode())
        player1_socket.send(result.encode())
        player2_socket.send(result.encode())

    client_socket.close()

# Server setup
host = '127.0.0.1'
port = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

print("Server started, waiting for clients...")

queue = deque()

# Accept clients
while True:
    client_socket, addr = server_socket.accept()
    print(f"New connection from {addr}")
    
    client_socket.send("Enter your name: ".encode())
    player_name = client_socket.recv(1024).decode().strip()
    
    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, player_name))
    client_thread.start()