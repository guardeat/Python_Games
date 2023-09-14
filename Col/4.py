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
        self.speed.ivector*=0.97
        self.speed.jvector*=0.97

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
        
        if distance<0.01: 
            return
        try:    
            i=5*(circle1.radius+circle2.radius-distance)*abs(circle1.center[0]-circle2.center[0])/(circle1.center[0]-circle2.center[0])
            j=5*(circle1.radius+circle2.radius-distance)*abs(circle1.center[1]-circle2.center[1])/(circle1.center[1]-circle2.center[1])
        except:
            i=0.01
            j=0.01
        
        vector1=Vector(i,j)
        vector2=Vector(-i,-j)


        circle1.collide(vector1)
        circle2.collide(vector2)

    def mover(circleList):
        for i2 in range(5):
            eventHandler.checkCircles(circleList)          
            eventHandler.addGravity(circleList)
            eventHandler.checkBordes(circleList,[700,400],300)
            for i in circleList:
                i.move()  

    def addGravity(circleList):
        ac=Vector(0,2.5)
        for i in circleList:
            i.speed.add(ac)

    def checkBordes(circleList,center,radius):

        for circle in circleList:
            distance=eventHandler.getDistance(circle.center,center)
            if(distance>(radius-circle.radius)):
                a=abs(circle.center[0]-center[0])
                b=abs(circle.center[1]-center[1])
                signa=-abs(circle.center[0]-center[0])/(circle.center[0]-center[0])
                signb=-abs(circle.center[1]-center[1])/(circle.center[1]-center[1])
                if a==0:
                    a=0.01
                c=math.hypot(b,b**2/a)
                i=b*circle.speed.getLength()/(c*1.2)*signa
                j=(b**2/a*circle.speed.getLength())/(c*1.2)*signb
                circle.speed=Vector(i,j)



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
    while run:
        screen.fill((0,0,0))
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type==pygame.MOUSEBUTTONDOWN or pressing:
                pressing=True
                pos=pygame.mouse.get_pos()
                circleList.append(Circle([pos[0],pos[1]],10))   
            if event.type==pygame.MOUSEBUTTONUP:
                pressing=False 
        pygame.draw.circle(screen,(255,0,0),[700,400],300,1)        
        drawCircle(screen,circleList)   
        eventHandler.mover(circleList) 
        pygame.display.update()    

if __name__=="__main__":
    main() 