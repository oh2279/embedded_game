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
monster.regeneration()
shot = bullet(dragon.current_x+10,dragon.current_y)

x= time.time()
while True:
    
    if not button_U.value:  # up pressed - 버튼이 눌리면 false, true
        dragon.move_up()

    if not button_D.value:  # down pressed
        dragon.move_down()

    if not button_L.value:  # left pressed
        dragon.move_left()

    if not button_R.value:  # right pressed
        dragon.move_right()

    if not button_C.value:  # center pressed
        pass

    if not button_A.value:  # A pressed - 총알 발사 - 직선
       shot.fire(dragon.current_x,dragon.current_y)
        
    if not button_B.value:  # B pressed - 아직 미정
        char = 1

    # Display the Image
    image.paste(stage.image, (0,0))
    image.paste(dragon.image, (dragon.current_x,dragon.current_y))
    for i in range(len(shot.shots)):
        if shot.shots[i][1] < 0:
            continue
        image.paste(shot.image, (shot.shots[i][0],shot.shots[i][1]))
        shot.shots[i] = [shot.shots[i][0], shot.shots[i][1] - 6]
    
    for i in range(len(monster.spot)):
        if monster.spot[i][4] > 240:
            continue
        image.paste(monster.image, (monster.spot[i][0],monster.spot[i][4]))
        image.paste(monster.image, (monster.spot[i][1],monster.spot[i][4]))
        image.paste(monster.image, (monster.spot[i][2],monster.spot[i][4]))
        image.paste(monster.image, (monster.spot[i][3],monster.spot[i][4]))
        monster.spot[i] = [monster.spot[i][0],monster.spot[i][1],monster.spot[i][2],monster.spot[i][3],monster.spot[i][4] + 4]

    if abs((time.time()-x)) >= 7:
        monster.regeneration()
        x = time.time()
   
    disp.image(image)
    # Display the Image
    #for window in windows:
    #    image.paste(window.image, (window.curr_x,window.curr_y), window.image)
    #image.paste(berry.image, (berry.curr_x, berry.curr_y),berry.image)
    #for rock in rocks:
    #    image.paste(rock.image, (rock.curr_x,rock.curr_y), rock.image)    
    #disp.image(image)

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
