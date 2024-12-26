# imports

import pygame
from network import Network

pygame.font.init()

# classes

class Button:
    """
    class to create a button in the pygame window
    """
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        """
        :param win: main pygame top level window where the button has to be placed
        :return: creates a button at the desired place
        """
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Halvetica", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        """
        :param pos: mouse-pointer position
        :return: True if the mouse-pointer lies within any button, False otherwise
        """
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


# functions

def redrawWindow(win, game, p):
    """
    :param win: main pygame top level window
    :param game: game object
    :param p: player
    :return:
    """

    win.fill((128, 128, 128)) # Colors the window grey

    if not game.connected():
        """
        If two player have not connected, then displays a waiting text.
        """

        font = pygame.font.SysFont("Halvetica", 80)
        text = font.render("Waiting for player...", 1, (255, 0, 0))
        win.blit(text, (width/2  - text.get_width()/2, height/2 - text.get_height()/2))

    else:
        """
        If both the players have connected to the game, text is rendered accordingly
        """

        # Text to display your move
        font = pygame.font.SysFont("Halvetica", 60)
        text = font.render("You", 1, (0, 255, 255))
        win.blit(text, (125, 200))

        # Text to display Opponent's move
        text = font.render("Opponent", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        # Get both players' move
        move1 = game.getPlayerMove(0)
        move2 = game.getPlayerMove(1)

        # If both the players have locked their moves in display both of 'em each other's moves
        if game.bothWent():

            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))

        else:
            # If player 1 has locked in
            if game.p1Went:
                if p == 0:
                    # Display the move to player 1
                    text1 = font.render(move1, 1, (0, 0, 0))
                else:
                    # Locked in status displayed to player 2
                    text1 = font.render("Locked In", 1, (0, 0, 0))

            # If player 1 has not locked in display waiting for move
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            # If player 2 has locked in
            if game.p2Went:
                if p == 1:
                    # Display the move to player 2
                    text2 = font.render(move2, 1, (0, 0, 0))
                else:
                    # Locked in status displayed to player 1
                    text2 = font.render("Locked In", 1, (0, 0, 0))

            # If player 2 has not locked in display waiting for move
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        # Display text to both players accordingly
        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))

        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        # Draw all the button objects to the pygame top level
        for button in buttons:
            button.draw(win)

    pygame.display.update()


def main():
    """
    main function: run game
    """
    run = True
    clock = pygame.time.Clock()
    n = Network() # Establish a network
    player = int(n.getP()) # get player number
    print(f"You are player {player}")

    while run:
        clock.tick(60)
        try:
            game = n.send("get") # constantly listen for player moves
        except:
            run = False
            print("Couldn't get game (1)") ########
            break

        # If both players have locked in
        if game.bothWent():

            redrawWindow(win, game, player)
            pygame.time.delay(500)

            try:
                game = n.send("reset") # reset the game
            except:
                run = False
                print("Couldn't get game (2)")
                break


            font = pygame.font.SysFont("Halvetica", 90)

            # Get winner and display appropriate message to both the players, if they have won, tied or lost the game

            if game.winner() == player:
                text = font.render("You Won", 1, (0, 255, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game", 1, (0, 0, 255))
            else:
                text = font.render("You Lost", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        # Listen for events in the pygame window
        for event in pygame.event.get():
            # Quit button
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # If mouse click, get mouse position and check which button has been clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check which button has been clicked
                for button in buttons:
                    if button.click(pos) and game.connected():
                        # Check which player has interacted, and if not already locked in... send in the player move
                        if player == 0:
                            if not game.p1Went:
                                n.send(button.text)
                        else:
                            if not game.p2Went:
                                n.send(button.text)

        redrawWindow(win, game, player)

def menuScreen():
    # Pre-game menu screen

    run = True
    clock = pygame.time.Clock()

    while run:
        win.fill((128, 128, 128))
        clock.tick(60)
        font = pygame.font.SysFont("Halvetica", 60)
        text = font.render("Click to Play", 1, (0, 255, 0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()

# code

# Pygame top-level
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# Button objects
buttons = [
    Button("Rock", 50, 500, (255, 0, 0)), # Rock Button
    Button("Paper", 250, 500, (0, 255, 0)), # Paper Button
    Button("Scissors", 450, 500, (0, 0, 255)) # Scissor Button
]

menuScreen()
