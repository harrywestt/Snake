"""
Project: Snake with pygame
Version: 1.1
Author: Harry West
Date: 09/2019
"""

from tkinter import Tk
from tkinter import messagebox

import pygame
import random
import sys


class fruit:
    def __init__(self, width, height):
        # Initialise a fruit with a random position and colour
        self.position = [random.randint(0, 19), random.randint(0, 19)]
        self.width = width
        self.height = height
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def getLocation(self):
        # Returns a rect with the fruit location
        return pygame.Rect((int(self.position[0] * (self.width / 20)), int(self.position[1] * (self.height / 20)),
                            int(self.width / 20), int(self.height / 20)))

    def newLocation(self):
        # Randomises a new position
        self.position = [random.randint(0, 19), random.randint(0, 19)]

    def draw(self):
        # Draws the fruit
        pygame.draw.circle(window, self.colour, (self.position[0] * self.width / 20 + self.width / 20 / 2,
                                                 self.position[1] * self.height / 20 + self.width / 20 / 2),
                           (self.width / 20 / 2))


class snake:
    def __init__(self, height, width):
        # Initialises a snake with a positions list, a random direction and two random colours for the body
        self.height = height
        self.width = width
        self.length = 1
        self.positions = [[int(20 / 2), int(20 / 2)]]
        self.direction = random.choice(["UP", "DOWN", "RIGHT", "LEFT"])
        self.firstColour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.secondColour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def getLocation(self):
        # Returns a rect for the location of the head
        return pygame.Rect((int(self.positions[0][0] * (self.width / 20)),
                            int(self.positions[0][1] * (self.height / 20)), int(self.width / 20),
                            int(self.height / 20)))

    def draw(self):
        # Iterate through body
        for i in self.positions:
            # Head has a different colour so needs to be drawn seperately
            if self.positions.index(i) == 0:
                pygame.draw.rect(window, (145, 75, 220), (
                    int(self.positions[0][0] * (self.width / 20)), int(self.positions[0][1] * (self.height / 20)),
                    int(self.width / 20), int(self.height / 20)))
            # Every other body section has a different colour
            elif self.positions.index(i) % 2 == 0:
                pygame.draw.rect(window, self.secondColour, (
                    int(self.positions[self.positions.index(i)][0] * (self.width / 20)),
                    int(self.positions[self.positions.index(i)][1] * (self.height / 20)),
                    int(self.width / 20), int(self.height / 20)))
            # Else draw the body like normal
            else:
                pygame.draw.rect(window, self.firstColour, (
                    int(self.positions[self.positions.index(i)][0] * (self.width / 20)),
                    int(self.positions[self.positions.index(i)][1] * (self.height / 20)),
                    int(self.width / 20), int(self.height / 20)))

    def move(self):
        # Iterates through the length of the body
        for i in range(len(self.positions)):
            # If we are at the head
            if i == 0:
                # Checks the direction
                if self.direction == "UP":
                    # Stores the previous location so the body can follow
                    storageList = [[self.positions[i][0], self.positions[i][1]]]
                    # Moves in the correct direction
                    self.positions[i][1] -= 1
                elif self.direction == "DOWN":
                    storageList = [[self.positions[i][0], self.positions[i][1]]]
                    self.positions[i][1] += 1
                elif self.direction == "RIGHT":
                    storageList = [[self.positions[i][0], self.positions[i][1]]]
                    self.positions[i][0] += 1
                else:
                    storageList = [[self.positions[i][0], self.positions[i][1]]]
                    self.positions[i][0] -= 1
            else:
                # Stores the current location for the next body piece
                storageList.append([self.positions[i][0], self.positions[i][1]])
                # Moves the body along
                self.positions[i][0], self.positions[i][1] = storageList[0][0], storageList[0][1]
                # Removes the first item in the list
                storageList.pop(-2)

    def checkCollision(self):
        # Checks if a wall has been hit
        if self.positions[0][0] < 0 or self.positions[0][0] > 19 or self.positions[0][1] < 0 or self.positions[0][1] > 19:
            return True
        # Iterates through the body positions but skips the head
        for i in range(1, len(self.positions)):
            # If the current body position is in the same location as the head
            if self.positions[i] == self.positions[0]:
                return True

    def growSnake(self):
        # Checks the direction of the snake
        if self.direction == "UP":
            # Adds a new body part at the rear of the snake
            self.positions.append([self.positions[-1][0], self.positions[-1][1] + 1])
        elif self.direction == "DOWN":
            self.positions.append([self.positions[-1][0], self.positions[-1][1] - 1])
        elif self.direction == "LEFT":
            self.positions.append([self.positions[-1][0] + 1, self.positions[-1][1]])
        else:
            self.positions.append([self.positions[-1][0] - 1, self.positions[-1][1]])
        # Increases the length, used for the score
        self.length += 1


def drawBackground(width, height):
    # Iterates through the height of the screen
    for h in range(0, height, int(height / 20)):
        # Iterates through the width of the screen
        for w in range(0, width, int(width / 20)):
            # Every other square has a slightly different shade
            if (h + w) % 2 == 0:
                pygame.draw.rect(window, (94, 177, 200), (w, h, width / 20, height / 20))
            else:
                pygame.draw.rect(window, (76, 145, 166), (w, h, width / 20, height / 20))


def main():
    # Creates the snake and fruits objects
    s = snake(screenHeight, screenWidth)
    fruits = [fruit(screenWidth, screenHeight)]

    # Sets up the score text
    font = pygame.font.SysFont(None, 48)
    text = font.render('Score: 0', True, (0, 0, 0))

    # Creates a pygame clock and a frame rate
    clock = pygame.time.Clock()
    frameRate = 5

    # Game loop
    while True:
        # Ensures that the game runs at a set frame rate
        clock.tick(frameRate)

        # Checks if the player has quit, if so will close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Checks if a key was pressed
        keys = pygame.key.get_pressed()
        # If a certain key was pressed and the snake can travel in that direction

        if keys[pygame.K_UP] and s.direction != "DOWN":
            # Sets the snake direction
            s.direction = "UP"
        elif keys[pygame.K_DOWN] and s.direction != "UP":
            s.direction = "DOWN"
        elif keys[pygame.K_LEFT] and s.direction != "RIGHT":
            s.direction = "LEFT"
        elif keys[pygame.K_RIGHT] and s.direction != "LEFT":
            s.direction = "RIGHT"

        pygame.event.pump()

        # Moves the snake
        s.move()

        # Checks if the snake has hit a wall
        if s.checkCollision():
            # Ends the game loop
            break

        # Iterates over the fruit objects
        for f in fruits:
            # If a fruit collides with the snake
            if s.getLocation().colliderect(f.getLocation()):
                # Grows the snake and puts the fruit in a new location
                f.newLocation()
                s.growSnake()
                # Increases the score text
                text = font.render("Score: " + str(s.length - 1), True, (0, 0, 0))
                # Slightly increases the movement speed, making the game slightly harder with time
                frameRate += 0.1
                # Randomly adds a new fruit to the game if there arent more than 5 already
                if random.randint(1, 5) == 1 and len(fruits) <= 5:
                    fruits.append(fruit(screenWidth, screenHeight))
                # Ends the game loop
                break

        # Draws the background each frame
        drawBackground(screenWidth, screenHeight)
        # Draws each fruit
        for f in fruits:
            f.draw()
        # Draws the snake
        s.draw()
        # Draws the text
        window.blit(text, (0, screenHeight - 35))
        # Updates the display (inefficient but as the game will never need to run at a high frame rate this doesn't matter)
        pygame.display.update()

    # Opens a popup box to show the final score if the game is lost. wm_withdraw() prevents a tk window opening
    Tk().wm_withdraw()
    messagebox.showinfo("Game Over", "Better Luck Next Time!\nYou scored: " + str(s.length - 1))
    pygame.quit()


if __name__ == '__main__':
    while True:
        # Initialises pygame
        pygame.init()

        # Sets the screen size and creates a window
        size = screenWidth, screenHeight = (500, 500)
        window = pygame.display.set_mode(size)
        pygame.display.set_caption("Snake")
        main()
