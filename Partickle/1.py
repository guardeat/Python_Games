import pygame
import random

class Vector:

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def add(self,aimVector):
        self.x+=aimVector.x
        self.y+=aimVector.y

class Partickle:

    def __init__(self,loc,xsize,ysize):

        self.loc=loc
        self.xsize=xsize
        self.ysize=ysize
        self.isStatic=False 
        self.speed=Vector(0,10)

    def move(self,dt):
        self.loc[0]+=self.speed.x*dt
        self.loc[1]+=self.speed.y*dt
        self.isStatic=False
        if(self.loc[1]>800-self.ysize-10):
            self.loc[1]=800-self.ysize-10

def drawPartickle(screen,aimList):
    a=0
    for i in aimList:
        pygame.draw.rect(screen,(0,50-a%50,150+a%100),pygame.Rect(i.loc[0],i.loc[1], i.xsize, i.ysize))
        a+=4

def moveAll(aimList,dt):
    for i in aimList:
        i.move(dt)

def solveColl(aimList):
    for i in range(len(aimList)):
        for i2 in range(i+1,len(aimList)):
            temp=aimList[i2].loc[1]+aimList[i2].ysize-aimList[i].loc[1]
            temp2=aimList[i2].loc[1]-aimList[i].ysize-aimList[i].loc[1]
            if(temp>0 and temp2<0 and aimList[i].loc[0]==aimList[i2].loc[0]):
                aimList[i2].loc[1]-=temp
                aimList[i2].isStatic=True

def fluid(aimList,k):

    for i in aimList:
        flag=True
        con1=False
        con2=False
        for i2 in aimList:
            if (i2.loc[0]== i.loc[0] and i.loc[1]-i.ysize==i2.loc[1]):
                flag=False
                break  
            if(not con1):
                if (i.loc==[i2.loc[0]-i.xsize,i2.loc[1]]or i.loc[0]+i.ysize>1300):
                    con1=True
            if(not con2):        
                if (i.loc==[i2.loc[0]+i.xsize,i2.loc[1]]or i.loc[0]-i.ysize<0):
                    con2=True      
        if(i.isStatic and flag):
            number = random.randint(0,k)
            if number == k and (not con1):
                i.loc[0]+=i.xsize
            elif number == 0 and (not con2):
                i.loc[0]-=i.ysize    


def main():
    pygame.init()
    x=1300
    y=800
    screen=pygame.display.set_mode((x,y))
    clock = pygame.time.Clock()
    run=True

    size=10

    aimList=[]

    pressing = False
    while run:
        clock.tick(30)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type==pygame.MOUSEBUTTONDOWN or pressing:
                if pygame.mouse.get_pressed()[0]:
                    aimList.append(Partickle([pygame.mouse.get_pos()[0]//size*size,pygame.mouse.get_pos()[1]//size*size],size,size))    
                pressing=True    
            elif event.type==pygame.MOUSEBUTTONUP:
                pressing=False
        moveAll(aimList,1)  
        solveColl(aimList)
        fluid(aimList,1) 
        drawPartickle(screen,aimList)     
        pygame.display.update() 

if __name__=="__main__":
    main()