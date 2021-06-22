import filght
from bullet import bullet 



def fire(self,x,y): # x,y는 드래곤의 좌표
        return bullet(2,self.x,self.y,x,y) # 2=적

# 아래로 수직 하강

#보스 구별