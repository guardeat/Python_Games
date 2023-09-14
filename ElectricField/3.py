import math
import pygame

class ChargedObject():
    def __init__(self,charge,pozition):
        self.charge=charge
        self.pozition=pozition
    def getSides(self):
        loc=self.pozition
        x=2
        return [[loc[0]-x,loc[1]-x],[loc[0],loc[1]-x],[loc[0]+x,loc[1]-x],[loc[0]-x,loc[1]],[loc[0]+x,loc[1]],[loc[0]-x,loc[1]+x],[loc[0],loc[1]+x],[loc[0]+x,loc[1]+x]] 

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
        end=[start[0]+self.i,start[1]+self.j]
        return (start,end)
    def format(self):
        magnitude=math.sqrt(self.i**2+self.j**2)  
        self.i=self.i*(2/magnitude)
        self.j=self.j*(2/magnitude)    
            

class Charger():

    ke=15000

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

    def getSumVector(chargedList,pozition):
        vector = Vector(0,0,pozition)
        for i in chargedList:
            vector.add(Charger.getVector(i,pozition))
        vector.format()    
        return vector

    def calculateField(x,y,chargeList):
        vectorList=[]
        for i in chargeList:
            for i2 in i.getSides():
                vectorList.append(Vector(i2[0]-i.pozition[0],i2[1]-i.pozition[1],i.pozition))
                x1=i2[0]
                y1=i2[1]
                vector = Charger.getSumVector(chargeList,[x1,y1])
                k=0
                while(True):
                    k+=1
                    if(i.charge>0):      
                        x1=vector.i+vector.location[0]
                        y1=vector.j+vector.location[1]
                    else:
                        x1=-vector.i+vector.location[0]
                        y1=-vector.j+vector.location[1] 
                    vector = Charger.getSumVector(chargeList,[x1,y1])                       
                    vectorList.append(vector)
                    if(Charger.checkEnd(x,y,vector,chargeList,x1,y1) or k > 1000):
                        break
        return vectorList

    def checkEnd(x,y,vector,chargeList,x1,y1): 
        if(x1>x or y1>y or x1<0 or y1<0):
            return True

        for i in chargeList:        
            if (Charger.calculateDistance(i,[x1,y1])<3):
                return True       

        return False            

class Printer():

    def printVectors(screen,vectorList):
        for i in vectorList:
            line=i.getVisual()
            pygame.draw.line(screen,(255,255,255),line[0],line[1],2)
            
def main():
    pygame.init()
    x=1300
    y=800
    screen=pygame.display.set_mode((x,y))
    clock = pygame.time.Clock()
    run=True

    COList=[]
    COList.append(ChargedObject(1,[705,400]))
    COList.append(ChargedObject(-1,[405,400]))

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