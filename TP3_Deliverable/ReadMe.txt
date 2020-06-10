README before starting the game.

Term Project Deliverable 3 - Raj Mehta


Project Name: Active Archer
Project Description: Using your computer webcam, you use two paddles in your hands and
imitate the movements of an archer to control an arrow that hits enemies. The goal of the game
is to shoot as many enemies as possible without being shot at by the enemies.

yt link: https://youtu.be/sF_LzRn_sfY

Click on the file FINALTERMPROJECT to start the game. The game requires you to have all the listed modules:
import cv2
import math, copy, random
import numpy as np
from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import os
import csv

Also make sure that the font is downloaded. Do this by either opening the file 'Guardians.tiff' or the DOWNLOADFONT file.


Note about the paddles and camera detection:

Currently the game works in detecting bright colored paddles that are distinct from their surroundings. 
The paddles you use also have to be the same colour. Ideally they should be different to what you are wearing.
I have noticed that bright yellow and red paddles work best. Make sure you do not play in a very reflective environment too.
The red side of ping pong paddles have worked for me. If you see that your webcam is constantly trying to adjust to the lighting, then the game will not work.
The lighting conditions have to be quite constant and there should not be concentrated sources of light in the view of the webcam.

Also note that any issues relating CV are mostly with your computers camera not giving permission to be accessed.

If the game does not detect the paddles, you can test the mask algorithm like this:

1) Open the file MaskTest that is within this folder
2) Run the code
3) Play around with the sliders until the camera masks everything except the paddles.
4) Note the values of every slider
5) Press 'q' on your key board, you will then see a second screen pop up
6) The second screen should draw contours around your object of choice.

If it correctly draws contours around your object and tracks your object continue to the next step.
Else, either chose a different paddle or use new slider values.

7) Open up the term project file again. 
8) Press command F and search for the phrase 'INSERT SLIDER VALUES'
9) Here you will find a varaible called lower_bound and upper_bound
10) replace the items within the np.array with the slider values
	In lower bounds, replace the things within the parentheses with [l_h,l_s,l_v]
	In upper bounds, replace the things within the parentheses with [u_h,u_s,u_v]
	If you are using a bright yellow paddle similar to mine, you can replace those two lines with:
	lower_bound = np.array([0,170,102])
        upper_bound = np.array([255,255,255])

I do not think that you should need to go through these steps, but after doing this the game should work.

Also please DO NOT modify or open the leaderboards and EXP csv files. There are two copy files that you can open if you want to see how I have stored my data.
These copy files do not update, so there is no read or write. 
If you want to check if these work, you can press X on the opening screen and the game automatically ends giving you a score of 0
This will be written in the file, and when you click on leaderboards you will see the name you entered in the console. 



Spamming keys x, y, or r will increase the chance of enemies to shoot projectiles. You can press these keys many times to see how projectiles work.
You can also make hardMode on to further increase the chances of projectiles being spawned.

I hope you enjoy my project :)
