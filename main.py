import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from dragon import character
import stage
from enemy import enemy
from bullet import bullet

def ending():
    while True:
        image.paste(stage.ending, (0,0))
        disp.image(image)


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

current_x = 100
current_y = 200
dragon = character(current_x,current_y)
monster = enemy()
shot = bullet(dragon.current_x+10,dragon.current_y)

enemy_count = 7 # 변수명 헷갈림,대문자(상수처럼 쓰는 것은 대문자)
rezen_time = 4
game_start = 0

final = 0

while True:

    if not button_U.value:  # up pressed - 버튼이 눌리면 false, true
        dragon.move(0)

    if not button_D.value:  # down pressed
        dragon.move(2)

    if not button_L.value:  # left pressed
        dragon.move(3)

    if not button_R.value:  # right pressed
        dragon.move(1)

    if not button_C.value:  # center pressed
        pass

    if not button_A.value:  # A pressed - 총알 발사 - 직선
       shot.fire(dragon.current_x,dragon.current_y)

    if not button_B.value and game_start ==0:
        game_start = 1
        x = time.time()
        
    if button_B.value and game_start == 0:  # B pressed 
        image.paste(stage.start,(0,0))
        disp.image(image)
        continue

    if not button_B.value and game_start ==1 :
        dragon.more_speed = 5
    elif game_start == 1 :
        dragon.more_speed = 0

    # Display the Image
    image.paste(stage.background, (0,0))
    image.paste(dragon.image, (dragon.current_x,dragon.current_y))
    for i in range(len(shot.shots)): # 총알 발사
     
        if shot.shots[i][1] < 0:
            continue
        if shot.shots[i][0] == 240 and shot.shots[i][1] ==0:
            continue # ??
        image.paste(shot.image, (shot.shots[i][0],shot.shots[i][1]))
        shot.shots[i] = [shot.shots[i][0], shot.shots[i][1] - 6]
    
    if abs((time.time()-x) >= rezen_time and monster.count < enemy_count): # 적 생성
        monster.regeneration()
        x = time.time()

    for i in range(len(monster.spot))[::-1]:  # enemy 이동
        
        if monster.spot[i][4] >= 210:
            continue
        for j in range(4):
            image.paste(monster.image, (monster.spot[i][j],monster.spot[i][4]))
        monster.spot[i] = [monster.spot[i][0],monster.spot[i][1],monster.spot[i][2],monster.spot[i][3],monster.spot[i][4] + 4]

        if monster.count >=1 and len(shot.shots) > 0:
            shot.check(monster.spot) #[i]
        
        dragon.check_hp(monster.spot)
        
    if monster.count >= enemy_count: # 보스 생성
        if monster.spot[enemy_count-1][4] >= 210:
            image.paste(monster.image2, (monster.boss_spot[0][0],monster.boss_spot[0][1]),monster.image2)
            life = monster.boss_life(shot.shots)
            if life == 0:
                ending()
            dragon.check_hp_to_boss(monster.boss_spot)
            monster.boss()
            if monster.boss_spot[0][1] > 210:
                ending()

    num = dragon.get_life()
    if num == 3 :
        image.paste(stage.life3,(0,180))
    elif num == 2:
        image.paste(stage.life2,(0,180))
    elif num == 1:
        image.paste(stage.life1,(0,180))
    elif num == 0 :
        ending()

    disp.image(image)

    #해야할 것 = 목숨 자꾸 이상하게 줄어드는데 오류 찾기, 처음부터 닿는게 아니라 뒤에서 닿으면 목숨 안줄어들음

    # 비행 -> 배경이 움직이는 모션 -> gif 작동하는지 확인 -> 안된다면 일단은 코드부터 짜고, 고정(?)

    # next stage

    # 엔딩 : 적이 계속 나오다가, 어느 수준으로 나오면 보스가 나온다 -> 잡으면 끝.

    # 보드 - 스틱(상하좌우 가운데), a버튼, b버튼(게임시작)

