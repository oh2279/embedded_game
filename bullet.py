from PIL import Image

class bullet():
    image = Image.open("/home/pi/beom/embedded_game/img/bullet.png")
    image2 = Image.open("/home/pi/beom/embedded_game/img/explosion.png")
    
    def __init__(self,current_x,current_y):
        self.current_x = current_x
        self.current_y = current_y
        self.shots = []
 
    def fire(self,dragon_x,dragon_y):
        self.shots.append([dragon_x + 10,dragon_y])

    def check(self,monster):
        if len(self.shots) > 0:
            for i in range(len(self.shots))[::-1]:
                flag = False
                for j in range(len(monster))[::-1]:
                    if flag:
                        break
                    for k in range(4):
                        if self.shots[i][0] + 8 > monster[j][k] and monster[j][k] + 30 > self.shots[i][0] and self.shots[i][1] <= monster[j][4] +30 :
                            self.shots.pop(i)
                            monster[j][k] = -3000 #리스트 문제
                            flag = True
                            break

                   # 만약 총알이랑 적이랑 닿으면, 적 이미지 삭제, 총알 이미지 삭제, 보스 피 -1

 
