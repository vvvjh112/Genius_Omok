import pygame
import os
import sys
import time
import datetime
from enum import Enum, auto

# 천재오목 ABP 미구현
# 현재 33 44 오류있는듯함 -> 금수체크때 하던거 가져다 써서그런듯
# 가중치는 더 연구해보면 승률 올라갈 듯 함
# 현재 depth 2인데도 꽤 오래걸림 반복문 최적화 필요 근데 어느정도 막을건 막는듯
# 게임 승리시 화면

bg_color = (128, 128, 128)
black = (0, 0, 0)
blue = (0, 50, 255)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)
fps = 60
infinity = 999999
fps_clock = pygame.time.Clock()

class STONE(Enum):
  NONE = 0
  BLACK = auto()
  WHITE = auto()
  forbidden = auto()



print(list(STONE))

window_height = 550
window_width = 850
screen = pygame.display.set_mode((window_height, window_width))

clock = pygame.time.Clock()

#stonelmg=pygame.image.load('D:\example\-NPr5eGRMm4WoLbHI-1.png')
#pygame.display.set_icon(stonelmg)
pygame.display.set_caption("오목")


class OMOK:
    
    def __init__(self, width, height, mode):
        self.at_score=[]
        self.run = True
        self.width = width
        self.height = height
        self.map = [[STONE.NONE] * (width + 1) for i in range(height + 1)]
        self.stoneRadius = (screen.get_height() / height+ (screen.get_width() - 300) / width) / 4 # / 2 / 2
        self.turn = STONE.BLACK
        #game init
        pygame.init()

    def posToStoneIdx(self, pos):
        for i in range(self.width + 1):
            for j in range(self.height + 1):
                width = (screen.get_width() - 300) / self.width
                height =  screen.get_height() / self.height

                halfw = width / 2
                halfh = height / 2

                if width * i - halfw < pos[0] < width * (i + 1) - halfw:
                    if height * j - halfh < pos[1] < height * (j + 1) - halfh:
                        return (i, j)
        return False
    



    def gameEndCheck(self,i,j):
        if self.map[i][j] != STONE.NONE:
            stone = self.check_five(i, j, self.map[i][j])
            if stone != False:
                return stone
        return STONE.NONE
       
    def proc(self, pos):
        print(pos)
        idx = self.posToStoneIdx(pos)
        if idx:

            if idx[0]!=10:                                  # 19번째 라인 해결
                if self.map[idx[0]][idx[1]] != STONE.NONE:
                    return
                if idx != False:                            # 돌 놓을 때 실행되는 구문
                    print("DEBUG : ", idx)
                    

                    if self.turn == STONE.BLACK:
                        self.map[idx[0]][idx[1]] = self.turn
                        stone = self.gameEndCheck(idx[0],idx[1])

                    if self.turn == STONE.WHITE:
                        self.minimax(0,-infinity,infinity,STONE.WHITE)
                        temp = self.get_best_coord()
                        x=temp[0]
                        y=temp[1]
                        self.map[x][y] = STONE.WHITE
                        stone = self.gameEndCheck(x,y)
                        #self.map[idx[0]][idx[1]] = self.turn
                        #for k in range(0,7,2):
                        #    self.block_check(idx[0],idx[1],self.turn,k)
                        #stone = self.gameEndCheck(idx[0],idx[1])
                        

                
                if stone != STONE.NONE:
                    print("WIN : ", stone)
                    self.run = False
                    return

                if self.turn == STONE.BLACK:
                    self.turn = STONE.WHITE

                elif self.turn==STONE.WHITE:
                    self.turn = STONE.BLACK



    def turn_pass(self):   # 0702 #
        if self.turn == STONE.BLACK:
            self.turn = STONE.WHITE 

        else:
            self.turn = STONE.BLACK


    def draw(self):
    # pygame.draw.line(screen, pygame.color.Color(0,0,0), (0,0), (screen.get_width(), screen.get_height()))
        width = (screen.get_width() - 300) / self.width
        height =  screen.get_height() / self.height
        for i in range(9):
            pygame.draw.line(screen, pygame.color.Color(0, 0, 0), (0, height * i), (screen.get_width() - 300, (height * i)))

        for j in range(9):
            pygame.draw.line(screen, pygame.color.Color(0, 0, 0), ((width * j), 0), ((width * j), screen.get_height()))

        for i in range(self.width + 1):
            for j in range(self.height + 1):
                if self.map[i][j] == STONE.BLACK:
          # pygame.draw.circle(screen, (0, 0, 0), [width * i - self.stoneRadius, height * j - self.stoneRadius], self.stoneRadius)
                    pygame.draw.ellipse(screen, (0,0,0), pygame.Rect([width * i - self.stoneRadius, height * j - self.stoneRadius], (self.stoneRadius * 2, self.stoneRadius * 2)))
                elif self.map[i][j] == STONE.WHITE:
                    pygame.draw.ellipse(screen, (0xff,0xff,0xff), pygame.Rect([width * i - self.stoneRadius, height * j - self.stoneRadius], (self.stoneRadius * 2, self.stoneRadius * 2)))
                    pygame.draw.ellipse(screen, (0xff,0xff,0xff), pygame.Rect([width * i - self.stoneRadius, height * j - self.stoneRadius], (self.stoneRadius * 2, self.stoneRadius * 2)), 2)
                elif self.map[i][j] == STONE.forbidden:
                    pygame.draw.ellipse(screen, (255,0,0), pygame.Rect([width * i - self.stoneRadius, height * j - self.stoneRadius], (self.stoneRadius * 2, self.stoneRadius * 2)))
                    pygame.draw.ellipse(screen, (255,0,0), pygame.Rect([width * i - self.stoneRadius, height * j - self.stoneRadius], (self.stoneRadius * 2, self.stoneRadius * 2)), 2)

        sf = pygame.font.SysFont("Monospace",25,bold=True)   # 0702 # ~
        sf_1 = pygame.font.SysFont("Monospace",20,bold=True)
        text_1 = sf.render("New Game",True,(0,0,0))
        screen.blit(text_1,(screen.get_width() - 250, screen.get_height() - 400))
        text_2 = sf.render("Turn Pass",True,(0,0,0))
        screen.blit(text_2,(screen.get_width() - 250, screen.get_height() - 350))
        text_4 = sf.render("TURN : ",True,(0,0,0))
        screen.blit(text_4,(screen.get_width() - 200, screen.get_height() - 550))
        if self.turn==STONE.BLACK:
            TURN = sf.render(str('Black'),True,(0,0,0))
            screen.blit(TURN,(screen.get_width() - 100, screen.get_height() - 550))
        else:
            TURN = sf.render(str('White'),True,(0,0,0))
            screen.blit(TURN,(screen.get_width() - 100, screen.get_height() - 550))

    

    def gameEnd(self,start):
        if self.turn == STONE.BLACK:
            screen.fill((0,0,0))
        else:
            screen.fill((0xff, 0xff, 0xff))
        sf = pygame.font.SysFont("Monospace",40,bold=True)
        textStr = "WIN"
        text = sf.render(textStr,True,(0,172,255))
        screen.blit(text,(((screen.get_width() - 300) /2, screen.get_height()/2)))
        if self.turn == STONE.BLACK:
            textStr = "BLACK"
        else:
            textStr = "WHITE"
        text = sf.render(textStr,True,(0,172,255))
        screen.blit(text,((screen.get_width() - 300)/2, screen.get_height()/2  + 100))
        end_time=str(datetime.timedelta(seconds=round(time.time()-start)))
        text = sf.render(str(end_time),True,(0,172,255))
        screen.blit(text,((screen.get_width() - 300)/2, screen.get_height()/2  + 150))
        pygame.display.flip()
        time.sleep(1)
        

    def newGame(self):   # 0702 #
        
        screen.fill((181,230,29))
        sf = pygame.font.SysFont("Monospace",40,bold=True)
        textStr = "New Game"
        text = sf.render(textStr,True,(255,255,255))
        screen.blit(text,(((screen.get_width() - 200) / 2), screen.get_height() - 500))
        pygame.display.flip()
        time.sleep(1)


############################################################################################################################################################

    def check_stone(self,i,j,stone,mode): ###################
        list=[[-1,0],[1,0],[-1,1],[1,-1],[0,1],[0,-1],[1,1],[-1,-1]]
        scount=1
        for q in range(0,2,1):
            k=0
            b=0
            while True:
                dir=mode+q
                k=k+list[dir][0]
                b=b+list[dir][1]
                if self.check_error(i+k,j+b):
                    break;
                elif self.map[i+k][j+b]!=stone:
                    break;
                else:
                    scount=scount+1

        return scount
        
                
    def check_five(self,i,j,stone):    ###################
        for c in range(0,7,2):
            a=self.check_stone(i,j,stone,c)
            if a==5:
                return stone
        return False


    def check_empty(self,mode,i,j,stone):                 # 빈 공간 확인
        t_list=[[-1,0],[1,0],[-1,1],[1,-1],[0,1],[0,-1],[1,1],[-1,-1]]
        while True:
            i=i+t_list[mode][0]
            j=j+t_list[mode][1]
            if self.check_error(i,j):
                break
            elif self.map[i][j] != stone:
                break
        if self.check_error(i,j) == False:
            if self.map[i][j] == STONE.NONE:
                return i,j
            else:
                return False
        else:
            return False

    def check_error(self,i,j):
        return (i<0 or i >= self.width or j <0 or j>=self.height)


    def open_four(self,mode,i,j,stone):              # mode를 2씩 증가해줘야함
        count=0
        for h in range(0,2,1):
            em_point= self.check_empty(mode+h,i,j,stone)
            if em_point != False:
                if self.check_five(em_point[0],em_point[1],stone)==stone:
                    count=count+1
        if count==2:
            a=self.check_stone(i,j,stone,mode)
            if a==4:
                count=1
        else:
            count=0
        return count

    def open_three(self,mode,i,j,stone):
        for h in range(0,2,1):
            em_point= self.check_empty(mode+h,i,j,stone)
            if em_point != False:
                self.map[em_point[0]][em_point[1]]=stone
                if 1==self.open_four(mode,em_point[0],em_point[1],stone):
                    if self.forbidden_point(em_point[0],em_point[1],stone)==False:
                        self.map[em_point[0]][em_point[1]]=STONE.NONE
                        return True
                self.map[em_point[0]][em_point[1]]=STONE.NONE
        return False

    def four(self,mode,i,j,stone):
        for h in range(0,2,1):
            em_point= self.check_empty(mode+h,i,j,stone)
            if em_point:
                if self.check_five(em_point[0],em_point[1],stone):
                    return True
        return False


    def double_three(self,i,j,stone):
        count=0
        self.map[i][j]=stone
        for k in range(0,7,2):
            if self.open_three(k,i,j,stone):
                count=count+1
        #self.map[i][j]=STONE.NONE   # 금수 알고리즘할 땐 풀어줘야함
        if count>=2:
            return True
        return False

    def double_four(self,i,j,stone):
        count=0
        self.map[i][j]=stone
        for k in range(0,7,2):
            if self.open_four(k,i,j,stone)==2:
                count=count+2
            elif self.four(k,i,j,stone):
                count=count+1
        #self.map[i][j]=STONE.NONE   # 금 수 알고리즘할 땐 풀어줘야 함
        if count>=2:
            return True
        return False

    def three_four(self,i,j,stone):
        count=0

    def forbidden_point(self,i,j,stone):
        temp=[]
        for k in range (0,7,2):
            temp.append((self.check_stone(i,j,stone,k)))
        if self.check_five(i,j,stone):  # 수를 놓았을 때 오목이면 금수 아님
            return False
        elif max(temp)>5:                  # 6목 이상의 장목시 금수
            return True
        elif self.double_three(i,j,stone):
            return True
        elif self.double_four(i,j,stone):
            return True
        return False

    def fianl_forbidden(self,stone):
        nop=[]
        for i in range(0, self.width+1 ):
            for j in range(0, self.height + 1):
                if self.map[i][j]!=STONE.NONE:
                    continue
                if self.forbidden_point(i,j,stone):
                    temp=[i,j]
                    if not temp in nop:
                        nop.append([i,j])
        return nop


    def block_check(self, i, j, stone, mode):
        list=[[-1,0],[1,0],[-1,1],[1,-1],[0,1],[0,-1],[1,1],[-1,-1]]
        count=0
        for q in range(0,2,1):
            k=0
            b=0
            while True:
                temp=mode+q
                k=k+list[temp][0]
                b=b+list[temp][1]
                if self.check_error(i+k,j+b):
                    break
                elif self.map[i+k][j+b] == stone:
                    continue
                elif self.map[i+k][j+b] == STONE.NONE:
                    break
                else:
                    #print(i+k,j+b,"에 돌있음")
                    count=count+1
                    break
        return count
                
                

    #####################################################

    def empty_point(self):
        coords = []
        for i in range(9):
            for j in range(9):
                if self.map[i][j]== STONE.NONE:
                    coords.append((i,j))
        return coords

    def get_best_coord(self):
        score = -999999
        best_coord = []
        for best in self.at_score:
            if best[0] > score:
                score = best[0]
                best_coord = best[1]
        self.at_score=[]
        return best_coord

    def minimax(self, depth, alpha, beta, player):
       
        if alpha >= beta:
            if player == STONE.WHITE:
                return infinity
            else:
                return -infinity
        if depth == 2:
            return self.get_status()

        coords = self.empty_point()      # 빈칸 탐색
        #print(coords)
        max_score = -infinity
        min_score = infinity
        for coord in coords:
            if player == STONE.WHITE:
                self.map[coord[0]][coord[1]] = STONE.WHITE
                score = self.minimax(depth + 1, alpha, beta, STONE.BLACK)
                max_score = max(score, max_score)
                alpha = max(max_score, alpha)
                
                if depth == 0:
                    self.at_score.append([max_score, coord])
                    #print(self.at_score)
            else:
                self.map[coord[0]][coord[1]] = STONE.BLACK
                score = self.minimax(depth + 1, alpha, beta, STONE.WHITE)
                min_score = min(score, min_score)
                beta = min(min_score, beta)
                
            self.map[coord[0]][coord[1]] = STONE.NONE
            if score == infinity or score == -infinity:
                break
            
        if player == STONE.WHITE:
            return max_score
        else:
            return min_score

    def get_status(self):
        statP=0
        for i in range(0,9,1):
            for j in range(0,9,1):
                if self.map[i][j] == STONE.NONE:
                    continue

                if self. map[i][j] == STONE.WHITE:
                    stone = STONE.WHITE

                    #for q in range(0,7,2):
                    #    temp = self.check_stone(i,j,stone,q)

                    #if self.double_four(i,j,stone):
                    #    statP += 1800
                    
                    #if self.double_three(i,j,stone):
                    #    statP += 900

                    if self.check_five(i,j,stone)==stone:
                        statP += 5000

                    for k in range(0,7,2):
                        #if self.open_four(k,i,j,stone) == 2:
                        #    statP += 1500

                        #if self.open_three(k,i,j,stone):
                        #    statP += 400

                        stoneC = self.check_stone(i,j,stone,k)

                        if stoneC ==2:
                            for k in range(0,7,2):
                                if self.block_check(i,j,stone,k)==0:
                                    #print("열린2")
                                    statP += 40
                                if self.block_check(i,j,stone,k)==1:
                                    #print("한쪽막힌2")
                                    statP += 30

                        if stoneC == 3:
                            for k in range(0,7,2):
                                if self.block_check(i,j,stone,k)==0:
                                    #print("열린3",i,j)
                                    statP += 400
                                if self.block_check(i,j,stone,k)==1:
                                    #print("한쪽막힌3")
                                    statP += 60

                        if stoneC == 4:
                            for k in range(0,7,2):
                                if self.block_check(i,j,stone,k)==0:
                                    #print("한쪽막힌3",i,j)
                                    statP += 1500
                                if self.block_check(i,j,stone,k)==1:
                                    #print("한쪽막힌4")
                                    statP += 200


                if self. map[i][j] == STONE.BLACK:
                    stone = STONE.BLACK


                    #if self.double_four(i,j,stone):
                    #    statP -= 1800
                    
                    #if self.double_three(i,j,stone):
                        #statP -= 900

                    if self.check_five(i,j,stone) == stone:
                        statP -= 5000

                    for k in range(0,7,2):
                        #if self.open_four(k,i,j,stone) == 2:
                        #    statP -= 1500

                        #if self.open_three(k,i,j,stone):
                        #    statP -= 400

                        stoneC = self.check_stone(i,j,stone,k)
                    
                        if stoneC ==2:
                            for k in range(0,7,2):
                                if self.block_check(i,j,stone,k)==0:
                                    #print("열린2",i,j)
                                    statP -= 40
                                if self.block_check(i,j,stone,k)==1:
                                    #print("한쪽막힌2",i,j)
                                    statP -= 30

                        if stoneC == 3:
                            for k in range(0,7,2):
                                if self.block_check(i,j,stone,k)==0:
                                    #print("열린3",i,j)
                                    statP -= 400

                                if self.block_check(i,j,stone,k)==1:
                                    #print("한쪽막힌3",i,j)
                                    statP -= 60

                        if stoneC == 4:
                            for k in range(0,7,2):
                                if self.block_check(i,j,stone,k)==0:
                                    #print("열린4",i,j)
                                    statP -= 1500

                                if self.block_check(i,j,stone,k)==1:
                                    #print("한쪽막힌4")
                                    statP -= 200



        return statP



omok = OMOK(8, 8, 0)
start=time.time()
pygame.init()
surface = pygame.display.set_mode((window_width, window_height))


while True:
    while omok.run:
        
        key = 1
        pos = 0
        #KEY INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    
                omok.run = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keyStatus = 1
                key = event.key

            elif event.type == pygame.KEYUP:
                keyStatus = 0
                key = event.key
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:  ###################
                    pos = event.pos
                    pos_x = event.pos[0]
                    pos_y = event.pos[1]

       #UPDATE
  
        if (pos != 0):   # 0702 #
            if (pos_x >= 600 and pos_x <= 720) and (pos_y >= 205 and pos_y <= 220):
                omok.turn_pass()
                continue
            elif (pos_x >= 600 and pos_x <= 720) and (pos_y >= 155 and pos_y <= 170):
                omok.newGame()
                start=time.time()
                omok = OMOK(8, 8, 0)
                omok.run = True
                pygame.init()
                surface = pygame.display.set_mode((window_width, window_height))
                continue
            omok.proc(pos)

        #DRAW
        screen.fill((254,205,56))
        omok.draw()
        pygame.display.flip()
        clock.tick(10)
    omok.gameEnd(start)
    time.sleep(1)
    start=time.time()
    omok.run = True
    #omok = OMOK(8, 8, 0)
    #pygame.init()
    surface = pygame.display.set_mode((window_width, window_height))

    
