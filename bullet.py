from PIL import Image, ImageDraw, ImageFont
import time
class bullet():
    image = Image.open("/home/pi/beom/embedded_game/bullet.png")
    def __init__(self,current_x,current_y):
        self.current_x = current_x
        self.current_y = current_y
        self.shots = []
    def fire(self,dragon_x,dragon_y):
        self.shots.append([dragon_x + 10,dragon_y])
    
    def auto_fire(self):
        self.image.paste(self.image,(self.current_x,self.current_y))
    def check(self):
        trash =1


# 히트박스(사각형), 총알의 왼쪽 위 좌표, 오른쪽 아래 좌표, 용의 왼쪽위 용의 오른쪽 아래 - 총 4개

# x, y
# sx, sy, ex, ey
# sx <= x <= ex and sy <= y <= ey - 위 조건을 만족한다면 (x, y)라는 점이 (sx, sy, ex, ey)로 표현되는 사각형 내에 있는지 판단하는 코드

# sx1, sy1, ex1, ey1
# sx2, sy2, ex2, ey2

#check(sx1, sy1, sx2, sy2, ex2, ey2) or check(sx1, ey1, sx2, sy2, ex2, ey2) or
#check(ex1, sy1, sx2, sy2, ex2, ey2) or check(ex1, ey1, sx2, sy2, ex2, ey2)  # 총알이 용과 겹쳤는지 판단

# 총알이 1, 용이 2
