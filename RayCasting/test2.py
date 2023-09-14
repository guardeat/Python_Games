import math
import pygame

SIZEX=1200
SIZEY=600

class LightSource:

    def __init__(self,location=[0,0],dens=12):
        self.location=location
        self.dens=dens
        self.rays=self.getRawRays()
    def getRawRays(self):
        rayList=[]
        for i in range(self.dens):
            alpha=(math.pi/180)*(i*360/self.dens)+0.00001
            rayList.append([math.cos(alpha)*2000,-math.sin(alpha)*2000])
        return rayList 
    def resetRays(self):
        self.rays=self.getRawRays()     
    
class Wall:

    def __init__(self,point1,point2):
        self.point1=point1
        self.point2=point2  
    def getAim(self):
        return (self.point1[1]-self.point2[1])/(self.point1[0]-self.point2[0])   


def updateRays(wallList,lightSource,screen):
    loc=lightSource.location
    for ray in lightSource.rays:
        for wall in wallList:

            mRay=ray[1]/(ray[0])
            mWall=wall.getAim()
            inter_x=(mRay*loc[0]-mWall*wall.point1[0]+wall.point1[1]-loc[1])/(mRay-mWall+0.0000001)    
            inter_y=mWall*(inter_x-wall.point1[0])+wall.point1[1]
            if(inter_x>min(loc[0]+ray[0],loc[0]) and inter_x<max(loc[0]+ray[0],loc[0]) 
                and inter_x>min(wall.point1[0],wall.point2[0]) and inter_x<max(wall.point1[0],wall.point2[0])):
                ray[0]=inter_x-loc[0]
                ray[1]=inter_y-loc[1]
                

def drawRays(screen,lightSource):
    for i in lightSource.rays:
        loc=lightSource.location
        pygame.draw.line(screen,(255,255,255),lightSource.location,[loc[0]+i[0],loc[1]+i[1]])


def drawWalls(screen,wallList):
    for i in wallList:
        pygame.draw.line(screen,(255,0,255),i.point1,i.point2,3)

def showInters(screen,lightSource):
    loc=lightSource.location
    for ray in lightSource.rays:
          pygame.draw.circle(screen,(255,255,0),[ray[0]+loc[0],ray[1]+loc[1]],2)         


def main():
    pygame.init()
    screen=pygame.display.set_mode((SIZEX,SIZEY))
    clock = pygame.time.Clock()
    run=True
    lightSource=LightSource([300,300],360)
    pressing=False
    wallList=[Wall([300,50],[301,500]),Wall([700,50],[701,300]),Wall([300,50],[700,50])
    ,Wall([301,500],[501,500]),Wall([30,50],[70,300]),Wall([90,310],[110,500]),Wall([601,500],[701,500]),Wall([700,350],[701,500])]

    while run:

        screen.fill((0,0,0))
        clock.tick(600)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  
            if event.type==pygame.MOUSEBUTTONDOWN or pressing:
                lightSource.location=pygame.mouse.get_pos()
                pressing=True   
            if event.type==pygame.MOUSEBUTTONUP:
                pressing=False 

        lightSource.resetRays()        
        drawWalls(screen,wallList)            
        updateRays(wallList,lightSource,screen)
        drawRays(screen,lightSource) 
        showInters(screen,lightSource)  

        pygame.display.update()   

if __name__=="__main__":
    main() 