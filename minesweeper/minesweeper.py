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
        self.unclearedBoxes = []
        self.taggedBoxes = []
       
    def createGrid(self, window):
        buttons = {}
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                buttons["btn{}{}".format(x,y)] = Button(window, text = "" , fg='black', state='normal', width = self.buttonSize)
                current_button=buttons["btn{}{}".format(x,y)]
                current_button.bind('<Button-1>', lambda btn=current_button,xx=x,yy=y: self.leftClick(xx,yy,btn))
                current_button.bind('<Button-2>', lambda btn=current_button,xx=x,yy=y: self.rightClick(xx,yy,btn))
                # set Button grid
                current_button.grid(column=x, row=y)
        self.buttons = buttons
                
        resetButton = Button(window, text = "Reset" , fg='black', state='normal', height = self.buttonSize, command = self.resetBoard)
        resetButton.grid(column=0, row = self.gridSize+2, columnspan = self.gridSize)

        settingsButton = Button(window, text = "Settings" , fg='black', state='normal', height = self.buttonSize, command = settingsWindow.openSettings)
        settingsButton.grid(column=0, row = self.gridSize+3, columnspan = self.gridSize)
        
    def leftClick(self,xx,yy,btn):
        print('left clicked button ',xx,' ',yy)
        if self.cellContents[(xx,yy)]=='m':
            self.revealBox(xx,yy)
        else:
            self.revealBox(xx,yy)
            x,y, revealed = self.revealSurroundings(xx,yy)
            self.revealBlanks(xx,yy,revealed)
        winCheck(self.numberOfMines, self.gridSize, self.unclearedBoxes)
        
        
    def rightClick(self,xx,yy,btn):
        print('right clicked button ',xx,' ',yy)
        if [xx,yy] not in self.taggedBoxes:
            self.buttons["btn{}{}".format(xx,yy)].config(image = self.flagImage)
            self.taggedBoxes.append([xx,yy])
        else:
            self.buttons["btn{}{}".format(xx,yy)].config(image = '')
            self.taggedBoxes.remove([xx,yy])

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
        self.unclearedBoxes = []
        self.taggedBoxes = []
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

    def revealBox(self,x,y):
        if self.cellContents[(x,y)] == 'm':
            self.buttons["btn{}{}".format(x,y)].config(image = self.mineImage)
            self.buttons["btn{}{}".format(x,y)].config(text = '')
            gameOver()
        else:
            self.buttons["btn{}{}".format(x,y)].config(text = self.cellContents[(x,y)])
            if [x,y] not in self.unclearedBoxes:
                self.unclearedBoxes.append([x,y])
            
    def revealSurroundings(self, x,y):
        revealed = []
        if self.cellContents[(x,y)] == 0:
            for xx in [-1,0,1]:
                for yy in [-1,0,1]:
                    try:
                        if xx==0 and yy==0:
                            pass
                        elif self.cellContents[(x+xx,y+yy)] != 'm':
                            self.revealBox(x+xx,y+yy)

                            revealed.append([x+xx,y+yy])
                    except:
                        print('edge cell clicked...')
        return x,y,revealed

    def revealBlanks(self,x,y, revealed):
        #add revealed cells to a checklist
        checkList=revealed
        checkedCells = []
        while len(checkList)>0:
            #check all cells in checklist for zero in surroundings
            for cell in checkList:
                x = cell[0]
                y = cell[1]
                for xx in [-1,0,1]:
                    for yy in [-1,0,1]:
                        try:
                            if self.cellContents[(x+xx,y+yy)] == 0:
                            #reveal any zeroes
                                self.revealBox(x+xx,y+yy)
                                self.revealSurroundings(x+xx,y+yy)
                            #add any zero cell coordinates to checkList
                                if [x+xx,y+yy] not in checkList and [x+xx,y+yy] not in checkedCells:
                                    checkList.append([x+xx,y+yy])
                        except:
                            print('cell ({},{}) not detected'.format(x+xx,y+yy))
                            pass
                        checkedCells.append([x+xx,y+yy])
                checkList.remove(cell)
                print('length of checklist:',len(checkList), '\nchecklist:',checkList)

    def refreshGrid(self, gridsize, numberofmines):
        global lbl
        global startMessage
        
        buttons = {}
        self.gridSize = gridsize
        self.numberOfMines = numberofmines

        widgets = root.grid_slaves()
        for l in widgets:
            l.destroy()
            
        message = startMessage
        lbl = Label(root, text = message)
        lbl.grid(column=0, row = self.gridSize+1, columnspan = self.gridSize)
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                buttons["btn{}{}".format(x,y)] = Button(root, text = "" , fg='black', state='normal', width = self.buttonSize)
                current_button=buttons["btn{}{}".format(x,y)]
                current_button.bind('<Button-1>', lambda btn=current_button,xx=x,yy=y: self.leftClick(xx,yy,btn))
                current_button.bind('<Button-2>', lambda btn=current_button,xx=x,yy=y: self.rightClick(xx,yy,btn))
                # set Button grid
                current_button.grid(column=x, row=y)
        self.buttons = buttons
                
        resetButton = Button(root, text = "Reset" , fg='black', state='normal', height = self.buttonSize, command = self.resetBoard)
        resetButton.grid(column=0, row = self.gridSize+2, columnspan = self.gridSize)

        settingsButton = Button(root, text = "Settings" , fg='black', state='normal', height = self.buttonSize, command = settingsWindow.openSettings)
        settingsButton.grid(column=0, row = self.gridSize+3, columnspan = self.gridSize)
        self.resetBoard()
        
                            
            

def gameOver():
        message = 'You Lose'
        updateMessage(message)

def onWin():
    message = 'You Win!'
    updateMessage(message)

def winCheck(numberOfMines,gridSize,clearedBoxes):
    if numberOfMines==gridSize**2-len(clearedBoxes):
        onWin()
    print('unclearedBoxes:',gridSize**2-len(clearedBoxes))
        
def updateMessage(message):
    lbl.config(text = message)

class SettingsWindow():
    def __init__(self, numberOfMines, gridSize):
        self.numberOfMines = numberOfMines
        self.gridSize = gridSize
        self.buttonSize = 25
    
    def openSettings(self):
        print('settings window opening...')
        self.settings = Tk()
        self.settings.geometry('1000x700')
        
        self.minesLabel = Label(self.settings, text = 'Number of mines: {}'.format(self.numberOfMines))
        self.minesLabel.grid(column=0, row=2)
        
        self.gridSizeLabel = Label(self.settings, text = 'Grid size: {}'.format(self.gridSize))
        self.gridSizeLabel.grid(column=0, row=3)
        
        increaseMinesButton = Button(self.settings, text = "increase mines" , fg='black', state='normal', height = self.buttonSize, command = self.increaseMines)
        increaseMinesButton.grid(column=0, row =1)

        decreaseMinesButton = Button(self.settings, text = "decrease mines" , fg='black', state='normal', height = self.buttonSize, command = self.decreaseMines)
        decreaseMinesButton.grid(column=1, row =1)

        increaseGridSizeButton = Button(self.settings, text = "increase grid size" , fg='black', state='normal', height = self.buttonSize, command = self.increaseGridSize)
        increaseGridSizeButton.grid(column=2, row =1)

        decreaseGridSizeButton = Button(self.settings, text = "decrease grid size" , fg='black', state='normal', height = self.buttonSize, command = self.decreaseGridSize)
        decreaseGridSizeButton.grid(column=3, row =1)

        okButton = Button(self.settings, text = "OK" , fg='black', state='normal', height = self.buttonSize, command = self.applySettings)
        okButton.grid(column=1, row =3)
        

    def increaseMines(self):
        self.numberOfMines+=1
        print('number of mines increased...')
        self.updateMessages()

    def decreaseMines(self):
        self.numberOfMines-=1
        print('number of mines decreased...')
        self.updateMessages()

    def increaseGridSize(self):
        self.gridSize+=1
        print('grid size increased...')
        self.updateMessages()

    def decreaseGridSize(self):
        self.gridSize-=1
        print('grid size decreased...')
        self.updateMessages()

    def applySettings(self):
        print('applying settings...')
        grid.refreshGrid(self.gridSize, self.numberOfMines)
        self.settings.destroy()


    def updateMessages(self):
        self.minesLabel['text'] = 'Number of mines: {}'.format(self.numberOfMines)
        self.gridSizeLabel['text'] = 'Grid size: {}'.format(self.gridSize)
        
        
def main():
    global startMessage
    global lbl
    global grid
    global settingsWindow
    global root
    
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
    settingsWindow = SettingsWindow(numberOfMines, gridSize)
    
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
