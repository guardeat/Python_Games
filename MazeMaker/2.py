import pygame

offsetX=0
offsetY=0

class drawMap():
    def __init__(self,blockSize=32):
        self.x1=0
        self.y1=0
        self.blockList=[]
        self.blockSize=blockSize
    def addBlock(self):
        for i in self.blockList:
            if(i.isEqual([self.x1*self.blockSize,self.y1*self.blockSize])):
                return
        self.blockList.append(Block((self.x1*self.blockSize,self.y1*self.blockSize),self.blockSize,self.blockSize,False))
    def getBlockList(self):
        return self.blockList
    def setPozition(self,location):
        self.x1=(location[0]-offsetX)//self.blockSize
        self.y1=(location[1]-offsetY)//self.blockSize
        self.control=1
        self.addBlock() 
    def deleteBlock(self,location):
        x=((location[0]-offsetX)//self.blockSize)*self.blockSize
        y=((location[1]-offsetY)//self.blockSize)*self.blockSize
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
    def getRectOffset(self):
        return pygame.Rect((self.leftUpCorner[0]+offsetX,self.leftUpCorner[1]+offsetY),(self.width,self.height))

class Printer():
    def printBlocks(screen,gameMap):
        for i in gameMap.blockList:
            pygame.draw.rect(screen,(205, 127, 50),i.getRectOffset())     
    
    def printEnds(screen,gameMap):
        for i in gameMap.blockList:
            pygame.draw.rect(screen,(0, 127, 50),i.getRectOffset())  

    def printPlayerPos(screen,gameMap):
        for i in gameMap.blockList:
            pygame.draw.rect(screen,(200, 0, 50),i.getRectOffset())   

def setWall(wall,wallList):
    #north-west-south-east
    text0=""
    height=wall.height
    pos=wall.leftUpCorner
    wallSides=([pos[0],pos[1]-height],[pos[0]-height,pos[1]],[pos[0],pos[1]+height],[pos[0]+height,pos[1]])

    for side in wallSides:
        flag=False
        for checkWall in wallList:
            if checkWall.leftUpCorner[0]==side[0] and checkWall.leftUpCorner[1]==side[1]:
                text0+="1"
                flag=True
                break

        if not flag:    
            text0+="0"
    
    return text0

def main():
    global offsetX
    global offsetY
    pygame.init()
    run=True
    screen=pygame.display.set_mode((1001,601))
    clock = pygame.time.Clock()
    run=True
    clock = pygame.time.Clock()

    walls=drawMap()
    ends=drawMap()
    playerPos=drawMap()
    chosen=walls


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
                chosen.setPozition(pos)
            if pygame.mouse.get_pressed()[2]:
                pos=pygame.mouse.get_pos()
                chosen.deleteBlock(pos)   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    chosen=walls
                if event.key == pygame.K_e:
                    chosen=ends
                if event.key == pygame.K_w:
                    chosen=playerPos
        
        offsetY +=(keys[pygame.K_UP]-keys[pygame.K_DOWN])*5
        offsetX +=(keys[pygame.K_LEFT]-keys[pygame.K_RIGHT])*5

        Printer.printBlocks(screen,walls)   
        Printer.printEnds(screen,ends) 
        Printer.printPlayerPos(screen,playerPos)


    with open("level_map.txt","w") as levelFile:
        for block in walls.getBlockList(): 
            levelFile.write("w"+setWall(block,walls.getBlockList())+"-"+str(block.leftUpCorner[0])+","+str(block.leftUpCorner[1])+","+str(block.height)+","+str(block.width)+"\n")

        for block in ends.getBlockList(): 
            levelFile.write("e-"+str(block.leftUpCorner[0])+","+str(block.leftUpCorner[1])+","+str(block.height)+","+str(block.width)+"\n")

        for block in playerPos.getBlockList(): 
            levelFile.write("p-"+str(block.leftUpCorner[0])+","+str(block.leftUpCorner[1])+","+str(block.height)+","+str(block.width)+"\n")

if __name__=="__main__":
    main()