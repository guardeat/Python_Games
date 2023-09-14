import math
import pygame

class Block:
    def __init__(self,x,y,width,height,canMove=True):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=[255,255,255]
        self.xspeed=0
        self.yspeed=0
        self.oldx=x
        self.oldy=y
        self.canMove=canMove
    def getCorners(self):
        return [[self.x,self.y],[self.x+self.width,self.y],[self.x,self.y+self.height],[self.x+self.width,self.y+self.height]]
    def setLoc(self,loc):
        self.x=loc[0]
        self.y=loc[1] 
    def move(self):
        if(self.canMove):
            self.x+=self.xspeed
            self.y+=self.yspeed       

def colSearch(blocks,window):
    for i1 in range(len(blocks)):
        control=blocks[i1].getCorners()
        for i2 in range(i1,len(blocks)):
            for corner in blocks[i2].getCorners():
                if(corner[0]>control[0][0] and corner[0]<control[1][0] and corner[1]>control[1][1] and corner[1]<control[3][1]):
                    blocks[i2].color=(255,0,0)
                    solveCol(blocks[i1],blocks[i2],window)
                    break 

def solveCol(block1,block2,window):

    m=(block2.y-block2.oldy)/(block2.x+0.0001-block2.oldx)
    block2_corners=block2.getCorners()

    if m>100:
        block2.y-=block2.y-block1.y+block2.height
        return

    if m == 0:
        if block2.xspeed>0:
            block2.x-=block2.x-block1.x+block2.width
        else:
            block2.x+=block1.x+block1.width-block2.x
        return

    if block2.xspeed>0 and block2.yspeed>0:

        block1_corner=0

        block2_corner=block2_corners[3-block1_corner]
        
        inter_test=[(block1.y-block2_corner[1])/(m)+block2_corner[0],block1.y]

        if inter_test[0]>block1.x:
            block2.setLoc([inter_test[0]-block2.width,inter_test[1]-block2.height])
            block2.yspeed=0
        else:
            inter_test=[block1.x,m*(block1.x-block2_corner[0])+block2_corner[1]]
            block2.setLoc([inter_test[0]-block2.width,inter_test[1]-block2.height])
            block2.xpseed=0
       
    elif block2.xspeed>0 and block2.yspeed<0:
        block1_corner=2

        block2_corner=block2_corners[3-block1_corner]
        
        inter_test=[(block1.y+block1.height-block2_corner[1])/(m)+block2_corner[0],block1.y+block1.height]

        if inter_test[0]>block1.x:
            block2.setLoc([inter_test[0]-block2.width,inter_test[1]])
            block2.yspeed=0
        else:
            inter_test=[block1.x,m*(block1.x-block2_corner[0])+block2_corner[1]]
            block2.setLoc([inter_test[0]-block2.width,inter_test[1]])
            block2.xpseed=0

    elif block2.xspeed<0 and block2.yspeed<0:
        block1_corner=3

        block2_corner=block2_corners[3-block1_corner]
        
        inter_test=[(block1.y+block1.height-block2_corner[1])/(m)+block2_corner[0],block1.y+block1.height]

        if inter_test[0]<block1.x+block1.width:
            block2.setLoc([inter_test[0],inter_test[1]])
            block2.yspeed=0
        else:
            inter_test=[block1.x+block1.width,m*(block1.x+block1.width-block2_corner[0])+block2_corner[1]]
            block2.setLoc([inter_test[0],inter_test[1]])
            block2.xpseed=0
            
    elif block2.xspeed<0 and block2.yspeed>0:
        block1_corner=1
        block2_corner=block2_corners[3-block1_corner]
        
        inter_test=[(block1.y-block2_corner[1])/(m)+block2_corner[0],block1.y]

        if inter_test[0]<block1.x+block1.width:
            block2.setLoc([inter_test[0],inter_test[1]-block2.height])
            block2.yspeed=0
        else:
            inter_test=[block1.x+block1.width,m*(block1.x+block1.width-block2_corner[0])+block2_corner[1]]
            block2.setLoc([inter_test[0],inter_test[1]-block2.height])
            block2.xpseed=0
        
def renderBlocks(window,blocklist):
    for block in blocklist:
        pygame.draw.rect(window,block.color,pygame.Rect(block.x,block.y,block.width,block.height),3)

def resetColors(blocks):
    for block in blocks:
        block.color=[255,255,255]

def mover(blocklist):
    for block in blocklist:
        block.move()        

def updateOldLoc(blocklist):
    for block in blocklist:
        block.oldx=block.x
        block.oldy=block.y     

def main():
    pygame.init()
    x=1300
    y=800
    screen=pygame.display.set_mode((x,y))
    clock = pygame.time.Clock()
    run=True
    player=Block(600,100,30,50)
    blocks=[Block(500,300,1000,200,False),player]
    x=0
    pressing = False

    while run:
        clock.tick(30)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()   
            if event.type == pygame.QUIT:
                run = False
            if event.type==pygame.MOUSEBUTTONDOWN or pressing:
                player.setLoc(pygame.mouse.get_pos())  
                pressing=True
            if event.type==pygame.MOUSEBUTTONUP:
                pressing=False
        player.xspeed-= (keys[pygame.K_a]-keys[pygame.K_d])
        player.yspeed-= (keys[pygame.K_w]-keys[pygame.K_s])  
        mover(blocks)        
        colSearch(blocks,screen)  
        updateOldLoc(blocks) 
        renderBlocks(screen,blocks)   
        pygame.display.update() 
        resetColors(blocks)

if __name__=="__main__":
    main()