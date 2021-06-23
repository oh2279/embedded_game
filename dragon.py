#import filght
from bullet import bullet 
from PIL import Image, ImageDraw, ImageFont, ImageChops


class character():#filght.filght):
    image = Image.open("/home/pi/beom/embedded_game/character.png")
    def __init__(self,current_x,current_y):
        self.current_x = current_x
        self.current_y = current_y

    #좌로이동
    def move_left(self):
        if self.current_x < 5:
            self.current_x = self.current_x
        else:
            self.current_x -= 5
        self.image.paste(self.image,(self.current_x,self.current_y))

    #우로이동
    def move_right(self):
        if self.current_x > 205:
            self.current_x = self.current_x
        else:
            self.current_x += 5
        self.image.paste(self.image,(self.current_x,self.current_y))

    #위로이동
    def move_up(self):
        if self.current_y < 5:
            self.current_y = self.current_y
        else:
            self.current_y -= 5
        self.image.paste(self.image,(self.current_x,self.current_y))

        #아래로 이동
    def move_down(self):
        if self.current_y > 205:
            self.current_y = self.current_y
        else:
            self.current_y += 5
        self.image.paste(self.image,(self.current_x,self.current_y))



