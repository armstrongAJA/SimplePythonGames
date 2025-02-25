# Import Module
from tkinter import *

# create root window
root = Tk()

# root window title and dimension
root.title("Welcome to Noughts and Crosses!")
# Set geometry(widthxheight)
root.geometry('350x200')

# adding a label to the root window
message = "x to go first!"
lbl = Label(root, text = message)
lbl.grid(column=4, row = 5)

# function to display text when
# button is clicked
current_turn = 'x'
isWin=False

def check_win(x,y):
    global message
    global lbl
    #check horizontal
    wincheck=0
    for i in [-2,-1,1,2]:
        try:
            if buttons["btn{}{}".format(x+i,y)]['text']==current_turn:
                wincheck+=1
        except:
            pass
    if wincheck>=2:
        onWin(current_turn)
    print("horwin?",wincheck)
    #check vertical
    wincheck=0
    for i in [-2,-1,1,2]:
        try:
            if buttons["btn{}{}".format(x,y+i)]['text']==current_turn:
                wincheck+=1
        except:
            pass
    if wincheck>=2:
        onWin(current_turn)
    print("verwin?",wincheck)
    #check forward diagonal
    wincheck=0
    for i in [-2,-1,1,2]:
        try:
            if buttons["btn{}{}".format(x+i,y+i)]['text']==current_turn:
                wincheck+=1
        except:
            pass
    if wincheck>=2:
        onWin(current_turn)
    print("fdiagwin?",wincheck)   
    #check backward diagonal
    wincheck=0
    for i in [-2,-1,1,2]:
        try:
            if buttons["btn{}{}".format(x-i,y+i)]['text']==current_turn:
                wincheck+=1
        except:
            pass    
    if wincheck>=2:
        onWin(current_turn)
    print("bdiagwin?",wincheck)
        
def clicked(x,y, current_button):
    global current_turn
    global message
    global lbl

    if current_button['text'] == "":
        current_button['text']=current_turn
        print("button clicked:", x,y)
        check_win(x,y)
        if current_turn == 'x':
            current_turn = 'o'
        else:
            current_turn = 'x'

    if isWin == False:    
        message = '{} to play next!'.format(current_turn)
        lbl["text"]= message

def ResetBoard():
    global message
    global lbl
    global buttons
    global isWin
    
    for btn in buttons.keys():
        buttons[btn]["text"]=""
        buttons[btn]["state"]="normal"
    message='x to go first!'
    lbl["text"]= message
    isWin=False

def onWin(player):
    global message
    global lbl
    global isWin
    global buttons
    
    isWin=True
    message='{} wins!'.format(player)
    lbl["text"]=message
    for btn in buttons.keys():
        buttons[btn]["state"]="disabled"

# generate all the buttons for the board and resetting the game:
buttons = {}
for x in range(3):
    for y in range(3):
        buttons["btn{}{}".format(x,y)]= Button(root, text = "" , fg = "red")
        current_button=buttons["btn{}{}".format(x,y)]
        current_button.configure(command=lambda btn=current_button,xx=x,yy=y: clicked(xx,yy,btn))
        # set Button grid
        current_button.grid(column=x, row=y)
        
Reset_button = Button(root, text = "Reset" , fg = "black", command=lambda: ResetBoard())
Reset_button.grid(column=4, row=2)
# Execute Tkinter
root.mainloop()
