import math
import pygame

class Vector():

    def __init__(self,ivector,jvector):
        self.ivector=ivector
        self.jvector=jvector
    def add(self,vector):
        self.ivector+=vector.ivector
        self.jvector+=vector.jvector  
    def getLength(self):
        return math.hypot(self.ivector,self.jvector)

class Circle():
    def __init__(self,center,radius):
        self.center=center
        self.radius=radius
        self.speed=Vector(0,0)
    def collide(self,jumpSpeed):
        self.speed.add(jumpSpeed)
    def move(self):
        self.center[0] +=self.speed.ivector/50
        self.center[1] +=self.speed.jvector/50
        self.speed.ivector*=0.90
        self.speed.jvector*=0.90

class eventHandler():
    def checkCircles(circleList):
        for i in range(len(circleList)-1):
            for i2 in range(i,len(circleList)):
                distance=eventHandler.getDistance(circleList[i].center,circleList[i2].center)
                if(distance<(circleList[i].radius+circleList[i2].radius)):
                    eventHandler.collider(circleList[i],circleList[i2],distance)

    def getDistance(loc1,loc2):
        return math.sqrt((loc1[0]-loc2[0])**2+(loc1[1]-loc2[1])**2)           

    def collider(circle1,circle2,distance):
        if(distance==0):
            distance=0.0001
        y=circle1.center[1]-circle2.center[1]
        x=circle1.center[0]-circle2.center[0]
        n=[x/distance,y/distance]
        a=(circle1.radius+circle2.radius)/2
        delta=2*a-distance
        circle1.center=[circle1.center[0]+n[0]*delta/2,circle1.center[1]+n[1]*delta/2]
        circle2.center=[circle2.center[0]-n[0]*delta/2,circle2.center[1]-n[1]*delta/2]

        

    def mover(circleList):
        for i2 in range(8):
            eventHandler.addGravity(circleList) 
            eventHandler.checkCircles(circleList) 
            eventHandler.checkBordes(circleList,[700,350],400)      
            for i in circleList:
                i.move()   

    def addGravity(circleList):
        ac=Vector(0,6)
        for i in circleList:
            i.speed.add(ac)

    def checkBordes(circleList,center,radius):

        for circle in circleList:
            distance=eventHandler.getDistance(circle.center,center)
            if(distance>(radius-circle.radius)):
                y=circle.center[1]-center[1]
                x=circle.center[0]-center[0]
                n=[x/distance,y/distance]
                circle.center=[center[0]+n[0]*(radius-circle.radius),center[1]+n[1]*(radius-circle.radius)]



def drawCircle(screen,circleList):
    for i in circleList:
        pygame.draw.circle(screen,(255,255,255),i.center,i.radius,0)
        



def main():
    pygame.init()
    screen=pygame.display.set_mode((1500,750))
    clock = pygame.time.Clock()
    run=True
    circleList=[]
    pressing=False
    a=30
    while run:
        screen.fill((255,255,255))
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type==pygame.MOUSEBUTTONDOWN or pressing:
                if pygame.mouse.get_pressed()[0]:
                    pressing=True
                    pos=pygame.mouse.get_pos()
                    circleList.append(Circle([pos[0],pos[1]],a))   
            if event.type==pygame.MOUSEBUTTONUP:
                pressing=False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    a+=2
                elif event.button == 5:
                    a-=2 
        pygame.draw.circle(screen,(0,0,0),[700,350],400,0)        
        drawCircle(screen,circleList)   
        eventHandler.mover(circleList) 
        pygame.display.update()    

if __name__=="__main__":
    main() 