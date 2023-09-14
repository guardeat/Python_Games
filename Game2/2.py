import pygame

class drawMap():
    def __init__(self):
        self.x1=0
        self.y1=0
        self.blockList=[]
        self.blockSize=30
    def addBlock(self):
        for i in self.blockList:
            if(i.isEqual([self.x1*self.blockSize,self.y1*self.blockSize])):
                return
        self.blockList.append(Block((self.x1*self.blockSize,self.y1*self.blockSize),self.blockSize,self.blockSize,False))
    def getBlockList(self):
        return self.blockList
    def setPozition(self,location):
        self.x1=location[0]//self.blockSize
        self.y1=location[1]//self.blockSize
        self.control=1
        self.addBlock() 
    def deleteBlock(self,location):
        x=(location[0]//self.blockSize)*self.blockSize
        y=(location[1]//self.blockSize)*self.blockSize
        for i in range(len(self.blockList)):
            if(self.blockList[i].isEqual([x,y])):
                self.blockList.pop(i)
                break

class Block():
    def __init__(self,leftUpCorner,height,width,move):
        self.leftUpCorner=leftUpCorner
        self.height=height
        self.width=width
        self.move=move
    def getRect(self):
        return pygame.Rect((self.leftUpCorner[0],self.leftUpCorner[1]),(self.width,self.height))
    def canMove(self):
        return self.move
    
    def isEqual(self,location):
        if(location[0]==self.leftUpCorner[0] and location[1]==self.leftUpCorner[1]):
            return True
        return False      

class Printer():
    def printBlocks(screen,gameMap):
        for i in gameMap.blockList:
            pygame.draw.rect(screen,(205, 127, 50),i.getRect())     

def main():
    pygame.init()
    run=True
    screen=pygame.display.set_mode((1001,601))
    clock = pygame.time.Clock()
    run=True
    clock = pygame.time.Clock()
    draw=drawMap()

    while run:
        pygame.display.update()
        screen.fill((0,100,200))
        clock.tick(300)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed() 
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]: 
                pos=pygame.mouse.get_pos()
                draw.setPozition(pos)
            if pygame.mouse.get_pressed()[2]:
                pos=pygame.mouse.get_pos()
                draw.deleteBlock(pos)    
        Printer.printBlocks(screen,draw)      
    blocks=draw.getBlockList()  

    with open("level_map.txt","w") as levelFile:
        for block in blocks: 
            levelFile.write(str(block.leftUpCorner[0])+","+str(block.leftUpCorner[1])+","+str(block.height)+","+str(block.width)+"\n")

if __name__=="__main__":
    main()