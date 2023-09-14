import pygame

windowx=1000
windowy=600
window=pygame.display.set_mode((windowx,windowy))

class Block:

    def __init__(self,x,y,xsize,ysize,xspeed=0,yspeed=0,isDynamic=True):

        self.x=x
        self.y=y
        self.xsize=xsize
        self.ysize=ysize
        self.xspeed=xspeed
        self.yspeed=yspeed
        self.isDynamic=isDynamic
        self.color=[255,255,255]
        self.oldx=x
        self.oldy=y

    def move(self):
        
        if self.isDynamic:
            self.x+=self.xspeed
            self.y+=self.yspeed
    
    def getCorners(self):
        return [[self.x,self.y],[self.x+self.xsize,self.y],[self.x,self.y+self.ysize],[self.x+self.xsize,self.y+self.ysize]]

    def updateCorner(self,corner_index,loc):

        if corner_index==0:
            self.x=loc[0]
            self.y=loc[1]
        elif corner_index==1:
            self.x=loc[0]-self.xsize
            self.y=loc[1]
        elif corner_index==2:
            self.x=loc[0]
            self.y=loc[1]-self.ysize
        elif corner_index==3:
            self.x=loc[0]-self.xsize
            self.y=loc[1]-self.ysize


def ColSolver(blocks):
        
    for block1_index in range(len(blocks)):

        block1_corners=blocks[block1_index].getCorners()

        for block2_index in range(len(blocks)):

            if block1_index == block2_index:
                continue

            block2_corners=blocks[block2_index].getCorners()

            for block2_corner in block2_corners:

                if block2_corner[0]<block1_corners[1][0] and block2_corner[0]>block1_corners[0][0] and block2_corner[1]<block1_corners[2][1] and block2_corner[1]>block1_corners[0][1]:

                    blocks[block2_index].color=[255,0,0]
                    blocks[block1_index].color=[255,0,0]

                    Solve(blocks[block1_index],blocks[block2_index])
    
def Solve(block1,block2):


    dx1=block1.x-block1.oldx
    dy1=block1.y-block1.oldy

    dx2=block2.x-block2.oldx
    dy2=block2.y-block2.oldy

    relative_xspeed=dx1-dx2
    relative_yspeed=dy1-dy2

    if relative_xspeed>0 and relative_yspeed>0:
        block2_corner=0
        tester=lambda x : x < block1.x + block1.xsize
    elif relative_xspeed<0 and relative_yspeed>0:
        block2_corner=1
        tester=lambda x : x > block1.x
    elif relative_xspeed>0 and relative_yspeed<0:
        block2_corner=2
        tester=lambda x : x < block1.x + block1.xsize
    elif relative_xspeed<0 and relative_yspeed<0:
        block2_corner=3
        tester=lambda x : x > block1.x
    else:
        
        if not block2.isDynamic:
            return
        if relative_xspeed==0:
            delta=block1.y-block2.y
            block2.updateCorner(0,[block2.x,block2.y+delta-block2.ysize])
        if relative_yspeed==0:
            block2.updateCorner(0,[block2.x+block2.xspeed,block2.y])

        return

    cornerSolver(block1,block2,block2_corner,tester,relative_xspeed,relative_yspeed)

    
        
def cornerSolver(block1,block2,block2_corner,tester,xspeed,yspeed):

    m=yspeed/xspeed

    block2_corner_loc=block2.getCorners()[block2_corner]

    block1_corner_loc=block1.getCorners()[3-block2_corner]

    intertest=[(block1_corner_loc[1]-block2_corner_loc[1])/m+block2_corner_loc[0],block1_corner_loc[1]]

    if not tester(intertest[0]):
        intertest=[block1_corner_loc[0],m*(block1_corner_loc[0]-block2_corner_loc[0])+block2_corner_loc[1]]
    
    else:
        block2.yspeed=0

    if(block2.isDynamic):
        block2.updateCorner(block2_corner,intertest)
    
    if block1.isDynamic and block2.isDynamic:

        block1.x-=xspeed/10
        block1.y-=yspeed/10
    
    print(intertest,block2.x,block2.y)
    pygame.draw.circle(window,(0,255,0),intertest,5)



def renderBlocks(window,blocks):
    for block in blocks:
        pygame.draw.rect(window,block.color,pygame.Rect(block.x,block.y,block.xsize,block.ysize),3)
    
def resetColors(blocks):
    for block in blocks:
        block.color=[255,255,255]
    
def mover(blocklist):
    for block in blocklist:
        block.move()

def gravity(blocks):
    for block in blocks:
        if block.isDynamic and block.yspeed<10:
            block.yspeed+=1

def updateOldLoc(blocks):
    for block in blocks:
        block.oldx=block.x
        block.oldy=block.y

def main():

    global window

    pygame.init()

    clock = pygame.time.Clock()
    run=True
    pressing = False

    player=Block(200,100,40,40,0,0,True)
    blocks=[player,Block(50,300,500,50,0,0,False),Block(650,300,500,50,0,0,False)]

    while run:

        clock.tick(30)
        window.fill((0,0,0))

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()  
            if event.type == pygame.QUIT:
                run = False
            if event.type==pygame.MOUSEBUTTONDOWN or pressing:
                pressing=True
                pos=pygame.mouse.get_pos()
                player.updateCorner(0,pos)
            if event.type==pygame.MOUSEBUTTONUP:
                pressing=False    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(player.yspeed)
                    if player.yspeed==0:
                        player.yspeed=-15

        player.xspeed = -(keys[pygame.K_a]-keys[pygame.K_d])*5

        gravity(blocks)
        mover(blocks)
        ColSolver(blocks)
        resetColors(blocks)
        renderBlocks(window,blocks)
        updateOldLoc(blocks)

        pygame.draw.line(window,(0,255,0),[50,50],[player.xspeed+50,player.yspeed+50])

        pygame.display.update() 

if __name__=="__main__":
    main()