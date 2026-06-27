#Worm Game Project by:
#242030108 Ibrahim Gambo
#242030002 Farouk Babagana Mustapha
#242030081 Ibrahim Ayomide Folorunsho
#242030048 Faozan Oladimeji Oseni
#242030009 Fuad Alaba


import random
from tkinter import *


GAME_RUNNING = False
GAME_OVER_STATE = False
GAME_HEIGHT = 800
GAME_WIDTH = 800
SPEED = 120
BODY_PARTS = 2
SPACE_SIZE = 50
WORM_COLOR = "#EEDEC5"
FOOD_COLOR = "#FF474C"
BACKGROUND_COLOR = "#9D6C3C"

class Worm:
    def __init__(self):
        self.bodySize = BODY_PARTS
        self.squares = []
        self.coordinates = []
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for xPos, yPos in self.coordinates:
            square = canvas.create_rectangle(xPos, yPos, xPos + SPACE_SIZE, yPos + SPACE_SIZE, fill=WORM_COLOR, tag="worm")
            self.squares.append(square)

class Food:
    def __init__(self):
        # the number of spaces food can spawn on is the width (x) or height(y) divided by the space size of the game, # the -1 is because 0 itself is a position, # multiplying by space size gives position in pixels
        xPos = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE 
        yPos = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE 
        self.coordinates = [xPos, yPos]
        canvas.create_rectangle(xPos, yPos, xPos + SPACE_SIZE, yPos + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def startGame(event):
    global GAME_RUNNING, GAME_OVER_STATE
    if GAME_OVER_STATE:
        restartGame()
        return
    
    if not GAME_RUNNING:
        GAME_RUNNING = True
        nextTurn(worm, food)

grow = False
directionChanged = False

def nextTurn(worm, food):
    global directionChanged, grow

    if not GAME_RUNNING:
        return

    directionChanged = False
    xPos, yPos = worm.coordinates[0]
    if facingDirection == "up":
        yPos -= SPACE_SIZE
    elif facingDirection == "down":
        yPos += SPACE_SIZE
    elif facingDirection == "left":
        xPos -= SPACE_SIZE
    elif facingDirection == "right":
        xPos += SPACE_SIZE
    
    worm.coordinates.insert(0, (xPos, yPos))
    square = canvas.create_rectangle(xPos, yPos, xPos + SPACE_SIZE, yPos + SPACE_SIZE, fill=WORM_COLOR)
    worm.squares.insert(0, square)
    
    if xPos == food.coordinates[0] and yPos == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()

    else:
        if grow == False:
            del worm.coordinates[-1] #remove the last part of the snake
            canvas.delete(worm.squares[-1])
            del worm.squares[-1]
        else:
            grow = False
    if checkCollisions(worm):
        gameOver()
    else:
        window.after(SPEED, nextTurn, worm, food)


def changeDirection(newDirection):
    global facingDirection, directionChanged

    if directionChanged:
        return
    if newDirection == 'left':
        if facingDirection != 'right':
            facingDirection = newDirection
    elif newDirection == 'up':
        if facingDirection != 'down':
            facingDirection = newDirection
    elif newDirection == 'right':
        if facingDirection != 'left':
            facingDirection = newDirection
    elif newDirection == 'down':
        if facingDirection != 'up':
            facingDirection = newDirection
    directionChanged = True

def checkCollisions(worm):
    xPos, yPos = worm.coordinates[0]
    if xPos < 0 or xPos >= GAME_WIDTH:
        return True
    elif yPos < 0 or yPos >= GAME_HEIGHT:
        return True
    
    for bodyPart in worm.coordinates[1:]:  # for every body part in the worm after the head, if the xposition of the head is equal to the  
        if xPos == bodyPart[0] and yPos == bodyPart[1]:
            return True
    return False

def gameOver():
    global GAME_RUNNING, GAME_OVER_STATE
    GAME_RUNNING = False
    GAME_OVER_STATE = True

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,
                      canvas.winfo_height()/2,
                      font=('papyrus', 40), text="GAME OVER\nPress Enter to try again.",
                        fill="bisque", tag="gameOver")

def restartGame():
    global worm, food, score, facingDirection, GAME_OVER_STATE
    canvas.delete(ALL)
    score = 0
    label.config(text="Score: 0")
    facingDirection = "right"
    worm = Worm()
    food = Food()
    GAME_OVER_STATE = False
    nextTurn(worm, food)

def up(event):
    changeDirection('up')
def down(event):
    changeDirection('down')
def left(event):
    changeDirection('left')
def right(event):
    changeDirection('right')
def eat(event):
    global grow
    grow = True
def speedUp(event):
    global SPEED
    SPEED = SPEED - 20
def slowDown(event):
    global SPEED
    SPEED = SPEED + 20


window = Tk()
window.title("Worm")

score = 0
facingDirection = "right"

label = Label(window, text="Score:{}".format(score), font=('papyrus', 20))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update_idletasks()
windowWidth = window.winfo_width()
windowHeight = window.winfo_height()
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

xPos = (screenWidth - windowWidth) // 2
yPos = (screenHeight - windowHeight) // 2
window.geometry(f"{windowWidth}x{windowHeight}+{xPos}+{yPos}")
worm = Worm()
food = Food()


window.bind('<Up>', up)
window.bind('<Down>', down)
window.bind('<Left>', left) 
window.bind('<Right>', right)
window.bind('<z>', eat)
window.bind('<x>', speedUp)
window.bind('<c>', slowDown)
window.bind('<Return>', startGame)

window.mainloop()