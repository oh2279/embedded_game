
from PIL import Image
import random

class enemy():
        image = Image.open("/home/pi/beom/embedded_game/img/enemy.png")
        image2 = Image.open("/home/pi/beom/embedded_game/boss.png")
        boss_heart = 20
        def __init__(self):
                self.count = 0
                self.spot=[]
                self.x1=self.x2=self.x3=self.x4 = 0
                self.y = 0
                self.boss_spot = []
                self.boss_spot.append([random.randint(60,120),0])
        def  regeneration(self):
                self.x1 = random.randint(0,40)
                self.x2 = random.randint(60,100)
                self.x3 = random.randint(120,160)
                self.x4= random.randint(170,210)
                self.spot.append([self.x1,self.x2,self.x3,self.x4,self.y])
                self.count += 1

        def boss(self):
                self.boss_spot[0] = [self.boss_spot[0][0],self.boss_spot[0][1] + 2]

        def boss_life(self,bullet):
                for i in range(len(bullet))[::-1]:
                        if bullet[i][0] + 8 > self.boss_spot[0][0] and bullet[i][0] < self.boss_spot[0][0] +50 and bullet[i][1] <= self.boss_spot[0][1] + 40 :
                                self.boss_heart -= 1
                                bullet.pop(i)
                                if self.boss_heart == 0:
                                        self.boss_spot = []
                                        return 0
