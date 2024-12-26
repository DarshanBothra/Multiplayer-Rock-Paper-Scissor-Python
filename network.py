import socket
import pickle

class Network:

    """
    Establishes a network to connect to the server, send message, get message
    """

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "<LOCALHOST SERVER IP HERE>"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        """
        :return: 0 or 1 (which player move is recorded)
        """
        return self.p

    def connect(self):
        """
        :return: establishes a connection with the server
        """
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()

        except socket.error as e:
            print(e)

    def send(self, data):
        """
        :param data: get, reset or move (R, P, S)
        :return: game object after updating game-data
        """
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print(e)


