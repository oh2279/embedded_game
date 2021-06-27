
from PIL import Image


class character():#filght.filght):
    image = Image.open("/home/pi/beom/embedded_game/img/character.png")
    life = 3
    move_speed = 7
    more_speed = 0
    dy = [-1,0,1,0] # 위, 오른쪽, 아래, 왼쪽
    dx = [0,1,0,-1]
    def __init__(self,current_x,current_y):
        self.current_x = current_x
        self.current_y = current_y

    def move(self,dir):
        nx = self.current_x + self.dx[dir] * (self.move_speed + self.more_speed)
        ny = self.current_y + self.dy[dir] * (self.move_speed + self.more_speed)
        if nx < 5 or nx > 205 or ny < 5 or ny > 205 :
            return
        self.current_x = nx
        self.current_y = ny

        
    #좌로이동
    #def move_left(self):
        #if self.current_x < 5:
         #   self.current_x = self.current_x
        #else:
            #self.current_x = self.current_x - self.move_speed - self.more_speed

    def check_hp(self,monster):
         if len(monster) > 0:
            for j in range(len(monster))[::-1]:
                for k in range(4):
                    if self.current_x + 30 > monster[j][k] and monster[j][k] + 30 > self.current_x and self.current_y <= monster[j][4] +30:
                        if self.life >0:
                            self.life -= 1
                        monster[j][k] = -3000
                        #if self.life == 0:
                            #self.current_x = -240
                            #self.current_y = 240

    def check_hp_to_boss(self,boss):
         if len(boss) > 0:
            if self.current_x + 30 > boss[0][0] and boss[0][0] + 50 > self.current_x and self.current_y <= boss[0][1] +50 :
                self.life = 0

    def get_life(self):
        return self.life
                            

