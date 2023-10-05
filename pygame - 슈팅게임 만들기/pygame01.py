import pygame #pygame 모듈을 불러온다. (불러오지 않고 pygame의 명령어를 사용하면 오류가 난다.)
import random #난수를 써야할 때 필요한 모듈을 불러온다. 예시로 무작위 뽑기 등
import sys    #sys모됼은 시스템을 다뤄야 하는 부분이 많을 때 활용하게 된다. 시스템과 관련된 작업 대부분을 처리하기 위한 다양한 메서드(방법?)를 제공한다.

def paintEntity(entity,x,y): 
    monitor.blit(entity,(int(x),int(y)))  #매개변수로 받은 객체를 화면에 그리는 함수이다.
    
def writeScore(score): #점수 텍스트 함수
    myfont = pygame.font.Font('NanumGothic.ttf',20) #점수 텍스트의 폰트를 바꿔준다.
    txt = myfont.render(u'파괴한 우주괴물 수 : ' + str(score), True, (0, 0, 0)) #txt 변수에 파괴한 우주괴물의 수와 점수에 관련된 명령어를 지정해준다.
    monitor.blit(txt, (10, sheight - 40)) #파괴한 우주괴물 수를 화면에 출력한다.

def playGame():  #게임 플레이 함수
    global monitor,ship,monster #프로그램 전체에서 데이터를 공유하고 유지하기 위해서 monitor, ship, monster 변수를 전역변수로 선언한다.

    r=239 #변수 r에 239의 값을 지정한다.
    g=228  #변수 g에 228의 값을 지정한다.
    b=179  #변수 r에 179의 값을 지정한다.
    
    shipX = swidth / 2 #우주선의 x값을 창 너비의 절반으로 지정한다.
    shipY = sheight * 0.8 #우주선의 y값을 창 높이의 0.8 만큼으로 지정한다.
    dx,dy = 0,0 #키보드를 누를 시 우주선의 x,y이동량
    
    monster = pygame.image.load(random.choice(monsterImage)) #몬스터의 사진을 아래에서 만든 monsterImage 리스트에서 랜덤으로 선택해서 정한다.
    monsterSize = monster.get_rect().size #monsterSize 변수에 monster 이미지의 가로, 세로 크기의 정보가 포함 되도록 한다.
    monsterX = 0 #몬스터의 x값을 0으로 바꾼다.
    monsterY = random.randrange(0,int(swidth*0.3)) #몬스터의 Y값을 0~창 너비의 0.3 만큼의 공간 안에서 랜덤으로 지정한다.
    monsterSpeed=random.randrange(1,5) #몬스터의 속도를 1~5의 값중 하나로 랜덤으로 지정한다.
    
    missileX, missileY = None,None #미사일의 x,y값을 없는 값으로 지정한다.
    
    fireCount = 0 #fireCount 변수를 0으로 지정한다.

    while True:
        (pygame.time.Clock()).tick(50) #게임 진행을 조금 늦춘다.
        monitor.fill((r,g,b))   #r,g,b,색으로 배경을 칠한다. 위에 random 함수를 사용하여 무작위의 값이 지정되었다.

        for e in pygame.event.get(): #키보드, 마우스 등 여러가지 이벤트가 파이썬에 들어오는지 체크한다.
            if e.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit() #위 3가지 코드는 창의 X를 클릭했을 때 pygame를 종료시킨다.
                
            if e.type in [pygame.KEYDOWN]:  #키보드의 키가 눌리면 아래의 명령어를 실행시킨다.
                if e.key == pygame.K_LEFT : dx -=5 #키보드의 눌린 키가 왼쪽 화살표이면 x 이동량을 -5로 정한다.
                if e.key == pygame.K_RIGHT : dx +=5 #키보드의 눌린 키가 오른쪽 화살표이면 캐릭터를 x 이동량을 +5로 정한다.
                if e.key == pygame.K_UP : dy -=5 #키보드의 눌린 키가 위쪽 화살표이면 y 이동량을 -5로 정한다.
                if e.key == pygame.K_DOWN : dy +=5 #키보드의 눌린 키가 아래쪽 화살표이면 y 이동량을 +5로 정한다.
                if e.key == pygame.K_SPACE : #키보드의 스페이스바가 눌리면 캐릭터가 미사일을 발사한다.
                    if missileX == None : #미사일x값이 None이라면
                        missileX = shipX + shipSize[0] / 2 
                        missileY = shipY #만약 스페이스바가 눌렸는데 미사일이 발사되지 않았다면 미사일의 X,Y에 우주선의 위치를 대입한다. (미사일을 발사 한다.)
                
            if e.type in [pygame.KEYUP]: #키보드의 키가 떼어지면 아래의 명령어를 실행시킨다.
                if e.key == pygame.K_LEFT : dx +=5 #키보드의 떼어진 키가 왼쪽 화살표이면 x 이동량을 +5로 정한다.
                if e.key == pygame.K_RIGHT : dx -=5 #키보드의 떼어진 키가 오른쪽 화살표이면 x 이동량을 -5로 정한다.
                if e.key == pygame.K_UP : dy +=5 #키보드의 떼어진 키가 위쪽 화살표이면 y 이동량을 +5로 정한다.
                if e.key == pygame.K_DOWN : dy -=5 #키보드의 떼어진 키가 아래쪽 화살표이면 y 이동량을 -5로 정한다.
        
        
        if(0<shipX + dx and shipX + dx <= swidth - shipSize[0]) and (sheight / 2 < shipY + dy and shipY + dy <= sheight - shipSize[1]): #우주선의 위치가 화면 안쪽일 때에만 우주선을 이동시킨다.
            shipX += dx #우주선의 x값에 이동량 x값을 더한다.
            shipY += dy #우주선의 y값에 이동량 y값을 더한다.
        paintEntity(ship,shipX,shipY) #객체(우주선)를 그린다.
        
        monsterX += monsterSpeed #몬스터의 x값에 몬스터의 속도를 더한다.
        if monsterX > swidth: #몬스터의 x값이 창크기보다 커진다면(몬스터가 창밖으로 나간다면) 아래의 명령어를 실행한다.
            monsterX = 0 #몬스터의 x값을 0으로 바꾼다.
            monsterY = random.randrange(0,int(swidth*0.3)) #몬스터의 Y값을 0~창 크기의 0.3 만큼의 공간 안에서 랜덤으로 지정한다.
            monster = pygame.image.load(random.choice(monsterImage)) #몬스터의 사진을 아래에서 만든 monsterImage 리스트에서 랜덤으로 선택해서 정한다.
            monsterSize = monster.get_rect().size #monsterSize 변수에 monster 이미지의 가로, 세로 크기의 정보가 포함 되도록 한다.
            monsterSpeed = random.randrange(1,5) #몬스터의 속도를 1~5의 값중 하나로 랜덤으로 지정한다.
            
        paintEntity(monster,monsterX,monsterY) #객체(몬스터)를 그린다.
        
        if missileX != None: #미사일 x값이 None이 아니라면
            missileY -= 10 #미사일이 발사되었으면 위로 움직이게 합니다.
            if missileY < 0: #미사일의 Y값이 0보다 작다면
                missileX, missileY = None, None #미사일의 Y값이 화면을 넘어가면 미사일의 X,Y좌표 값을 초기화시켜줍니다.
        if missileX != None: #미사일 x값이 None이 아니라면
            paintEntity(missile, missileX, missileY) #미사일의 x값이 None이 아니라면 미사일을 그린다.
            
            if(monsterX < missileX and missileX < monsterX + monsterSize[0]) and (monsterY < missileY and missileY < monsterY + monsterSize[1]):
                fireCount += 1 #미사일이 몬스터에 맞았다면 점수를 1 더해준다.
                
                monster = pygame.image.load(random.choice(monsterImage)) #몬스터의 사진을 아래에서 만든 monsterImage 리스트에서 랜덤으로 선택해서 정한다.
                monsterSize = monster.get_rect().size #monsterSize 변수에 monster 이미지의 가로, 세로 크기의 정보가 포함 되도록 한다.
                monsterX = 0 #몬스터의 x값을 0으로 바꾼다.
                monsterY = random.randrange(0, int(swidth*0.3)) #몬스터의 Y값을 0~창 크기의 0.3 만큼의 공간 안에서 랜덤으로 지정한다.
                monsterSpeed = random.randrange(1,5) #몬스터의 속도를 1~5의 값중 하나로 랜덤으로 지정한다.
                
                missileX, missileY = None, None #미사일의 X, Y값을 없앤다.(미사일이 사라지게 한다.) 
                
        writeScore(fireCount) #위에 지정한 점수 텍스트 함수에 fireCount 변수를 지정한다.
                
        pygame.display.update()   #화면을 업데이트 시켜준다.
        print("~",end = '') 

r,g,b=[0]*3 #r, g, b  변수들을 모두 0으로 초기화 한다.(*3이 있는 이유는 본래 형태가 (r, g, b)인 것을 생각하면 됨)
swidth,sheight = 500,700 #pygame 창의 크기 설정
monitor = None #monitor 변수에 None을 지정한다.
ship,shipSize = None,0 #ship 변수에 None을, shipsize 변수에 0을 지정한다.

monsterImage = ['monster01.png','monster02.png','monster03.png','monster04.png','monster05.png', 'monster06.png','monster07.png','monster08.png','monster09.png','monster10.png']  #모든 몬스터의 사진을 monsterImage 변수로 지정한다.
monster = None #monitor 변수에 None을 지정한다.

missile = None #missile 변수에 None을 지정한다.

pygame.init() #pygame을 임포트한 후에 초기화한다.
monitor=pygame.display.set_mode((swidth,sheight)) #monitor 변수에 해당 함수를 호출하면 새로운 게임 창이나 화면이 생성되도록 지정한다.
pygame.display.set_caption('우주괴물 무찌르기') #실행창의 제목을 지정한다.

ship = pygame.image.load('ship02.png') #우주선의 이미지를 불러온다.
shipSize = ship.get_rect().size #우주선의 크기를 설정한다.

missile = pygame.image.load('missile.png') #missile 변수에 미사일 그림을 불러오는 명령어를 지정한다.

playGame() #게임 플레이 함수를 실행한다.