import pygame, sys
from pygame.locals import *
from random import randrange
from itertools import cycle
import time

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((800, 300))
screen.fill(BLACK)
pygame.display.set_caption("BlackBoard")
bg = pygame.image.load('bg.jpg')
positionArray = list(range(9))
doneArrayO = []
doneArrayX = []
it = 0
running = True
board = [[None, None, None], [None, None, None], [None, None, None]]
restring = "Status"
stop = False
user = None

pygame.draw.line(screen, WHITE, (0,100), (300,100), 5)
pygame.draw.line(screen, WHITE, (0,200), (300,200), 5)
pygame.draw.line(screen, WHITE, (100,0), (100,300), 5)
pygame.draw.line(screen, WHITE, (200,0), (200,300), 5)
pygame.draw.line(screen, WHITE, (300,0), (300,300), 5)
pygame.draw.line(screen, WHITE, (0,300), (300,300), 5)
screen.blit(bg, (300, 0))

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('TicTacToe', True, WHITE, BLACK)
textRect = text.get_rect()
textRect.center = (500,100)
screen.blit(text, textRect)

fontsub = pygame.font.Font('freesansbold.ttf', 16)
textsub = fontsub.render('Computer O | Player X', True, WHITE, BLACK)
textRectsub = textsub.get_rect()
textRectsub.center = (500,130)
screen.blit(textsub, textRectsub)

def displayBoard(board):
    for i in board:
        print(i)

def getComputerInput():
    return randrange(0, 9)

def isPositionAvailable(position):
    return position in positionArray

def getIndexLocation(position):
    row = position//3
    coloumn = position%3
    return (row,coloumn)

def getCenter(row, col):
    x1 = col*100
    y1 = (row+1)*100
    x2 = (col+1)*100
    y2 = row*100

    cx = (x1+x2)//2
    cy = (y1+y2)//2
    return (cx,cy)

def drawCircle(position):
    pos = getIndexLocation(position)
    pygame.draw.circle(screen, (255, 255, 255), getCenter(pos[0], pos[1]), 30, 2)
    board[pos[0]][pos[1]] = 'O'

def getPosition(x,y):
    if(y <= 100):
        if(x <= 100):
            return 0
        if (x <= 200):
            return 1
        if (x <= 300):
            return 2
    if (y <= 200):
        if (x <= 100):
            return 3
        if (x <= 200):
            return 4
        if (x <= 300):
            return 5
    if (y <= 300):
        if (x <= 100):
            return 6
        if (x <= 200):
            return 7
        if (x <= 300):
            return 8


def rowCrossed(board):
    for i in range(3):
        if(board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != None):
            pygame.draw.line(screen, WHITE, getCenter(i,0), getCenter(i,2), 3)
            return True

    return False

def columnCrossed(board):
    for i in range(3):
        if (board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != None):
            pygame.draw.line(screen, WHITE, getCenter(0,i), getCenter(2,i), 3)
            return True

    return False

def diagonalCrossed(board):
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != None):
        pygame.draw.line(screen, WHITE, getCenter(0, 0), getCenter(2, 2), 3)
        return True

    if (board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != None):
        pygame.draw.line(screen, WHITE, getCenter(0, 2), getCenter(2, 0), 3)
        return True

    return False

def isAny(board):
    return (rowCrossed(board) or columnCrossed(board) or diagonalCrossed(board))

def drawText(iptext):
    screen.fill(pygame.Color("black"), (380, 160, 250, 20))
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render(iptext, True, WHITE)

    textRect = text.get_rect()
    textRect.center = (500, 170)

    screen.blit(text, textRect)

def mouseDraw():
    last_pos = None
    mouse_position = (0, 0)
    drawing = False
    running = True
    req = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if(event.key==pygame.K_RETURN):
                    running = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == MOUSEMOTION:
                if (drawing):
                    mouse_position = pygame.mouse.get_pos()
                    if (mouse_position[0] < 300 and mouse_position[1] < 300):
                        if last_pos is not None:
                            pygame.draw.line(screen, WHITE, last_pos, mouse_position, 3)
                        last_pos = mouse_position
            elif event.type == MOUSEBUTTONUP:
                mouse_position = (0, 0)
                drawing = False
                req = last_pos
                last_pos = None
            elif event.type == MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if(mouse_position[0]<300 and mouse_position[1]<300):
                    drawing = True

        pygame.display.update()

    return req

def main():
    global it, restring, running, stop

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if(running and len(positionArray)!=0 and not stop):
            if (it % 2 == 0):
               user = "computer"
               flag = True
               while (flag):
                    drawText("Now, Computer's turn")
                    pygame.display.update()
                    time.sleep(1.5)
                    userInputPosition = getComputerInput()
                    flag = not isPositionAvailable(userInputPosition)
                    if (flag):
                        # print("Location Already Occupied")
                        continue
                    else:
                        print("Computer position " + str(userInputPosition))
                        # pygame.time.delay(2000)
                        drawCircle(userInputPosition)
                        doneArrayO.append(userInputPosition)
                        positionArray.remove(userInputPosition)
                        if(isAny(board)):
                            restring = "Computer Won"
                            print(restring)
                            stop = True
                            # running = False

                        # print("positionArray " + str(positionArray))
                        # print("doneArrayO " + str(doneArrayO))
                        # print("----------xxxxxxxxxx----------")
            else:
                user = "player"
                flag = True
                while (flag):
                    drawText("Now, Your turn")
                    pygame.display.update()
                    mos = mouseDraw()
                    userInputPosition = getPosition(mos[0], mos[1])
                    rctuple = getIndexLocation(userInputPosition)
                    flag = not isPositionAvailable(userInputPosition)
                    if (flag):
                        # print("Location Already Occupied")
                        continue
                    else:
                        print("User position " + str(userInputPosition))
                        board[rctuple[0]][rctuple[1]] = 'X'
                        doneArrayX.append(userInputPosition)
                        positionArray.remove(userInputPosition)
                        if (isAny(board)):
                            restring = "Player Won"
                            print(restring)
                            stop = True
                            # running = False

                        # print("positionArray " + str(positionArray))
                        # print("doneArrayX " + str(doneArrayX))
                        # print("----------xxxxxxxxxx----------")

            print("positionArray " + str(positionArray))
            print("doneArrayO " + str(doneArrayO))
            print("doneArrayX " + str(doneArrayX))
            displayBoard(board)
            print("----------xxxxxxxxxx----------")
            it+=1
        else:
            if not stop:
                restring = "Match drawn"
            else:
                if(user == "player"):
                    restring = "Player won"
                else:
                    restring = "Computer won"
            # running = False
            screen.fill(pygame.Color("black"), (380, 160, 250, 20))
            drawText(restring)
            # print(restring)
        pygame.display.update()

if __name__ == "__main__":
    main()