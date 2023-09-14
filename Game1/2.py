import pygame

class Enemy():
    def __init__(self,location,direction):
        self.xlocation=location[0]
        self.ylocation=location[1]
        self.direction=direction
        self.width=15
        self.height=25
        self.speed=3*direction
        self.yspeed=0
    def changeDirection(self):
        self.direction=-1 if self.direction==1 else 1
        self.speed=-1*self.speed
    def move(self,gameMap):
        Physics.gravity(self,gameMap)
        for i in range(self.yspeed):
                if(not gameMap.checkLandBlock(self.getLowestPoints())):
                    self.yspeed=0
                    break
                self.ylocation+=1
        self.addxLocation(gameMap)                
    def addxLocation(self,gamemap):
        if(self.yspeed==0):
            if(self.direction>0):
                for i in range(self.speed):
                    if(gamemap.checkCollRight(self.getLeftSidePoints())):
                        self.xlocation-=1   
                    else:
                        self.changeDirection()
                        break    
            elif(self.direction<0):
                for i in range(abs(self.speed)):
                    if(gamemap.checkCollLeft(self.getRightSidePoints())):
                        self.xlocation+=1 
                    else:
                        self.changeDirection()  
                        break  
    def getLowestPoints(self):
        return [[self.xlocation,self.ylocation+self.height],[self.xlocation+self.width,self.ylocation+self.height]]  
    def getUpperPoints(self):
        return [[self.xlocation,self.ylocation],[self.xlocation+self.width,self.ylocation]]
    def getLeftSidePoints(self):
        return [[self.xlocation,self.ylocation],[self.xlocation,self.ylocation+self.height]]
    def getRightSidePoints(self):
        return [[self.xlocation+self.width,self.ylocation],[self.xlocation+self.width,self.ylocation+self.height]] 
    def getRect(self):
        return pygame.Rect((self.xlocation,self.ylocation),(self.width,self.height)) 
    def getBlock(self):
        return Block([self.xlocation,self.ylocation],self.height,self.width,False)                          

class AllEnemies:
    def __init__(self):
        self.enemylist=[]
        self.enemyblocklist=[]
    def addEnemy(self,enemy):
        self.enemylist.append(enemy)
        self.enemyblocklist.append(enemy.getBlock())
    def moveAll(self,gamemap):
        for i in range(len(self.enemylist)):
            self.enemylist[i].move(gamemap) 
            self.enemyblocklist[i]=self.enemylist[i].getBlock()
    def checkPlayertouch(self,player):
        playerpoints=player.getUpperPoints()+player.getLowestPoints()
        flag=False
        for i in self.enemylist:
            for i2 in playerpoints:
                x3=i2[0]
                y3=i2[1]
                x1=i.xlocation
                x2=i.xlocation+i.width
                y1=i.ylocation
                y2=i.ylocation+i.height
                if(x2>=x3 and x3>=x1 and y2>=y3 and y3>=y1):
                    player.checkDie(True)
                    flag=True
            if(flag):
                break        


class Player():
    def __init__(self):
        self.xlocation=0
        self.ylocation=0
        self.xspeed=0
        self.yspeed=0
        self.height=30
        self.width=10
        self.jumpc=0
    def getLowestPoints(self):
        return [[self.xlocation,self.ylocation+self.height],[self.xlocation+self.width,self.ylocation+self.height]]
    def getUpperPoints(self):
        return [[self.xlocation,self.ylocation],[self.xlocation+self.width,self.ylocation]]
    def getLeftSidePoints(self):
        return [[self.xlocation,self.ylocation],[self.xlocation,self.ylocation+self.height]]
    def getRightSidePoints(self):
        return [[self.xlocation+self.width,self.ylocation],[self.xlocation+self.width,self.ylocation+self.height]]
    def moveWithSpeed(self,gameMap):
        if(self.yspeed>0):   
            for i in range(self.yspeed):
                if(not gameMap.checkLandBlock(self.getLowestPoints())):
                    self.yspeed=0
                    break
                self.ylocation+=1
        elif(self.jumpc>0):
            for i in range(self.jumpc):
                if(not gameMap.checkUpperBlock(self.getUpperPoints())):
                    self.jumpc=0
                    break
                self.ylocation-=1
            self.yspeed-=2
            self.jumpc-=1
        self.checkDie()    
    def addxLocation(self,x,gamemap):
        if(x<0):
            for i in range(abs(x)):
                if(gamemap.checkCollRight(self.getLeftSidePoints())):
                    self.xlocation-=1    
        elif(x>0):
            for i in range(x):
                if(gamemap.checkCollLeft(self.getRightSidePoints())):
                    self.xlocation+=1     
    def jump(self,gameMap):
        if(not gameMap.checkLandBlock(self.getLowestPoints())):
            self.jumpc=15       
    def checkDie(self,status=False):
        if(self.ylocation>600 or status):
            self.ylocation=0
            self.xlocation=0
            self.yspeed=0        

class Physics():
    def gravity(player,gameMap):
        if(gameMap.checkLandBlock(player.getLowestPoints())):
            if(player.yspeed<31):
                player.yspeed+=2  
            
class GameMap():
    def __init__(self):
        self.blockList=[]
    def addBlock(self,block):
        self.blockList.append(block) 
    def checkLandBlock(self,location):
        for i in self.blockList:
            if(i.isUnder(location)):
                return False
        return True
    def checkUpperBlock(self,location):
        for i in self.blockList:
            if(i.isOnit(location)):
                print("There is a block on it")
                return False
        return True 
    def checkCollLeft(self,location):
        for i in self.blockList:
            if(i.isColLeft(location)):
                print("LeftCollition")
                return False
        return True
    def checkCollRight(self,location):
        for i in self.blockList:
            if(i.isColRight(location)):
                print("RightCollition")
                return False
        return True           

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
    def isUnder(self,location):
        if(self.leftUpCorner[1]==location[0][1] and (location[1][0]-self.leftUpCorner[0]>0 and self.leftUpCorner[0]+self.width-location[0][0]>0)):
            return True
        return False
    def isOnit(self,location): 
        if(self.leftUpCorner[1]+self.height==location[1][1] and (location[1][0]-self.leftUpCorner[0]>0 and self.leftUpCorner[0]+self.width-location[0][0]>0)):
            return True
        return False
    def isColLeft(self,location):
        y1=self.leftUpCorner[1]
        y2=self.leftUpCorner[1]+self.height
        y3=location[0][1]
        y4=location[1][1]
        con1=y3<y2 and y3>y1
        con2=y4<y2 and y4>y1
        con3=y1>y3 and y1<y4
        con4=y2>y3 and y2<y4
        if(self.leftUpCorner[0]==location[1][0] and (con1 or con2 or con3 or con4)):
            return True
        return False    
    def isColRight(self,location2):
        y1=self.leftUpCorner[1]
        y2=self.leftUpCorner[1]+self.height
        y3=location2[0][1]
        y4=location2[1][1]
        con1=y3<y2 and y3>y1
        con2=y4<y2 and y4>y1
        con3=y1>y3 and y1<y4
        con4=y2>y3 and y2<y4
        if(self.leftUpCorner[0]+self.width==location2[1][0] and (con1 or con2 or con3 or con4)):
            return True
        return False 
    def isEqual(self,location):
        if(location[0]==self.leftUpCorner[0] and location[1]==self.leftUpCorner[1]):
            return True
        return False         

class Printer():
    def printBlocks(screen,gameMap):
        for i in gameMap.blockList:
            pygame.draw.rect(screen,(205, 127, 50),i.getRect())    
    def printPlayer(screen,player):
        pygame.draw.rect(screen,(255,0,0),(player.xlocation,player.ylocation,player.width,player.height))  
    def printEnemy(screen,enemylist):
        for i in enemylist:
            pygame.draw.rect(screen,(250,0,0),i.getRect())  

class drawMap():
    def __init__(self):
        self.x1=0
        self.y1=0
        self.blockList=[]
    def addBlock(self):
        for i in self.blockList:
            if(i.isEqual([self.x1*20,self.y1*20])):
                return
        self.blockList.append(Block((self.x1*20,self.y1*20),20,20,False))
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

def main():
    pygame.init()
    run=True
    screen=pygame.display.set_mode((1001,601))
    clock = pygame.time.Clock()
    gameMap=GameMap()
    player=Player()
    run=True
    clock = pygame.time.Clock()
    draw=drawMap()
    enemy1=Enemy([100,0],-1)
    enemy2=Enemy([200,0],1)
    enemies=AllEnemies()
    enemies.addEnemy(enemy1)
    enemies.addEnemy(enemy2)
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

    for i in blocks:
        gameMap.addBlock(i)
    run=True
    while run:
        pygame.display.update()
        screen.fill((0,100,200))
        clock.tick(30)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()  
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump(gameMap)                
        x=0        
        x -= (keys[pygame.K_a]-keys[pygame.K_d])*5
        player.addxLocation(x,gameMap)
        enemies.moveAll(gameMap)
        Physics.gravity(player,gameMap)
        player.moveWithSpeed(gameMap)
        enemies.checkPlayertouch(player)
        Printer.printBlocks(screen,gameMap) 
        Printer.printPlayer(screen,player)  
        Printer.printEnemy(screen,enemies.enemylist)

if __name__=="__main__":
    main()
