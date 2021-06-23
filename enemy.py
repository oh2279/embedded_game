import filght
from bullet import bullet 
from PIL import Image, ImageDraw, ImageFont, ImageChops
import random
import time

class enemy():
        image = Image.open("/home/pi/beom/embedded_game/enemy.png")
        def __init__(self):
                self.spot=[]
                self.x1=self.x2=self.x3=self.x4 = 0
                self.y = 0
                
        def  regeneration(self):
                self.x1 = random.randint(0,40)
                self.x2 = random.randint(60,100)
                self.x3 = random.randint(120,160)
                self.x4= random.randint(180,220)
                self.spot.append([self.x1,self.x2,self.x3,self.x4,self.y])
                
       # def move(self):
                

        def fire(self,x,y): # x,y는 드래곤의 좌표
                shot = bullet(x,y)
                shot.auto_fire()

# 아래로 수직 하강

#보스 구별
