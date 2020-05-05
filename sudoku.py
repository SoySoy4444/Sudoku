import pygame, sys, numpy, copy

pygame.init()
global windowSize, screen
windowSize = (720, 720)
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Sudoku")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (220, 220, 220)
YELLOW = (255, 255, 237)
RED = (255, 0, 0)

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
        self.originalGrid = copy.deepcopy(grid)
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
            self.fontSize -= 1
        print("Font size found: ", self.fontSize)
    
    #accepts a GRID coordinate like 7, 6. Checks if it is valid to play a number N at x, y.
    def isPossible(self, y, x, n):
        #check along the y axis
        if n in grid[y]:
            return False
        
        #check along the x axis
        for row in grid:
            if row[x] == n:
                return False
        
        #check for the 3x3 square
        startRow = y - (y % 3)
        startCol = x - (x % 3)
        for row in grid[startRow:startRow+3]:
            for number in row[startCol:startCol+3]:
                if number == n:
                    return False
        return True
        
    def solve(self, animation=False): #Specify whether to display how it was solved
        return grid
        
    
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
    
        for row in range(9):
            for col in range(9):
                if self.grid[col][row] != 0: #num is one of the original clues
                    top = int(self.yTop + (col * self.squareSize))
                    left = int(self.xLeft + (row * self.squareSize))
                    
                    region = pygame.Rect(left+self.lineThickness, top+self.lineThickness, self.squareSize-self.lineThickness, self.squareSize-self.lineThickness) #the square to cover with blue
                    self.currentHighLightedSquare = region
                    self.addNumber(str(self.grid[col][row]), colour=RED)
        
        self.currentHighLightedSquare = None
        matrix = numpy.matrix(self.grid)
        print(matrix)
    
    #accepts a GRID coordinate like 4, 1
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
            
            #If we unhighlighted an original square,
            if self.originalGrid[highlightedSquareY][highlightedSquareX] != 0:
                self.addNumber(str(self.originalGrid[highlightedSquareY][highlightedSquareX]), colour=RED)
            #if we unhighlighted a square that had a non-original number inside, then we need to undo. 
            elif grid[highlightedSquareY][highlightedSquareX] != 0:
                self.addNumber(grid[highlightedSquareY][highlightedSquareX])
            #otherwise, there was never a number in the first place, so it doesn't matter
            
        self.currentHighLightedSquare = None
        self.squareSelected = False #a square is no longer selected
    
    #Converts MOUSE POSITION to GRID COORDINATE. Something like (431.9, 221.2) to (6, 5). 
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
    
    #Accepts "" (backspace), "1", "2", "3"..."9", ADDS to the grid
    def addNumber(self, number, colour=BLACK):
        x, y = self.currentHighlightedSquareGridCoordinates() #get the coordinates of the current active square
        
        if number == "": #if user pressed BACKSPACE
            number = "0" #reset the square to 0
        grid[y][x] = int(number) #TODO: Opposite is better. Check why.
        print(number)
        if number == "0": #backspace
            number = " "
        
        arialFont = pygame.font.SysFont("arialunicodettf", self.fontSize)
        numberText = arialFont.render(str(number), True, colour)
        screen.blit(numberText, self.currentHighLightedSquare)
    
    #Returns the GRID COORDINATES of the CURRENT SELECTED SQUARE
    def currentHighlightedSquareGridCoordinates(self):
        x, y = self.screenCoordinateToGridCoordinate((self.currentHighLightedSquare.x, self.currentHighLightedSquare.y))
        return x, y
    
    #Returns whether the current SELECTED square is a clue square
    def originalSquare(self):
        x, y = self.screenCoordinateToGridCoordinate((self.currentHighLightedSquare.x, self.currentHighLightedSquare.y))
        return self.originalGrid[y][x] != 0
        
def run():
    global grid
    grid = [
        #C                        C
        #O                        O
        #L                        L
        #0                        8
        [9, 8, 0, 0, 0, 0, 0, 0, 0],        #ROW 0
        [0, 0, 3, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 9],        #ROW 8
    ]
    
    mySudoku = Sudoku(grid, 540) #for best results, should be a multiple of 9
    mySudoku.draw()
    
    assert mySudoku.isPossible(0, 2, 9) == False, "it's false by horizontal!"
    assert mySudoku.isPossible(0, 2, 1) == True, "it's true by horizontal!"
    assert mySudoku.isPossible(3, 3, 4) == True
    assert mySudoku.isPossible(3, 3, 6) == False, "it's false by vertical!"
    print(mySudoku.isPossible(8, 8, 6))

    print(f"Each little square is {mySudoku.squareSize} big.")
    print(f"The top left of the square is at {mySudoku.xLeft}, {mySudoku.yTop}")
    print(f"The bottom right of the square is at {mySudoku.xRight}, {mySudoku.yBottom}")
    
    solveButton = Button(WHITE, text="Solve", fontSize = 24, widthScale=1.5)
    solveButton.draw(200, 680)
    
    checkButton = Button(WHITE, text="Check", fontSize = 24, widthScale=1.5)
    checkButton.draw(400, 680)
    
    generateButton = Button(WHITE, text="Generate", fontSize = 24, widthScale=1.5)
    generateButton.draw(300, 100)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                coordinates = mySudoku.screenCoordinateToGridCoordinate(mousePosition)
                                
                if coordinates: #if the place clicked is INSIDE the grid, then
                    mySudoku.unhighlight()
                    mySudoku.highlight(coordinates) #highlight the new square
                else: #coordinates == False and the place is OUTSIDE the grid
                    mySudoku.unhighlight() #unhighlight

                if solveButton.isMouseHover(mousePosition):
                    #grid = mySudoku.solve()
                    #print(grid)
                    pass
                if checkButton.isMouseHover(mousePosition):
                    #check if all squares have been filled
                    filled = True
                    for row in grid:
                        for num in row:
                            if num == 0:
                                filled = False
                                break
                        if not filled:
                            break
                        
                    print("Filled: ", filled)
                    #TODO: If filled is True, mySudoku.check()
                    if filled:
                        #mySudoku.check()
                        pass
                    
            if event.type == pygame.KEYDOWN:
                if (event.unicode.isnumeric() or event.key == pygame.K_BACKSPACE) and mySudoku.squareSelected and event.unicode != "0" and not mySudoku.originalSquare():
                    mySudoku.addNumber(event.unicode)
                    print(grid)

                
        pygame.display.update()
if __name__ == "__main__":
    run()