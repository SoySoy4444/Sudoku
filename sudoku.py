import pygame, sys

pygame.init()
global windowSize, screen
windowSize = (720, 720)
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Sudoku")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (220, 220, 220)

class Button():
    #width and height will only be passed in for buttons with no text (images and plain buttons)
    #windowSize will only be passed in if width="horizontalCentre" or height="verticalCentre"
    def __init__(self, color, text='', textColour = BLACK, image = None, fontSize=48, width=None, height=None, widthScale=1):
        self.color = color
        self.text = text
        self.textColour = textColour
        self.image = image
        self.fontSize = fontSize
        
        self.widthScale = widthScale
        if self.text != '': #We want text displayed on our button
            arialFont = pygame.font.SysFont("arialunicodettf", fontSize)
            text = arialFont.render(self.text, 1, self.textColour)
            self.width, self.height = arialFont.size(self.text)
            self.width *= self.widthScale
        else:
            self.width, self.height = width, height
        
        #the location depends on the width and height and so must be set after the width/height


    def draw(self, x, y):
        #Call this method to draw the button on the screen
        
        self.x = x
        self.y = y
        
        
        
        if self.image != None: #We want an image button
            img = pygame.image.load(self.image)
            img = pygame.transform.scale(img, (self.width, self.height))
            screen.blit(img, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '': #We want text displayed on our button
            arialFont = pygame.font.SysFont("arialunicodettf", self.fontSize)
            text = arialFont.render(self.text, 1, self.textColour)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isMouseHover(self, mousePos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if mousePos[0] > self.x and mousePos[0] < self.x + self.width:
            if mousePos[1] > self.y and mousePos[1] < self.y + self.height:
                return True
        return False

class Sudoku:
    def __init__(self, grid, gridSize):
        self.grid = grid
        self.gridSize = gridSize
        self.squareSize = gridSize//9
    
    def isPossible(self):
        pass
    
    def solve(self, animation=False): #Specify whether to display how it was solved
        pass
        
    def update(self):
        pass
    
    def hint(self, square):
        pass
    
    def generate(self):
        pass
    
    def draw(self):
        pass