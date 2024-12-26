# imports

import socket
from _thread import *
import pickle
from game import Game


def threadClient(conn, p, gameId):
    """
    :param conn: connection
    :param p: player (0 or 1) to start a thread respectively
    :param gameId: gameId to start the thread for
    :return:
    """
    global id_count # to keep track of the number of people, games and stuff
    conn.send(str.encode(str(p))) # Send which player is interacting/ has been created

    while True:
        try:
            # Constantly try and receive server data to get player moves and commands
            data = conn.recv(4096).decode()

            # If the game exists
            if game_id in games:
                game = games[game_id]

                # If no message is received
                if not data:
                    break

                else:
                    # If the message is reset, reset the game
                    if data == "reset":
                        game.resetWent()
                    # If the message is get, get the player move/ interaction
                    elif data != "get":
                        game.player(p, data)

                    # Send Game object after updating it
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    # If no message is received disconnect from the server
    print("Lost Connection")

    try:
        # If one of the player exits, close the game and remove the game from game list
        del games[game_id]
        print(f"Closing Game: {game_id}")
    except:
        pass

    id_count -= 1
    conn.close()

# Creating a server side socket with TCP Data Comm.

SERVER = "localhost"
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER, PORT))
except socket.error as e:
    print(e)

s.listen()
print("Server Started!\nWaiting for connection...")

connected = set()
games = {}
id_count = 0

while True:
    # Actively listen for incoming connections, accept
    conn, addr = s.accept()
    print(f"Connected to: {addr}")

    id_count += 1
    p = 0
    game_id = (id_count-1)//2

    if id_count%2 == 1:
        # Create a New Game
        games[game_id] = Game(game_id)
        print("Creating a new game...")
    else:
        # Add player to an already existing game
        games[game_id].ready = True
        p = 1

    # start a new thread for every client connected
    start_new_thread(threadClient, (conn, p, game_id))
