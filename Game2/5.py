import pygame

xSize=1000
ySize=600

class Keyboard:

    keyList={"w":False,"a":False,"s":False,"d":False}
    
    def updateKeys(keys):

        Keyboard.keyList["w"]=keys[pygame.K_w]
        Keyboard.keyList["s"]=keys[pygame.K_s]
        Keyboard.keyList["a"]=keys[pygame.K_a]
        Keyboard.keyList["d"]=keys[pygame.K_d]


class Entity:

    def __init__(self,location,speed=5,w=15,h=15):
        self.loc=location
        self.speed=speed
        self.h=h
        self.w=w
        self.oldloc=location.copy()
    
    def run(self):
        
        pass

    def getShape(self):

        return (self.loc[0],self.loc[1],self.w,self.h)

    def centerX(self):

        return self.loc[0]+self.w/2

    def centerY(self):

        return self.loc[1]+self.h/2

    def getCorners(self):
        return [[self.loc[0],self.loc[1]],[self.loc[0]+self.w,self.loc[1]],[self.loc[0],self.loc[1]+self.h],[self.loc[0]+self.w,self.loc[1]+self.h]]




class Player(Entity):

    def __init__(self,location,speed=5,w=15,h=15):
        super().__init__(location,speed,w,h)

    def run(self):

        self.oldloc=self.loc.copy()

        if Keyboard.keyList["w"]:
            self.loc[1] -= self.speed
        if Keyboard.keyList["s"]:
            self.loc[1] += self.speed
        if Keyboard.keyList["a"]:
            self.loc[0] -= self.speed
        if Keyboard.keyList["d"]:
            self.loc[0] += self.speed


def renderEntities(window,entityList,offset):
    for entity in entityList:
        rect=entity.getShape()
        pygame.draw.rect(window,(255,255,255),pygame.Rect(rect[0]-offset[0]+xSize/2,rect[1]-offset[1]+ySize/2,rect[2],rect[3]))

def renderWalls(window,wallList,offset):
    for wall in wallList:
        rect=wall.getShape()
        pygame.draw.rect(window,(255,0,0),pygame.Rect(rect[0]-offset[0]+xSize/2,rect[1]-offset[1]+ySize/2,rect[2],rect[3]))

def renderEnds(window,endList,offset):
    for end in endList:
        rect=end.getShape()
        pygame.draw.rect(window,(0,255,0),pygame.Rect(rect[0]-offset[0]+xSize/2,rect[1]-offset[1]+ySize/2,rect[2],rect[3]))

def runEntities(entityList):
    for entity in entityList:
        entity.run()


class Collider:

    def solveEntity_Wall(entityList,wallList):

        for i in range(len(wallList)):
            control=wallList[i].getCorners()
            for corner in entityList[0].getCorners():
                if(corner[0]>control[0][0] and corner[0]<control[1][0] and corner[1]>control[1][1] and corner[1]<control[3][1]):
                    Collider.solve(entityList[0],wallList[i])
                    break 
    
    def solve(entity,wall):
        w = 0.5 * (entity.w + wall.w)
        h = 0.5 * (entity.h + wall.h)
        dx = entity.centerX() - wall.centerX()
        dy = entity.centerY() - wall.centerY()

        if (abs(dx) <= w and abs(dy) <= h):
            wy = w * dy
            hx = h * dx

            if (wy > hx):
                if (wy > -hx):
                    print("bottom")
                    entity.loc[1]+=5
                else:
                    print("left")
                    entity.loc[0]-=5
            else:
                if (wy > -hx):
                    print("right")
                    entity.loc[0]+=5
                else:
                    print("top")
                    entity.loc[1]-=5
    
    def solveEntity_End(entityList,endList):

        for i in range(len(endList)):
            control=endList[i].getCorners()
            for corner in entityList[0].getCorners():
                if(corner[0]>control[0][0] and corner[0]<control[1][0] and corner[1]>control[1][1] and corner[1]<control[3][1]):
                    return True 
        
        return False

def importMap(fileName):
    with open(fileName,"r") as levelFile:
        blocks=levelFile.readlines()

    wallList=[]
    endList=[]
    playerPos=[]

    for block in blocks:
        flag=block.split("-")[0]
        block=block.split("-")[1]
        block=[int(i) for i in block.split(",")]
        if flag=="w":
            wallList.append(Entity([block[0],block[1]],0,block[2],block[3]))
        if flag == "e":
            endList.append(Entity([block[0],block[1]],0,block[2],block[3]))
        if flag=="p":
            playerPos=[block[0],block[1]]
        

    return (wallList,endList,playerPos)

def main():

    pygame.init()
    screen=pygame.display.set_mode((xSize,ySize))
    clock = pygame.time.Clock()
    run=True

    blocks=importMap("level_map.txt")
    wallList=blocks[0]
    endList=blocks[1]
    playerPos=blocks[2]

    player=Player(playerPos,5,20,20)

    offset=player.loc

    entityList=[player]

    while run:
        screen.fill((0,0,0))
        clock.tick(30)
        for event in pygame.event.get():

            keys = pygame.key.get_pressed()  
            
            if event.type == pygame.QUIT:
                run = False
        
        Keyboard.updateKeys(keys)

        renderWalls(screen,wallList,offset)
        renderEnds(screen,endList,offset)
        runEntities(entityList)
        Collider.solveEntity_Wall(entityList,wallList)
        
        if Collider.solveEntity_End(entityList,endList):
            run=False

        renderEntities(screen,entityList,offset)
        pygame.display.update()   

 

if __name__=="__main__":
    main()             
