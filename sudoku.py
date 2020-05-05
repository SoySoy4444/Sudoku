import pygame, sys, copy, time

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

clock = pygame.time.Clock()

def fade(width, height, alpha=95, colour=WHITE):
    fade = pygame.Surface((width, height))
    fade.fill(colour)
    fade.set_alpha(alpha)
    screen.blit(fade, (0, 0))

def pause(seconds = None):
    paused = True
    startTime = time.time()
    currentScreen = screen.copy()
    
    if seconds == None: #display "Paused" message indefinitely until the user presses c.
        fade(windowSize[0], windowSize[1]) #make the screen look whitish
        pauseMessage = Message("Paused", 48)
        pauseMessage.blit(screen, ("horizontalCentre", "verticalCentre"))

    while paused:
        clock.tick(2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: #if c pressed, continue playing
                    screen.blit(currentScreen, (0, 0))
                    paused = False
                    
        if seconds != None and time.time() - startTime > seconds:
            paused = False
        pygame.display.update()

class Message():
    def __init__(self, text, fontSize, fontStyle = "arialunicodettf", textColour = BLACK, backgroundColour = WHITE):        
        font = pygame.font.SysFont(fontStyle, fontSize)
        self.myText = font.render(text, 1, textColour, backgroundColour)
        self.width, self.height = self.myText.get_size()[0], self.myText.get_size()[1]

    def blit(self, screen, pos):
        self.x = windowSize[0]//2 - self.width//2 if pos[0] == "horizontalCentre" else pos[0]
        self.y = windowSize[1]//2 - self.height//2 if pos[1] == "verticalCentre" else pos[1]
        screen.blit(self.myText, (self.x, self.y))

class Button():
    #width and height will only be passed in for buttons with no text (images and plain buttons)
    #windowSize will only be passed in if width="horizontalCentre" or height="verticalCentre"
    def __init__(self, color, text='', textColour = BLACK, fontSize=48, width=None, height=None, widthScale=1):
        self.color = color
        self.text = text
        self.textColour = textColour
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
        
        pygame.draw.rect(screen, self.color, (self.x, self.y, int(self.width), int(self.height)), 0)
        
        if self.text != '': #We want text displayed on our button
            arialFont = pygame.font.SysFont("arialunicodettf", self.fontSize)
            text = arialFont.render(self.text, 1, self.textColour)
            screen.blit(text, (int(self.x + (self.width//2 - text.get_width()//2)), int(self.y + (self.height//2 - text.get_height()//2))))

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
        #print("Font size found: ", self.fontSize)
    
    #Used for solving only
    #accepts a GRID coordinate like 7, 6. Checks if it is valid to play a number N at x, y.
    def isValid(self, board, y, x, n):
        #check along the y axis
        if n in board[y]:
            return False
        
        #check along the x axis
        for row in board:
            if row[x] == n:
                return False
        
        #check for the 3x3 square
        startRow = y - (y % 3)
        startCol = x - (x % 3)
        for row in board[startRow:startRow+3]:
            for number in row[startCol:startCol+3]:
                if number == n:
                    return False
        return True
    
    #Used for checking only
    #Unlike isPossible, it doesn't check if it can add at a certain location, but it checks if the square is valid. 
    def noDuplicates(self, y, x, n):
        #check along the y axis
        if grid[y].count(n) != 1: #continue only if the number appears only once in the row. Otherwise, false
            return False
        
        #check along the x axis
        nCount = 0
        for row in grid:
            if row[x] == n:
                nCount += 1
        if nCount != 1: #continue only if the number appears only once in the col. Otherwise, false
                return False
        
        nCount = 0
        #check for the 3x3 square
        startRow = y - (y % 3)
        startCol = x - (x % 3)
        for row in grid[startRow:startRow+3]:            
            for number in row[startCol:startCol+3]:
                if number == n:
                    nCount += 1
        if nCount != 1: #continue only if the number appears only once in the square.
            return False
        
        return True
    
    """
    #recursive function, backtracking.
    def solve(self):
        for row in range(9):
            for col in range(9):
                if self.solvedGrid[row][col] == 0: #for each unsolved square (unsolved square == 0)
                    for i in range(1, 10): #test numbers from 1 - 9
                        if self.isValid(row, col, i): #when we reach a number that is possible
                            self.solvedGrid[row][col] = i #set the square to that number regardless of whether it is correct or not
                            self.solve() #recursion
                            self.solvedGrid[row][col] = 0
                    return
    
    def getAnswer(self):#, animation=False): #Specify whether to display how it was solved
        self.solvedGrid = copy.deepcopy(self.originalGrid)
        self.solve()
        return self.solvedGrid
"""

    def solve(self):
        emptySquare = self.nextEmptySquare()
        if not emptySquare: #no more empty squares, finished solving so return the solved grid back to getAnswer()
            return self.solvedGrid
        else:
            row, col = self.nextEmptySquare()
        
            for i in range(1, 10):
                if self.isValid(self.solvedGrid, row, col, i):
                    self.solvedGrid[row][col] = i
                    if self.solve():
                        return self.solvedGrid #keep returning the board as long as the current board is valid
                    self.solvedGrid[row][col] = 0 #as soon as the current board becomes impossible to solve, backtrack
            return False
    
    def nextEmptySquare(self):
        for row in range(9):
            for col in range(9):
                if self.solvedGrid[row][col] == 0: #for each unsolved square (unsolved square == 0)
                    return row, col #return next empty square
        return False #no more empty squares, finished solving!
    
    def getAnswer(self):
        self.solvedGrid = copy.deepcopy(self.originalGrid)
        self.solvedGrid = self.solve()
        return self.solvedGrid
    
    def check(self):
        for row in range(9):
            for col in range(9):
                if not self.noDuplicates(row, col, grid[row][col]):
                    return False
        return True
    
    def hint(self):
        pass
    
    def generate(self):
        pass
    
    def draw(self, board):
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
                if board[col][row] != 0: #num is one of the original clues
                    top = int(self.yTop + (col * self.squareSize))
                    left = int(self.xLeft + (row * self.squareSize))
                    
                    region = pygame.Rect(left+self.lineThickness, top+self.lineThickness, self.squareSize-self.lineThickness, self.squareSize-self.lineThickness) #the square to cover with blue
                    self.currentHighLightedSquare = region
                    self.addNumber(str(board[col][row]), colour=RED)
        
        self.currentHighLightedSquare = None
    
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
    """
    grid = [
        #C                        C
        #O                        O
        #L                        L
        #0                        8
        [0, 3, 5, 2, 6, 9, 7, 8, 1],        #ROW 0
        [6, 8, 2, 5, 7, 1, 4, 9, 3],
        [1, 9, 7, 8, 3, 4, 5, 6, 2],
        [8, 2, 6, 1, 9, 5, 3, 4, 7],
        [3, 7, 4, 6, 8, 2, 9, 1, 5],
        [9, 5, 1, 7, 4, 3, 6, 2, 8],
        [5, 1, 9, 3, 2, 6, 8, 7, 4],
        [2, 4, 8, 9, 5, 7, 1, 3, 6],
        [7, 6, 3, 4, 1, 8, 2, 5, 9],        #ROW 8
    ]

    grid = [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 1, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0],
    ]
    """
    
    grid = [
        [0, 3, 5, 2, 6, 9, 7, 8, 1],
        [6, 8, 2, 0, 7, 1, 0, 9, 3],
        [1, 9, 0, 8, 3, 4, 5, 6, 2],
        [8, 2, 6, 1, 9, 5, 3, 0, 7],
        [3, 7, 4, 0, 8, 2, 9, 1, 5],
        [9, 5, 1, 7, 4, 3, 6, 2, 8],
        [5, 1, 9, 0, 2, 6, 8, 7, 4],
        [2, 4, 0, 9, 5, 7, 1, 3, 6],
        [7, 6, 3, 4, 1, 8, 2, 5, 9],
    ]
    
    mySudoku = Sudoku(grid, 540) #for best results, should be a multiple of 9
    mySudoku.draw(grid)
    
    #assert mySudoku.isPossible(0, 2, 9) == False, "it's false by horizontal!"
    #assert mySudoku.isPossible(0, 2, 1) == True, "it's true by horizontal!"
    #assert mySudoku.isPossible(3, 3, 4) == True
    #assert mySudoku.isPossible(3, 3, 6) == False, "it's false by vertical!"
    #print(mySudoku.isPossible(8, 8, 6))
    
    solveButton = Button(WHITE, text="Solve", fontSize = 24, widthScale=1.5)
    solveButton.draw(200, 680)
    
    checkButton = Button(WHITE, text="Check", fontSize = 24, widthScale=1.5)
    checkButton.draw(400, 680)
    
    generateButton = Button(WHITE, text="Generate", fontSize = 24, widthScale=1.5)
    generateButton.draw(300, 50)
    
    newGameButton = Button(WHITE, text="New Game", fontSize = 24, widthScale=1.5)
    newGameButton.draw(20, 20)
    
    while True:
        clock.tick(30)
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
                    screen.fill(GREY)
                    
                    solvedGrid = mySudoku.getAnswer()
                    mySudoku.draw(solvedGrid)
                    newGameButton.draw(20, 20)
                
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
                    
                    if filled:
                        if mySudoku.check():
                            
                            currentScreen = screen.copy()
                            
                            gameEndMessage = Message("Well done!", 48)
                            gameEndMessage.blit(screen, ("horizontalCentre", "verticalCentre"))
                            pause(seconds=2)
                            screen.blit(currentScreen, (0, 0))
                        else:
                            currentScreen = screen.copy()
                            
                            tryAgainMessage = Message("Incorrect. Try again", 48)
                            tryAgainMessage.blit(screen, ("horizontalCentre", "verticalCentre"))
                            pause(seconds=2)
                            screen.blit(currentScreen, (0, 0))
                
                if newGameButton.isMouseHover(mousePosition):
                    run()
                
            if event.type == pygame.KEYDOWN:
                if (event.unicode.isnumeric() or event.key == pygame.K_BACKSPACE) and mySudoku.squareSelected and event.unicode != "0" and not mySudoku.originalSquare():
                    mySudoku.addNumber(event.unicode)
                    
                if event.key == pygame.K_p: #if p pressed, pause
                    pause()
                
        pygame.display.update()
if __name__ == "__main__":
    run()