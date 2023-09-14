import math
import pygame

class ChargedObject():
    def __init__(self,charge,pozition):
        self.charge=charge
        self.pozition=pozition

class Vector():
    def __init__(self,i,j,location):
        self.i=i
        self.j=j
        self.location=location
    def add(self,vector):
        self.i += vector.i
        self.j += vector.j    
    def getVisual(self):
        start=self.location
        end=[int(start[0]+self.i),int(start[1]+self.j)]
        return (start,end)

class Charger():

    ke=150000

    def calculateCharge(chargedList,location):
        fieldVector=Vector(0,0,location)
        for i in chargedList:
            fieldVector.add(Charger.getVector(i,location))   
        if(fieldVector.i>10):
            fieldVector.i=10
        elif(fieldVector.i<-10):
            fieldVector.i=-10
        if(fieldVector.j>10):
            fieldVector.j=10
        elif(fieldVector.j<-10):
            fieldVector.j=-10       
        return fieldVector    

    def getVector(charged,point):
        distance=Charger.calculateDistance(charged,point)
        if(distance==0):
            return Vector(0,0,point)
        magnitude=Charger.getMagnitude(charged,distance)
        ivector=magnitude*((point[0]-charged.pozition[0])/distance)
        jvector=magnitude*((-charged.pozition[1]+point[1])/distance)
        return Vector(ivector,jvector,point)
      
    def getMagnitude(charged,distance):
        return Charger.ke*charged.charge/distance**2

    def calculateDistance(charged,point):
        return math.sqrt((charged.pozition[0]-point[0])**2+(charged.pozition[1]-point[1])**2)

    def calculateField(x,y,chargeList):
        vectorList=[]
        for i in range(0,x,20):
            for i2 in range(0,y,20):
                vectorList.append(Charger.calculateCharge(chargeList,[i,i2]))
        return vectorList

class Printer():

    def printVectors(screen,vectorList):
        for i in vectorList:
            line=i.getVisual()
            pygame.draw.line(screen,(255,255,255),line[0],line[1],1)
            pygame.draw.circle(screen,(255,255,0),line[1],1)

def main():
    pygame.init()
    x=1300
    y=800
    screen=pygame.display.set_mode((x,y))
    clock = pygame.time.Clock()
    run=True

    COList=[]
    COList.append(ChargedObject(1,[305,200]))
    COList.append(ChargedObject(-1,[505,200]))

    pressing=False
    while run:
        clock.tick(30)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type==pygame.MOUSEBUTTONDOWN or pressing:
                if pressing and len(COList)>2:
                    COList.pop() 
                if pygame.mouse.get_pressed()[0]:
                    COList.append(ChargedObject(1,pygame.mouse.get_pos())) 
                elif pygame.mouse.get_pressed()[2]:
                    COList.append(ChargedObject(-1,pygame.mouse.get_pos()))    
                pressing=True    
            elif event.type==pygame.MOUSEBUTTONUP:
                pressing=False
                COList.pop()     
            keys = pygame.key.get_pressed()
        vectorList=Charger.calculateField(x,y,COList)
        Printer.printVectors(screen,vectorList)
        pygame.display.update() 

if __name__=="__main__":
    main()

        
