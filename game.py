class Game:
    """
    Stores all data about the current game
    . Game ID
    . Players
    . Player Moves
    . Wins
    . Ties
    . If players have locked moves in
    """

    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def getPlayerMove(self, p):
        """
        :param p: 0 or 1
        :return: Player move
        """
        return self.moves[p]

    def player(self, player, move):
        """
        :param player: 0 or 1
        :param move: R, P or S
        :return: updates the player moves and sets the locked in player to True
        """

        self.moves[player] = move
        if player == 0:
            self.p1Went = True

        else:
            self.p2Went = True

    def connected(self):
        """
        :return: Returns true if both players are connected to the game else false
        """
        return self.ready

    def bothWent(self):
        """
        :return: True if both players have locked in their moves
        """
        return self.p1Went and self.p2Went

    def winner(self):
        """
        :return: 0, 1 - 1 (0: player 1 wins, 1: player 2 wins, -1: tie game)
        """
        p1_move = self.moves[0].upper()[0]
        p2_move = self.moves[1].upper()[0]

        winner = -1

        if p1_move == "R":
            if p2_move == "P":
                winner = 1
            elif p2_move == "S":
                winner = 0
        elif p1_move == "P":
            if p2_move == "S":
                winner = 1
            elif p2_move == "R":
                winner = 0
        elif p1_move == "S":
            if p2_move == "R":
                winner = 1
            elif p2_move == "P":
                winner = 0

        if winner == -1:
            self.ties +=1
        else:
            self.wins[winner] +=1

        return winner

    def resetWent(self):
        """
        :return: reset game after every round
        """
        self.p1Went, self.p2Went = False, False

