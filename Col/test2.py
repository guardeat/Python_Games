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
        self.mass=1
    def collide(self,jumpSpeed):
        self.speed.add(jumpSpeed)
    def move(self):
        self.center[0] +=self.speed.ivector
        self.center[1] +=self.speed.jvector
    
    def addSpeed(self,vector):
        self.speed.add(vector)

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
            for i in circleList:
                i.move()   

class Gravity():
    def __init__(self):
        self.G=100000
    def calculateDistance(self,planet1,planet2):
        return math.sqrt(math.pow(planet1.center[0]-planet2.center[0],2)+math.pow(planet1.center[1]-planet2.center[1],2))  
    def calculateForce(self,planet1,planet2):
        hip=self.calculateDistance(planet1,planet2) 
        if hip==0:
            hip=1
        mag=self.G*planet1.mass*planet2.mass/(hip*hip)
        x=planet2.center[0]-planet1.center[0]
        y=planet2.center[1]-planet1.center[1]
        return Vector(mag*x/hip,mag*y/hip)
    def calculateSpeed(self,force,seconds,mass):
        return Vector(force.ivector*seconds/mass,force.jvector*seconds/mass) 

    def eventMaker(self,planetlist,seconds):
        gravity=Gravity()
        for i in range(len(planetlist)):
            for i2 in range(i+1,len(planetlist)):
                force=gravity.calculateForce(planetlist[i],planetlist[i2])
                speed1=gravity.calculateSpeed(force,seconds,planetlist[i].mass)
                speed2=gravity.calculateSpeed(Vector(-1*force.ivector,-1*force.jvector),seconds,planetlist[i2].mass)
                planetlist[i2].addSpeed(speed2)
                planetlist[i].addSpeed(speed1)  

def drawCircle(screen,circleList,x,y,k):
    for i in circleList:
        location=[int(i.center[0]/k),int(i.center[1]/k)]
        radius= int(i.radius/k)
        if radius == 0:
            radius =1
        pygame.draw.circle(screen, (255,255,255),(location[0]+x/k, location[1]+y/k) , radius, 1)
        
def main():
    pygame.init()
    screen=pygame.display.set_mode((1500,750))
    clock = pygame.time.Clock()
    run=True
    circleList=[]
    pressing=False
    a=10

    gravity=Gravity()

    x = 0
    y = 0
    k = 1

    while run:
        screen.fill((0,0,0))
        clock.tick(30)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()    
            if event.type == pygame.QUIT:
                run = False
            if event.type==pygame.MOUSEBUTTONDOWN or pressing:
                if pygame.mouse.get_pressed()[0]:
                    pressing=True
                    pos=pygame.mouse.get_pos()
                    circleList.append(Circle([pos[0]*k - x,pos[1]*k - y],a))   
            if event.type==pygame.MOUSEBUTTONUP:
                pressing=False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    a+=2
                elif event.button == 5:
                    a-=2    
        y += (keys[pygame.K_w]-keys[pygame.K_s])*k*k   
        x += (keys[pygame.K_a]-keys[pygame.K_d])*k*k 
        k +=(keys[pygame.K_o]-keys[pygame.K_l])*(k/10)  
        drawCircle(screen,circleList,x,y,k)  
        eventHandler.mover(circleList) 
        gravity.eventMaker(circleList,1/1000) 
        pygame.display.update()    

if __name__=="__main__":
    main() 