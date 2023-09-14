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

    relative_xspeed=block1.xspeed-block2.xspeed
    relative_yspeed=block1.yspeed-block2.yspeed

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
        return

    m=relative_yspeed/relative_xspeed

    cornerSolver(block1,block2,block2_corner,m,tester)

    
        
def cornerSolver(block1,block2,block2_corner,m,tester):

    block2_corner_loc=block2.getCorners()[block2_corner]

    block1_corner_loc=block1.getCorners()[3-block2_corner]

    intertest=[(block1_corner_loc[1]-block2_corner_loc[1])/m+block2_corner_loc[0],block1_corner_loc[1]]

    if not tester(intertest[0]):
        intertest=[block1_corner_loc[0],m*(block1_corner_loc[0]-block2_corner_loc[0])+block2_corner_loc[1]]
    
    if block1.isDynamic and block2.isDynamic:
        intertest[0]=(intertest[0]+block2_corner_loc[0])/2
        intertest[1]=(intertest[1]+block2_corner_loc[1])/2

    if(block2.isDynamic):
        block2.updateCorner(block2_corner,intertest)
    
    if(block1.isDynamic):
        block1.updateCorner(3-block2_corner,intertest)

    pygame.draw.circle(window,(0,255,0),intertest,4)



def renderBlocks(window,blocks):
    for block in blocks:
        pygame.draw.rect(window,block.color,pygame.Rect(block.x,block.y,block.xsize,block.ysize),3)
    
def resetColors(blocks):
    for block in blocks:
        block.color=[255,255,255]

def main():

    global window

    pygame.init()

    clock = pygame.time.Clock()
    run=True
    pressing = False

    testBlock=Block(200,100,40,40,3,3,True)
    blocks=[Block(500,300,100,100,0,0,False),testBlock]

    while run:

        clock.tick(30)
        window.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type==pygame.MOUSEBUTTONDOWN or pressing:
                pressing=True
                pos=pygame.mouse.get_pos()
                testBlock.x=pos[0]
                testBlock.y=pos[1]
            if event.type==pygame.MOUSEBUTTONUP:
                pressing=False     

        ColSolver(blocks)
        renderBlocks(window,blocks)
        resetColors(blocks)
        testBlock.move()
        blocks[0].move()

        pygame.display.update() 

if __name__=="__main__":
    main()