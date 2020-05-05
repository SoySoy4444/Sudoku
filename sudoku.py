import pygame, sys, numpy

pygame.init()
global windowSize, screen
windowSize = (720, 720)
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Sudoku")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (220, 220, 220)
YELLOW = (255, 255, 237)

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
    def __init__(self, grid, gridSize, lineThickness=1):
        self.grid = grid
        self.gridSize = gridSize
        self.squareSize = gridSize//9
        self.lineThickness = lineThickness
        self.currentHighLightedSquare = None #Initially, no squares should be highlighted
        self.squareSelected = False #Initially, no squares should be selected
        
        self.verticalOffset = (windowSize[0] - self.gridSize) // 2 #distance from the vertical edge of the screen to the vertical edge of the grid
        self.horizontalOffset = (windowSize[1] - self.gridSize) // 2 #distance from the horizontal edge of the screen to the horizontal edge of the grid
        
        self.xLeft, self.xRight = self.verticalOffset, windowSize[0]-self.verticalOffset
        self.yTop, self.yBottom = self.horizontalOffset, windowSize[1]-self.horizontalOffset
        
        
        
        
        self.fontSize = 100 #starting font size, adjust until correct font size found

        arialFont = pygame.font.SysFont("arialunicodettf", self.fontSize)
        fontWidth, fontHeight = arialFont.size("0")
        while fontWidth > self.squareSize or fontHeight > self.squareSize:
            arialFont = pygame.font.SysFont("arialunicodettf", self.fontSize)
            fontWidth, fontHeight = arialFont.size("0")
            print("Finding size", self.fontSize)
            self.fontSize -= 1
        print(self.fontSize)
    
    def isPossible(self):
        pass
    
    def solve(self, animation=False): #Specify whether to display how it was solved
        return grid
        
    def update(self):
        pass
    
    def hint(self):
        pass
    
    def generate(self):
        pass
    
    def draw(self):
        screen.fill(GREY)
        
        #Start drawing at the top left of the grid
        currentXPosition = self.xLeft #start from the left of the grid
        currentYPosition = self.yTop
        
        #Where do we want to go? To the right and down
        destinationXPosition = self.xRight
        destinationYPosition = self.yBottom
        
        #horizontal lines     
        for x in range(10): #10 lines needed to produce 9 boxes
            colour = BLACK if x % 3 == 0 else WHITE
            pygame.draw.line(screen, colour, (currentXPosition, currentYPosition), (destinationXPosition, currentYPosition), self.lineThickness) #horizontal line
            currentYPosition += self.squareSize #move on to the next horizontal line, down the grid

        #vertical lines
        currentYPosition = self.yTop #reset currentYPosition
        for y in range(10): #10 lines needed to produce 9 boxes
            colour = BLACK if y % 3 == 0 else WHITE
            pygame.draw.line(screen, colour, (currentXPosition, currentYPosition), (currentXPosition, destinationYPosition), self.lineThickness) #vertical line
            currentXPosition += self.squareSize #move on to the next vertical line, to the right of the grid
    
    def highlight(self, gridCoordinate):
        
        #the new highlight
        top = int(self.yTop + (gridCoordinate[1] * self.squareSize))
        left = int(self.xLeft + (gridCoordinate[0] * self.squareSize))
        region = pygame.Rect(left+self.lineThickness, top+self.lineThickness, self.squareSize-self.lineThickness, self.squareSize-self.lineThickness) #the square to cover with blue
        screen.fill(YELLOW, rect=region)
        
        self.currentHighLightedSquare = region
        self.squareSelected = True
        
    def unhighlight(self):
        if self.currentHighLightedSquare: #if a square is currently highlighted already,
            screen.fill(GREY, rect=self.currentHighLightedSquare)
            highlightedSquareX, highlightedSquareY = self.currentHighlightedSquareGridCoordinates()
            
            #if we unhighlighted a square that had a number inside, then we need to undo. 
            if grid[highlightedSquareY][highlightedSquareX] != 0:
                self.addNumber(self.previousNumber)
        self.currentHighLightedSquare = None
        self.squareSelected = False #a square is no longer selected
    
        #Something like (431.9, 221.2) to (6, 5)
    def screenCoordinateToGridCoordinate(self, mousePosition):
        mouseX, mouseY = mousePosition
        #if the location clicked is outside the grid
        if not (mouseX > self.xLeft and mouseX < self.xRight and mouseY > self.yTop and mouseY < self.yBottom):
            return False
            self.squareSelected = False
        else: #must be inside the grid, so find the corresponding coordinate.
            row = (mouseX - self.xLeft) // ((self.xRight - self.xLeft)/9)  #calculate the row number from 0 - 8
            col = (mouseY - self.yTop) // ((self.yBottom - self.yTop)/9)  #calculate the col number from 0 - 8
            return int(row), int(col)
            self.squareSelected = True
    
    def addNumber(self, number):
        x, y = self.currentHighlightedSquareGridCoordinates()
        grid[y][x] = number #TODO: Opposite is better. Check why.
        print("Added", number, "to", x, y)
        
        arialFont = pygame.font.SysFont("arialunicodettf", self.fontSize)
        numberText = arialFont.render(number, True, BLACK)
        screen.blit(numberText, self.currentHighLightedSquare)
        
        self.previousNumber = number
        
        matrix = numpy.matrix(grid)
        print(matrix)
        
    def currentHighlightedSquareGridCoordinates(self):
        x, y = self.screenCoordinateToGridCoordinate((self.currentHighLightedSquare.x, self.currentHighLightedSquare.y))
        return x, y
        
def run():
    global grid
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    
    mySudoku = Sudoku(grid, 540) #for best results, should be a multiple of 9
    mySudoku.draw()
    
    print(f"Each little square is {mySudoku.squareSize} big.")
    print(f"The top left of the square is at {mySudoku.xLeft}, {mySudoku.yTop}")
    print(f"The bottom right of the square is at {mySudoku.xRight}, {mySudoku.yBottom}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                coordinates = mySudoku.screenCoordinateToGridCoordinate(mousePosition)
                print(coordinates)
                
                if coordinates: #if the place clicked is INSIDE the grid, then
                    mySudoku.unhighlight()
                    mySudoku.highlight(coordinates) #highlight the new square
                else: #coordinates == False and the place is OUTSIDE the grid
                    mySudoku.unhighlight() #unhighlight

            if event.type == pygame.KEYDOWN:
                if event.unicode.isnumeric() and mySudoku.squareSelected:
                    print(event.unicode)
                    mySudoku.addNumber(event.unicode)

                
        pygame.display.update()
if __name__ == "__main__":
    run()