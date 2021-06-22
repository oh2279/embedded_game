import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import dragon
import enemy
import bullet

class Queue():
    def __init__(self, queue=None):
        
        if queue is None: # 큐가 없으면
            self.queue = [] # 큐 생성
        else:
            self.queue = queue
        
    def empty(self): # 큐가 비어있는지 검사하는 함수
        if(bool(self.queue) == False): #큐가 비어있으면
            return True # true 반환
        else: # 비어있지 않다면
            return False # false 반환
        
    def size(self): # 큐의 사이즈를 검사하는 함수
        return len(self.queue) # 큐의 사이즈를 반환
    
    def push(self, element): # 큐에 값을 넣는 함수
        self.queue.append(element) # 큐에 값을 추가
        #print "list = "+str(self.queue)

    def pop(self): # 큐에서 값을 빼내는 함수
        self.queue.pop(0) # 큐에서 첫번째 값을 제거
        #print "list = "+str(self.queue)

    def index(self,i):
        return self.queue[i]


# Create the display
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT

# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for color.
width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Clear display.
draw.rectangle((0, 0, width, height), outline=0, fill=(255, 0, 0))
disp.image(image)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

background = Image.open('C:\Users\오범석\Desktop\emb\Images')
background.show()

circle_x = width/2
circle_y = height/2

que = Queue()
dy = [-5,5]

udlr_fill = "#00FF00"
udlr_outline = "#00FFFF"
button_fill = "#FF00FF"
button_outline = "#FFFFFF"
black= "#000000"    # 도형을 검은색으로 만들어서, 움직일 때 이전 도형을 지움 

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

#circle_shot_position = height/2
move_button_pressed = 0    # move 버튼 - 0과 1로 구별해 1일 땐, move
#front_shoting = [] # 앞으로 나가는 총알
#back_shoting = []   # 뒤로 나가는 총알 
while True:
    up_fill = 0
    prev_x = circle_x
    prev_y = circle_y
    if not button_U.value:  # up pressed - 버튼이 눌리면 false, true
        up_fill = udlr_fill
        move_button_pressed = 1
        circle_y -= 10

    draw.polygon(
        [(40, 40), (60, 4), (80, 40)], outline=udlr_outline, fill=up_fill
    )  # Up

    down_fill = 0
    if not button_D.value:  # down pressed
        down_fill = udlr_fill
        move_button_pressed = 1
        circle_y += 10

    draw.polygon(
        [(60, 120), (80, 84), (40, 84)], outline=udlr_outline, fill=down_fill
    )  # down

    left_fill = 0
    if not button_L.value:  # left pressed
        left_fill = udlr_fill
        move_button_pressed = 1
        circle_x -= 10

    draw.polygon(
        [(0, 60), (36, 42), (36, 81)], outline=udlr_outline, fill=left_fill
    )  # left   
    right_fill = 0

    if not button_R.value:  # right pressed
        right_fill = udlr_fill
        move_button_pressed = 1
        circle_x += 10

    draw.polygon(
        [(120, 60), (84, 42), (84, 82)], outline=udlr_outline, fill=right_fill
    )  # right

    center_fill = 0
    if not button_C.value:  # center pressed
        center_fill = button_fill
        # 가운데 버튼은 움직임 x
    draw.rectangle((40, 44, 80, 80), outline=button_outline, fill=center_fill)  # center

    A_fill = 0
    if not button_A.value:  # A pressed - 뒤로 쏘는 버튼 
        A_fill = button_fill
        direct = 1
        que.push([prev_x, prev_y, direct])
        #back_shoting.append((prev_center_x, prev_center_y)) 
    draw.ellipse((140, 80, 180, 120), outline=button_outline, fill=A_fill)  # A button

    B_fill = 0
    if not button_B.value:  # B pressed - 앞으로 쏘는 버튼 
        B_fill = button_fill
        direct = 0
        que.push([prev_x, prev_y, direct])
    draw.ellipse((190, 40, 230, 80), outline=button_outline, fill=B_fill)  # B button

    # make a random color and print text
    rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
    # draw.text((20, 150), "Hello World", font=fnt, fill=rcolor)
    # rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
    # draw.text((20, 180), "Hello World", font=fnt, fill=rcolor)
    # rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
    # draw.text((20, 210), "Hello World", font=fnt, fill=rcolor)
    #while not que.empty():
    for i in range(que.size()):
        x = que.index(i)[0]
        y = que.index(i)[1]
        dir = que.index(i)[2]
        #que.pop()

        if dir == 0 :
            draw.rectangle((x - 3, y - 10, x + 3, y - 20), outline = black, fill = black)

            que.index(i)[1] += dy[dir]

            draw.rectangle((x - 3, y - 10, x + 3, y - 20), outline = button_outline, fill=(255,255,0))

        if dir == 1:
            draw.rectangle((x - 3, y + 10, x + 3, y + 20), outline = black, fill = black)

            que.index(i)[1] += dy[dir]

            draw.rectangle((x - 3, y + 10, x + 3, y + 20), outline = button_outline, fill=(255,255,0))

    if move_button_pressed: # 움직임 = 1 일때 
        # (left,top,right,bottom) 이므로 원의 지름은 40 
        draw.ellipse((prev_x-20, prev_y-20, prev_x+20, prev_y+20), outline = black, fill = black) # 이전에 있던 도형을 지움 
    draw.ellipse((circle_x-20, circle_y-20, circle_x+20, circle_y+20), outline = button_outline, fill=(0,0,255)) # 움직인 후의 도형을 그림 or 움직임이 없을 땐 마지막 원 위치
    #draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Display the Image
    disp.image(image)

    time.sleep(0.01)


    # 게임 만들기, 모듈화, 클래스 사용, py파일 나눠서 import하기

    # py파일 나누기 - 객체별로
    
    # 주제 : 드래곤플라이트 (실습 - 원을 만들고 그 원을 움직이기, 원에서 총알 발사 앞뒤로)
    
    # 객체 : 용, 총알, 적 (버튼 - 발사, 횟수제한있는 아이템 사용- 쉴드(3초동안 지속))

    # main 게임 시작 -> 용 생성, 게임 시작 -> 시작 전 화면(이미지)

    # 적 생성(반복실행) 랜덤(0,0) ~~ (240,0)

    # 적을 잡는 기준 : 총알 닿았을 때 count--

    # 목숨, 하트

    # 비행 -> 배경이 움직이는 모션 -> gif 작동하는지 확인 -> 안된다면 일단은 코드부터 짜고, 고정(?)

    # 비행 물체 클래스 -> 용, 적, 보스

    # next stage

    # 체력 (ex. 용 3번, 적 1번, 보스-10번)

    # def class filght() :
        # 체력
    # def class dragon(filght):
    
    # 총알 클래스 - 총알을 쏜 주체, 속도, 방향, 이미지, 용 - 총알 직선, 방향 무조건 용을 향햐게(생성될 때 용의 좌표, 적의 위치)

    #def class 총알():

    # 엔딩 : 적이 계속 나오다가, 어느 수준으로 나오면 보스가 나온다 -> 잡으면 끝.

    # 보드 - 스틱(상하좌우 가운데), a버튼, b버튼

    # 이미지 x*y 그림판 아무거나 - 작동 체크 -> 이미지 수정

    # 2d게임

    # 18일 저녁 ~ 21일 1과목, 프로젝트 병행

    # 일요일 저녁 - 8시쯤(시작)

    # 코드완성 !!
