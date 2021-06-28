from PIL import Image

class bullet():
    image = Image.open("/home/pi/beom/embedded_game/img/bullet.png")
    image2 = Image.open("/home/pi/beom/embedded_game/img/explosion.png")
    
    def __init__(self,current_x,current_y):
        self.current_x = current_x
        self.current_y = current_y
        self.shots = []
 
    def fire(self,filght_x,filght_y):
        self.shots.append([filght_x + 10,filght_y]) # 내 캐릭터의 가운데에서 총알 발사

    def check_kill_enemy(self,enemy):   # bullet이 enemy와 닿았는지 검사
        if len(self.shots) > 0:
            for i in range(len(self.shots))[::-1]:
                flag = False
                for j in range(len(enemy))[::-1]:
                    if flag:
                        break
                    for k in range(4):
                        if self.shots[i][0] + 8 > enemy[j][k] and enemy[j][k] + 30 > self.shots[i][0] and self.shots[i][1] <= enemy[j][4] +30 :
                            self.shots.pop(i)
            
                            enemy[j][k] = -3000 #리스트 문제
                            flag = True # 닿았다면 flag를 True로 만들고
                            break
