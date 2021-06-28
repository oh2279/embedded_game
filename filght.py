from PIL import Image

class character():
    image = Image.open("/home/pi/beom/embedded_game/img/character.png")

    life = 3    # 캐릭터 목숨 = 3
    move_speed = 7  # 기본 속도
    more_speed = 0  # b버튼 누를 시 가속될 속도

    dy = [-1,0,1,0] # 방향 벡터
    dx = [0,1,0,-1] # 위로 갈땐 y--, 오른쪽으로 갈땐 x++, 아래로 갈땐 y++, 왼쪽으로 갈땐 x--

    def __init__(self,current_x,current_y):
        self.current_x = current_x
        self.current_y = current_y

    def move(self,dir): # 캐릭터 이동 관련 함수
        nx = self.current_x + self.dx[dir] * (self.move_speed + self.more_speed)
        ny = self.current_y + self.dy[dir] * (self.move_speed + self.more_speed)

        if nx < 5 or nx > 205 or ny < 5 or ny > 205 :   # 벽에 닿으면 더이상 이동x
            return
        self.current_x = nx
        self.current_y = ny


    def check_to_enemy(self,enemy): # 상대와 부딪혔는지 검사
         if len(enemy) > 0:
            for j in range(len(enemy))[::-1]:   #pop하기 위해 역순으로 돌림 + 인덱스 에러 피하기 위해
                for k in range(4):
                    if self.current_x + 30 > enemy[j][k] and enemy[j][k] + 30 > self.current_x and self.current_y <= enemy[j][4] +30:
                        if self.life >0:
                            self.life -= 1
                        enemy[j][k] = -3000
                        

    def check_to_boss(self,boss):    #보스와 부딪혔는지 검사
         if len(boss) > 0:
            if self.current_x + 30 > boss[0][0] and boss[0][0] + 50 > self.current_x and self.current_y <= boss[0][1] +50 :
                self.life = 0

    def get_life(self): # 남은 life 리턴
        return self.life
