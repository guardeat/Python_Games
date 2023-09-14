import pygame

class Block:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=[255,255,255]
    def getCorners(self):
        return [[self.x,self.y],[self.x+self.width,self.y],[self.x,self.y+self.height],[self.x+self.width,self.y+self.height]]
    def setLoc(self,loc):
        self.x=loc[0]
        self.y=loc[1]    

def colSearch(blocks):
    for i1 in range(len(blocks)):
        control=blocks[i1].getCorners()
        for i2 in range(i1,len(blocks)):
            for corner in blocks[i2].getCorners():
                if(corner[0]>control[0][0] and corner[0]<control[1][0] and corner[1]>control[1][1] and corner[1]<control[3][1]):
                    blocks[i2].color=(255,0,0)
                    break 

def renderBlocks(window,blocklist):
    for block in blocklist:
        pygame.draw.rect(window,block.color,pygame.Rect(block.x,block.y,block.width,block.height),3)

def resetColors(blocks):
    for block in blocks:
        block.color=[255,255,255]

def main():
    pygame.init()
    x=1300
    y=800
    screen=pygame.display.set_mode((x,y))
    clock = pygame.time.Clock()
    run=True
    blocks=[Block(500,300,100,200),Block(600,100,100,50)]
    size=50

    pressing = False
    while run:
        clock.tick(300)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type==pygame.MOUSEBUTTONDOWN or pressing:
                blocks[1].setLoc(pygame.mouse.get_pos())  
                pressing=True
            if event.type==pygame.MOUSEBUTTONUP:
                pressing=False
        colSearch(blocks)       
        renderBlocks(screen,blocks)           
        pygame.display.update() 
        resetColors(blocks)

if __name__=="__main__":
    main()