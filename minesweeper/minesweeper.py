# Import Module
from tkinter import *
from tkmacosx import Button
import random

#define grid class that takes in grid size and number of mines to create the grid using a constructor
class Grid():
    def __init__(self,gridSize, numberOfMines):
        self.gridSize=gridSize
        self.numberOfMines = numberOfMines
        self.buttonSize = 25
        self.cellContents = {}
        self.mineImage = PhotoImage(file = r"mine.png").subsample(13,13)
        self.flagImage = PhotoImage(file = r"flag.png").subsample(30,30)
        
    def createGrid(self, window):
        buttons = {}
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                print('adding button:',x,y)
                buttons["btn{}{}".format(x,y)] = Button(window, text = "" , fg='black', state='normal', width = self.buttonSize)
                current_button=buttons["btn{}{}".format(x,y)]
                current_button.bind('<Button-1>', lambda btn=current_button,xx=x,yy=y: self.leftClick(xx,yy,btn))
                current_button.bind('<Button-2>', lambda btn=current_button,xx=x,yy=y: self.rightClick(xx,yy,btn))
                # set Button grid
                current_button.grid(column=x, row=y)
        resetButton = Button(window, text = "Reset" , fg='black', state='normal', height = self.buttonSize, command = self.resetBoard)
        resetButton.grid(column=0, row = self.gridSize+2, columnspan = self.gridSize)
        self.buttons = buttons
        
    def leftClick(self,xx,yy,btn):
        print('left clicked button ',xx,' ',yy)
        if self.cellContents[(xx,yy)]=='m':
            self.buttons["btn{}{}".format(xx,yy)]['text'] = ''
            self.buttons["btn{}{}".format(xx,yy)].config(image = self.mineImage)
            gameOver()
        else:
            self.buttons["btn{}{}".format(xx,yy)]['text'] = self.cellContents[(xx,yy)]
            self.revealSurroundings(xx,yy)
        
        
    def rightClick(self,xx,yy,btn):
        print('right clicked button ',xx,' ',yy)
        self.buttons["btn{}{}".format(xx,yy)].config(image = self.flagImage)

    def generateMinePositions(self):
        mineCoords = []
        freeCells = []
        
        #initialize a list of all possible coordinates
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                freeCells.append([x,y])
                
        #randomly initialize mine positions
        for i in range(self.numberOfMines):
            mineCoord = random.choice(freeCells)
            mineCoords.append(mineCoord)
            freeCells.remove(mineCoord)

        self.mineCoords = mineCoords

    def resetBoard(self):
        message = startMessage
        updateMessage(message)
        self.generateMinePositions()
        self.countAdjacentMines()
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                self.buttons["btn{}{}".format(x,y)]['text'] = ''
                self.buttons["btn{}{}".format(x,y)].config(image = '')
                
    def countAdjacentMines(self):
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                mineCount = 0
                for xx in [-1,0,1]:
                    for yy in [-1,0,1]:
                        if xx==0 and yy==0:
                            pass
                        if [x+xx,y+yy] in self.mineCoords:
                            mineCount+=1
                if [x,y] in self.mineCoords:
                    self.cellContents[(x,y)] = 'm'
                else:
                    self.cellContents[(x,y)] = mineCount
                    
    def showAllCellContents(self):
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                if self.cellContents[(x,y)] == 'm':
                    self.buttons["btn{}{}".format(x,y)].config(image = self.mineImage)
                    self.buttons["btn{}{}".format(x,y)].config(text = '')
                else:
                    self.buttons["btn{}{}".format(x,y)].config(text = self.cellContents[(x,y)])

    def revealSurroundings(self, x,y):
        for xx in [-1,0,1]:
            for yy in [-1,0,1]:
                if xx==0 and yy==0:
                    pass
                elif self.cellContents[(x+xx,y+yy)] != 'm':
                    self.buttons["btn{}{}".format(x+xx,y+yy)].config(text = self.cellContents[(x+xx,y+yy)])
                    self.buttons["btn{}{}".format(x+xx,y+yy)].config(image = '')

def gameOver():
        message = 'You Lose'
        updateMessage(message)
        
def updateMessage(message):
    lbl.config(text = message)
        
def main():
    global startMessage
    global lbl
    # create root window
    root = Tk()
    root.geometry('1000x700')
    
    #set starting parameters for grid
    gridSize = 10
    numberOfMines = 15
    isWin=False
    isLoss=False
    # root window title and dimension
    root.title("Welcome to Minesweeper!")
    # adding a label to the root window

    grid = Grid(gridSize, numberOfMines)
    grid.createGrid(root)
    startMessage = "Click to remove cell, right click to flag cell!"
    message = startMessage
    lbl = Label(root, text = message)
    lbl.grid(column=0, row = gridSize+1, columnspan = gridSize)
    grid.generateMinePositions()
    grid.countAdjacentMines()
    #grid.showAllCellContents()
    
    # function to display text when
    # button is clicked


    # Execute Tkinter to run the game
    root.mainloop()

main()
