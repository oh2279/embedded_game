from os import X_OK


class bullet():
    def __init__(self,owner, x,y,ex,ey):#현재 좌표(출발 위치, 도착위치))
    # 아군(위로 직진), 적군(드래곤을 향해), 방향 ,현재위치
        self.owner = owner
        self.x = x
        self.y = y
        self.dx = ex-x
        self.dy = ey-y
        d = math.sqrt(self.dx**2 + self.dy**2) # 속도 맞춰주기
        self.dx /= d
        self.dy /= d

    def move(self):
        self.x += dx
        self.y += dy

    def check(x, y, sx, sy, ex, ey):
        sx <= x <= ex and sy <= y <= ey


# 히트박스(사각형), 총알의 왼쪽 위 좌표, 오른쪽 아래 좌표, 용의 왼쪽위 용의 오른쪽 아래 - 총 4개

# x, y
# sx, sy, ex, ey
# sx <= x <= ex and sy <= y <= ey - 위 조건을 만족한다면 (x, y)라는 점이 (sx, sy, ex, ey)로 표현되는 사각형 내에 있는지 판단하는 코드

# sx1, sy1, ex1, ey1
# sx2, sy2, ex2, ey2

check(sx1, sy1, sx2, sy2, ex2, ey2) or check(sx1, ey1, sx2, sy2, ex2, ey2) or
check(ex1, sy1, sx2, sy2, ex2, ey2) or check(ex1, ey1, sx2, sy2, ex2, ey2)  # 총알이 용과 겹쳤는지 판단

# 총알이 1, 용이 2