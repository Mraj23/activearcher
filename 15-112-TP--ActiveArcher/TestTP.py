#################################################
# Term Project - Raj Mehta (rajm)
# Your andrew id: rajm
#################################################

import cv2
import math, copy, random
import numpy as np
from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import os
import csv

#################################################
#Citations:

#15-112 Website
#Animations:
    # 1) https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    # 2) https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

#Classes Part 2: https://www.cs.cmu.edu/~112/notes/notes-oop-part2.html

# Programming Knowledge OpenCV tutorial youtube
#https://www.youtube.com/watch?v=kdLM6AOd2vc

#Font:
#https://www.dafont.com/guardians.font

#Backgrounds:
#Opening Screen and Game: https://www.wallpaperflare.com/
#Cailbartion Screen: http://getwallpapers.com/collection/fantasy-space-art-wallpaper
#Ready Screen: https://www.pinterest.com/pin/247557310746812366/

# from: https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def readFile(path):
    with open(path, "rt") as f:
        return f.read()


#################################################

class OpeningScreenMode(Mode):

    def appStarted(mode):
        mode.background1 = mode.loadImage('bg.jpg')
        mode.background = mode.scaleImage(mode.background1, 1/3)
        mode.title1 = mode.loadImage('title.png')
        mode.title = mode.scaleImage(mode.title1, 1/3)
        mode.start1 = mode.loadImage('start.png')
        mode.start = mode.scaleImage(mode.start1, 1/3)
        mode.instructions1 = mode.loadImage('instructions1.png')
        mode.instructions = mode.scaleImage(mode.instructions1, 1/3)
        mode.leaderboards1 = mode.loadImage('leaderboards.png')
        mode.leaderboards = mode.scaleImage(mode.leaderboards1, 1/3)
    
    def mousePressed(mode, event):
        print(event.x, event.y)   
        if event.x - 100 < mode.width/2 and event.x + 100 > mode.width/2 and event.y + 100 >mode.height*(2/5) and event.y - 100 < mode.height*(2/5):
            mode.app.setActiveMode(mode.app.calibrate)
        if event.x - 100 < mode.width/2 and event.x + 100 > mode.width/2 and event.y + 100 >mode.height*(3/5) and event.y - 100 < mode.height*(3/5):
            mode.app.setActiveMode(mode.app.instructions)
        if event.x - 100 < mode.width/2 and event.x + 100 > mode.width/2 and event.y + 100 >mode.height*(4/5) and event.y - 100 < mode.height*(4/5):
            mode.app.setActiveMode(mode.app.leaderBoards)

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.background))
        canvas.create_image(mode.width/2, mode.height/5, image=ImageTk.PhotoImage(mode.title))
        canvas.create_image(mode.width/2, mode.height*(2/5), image=ImageTk.PhotoImage(mode.start))
        canvas.create_image(mode.width/2, mode.height*(3/5), image=ImageTk.PhotoImage(mode.instructions))
        canvas.create_image(mode.width/2, mode.height*(4/5), image=ImageTk.PhotoImage(mode.leaderboards))


    def keyPressed(mode, event):
        if (event.key == "e"):
            mode.app.setActiveMode(mode.app.calibrate)
        if (event.key == "l"):
            mode.app.setActiveMode(mode.app.leaderBoards)
        if (event.key == "i"):
            mode.app.setActiveMode(mode.app.instructions)
        if (event.key == "s"):
            mode.app.setActiveMode(mode.app.game)
        if (event.key == "x"):
            mode.app.setActiveMode(mode.app.gameOver)

class ReadyMode(Mode):
    def appStarted(mode):
        mode.bg1 =  mode.background1 = mode.loadImage('spaceshipbg1.jpg')
        mode.bg = mode.scaleImage(mode.bg1, 1)


    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.bg))
        #canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'Light Pink')
        canvas.create_text(mode.width/2, mode.height/2, text = "Are You Ready?", font = "Guardians 25 bold", fill = "Blue")
        canvas.create_text(mode.width/2, mode.height*(2/3), text = "Press B to go Continue", font = "Guardians 18 bold", fill = "Blue")
    
    def keyPressed(mode, event):
        if (event.key == "b"):
            mode.app.setActiveMode(mode.app.game)


class LeaderBoardsMode(Mode):
    
    def appStarted(mode):
        mode.selectionSort()
        lenL = len(mode.finalList)
        mode.pos5 = mode.finalList[lenL-1]
        mode.pos4 = mode.finalList[(lenL-2)]
        mode.pos3 = mode.finalList[(lenL-3)]
        mode.pos2 = mode.finalList[(lenL-4)]
        mode.pos1 = mode.finalList[(lenL-5)]


        
    
    def leaderboardList(mode, files):
        
        LBList = []
        newRow = []        
        for row in readFile(files).strip().split('\n'): 
            LBList.append(row.split(","))        
        print(LBList)
        return LBList

    def cleanList(mode, data):
        L = data
        Lcopy = []
        for i in range((len(L))):
            if (i+1)%2 == 0:
                Lcopy.append(L[i])           
        return Lcopy

    def convert2int(mode, data):
        L = data
        for i in L:
            i[1] = int(i[1])
        return L

    def mergeFunction(mode):
        data = mode.leaderboardList('LeaderBoards.csv')
        cleanData = mode.cleanList(data)
        converted = mode.convert2int(cleanData)
        print(converted)
        return converted

    def swap2(mode, a, i, j):
        (a[i][1], a[j][1]) = (a[j][1], a[i][1])

    def swap3(mode, a, i, j):
        (a[i][0], a[j][0]) = (a[j][0], a[i][0])

    def selectionSort(mode):
        
        a = mode.mergeFunction()
        n = len(a)
        for startIndex in range(n):
            minIndex = startIndex
            for i in range(startIndex+1, n):
                if (a[i][1] < a[minIndex][1]):
                    minIndex = i
            mode.swap2(a, startIndex, minIndex)
            mode.swap3(a, startIndex, minIndex)
        mode.finalList = a
        return mode.finalList

   
    
    ''''def leaderboardList():
        LBList = []
        newRow = []
        for row in readFile('LeaderBoards.csv').strip().split('\n'): 
            LBList.append(row.split(","))
        return LBList'''

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'Orange')
        canvas.create_text(mode.width/2, mode.height/8, text = "Leader Boards", font = "Guardians 12 bold", fill = "red")
        
        canvas.create_text(mode.width*(1/5), mode.height*(2/8), text = f'{mode.pos5[0]}', font = "Guardians 12 bold", fill = "red")
        canvas.create_text(mode.width*(4/5), mode.height*(2/8), text = f'{mode.pos5[1]}', font = "Guardians 12 bold", fill = "red")
        
        canvas.create_text(mode.width*(1/5), mode.height*(3/8), text = f'{mode.pos4[0]}', font = "Guardians 12 bold", fill = "red")
        canvas.create_text(mode.width*(4/5), mode.height*(3/8), text = f'{mode.pos4[1]}', font = "Guardians 12 bold", fill = "red")
        
        canvas.create_text(mode.width*(1/5), mode.height*(4/8), text = f'{mode.pos3[0]}', font = "Guardians 12 bold", fill = "red")
        canvas.create_text(mode.width*(4/5), mode.height*(4/8), text = f'{mode.pos3[1]}', font = "Guardians 12 bold", fill = "red")
        
        canvas.create_text(mode.width*(1/5), mode.height*(5/8), text = f'{mode.pos2[0]}', font = "Guardians 12 bold", fill = "red")
        canvas.create_text(mode.width*(4/5), mode.height*(5/8), text = f'{mode.pos2[1]}', font = "Guardians 12 bold", fill = "red")
        
        canvas.create_text(mode.width*(1/5), mode.height*(6/8), text = f'{mode.pos1[0]}', font = "Guardians 12 bold", fill = "red")
        canvas.create_text(mode.width*(4/5), mode.height*(6/8), text = f'{mode.pos1[1]}', font = "Guardians 12 bold", fill = "red")

        canvas.create_text(mode.width/2, mode.height*(7/8), text = "Press B to go Back", font = "Guardians 12 bold", fill = "red")

    def keyPressed(mode, event):
        if (event.key == "b"):
            mode.app.setActiveMode(mode.app.openingScreen)


class InstructionsMode(Mode):
    def appStarted(mode):
        mode.image = mode.loadImage('Instructions.png')
        mode.image2 = mode.scaleImage(mode.image, 60/99)

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.image2))
        
    def keyPressed(mode, event):
        if (event.key == "b"):
            mode.app.setActiveMode(mode.app.openingScreen)

class CalibrationMode(Mode):
    def appStarted(mode):
        mode.bg1 =  mode.background1 = mode.loadImage('spacebg.jpg')
        mode.bg = mode.scaleImage(mode.bg1, 1/2)
        mode.capture = cv2.VideoCapture(0)
        mode.ret, mode.frame = mode.capture.read()
        cv2.namedWindow('mouseRGB')

    #Controller of the game
    def keyPressed(mode, event):
        if (event.key == "k"):
            mode.app.setActiveMode(mode.app.ready)
            mode.capture.release()
            cv2.destroyAllWindows()
        
    def mouseRGB(mode,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
            blue = mode.frame[y,x,0]
            green = mode.frame[y,x,1]
            red = mode.frame[y,x,2]
            colors = mode.frame[y,x]
            temp = np.uint8([[[int(blue), int(green), int(red)]]])
            HSV = cv2.cvtColor(temp, cv2.COLOR_BGR2HSV)
            print(temp)
            mode.app.H.add(HSV[0][0][0])
            mode.app.S.add(HSV[0][0][1])
            mode.app.V.add(HSV[0][0][2])
            print(HSV)
            print(mode.app.H, mode.app.S, mode.app.V)
            
    def timerFired(mode):
        cv2.putText(mode.frame,'Click the paddle in different lightings and press k to begin', (0,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0),1) 
        mode.ret, mode.frame = mode.capture.read()
        cv2.putText(mode.frame,'Click the paddle in different lightings and press k to begin', (0,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0),1)
        cv2.imshow('mouseRGB', mode.frame)
        cv2.setMouseCallback('mouseRGB', mode.mouseRGB)
        
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.bg))
        #canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'Light Green')
        canvas.create_text(mode.width/2, mode.height/2, text = 'Calibrate Your Device', font = "Guardians 14 bold", fill = "black")
        canvas.create_text(mode.width/2, mode.height*(4/5), text = 'Press K When Ready to Start the Game', font = "Guardians 14 bold", fill = "black")


class GameMode(Mode):
    
    def appStarted(mode):
        mode.bg1 = mode.loadImage('desertbg.jpg')
        mode.bg = mode.scaleImage(mode.bg1,8/9)
        mode.playerImage1 = mode.loadImage('yondu.jpg')
        mode.playerImage = mode.scaleImage(mode.playerImage1, 1/6)
        mode.handImage1 = mode.loadImage('Bow.png')
        mode.handImage = mode.scaleImage(mode.handImage1, 1/6)
        mode.Arrow1 = mode.loadImage('Arrow.png')
        mode.playerX = 800
        mode.playerY = 600
        mode.Arrow = mode.scaleImage(mode.Arrow1, 1/5)   
        mode.capture = cv2.VideoCapture(0)
        mode.ret, mode.frame1 = mode.capture.read()
        cv2.namedWindow('game')
        mode.L = [0,0]   
        mode.i = 0
        mode.x1 = 10
        mode.x2 = 5
        mode.y1 = 5
        mode.y2 = 10
        mode.rDistance = ((mode.x1-mode.x2)**2-(mode.y1-mode.y2)**2)**0.5    
        mode.theta = math.atan((mode.y2-mode.y1)/(mode.x2-mode.x1))
        mode.rDistanceCalib = mode.rDistance/7
        mode.power = mode.rDistanceCalib*math.sin(mode.theta)
        mode.rcos = mode.rDistanceCalib*math.cos(mode.theta)
        mode.count = 0
        mode.r = 10
        mode.x = 780 
        mode.y = 600
        mode.dx = mode.rcos
        mode.dy = -mode.power
        mode.gravity = 4
        mode.newArrow = False
        mode.timeShoot = 0
        mode.static = True
        mode.angle = 0
        mode.angleTime = 0
        mode.angleIncrement = 0
        mode.arrowRotate = mode.Arrow.rotate(mode.angle)
        mode.enemyImage1 = mode.loadImage('enemy3.png')
        mode.enemyImage = mode.scaleImage(mode.enemyImage1, 5/8)
        mode.enemyList = []
        mode.gameStart = True
        mode.explosion = False
        mode.bombCount = 0
        mode.bombImage1 = mode.loadImage('explosion.png')
        mode.bombImage = mode.scaleImage(mode.bombImage1, 1/4)
        mode.bombX = 0
        mode.bombY = 0
        mode.projectiles = []
        mode.fireball1 =  mode.loadImage('fireball.png')
        mode.fireball = mode.scaleImage(mode.fireball1,1/5)
        mode.health0 = 50
        mode.health = 50
        mode.dodgeY = 0
        mode.dodgePos = mode.playerY - mode.dodgeY
        
        
    
    def moveArrow(mode):
        if mode.static == False:
            mode.dy += mode.gravity 
            mode.x = mode.x - mode.dx
            mode.y = mode.y + mode.dy
            mode.angle += (mode.angleIncrement)
            mode.arrowRotate = mode.Arrow.rotate(mode.angle)
        
    def shootProjectile(mode):
        for e in mode.enemyList:
                rand = random.randint(1,120)
                if rand == 2:
                    newProjectile = Projectile(e.x+45, e.y-60)
                    mode.projectiles.append(newProjectile)
    

    def keyPressed(mode, event):
        if (event.key == "f"):
            mode.capture.release()
            cv2.destroyAllWindows()
        if (event.key == "h"):
            mode.explosion = True
        if (event.key == 'x'):
            for e in mode.enemyList:
                rand = random.randint(1,3)
                if rand == 2:
                    newProjectile = Projectile(e.x+45, e.y-60)
                    mode.projectiles.append(newProjectile)
        
    
    def placeEnemy(mode):
        
        chanceSpawn = random.randint(1,12)
        a = random.randint(100, mode.width/2)
        b = random.randint(100, mode.height-100)
        for e in mode.enemyList:
            if a + 150 > e.posX[0] and a - 150 < e.posX[1] and b + 150 > e.posY[0] and b - 150 < e.posY[1]:
                return
        if chanceSpawn == 5 and Enemy.EnemyCount < 3:
            newEnemy = Enemy(a,b)
            mode.enemyList.append(newEnemy)


        
    def checkHit(mode):
        for e in mode.enemyList:
            if mode.x > e.posX[0] and mode.x < e.posX[1] and mode.y > e.posY[0] and mode.y < e.posY[1]:
                mode.bombX = e.x
                mode.bombY = e.y
                mode.explosion = True
                mode.enemyList.remove(e)
                Enemy.EnemyCount -= 1
                mode.x = 900
                mode.y = 900
                mode.app.score += 1
    
    def killPlayer(mode):     
        for p in mode.projectiles:
            if p.x > mode.playerX - 100 and p.x < mode.playerX + 100 and p.y > mode.dodgePos - 100 and p.y < mode.dodgePos + 100:
                mode.health -= 1
                print(f'Ur Health: {mode.health}')

    def endGame(mode):
        if mode.health < 1:
            mode.gameStart = False
            mode.app.setActiveMode(mode.app.gameOver)
            cv2.destroyAllWindows()
            mode.capture.release()
            


    def timerFired(mode):
        mode.endGame()        
        mode.ProjectileMove()
        mode.killPlayer()
        
        if mode.newArrow == True:
            mode.timeShoot += 1
            mode.static = True
            if mode.timeShoot == 25:
                mode.static = False
                mode.timeShoot = 0
                mode.count = 0
                mode.angle = -mode.theta*(180/math.pi)
                mode.dy = -mode.power
                mode.dx = mode.rcos
                mode.y = 600
                mode.x = 750
                mode.angleTime = mode.power/mode.gravity
                mode.angleIncrement = (mode.theta/mode.angleTime)*(180/math.pi)
                mode.arrowRotate = mode.Arrow.rotate((mode.theta)*180/math.pi)
                mode.newArrow = False
       
        mode.moveArrow()
        mode.placeEnemy()
        mode.checkHit()
        mode.shootProjectile()

        if mode.explosion == True:
            mode.bombCount += 1
            if mode.bombCount == 6:
                mode.bombCount = 0
                mode.explosion = False
            

        cv2.imshow('game', mode.frame1)
        mode.ret, mode.frame1 = mode.capture.read()
        if mode.gameStart == True:

            hsv = cv2.cvtColor(mode.frame1, cv2.COLOR_BGR2HSV)
            blur = cv2.GaussianBlur(hsv, (5,5), 0)
            #Same bounds from previous function
            
            #INSERT SLIDER VALUES#

            #lower_bound = np.array([0, min(mode.app.S), min(mode.app.V)])
            #upper_bound = np.array([255, max(mode.app.S), max(mode.app.V)])
            upper_bound = np.array([255,255,255])
            lower_bound = np.array([0,170,102])
            
           
            
            mask = cv2.inRange(blur, lower_bound, upper_bound)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            
                
            #These sets of lines that identify countours around desired object
            #_, thresh = cv2.threshold(mask, 20, 255, cv2.THRESH_BINARY)
            #dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                #Created a list to add the coordinates of the two paddles
            mode.L = [0,0]   
            mode.i = 0
                #Appends contours to list, prevents more than two objects from being detected
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                if cv2.contourArea(contour) < 1000 :
                    continue
                if mode.i > 1:
                    mode.i = 1
                mode.L[mode.i] = (x,y)
                mode.i += 1
                    #Draws shapes around paddles and tells us if we need to reposition them
                cv2.rectangle(mode.frame1, (x,y), (x+w, y+h), (255,0,0), 2)
                cv2.putText(mode.frame1, f'C {x},{y}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
            if mode.L[0] == 0 or mode.L[1]  == 0:
                cv2.putText(mode.frame1, f'Reposition Paddles', (10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)        
                

                #Convert x,y coordinates of paddles into polar coordiantes
            if type(mode.L[0]) == tuple and type(mode.L[1]) == tuple:
                mode.x1 = mode.L[0][0]
                mode.y1 = mode.L[0][1]
                mode.x2 = mode.L[1][0]
                mode.y2 = mode.L[1][1]
                mode.rDistance = ((mode.x1-mode.x2)**2+(mode.y1-mode.y2)**2)**0.5
                mode.dodge()
                #if #abs(mode.x1-mode.x2) < 100 or abs(mode.y1-mode.y1) < 100:
                if mode.rDistance < 150:
                    print('NewArrow')
                    mode.newArrow = True
                    if mode.newArrow == True:
                        print(mode.newArrow == True)
                if (mode.x2 - mode.x1) < 0.00001:
                    mode.theta = math.pi/2
                mode.theta = math.atan((mode.y2-mode.y1)/(mode.x2-mode.x1))
                mode.theta = abs(mode.theta)*2
                mode.rDistanceCalib = mode.rDistance/4
                mode.power = abs(mode.rDistanceCalib*math.sin(mode.theta))
                
                mode.rcos = mode.rDistanceCalib*math.cos(mode.theta)
            
            

           # print(mode.rDistance)
            #print((mode.theta*180/math.pi))
    def dodge(mode):
        mode.dodgeY = 30000*(1/mode.L[1][1])
        mode.dodgePos = (mode.playerY - mode.dodgeY)
        
        
    def redrawAll(mode, canvas):
        
        #canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'Orange')
        canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.bg))
        canvas.create_image(mode.playerX, mode.dodgePos, image=ImageTk.PhotoImage(mode.playerImage))
        
        
        for enemy in mode.enemyList:
            canvas.create_image(enemy.x, enemy.y, image=ImageTk.PhotoImage(mode.enemyImage))

        if mode.static == False:
            canvas.create_image(mode.x, mode.y, image=ImageTk.PhotoImage(mode.arrowRotate))
        
        if mode.static == True:
            #canvas.create_oval(mode.x-mode.r, mode.y-mode.r, mode.x+mode.r, mode.y+mode.r,
             #              fill='red')
            #canvas.create_oval(750-mode.r, 600-mode.r, 750+mode.r, 600+mode.r,
             #              fill='red')
            canvas.create_image(750, 600, image=ImageTk.PhotoImage(mode.Arrow.rotate(-mode.theta*180/math.pi)))
        
        canvas.create_text(mode.width/2, 50, text = f'Score: {mode.app.score}', font = "Guardians 12", fill = "black")
        
        if mode.explosion == True:
            canvas.create_image(mode.bombX, mode.bombY, image=ImageTk.PhotoImage(mode.bombImage))
        
        for p in mode.projectiles:
            canvas.create_oval(p.x - 10, p.y - 10, p.x + 10, p.y + 10, fill = 'red')
            canvas.create_image(p.x, p.y, image=ImageTk.PhotoImage(mode.fireball))

        #canvas.create_text(mode.width/2, 50, text = f'Score: {mode.app.score}', font = "Guardinas 12 bold", fill = "black")
        canvas.create_text(mode.width*(9/10) - 50, 50, text = 'Health', font = "Guardians 12 bold", fill = "black")
        canvas.create_line(mode.width*(9/10) - 100, mode.height*(1/10), mode.width*(9/10), mode.height*(1/10), fill = 'Red', width = 10)        
        canvas.create_line(mode.width*(9/10) - 100, mode.height*(1/10), mode.width*(9/10) - 100 + 100*(mode.health/mode.health0), mode.height*(1/10), fill = 'Green', width = 10)        
        canvas.create_text(mode.width*(9/10) - 50, mode.height*(2/10)- 25, text = 'Power', font = "Guardians 12 bold", fill = "black")
        canvas.create_line(mode.width*(9/10) - 100, mode.height*(2/10), mode.width*(9/10), mode.height*(2/10), fill = 'Grey', width = 10)        
        canvas.create_line(mode.width*(9/10) - 100, mode.height*(2/10), mode.width*(9/10) - 100 + 100*(mode.power/100), mode.height*(2/10), fill = 'Blue', width = 10)
    
    def ProjectileMove(mode):
        for p in mode.projectiles:
            p.dy += 3
            p.x = p.x + p.dx
            p.y = p.y + p.dy


class GameOver(Mode):

    
    def appStarted(mode):
        mode.name = ''
        mode.name = mode.getUserInput("Enter your Name")
        contentsToWrite = str(mode.name)
        with open("LeaderBoards.csv", "a") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([mode.name, mode.app.score])

            
        
    
    
    

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'Red')
        canvas.create_text(mode.width/2, mode.height/4, text = "Game Over!", font = "Guardians 18 bold", fill = "red")
        canvas.create_text(mode.width/2, mode.height*(2/4), text = f'Your Score Was: {mode.app.score}', font = "Guardians 12 bold", fill = "black")
        #canvas.create_text(mode.width/2, mode.height*(3/4), text = f'Enter your name {mode.app.score}', font = "Arial 12 bold", fill = "black")
        canvas.create_text(mode.width/2, mode.height*(3/4), text = f'Press B to Go Back', font = "Guardians 12 bold", fill = "black")



    def keyPressed(mode, event):
        if (event.key == "b"):
            mode.app.setActiveMode(mode.app.openingScreen)
        if (event.key == "x"):
            mode.health = 2


class Enemy(object):
    EnemyCount = 0
  
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.alive = True
        self.posX = (self.x - 30, self.x + 30)
        self.posY = (self.y - 70, self.y + 70)
        Enemy.EnemyCount += 1

class Projectile(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = random.randint(3,6)
        self.angle = random.randint(5,10)
        self.dx = 5*self.r*math.cos(self.angle*(math.pi/180))
        self.dy = -(1/2)*(self.y*math.sin(self.angle*(math.pi/180))) 


class ModalApp(ModalApp):
    def appStarted(app):
        app.openingScreen = OpeningScreenMode()
        app.leaderBoards = LeaderBoardsMode()
        app.calibrate = CalibrationMode()
        app.instructions = InstructionsMode()
        app.ready = ReadyMode()
        app.game = GameMode()
        app.gameOver = GameOver()
        app.setActiveMode(app.openingScreen)
        (app.H, app.S, app.V) = (set(),set(),set())
        app.score = 0
    
        



    
app = ModalApp(width=900, height=700) 

