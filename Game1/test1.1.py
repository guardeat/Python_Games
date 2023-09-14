import pygame
class Block():
    def __init__(self,leftUpCorner,height,width,move,color):
        self.leftUpCorner=leftUpCorner
        self.height=height
        self.width=width
        self.move=move
        self.color=color
    def getRect(self):
        return pygame.Rect((self.leftUpCorner[0],self.leftUpCorner[1]),(self.width,self.height))
    def canMove(self):
        return self.move
    def isEqual(self,location):
        if(location[0]==self.leftUpCorner[0] and location[1]==self.leftUpCorner[1]):
            return True
        return False     
                
class drawMap():
    def __init__(self):
        self.x1=0
        self.y1=0
        self.blockList=[]
    def addBlock(self):
        for i in self.blockList:
            if(i.isEqual([self.x1*20,self.y1*20])):
                return
        self.blockList.append(Block((self.x1*20,self.y1*20),20,20,False,(255,0,0)))
    def getBlockList(self):
        return self.blockList
    def setPozition(self,location):
        self.x1=location[0]//20
        self.y1=location[1]//20
        self.control=1
        self.addBlock() 
    def deleteBlock(self,location):
        x=(location[0]//20)*20
        y=(location[1]//20)*20
        for i in range(len(self.blockList)):
            if(self.blockList[i].isEqual([x,y])):
                self.blockList.pop(i)
                break

class Printer():
    def printBlocks(screen,gameMap):
        for i in gameMap.blockList:
            pygame.draw.rect(screen,i.color,i.getRect())
    def printChoser(screen,array):
        for i in array:
            pygame.draw.rect(screen,i[0],i[1])                 

class colorChoser():
    white=((255,255,255), pygame.Rect(1011, 10, 40, 40))
    black=((0,0,0), pygame.Rect(1060, 10, 40, 40))
    pink=((148, 0, 211), pygame.Rect(1011, 10, 40, 40))
    purple=((75, 0, 130), pygame.Rect(1011, 10, 40, 40))
    blue=((0, 0, 255), pygame.Rect(1011, 10, 40, 40))
    green=((0, 255, 0), pygame.Rect(1011, 10, 40, 40))
    yellow=((255,255,255), pygame.Rect(1011, 10, 40, 40))
    orange=((255,255,255), pygame.Rect(1011, 10, 40, 40))
    red=((255,255,255), pygame.Rect(1011, 10, 40, 40))
    def getWindow():
        return [((255,0,0), pygame.Rect(1001, 0, 200, 601)),colorChoser.white,colorChoser.black]

def main():
    pygame.init()
    screen=pygame.display.set_mode((1201,601))
    clock = pygame.time.Clock()
    run=True
    clock = pygame.time.Clock()
    draw=drawMap()
    while run:
        Printer.printChoser(screen,colorChoser.getWindow())
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

if __name__=="__main__":
    main()