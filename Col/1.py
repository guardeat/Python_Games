import math
import pygame

class Vector():

    def __init__(self,ivector,jvector):
        self.ivector=ivector
        self.jvector=jvector
    def add(self,vector):
        self.ivector+=vector.ivector
        self.jvector+=vector.jvector
    def div(self,vector):
        if(self.ivector>1):
            self.ivector/=vector.ivector
        if(self.jvector>1):
            self.jvector/=vector.jvector   

class Circle():
    def __init__(self,center,radius):
        self.center=center
        self.radius=radius
        self.speed=Vector(0,0)
    def collide(self,jumpSpeed):
        self.speed.add(jumpSpeed)
    def move(self):
        self.center[0] +=self.speed.ivector
        self.center[1] +=self.speed.jvector  

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
        
        if distance==0: 
            distance=0.1
        i=(circle1.center[0]-circle2.center[0])/(distance)
        j=(circle1.center[1]-circle2.center[1])/(distance)

        vector1=Vector(i,j)
        vector1.div(circle1.speed)
        vector2=Vector(-i,-j)
        vector2.div(circle2.speed)

        print(i,j)
        circle1.collide(vector1)
        circle2.collide(vector2)

    def mover(circleList):
        for i in circleList:
            i.move()  

    def addGravity(circleList):
        ac=Vector(0,3)
        for i in circleList:
            i.speed.add(ac)


def drawCircle(screen,circleList):
    for i in circleList:
        pygame.draw.circle(screen,(255,255,255),i.center,i.radius)
        



def main():
    pygame.init()
    screen=pygame.display.set_mode((1500,750))
    clock = pygame.time.Clock()
    run=True
    circleList=[]
    circleList.append(Circle([500,500],5))
    circleList.append(Circle([505,497],10))
    circleList.append(Circle([503,496],5))
    while run:
        screen.fill((0,0,0))
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        drawCircle(screen,circleList)        
        eventHandler.checkCircles(circleList)   
        eventHandler.mover(circleList) 
        eventHandler.addGravity(circleList)
        pygame.display.update()    

if __name__=="__main__":
    main()             