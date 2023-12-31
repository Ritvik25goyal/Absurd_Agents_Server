import random


instructions = b"""----------------------------
        Schrodinger's Cat
----------------------------
Here a Schrodinger's cat riddle for you 

it's a pretty simple game just you have to guess the box in which the cat hidden among the 5 boxes if you guess correctly you win if you don't the cat moves to its adjacent box (for ex:- if the cat in box 2 then it either moves to box 1 or box 3 ) so now you have understood the rules lets start the game\n"""

def pick_location(original_location):
    location = original_location.index('X')
    new_location = ['_', '_', '_', '_', '_']
    choice = random.randint(0,1)
    if choice == 0:
        if location == 0:
            new_location[1] = "X"
        else:
            new_location[location-1] = "X"
    else:
        if location == 4:
            new_location[3] = "X"
        else:
            new_location[location+1] = "X"
    return new_location

def play_game(client_socket):
    starting_position = random.randint(0, 4)
    original_location = ['_', '_', '_', '_','_' ]
    original_location[starting_position] = "X"
    victory = False
    client_socket.send(instructions)
    display = b"_ _ _ _ _ \n"

    while not victory:
        client_socket.send(b"Guess the position: ")
        client_socket.send(display)
        location = original_location.index("X")
        client_socket.send(b"Please guess a position: ")
        choice = int(client_socket.recv(10).decode().strip("\n"))
        if choice-1 == location:

            client_socket.send(b"You found the cat \n")
            client_socket.send(b"Cat's position: ")
            client_socket.send((" ".join(original_location) + "\n").encode())
            victory = True
        else:
            client_socket.send(b"Cat was not in this box \n")
            original_location = pick_location(original_location)

def askplayagain(client_socket):
    client_socket.send(b"Play Again? (Y/N):\n>")
    reply = client_socket.recv(2).decode().strip("\n").upper()
    return reply

def main(client_socket):
    
    play_game(client_socket)
    reply = askplayagain(client_socket)
    while reply == "Y":
        play_game(client_socket)
        reply = askplayagain(client_socket)

if __name__ == "__main__":
    main()