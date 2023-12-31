import socket
import threading
import wordle
import hangman
import schrodinger
import evilwordle
import dordle


# Server setup
SERVER_HOST = '0.0.0.0'  # Listen on all available network interfaces
SERVER_PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)  # Listen for up to 5 incoming connections
print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

Instruction = b"Welcome to the server.\nFor playing Wordle press W \nFor playing Hangman press H \nFor playing Evil Wordle press E \nFor playing Dordle press D \nFor playing Schrodinger's Cat press S \nFor exit press Q \n>"


# Handle client 
def handle_client(client_socket, client_address):
    while True:
        client_socket.send(Instruction)
        # Receive data from the client
        data = client_socket.recv(2).decode().strip("\n")
        if data.lower() == "q":
            client_socket.send(b"You have successfully exited.\n")
            break

        # Process player input and send responses
        process_game_input(data,client_socket) 
    client_socket.close()


def process_game_input(input_data,client_socket):
    if input_data.lower() == "w":
        wordle.main(client_socket)
    if input_data.lower() == "h":
        hangman.main(client_socket)
    if input_data.lower() == "s":
        schrodinger.main(client_socket)
    if input_data.lower() == "e":
        evilwordle.main(client_socket)
    if input_data.lower() == "d":
        dordle.main(client_socket)
        


while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()




