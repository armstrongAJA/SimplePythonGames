# Import Module
from tkinter import *
from tkmacosx import Button
from random import randrange

def SetUpGrid(gridSize):
    global buttons
    global root
    global lbl
# Set geometry(widthxheight)
    root.destroy()
    root = Tk()
    root.geometry('1000x700')
    lbl = Label(root, text = message)
    lbl.grid(column=4, row = 5)
    for rowAndColumn in range(gridSize):
            Grid.rowconfigure(root,rowAndColumn,weight=5, minsize=100)
            Grid.columnconfigure(root,rowAndColumn,weight=5, minsize=100)
            
    # generate all the buttons for the board
    buttons = {}
    for x in range(gridSize):
        for y in range(gridSize):
            print('adding button:',x,y)
            buttons["btn{}{}".format(x,y)] = Button(root, text = "" , bg='red', fg='black', state='normal')
            current_button=buttons["btn{}{}".format(x,y)]
            current_button.configure(command=lambda btn=current_button,xx=x,yy=y: clicked(xx,yy,btn))
            # set Button grid
            current_button.grid(column=x, row=y, sticky="NSEW")
            
    #Generate all the settings buttons
    Reset_button = Button(root, text = "Reset" , fg = "black", bg = "red", command=lambda: SetUpGrid(gridSize))
    Reset_button.grid(column=gridSize, row=gridSize)
    
    IncreaseGridSize_button = Button(root, text = "Increase grid size" , fg = "black", bg = "red", command=lambda: IncreaseGridSize())
    IncreaseGridSize_button.grid(column=gridSize, row=gridSize-1)
    
    DecreaseGridSize_button = Button(root, text = "Decrease grid size" , fg = "black", bg = "red", command=lambda: DecreaseGridSize())
    DecreaseGridSize_button.grid(column=gridSize, row=gridSize-2)

    IncreaseLevel_button = Button(root, text = "Increase Level" , fg = "black", bg = "red", command=lambda: IncreaseLevel())
    IncreaseLevel_button.grid(column=gridSize, row=0)

    DecreaseLevel_button = Button(root, text = "Decrease Level" , fg = "black", bg = "red", command=lambda: DecreaseLevel())
    DecreaseLevel_button.grid(column=gridSize, row=1)    
    
    ResetBoard()
        
def clicked(x,y, current_button):
    global buttons
        #change color of button clicked
    if current_button["bg"]=="red":
        current_button.config(bg='yellow')
    else:
        current_button.config(bg='red')
    #change color of surrounding buttons
    for i in [-1,1]:
            try:
                print
                if buttons['btn{}{}'.format(x+i,y)]['bg']=='yellow':
                    buttons['btn{}{}'.format(x+i,y)].config(bg='red')
                    print('buttonisyellow')
                else:
                    buttons['btn{}{}'.format(x+i,y)].config(bg='yellow')
                    print('buttonisred')
            except:
                pass
            
            try:
                if buttons['btn{}{}'.format(x,y+i)]['bg']=='yellow':
                    buttons['btn{}{}'.format(x,y+i)].config(bg='red')
                else:
                    buttons['btn{}{}'.format(x,y+i)].config(bg='yellow')
            except:
                pass
    CheckWin()
    
    return


def ResetBoard():
    global message
    global lbl
    global buttons
    global isWin
    print('resetting board')
    isWin=False
    random_numbers = GenerateRandomNumbers(difficultyLevel)
    
    for btn in buttons.keys():
        buttons[btn].config(state='normal')
        btn_id = ''.join(char for char in btn if char.isdigit())
        print(btn_id)
        for x,y in random_numbers:
            if btn == 'btn{}{}'.format(x,y):
                print('clicking:',x,y)
                clicked(x,y,buttons["btn{}{}".format(x,y)])
    message='Click a button to switch all neighboring buttons!'
    lbl["text"]= message


def IncreaseGridSize():
    global gridSize
    print('increasing_grid size')
    if gridSize <= 10:
        gridSize+=1
        SetUpGrid(gridSize)

def DecreaseGridSize():
    global gridSize
    print('decreasing_grid size')
    if gridSize>1:
        gridSize-=1
        SetUpGrid(gridSize)

def onWin():
    global message
    global lbl
    global isWin
    global buttons
    
    isWin=True
    message='You win!'
    lbl["text"]=message
    for btn in buttons.keys():
        print('disabling all buttons...')
        buttons[btn]["state"]="disabled"
        buttons[btn]["bg"]='red'

def IncreaseLevel():
    global difficultyLevel
    print('increasing difficulty')
    difficultyLevel+=1
    SetUpGrid(gridSize)

def DecreaseLevel():
    global difficultyLevel
    print('decreasing difficulty')
    difficultyLevel-=1
    SetUpGrid(gridSize)

def GenerateRandomNumbers(difficultyLevel):
    xyCoords=[]
    for i in range(difficultyLevel):
        x = randrange(gridSize)
        y = randrange(gridSize)
        xyCoords.append((x,y))
    return xyCoords

def CheckWin():
    global isWin
    global buttons
    
    yellowCount=0
    for btn in buttons.values():
        if btn["bg"]=="yellow":
            yellowCount+=1
            
    if yellowCount==0:
        isWin=True
        
    if isWin==True:
        onWin()


# create root window
root = Tk()
gridSize = 4
difficultyLevel = 1
isWin=False
# root window title and dimension
root.title("Welcome to Lights Out!")
# adding a label to the root window
message = "Click a button to switch all neighboring buttons!"
lbl = Label(root, text = message)

SetUpGrid(gridSize)

# function to display text when
# button is clicked


# Execute Tkinter to run the game
root.mainloop()
