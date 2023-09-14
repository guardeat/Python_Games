import pygame

def getDirections(location):
    x=location[0]
    y=location[1]
    return ([x+1,y+1],[x-1,y-1],[x+1,y-1],[x-1,y+1],[x,y+1],[x,y-1],[x+1,y],[x-1,y])

def findNeighbours(location,rectPozitions):
    neighbours=0
    directions=getDirections(location)
    for i in directions:
        if i in rectPozitions:
            neighbours+=1
    return neighbours        

def aliveOrDie(location,rectPozitions):
    neighbors=findNeighbours(location,rectPozitions)
    if(neighbors==3):
        return "Alive"
    if(neighbors<2 or neighbors>3):
        return "Death"
    return "Same"

def operate(rectPozitions):
    removelist=[]
    appendlist=[]
    for i in range(50):
        for i2 in range(30):
            condition=aliveOrDie([i,i2],rectPozitions)
            if(condition=="Alive"):
                if not([i,i2] in rectPozitions):
                    appendlist.append([i,i2])
            elif(condition=="Death"):
                if([i,i2] in rectPozitions):
                    removelist.append([i,i2])                    
    for i in removelist:
        rectPozitions.remove(i)
    for i in appendlist:
        rectPozitions.append(i)   

def main():
    pygame.init()
    run=True
    screen=pygame.display.set_mode((1001,601))
    clock = pygame.time.Clock()
    for i in range(50):
        pygame.draw.line(screen, (0,255,0), (i*20, 0), (i*20, 601))
    for i in range(30):
        pygame.draw.line(screen, (0,255,0), (0, i*20), (1001, i*20))
    rectPozitions=[]   
    while run:
        pygame.display.update()
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    run=False    
            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                pos=[pos[0]//20,pos[1]//20]
                if not(pos in rectPozitions):
                    pygame.draw.rect(screen,(255,255,255),(pos[0]*20+1,pos[1]*20+1,19,19))
                    rectPozitions.append(pos)
            if pygame.mouse.get_pressed()[2]:
                pos=pygame.mouse.get_pos()
                pos=[pos[0]//20,pos[1]//20]
                if pos in rectPozitions:
                    pygame.draw.rect(screen,(0,0,0),(pos[0]*20+1,pos[1]*20+1,19,19))
                    rectPozitions.remove(pos)        
    run = True
    pygame.init()
    while run:
        pygame.display.update()
        clock.tick(10)                                      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for i in range(50):
            for i2 in range(30):
                if([i,i2] in rectPozitions):
                    pygame.draw.rect(screen,(255,255,255),(i*20+1,i2*20+1,19,19))  
                else:
                    pygame.draw.rect(screen,(0,0,0),(i*20+1,i2*20+1,19,19))
        operate(rectPozitions)            
main()