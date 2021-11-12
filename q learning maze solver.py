import pygame
import random
import math
pygame.init()
win = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()
run = True
colors = [(255,235,240),(160,60,130),(0,255,0)]
font = pygame.font.Font('freesansbold.ttf',25)
Gen = 0
dotx = 1
doty = 1

moves = []
moves.append([random.randint(0,1),[-1,1][random.randint(0,1)]])
moves.append([1,-1])
tiles = [[2,2]]



class Rects:
    def __init__(self,x,y,obstacle,value):
        self.x = x
        self.y = y
        self.obstacle = obstacle
        self.value = value
    def draw(self,rect):
        global Gen
        global dotx
        global doty
        global tiles
        self.rect = pygame.draw.rect(win,colors[self.obstacle],(self.x+1,self.y+1,59,59))

        #WRITING THE VALUES OF THE RECTS#
        font2 = pygame.font.Font('freesansbold.ttf',10)
        txt = font2.render(str(int(self.value)),True,(150,150,150))
        win.blit(txt,(self.x,self.y+10))

        if self.rect.collidepoint(dotx*60+30,doty*60+30):
            #DYING#
            if self.obstacle==1:
                t = font.render("Dead",True,(255,0,0))
                win.blit(t,(5,440))
                grid[dotx][doty].value -= 10000
                for i in range(len(tiles)):
                    grid[tiles[i][0]][tiles[i][1]].value -= int(math.sqrt(i+1))
                tiles = [[1,1]]
                Gen += 1
                dotx = 1
                doty = 1
            #WINNING#
            if self.obstacle==2:
                t = font.render('WON!!!', True, (0,0,255))
                win.blit(t,(5,440))
                grid[dotx][doty].value = 10000
                for i in range(len(tiles)):
                    grid[tiles[i][0]][tiles[i][1]].value +=1
                tiles = [[1,1]]
                dotx = 1
                doty = 1





#CREATING THE GRID AND THE OBSTACLES#
grid = [[0]*10 for i in range(10)]
for i in range(10):
    for j in range(10):
        grid[i][j] = Rects(i*60,j*60,0,0)
#######################
grid[0][0].obstacle = 1
grid[1][0].obstacle = 1
grid[2][0].obstacle = 1
grid[0][1].obstacle = 1
grid[0][2].obstacle = 1
grid[3][1].obstacle = 1
grid[4][1].obstacle = 1
grid[5][2].obstacle = 1
grid[6][3].obstacle = 1
grid[6][4].obstacle = 1
grid[7][5].obstacle = 1
grid[8][5].obstacle = 1
grid[9][6].obstacle = 1
grid[9][7].obstacle = 1
grid[9][8].obstacle = 1
grid[9][9].obstacle = 1
grid[1][3].obstacle = 1
grid[2][4].obstacle = 1
grid[3][3].obstacle = 1
grid[3][5].obstacle = 1
grid[4][6].obstacle = 1
grid[5][7].obstacle = 1
grid[5][9].obstacle = 1
grid[6][9].obstacle = 1
grid[4][8].obstacle = 1
grid[7][9].obstacle = 1
grid[7][8].obstacle = 1
grid[7][7].obstacle = 1
grid[8][9].obstacle = 2
#######################


a = 0




#MAIN LOOP#
while run:
    #GENERAL STUFF#
    win.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #DRAWING THE RECTANGLES AND THE LINES#
    for i in range(10):
        pygame.draw.line(win,(0,0,0),(i*60,0),(i*60,600))
    for i in range(10):
        pygame.draw.line(win,(0,0,0),(0,i*60),(600,i*60))
    for i in range(10):
        for j in range(10):
            grid[i][j].draw(0)
    



    #DRAWING THE CHARACTER AND MOVEMENTS
    #brain.exe storming
    values = [grid[dotx+1][doty].value,
              grid[dotx-1][doty].value,
              grid[dotx][doty+1].value,
              grid[dotx][doty-1].value]
    
    pygame.draw.circle(win, (230,180,0) , (dotx*60+30,doty*60+30) , 10)

    
    if values.count(max(values))>1:
        ass = []
        zz = 0
        for h in range(values.count(max(values))):
            zz = values.index(max(values),zz)
            ass.append(zz)
            zz+=1
        n = ass[random.randint(0,values.count(max(values))-1)]
    else:
        n = values.index(max(values))
        
    if n==0:
        dotx+=1
    elif n==1:
        dotx-=1
    elif n==2:
        doty+=1
    elif n==3:
        doty-=1

    grid[dotx][doty].value -= 2
    tiles.append([dotx,doty])



    #WRITING THE GEN AND FINAL DETAILS
    text = font.render("Gen : " + str(Gen),True,(0,255,0))
    win.blit(text,(5,560))
    clock.tick(10)
    pygame.display.update()

pygame.quit()
