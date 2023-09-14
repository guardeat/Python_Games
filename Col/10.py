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
        y=circle1.center[1]-circle2.center[1]
        x=circle1.center[0]-circle2.center[0]
        try:
            signx=abs(circle1.center[0]-circle2.center[0])/(circle1.center[0]-circle2.center[0])
            signy=abs(circle1.center[1]-circle2.center[1])/(circle1.center[1]-circle2.center[1])
        except:
            signx=1
            signy=1
        if(x==0):
            x=0.01        
        m=abs(y/x)
        k=(circle1.radius+circle2.radius-distance)/1.2
        x2=k/math.sqrt(m**2+1)*signx
        y2=abs(m*x2)*signy
        circle1.center=[circle1.center[0]+x2,circle1.center[1]+y2]
        circle2.center=[circle2.center[0]-x2,circle2.center[1]-y2]

        

    def mover(circleList):
        for i2 in range(5):
            eventHandler.checkCircles(circleList)  
            eventHandler.addGravity(circleList)        
            for i in circleList:
                i.move()  
            eventHandler.checkBordes(circleList,[700,200],400)    

    def addGravity(circleList):
        ac=Vector(0,7)
        for i in circleList:
            i.speed.add(ac)

    def checkBordes(circleList,center,radius):

        for circle in circleList:
            distance=eventHandler.getDistance(circle.center,center)
            if(distance>(radius-circle.radius)):
                y=center[1]-circle.center[1]
                x=center[0]-circle.center[0]
                signx=abs(center[0]-circle.center[0])/(center[0]-circle.center[0])
                signy=abs(center[1]-circle.center[1])/(center[1]-circle.center[1])
                m=y/x
                k=distance+circle.radius-radius
                x2=k/math.sqrt(m**2+1)*signx
                y2=abs(m*x2)*signy
                circle.center=[circle.center[0]+x2,circle.center[1]+y2]



def drawCircle(screen,circleList):
    for i in circleList:
        pygame.draw.circle(screen,(255,255,255),i.center,i.radius,2)
        



def main():
    pygame.init()
    screen=pygame.display.set_mode((1500,750))
    clock = pygame.time.Clock()
    run=True
    circleList=[]
    pressing=False
    a=30
    while run:
        screen.fill((0,0,0))
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
        pygame.draw.circle(screen,(255,0,0),[700,200],400,1)        
        drawCircle(screen,circleList)   
        eventHandler.mover(circleList) 
        pygame.display.update()    

if __name__=="__main__":
    main() 