import time
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from filght import character
import stage
from enemy import enemy
from bullet import bullet
import sys

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

#----------------------------------------------------------------

CURRENT_X = 100 # filght 시작 위치
CURRENT_Y = 200 

filght = character(CURRENT_X,CURRENT_Y)

Enemy = enemy()

Bullet = bullet(filght.current_x+10,filght.current_y)

BOSS_COUNT = 10  # boss 출현전까지의 enemy 생성 횟수
REZEN_TIME = 3  # enemy 재생성 시간
GAME_START = 0  # game의 start 여부 판단

def ending(tag):
    if tag == 0:
        image.paste(stage.ending, (0,0))
        disp.image(image)
        sys.exit()

    elif tag == 1:
        image.paste(stage.win, (0,0))
        disp.image(image)
        sys.exit()

while True:

    if not button_U.value:  # up pressed - 버튼이 눌리면 false, true
        filght.move(0)

    if not button_D.value:  # down pressed
        filght.move(2)

    if not button_L.value:  # left pressed
        filght.move(3)

    if not button_R.value:  # right pressed
        filght.move(1)

    if not button_C.value:  # center pressed
        pass

    if not button_A.value:  # A pressed - 총알 발사 - 직선
       Bullet.fire(filght.current_x,filght.current_y)

    if not button_B.value and GAME_START ==0:   # b버튼을 눌렀는데 게임이 아직 시작안됐다면, 게임 시작
        GAME_START = 1
        x = time.time()
        
    if button_B.value and GAME_START == 0:  # b버튼을 안눌렀는데 게임이 시작 전이라면, 시작 보류
        image.paste(stage.start,(0,0))
        disp.image(image)
        continue

    if not button_B.value and GAME_START ==1 :  # b버튼을 눌렀는데 게임이 진행중이라면, b버튼은 가속버튼
        filght.more_speed = 5
    elif GAME_START == 1 :  # b버튼 안누르고 있으면 가속 x
        filght.more_speed = 0


    # Display the Image
    image.paste(stage.background, (0,0))
    image.paste(filght.image, (filght.current_x,filght.current_y))

    for i in range(len(Bullet.shots))[::-1]: # 총알 발사

        if Bullet.shots[i][1] < 0:  # 화면 밖으로 나가면 paste x
            Bullet.shots.pop(i)
        else:
            image.paste(Bullet.image, (Bullet.shots[i][0],Bullet.shots[i][1]))

            Bullet.shots[i] = [Bullet.shots[i][0], Bullet.shots[i][1] - 9]

    
    if abs((time.time()-x) >= REZEN_TIME and Enemy.count < BOSS_COUNT): # 적 생성(Enemy.count = 생성된 횟수, boss_count = boss 생성 조건 )
        Enemy.regeneration()
        x = time.time()
    
    
    for i in range(len(Enemy.spot))[::-1]:  # enemy 이동
        
        if Enemy.spot[i][4] > 210:  # 하나라도 땅에 닿으면 실패
            for k in range(4):
                if Enemy.spot[i][k] != -3000:
                        ending(0)

        for j in range(4):
            image.paste(Enemy.image, (Enemy.spot[i][j],Enemy.spot[i][4]))

        Enemy.spot[i] = [Enemy.spot[i][0],Enemy.spot[i][1],Enemy.spot[i][2],Enemy.spot[i][3],Enemy.spot[i][4] + 4]

        if Enemy.count >=1 and len(Bullet.shots) > 0:   # enemy가 생성되었고, 총알이 발사 되었으면 검사
            Bullet.check_kill_enemy(Enemy.spot) 
        
        filght.check_to_enemy(Enemy.spot)   # enemy와 filght가 닿았는지 검사

    if Enemy.count >= BOSS_COUNT: # 보스 생성
        if Enemy.spot[BOSS_COUNT - 1][4] >= 210: # 마지막으로 생성된 enemy그룹이 땅에 닿아 사라지면 보스 출현
            
            image.paste(Enemy.image2, (Enemy.boss_spot[0][0],Enemy.boss_spot[0][1]),Enemy.image2)
            boss_life = Enemy.check_boss_life(Bullet.shots)

            if boss_life == 0:
                ending(1)
                
            filght.check_to_boss(Enemy.boss_spot)
            Enemy.boss_move()

            if Enemy.boss_spot[0][1] > 210:
                ending(0)


    filght_life = filght.get_life()

    if filght_life == 3 :
        image.paste(stage.life3,(0,200))

    elif filght_life == 2:
        image.paste(stage.life2,(0,200))

    elif filght_life == 1:
        image.paste(stage.life1,(0,200))

    elif filght_life == 0 :
        ending(0)

    disp.image(image)

