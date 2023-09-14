import pygame

def getDirections(location):
    x=location[0]
    y=location[1]
    return [[x+1,y+1],[x-1,y-1],[x+1,y-1],[x-1,y+1],[x,y+1],[x,y-1],[x+1,y],[x-1,y]]

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
    templist=[]
    temp2=[]
    for i in rectPozitions:
        temp2=getDirections(i)
        for i2 in temp2:
            if (i2 not in templist)and((i2 not in rectPozitions)):
                templist.append(i2)
    templist+=rectPozitions
    for [i,i2] in templist:
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

def drawsquare(screen,rectPozitions,x,y,k):
    for [i,i2] in rectPozitions:
        pygame.draw.rect(screen,(255,255,255),(int((i*20)/k)+1+x,int((i2*20)/k)+1+y,int(19/k),int(19/k)))  
           

def main():
    pygame.init()
    x=0
    y=0
    k=1
    run=True
    screen=pygame.display.set_mode((1001,601))
    clock = pygame.time.Clock()
    rectPozitions=[] 
    while run:
        pygame.display.update()
        clock.tick(300)
        screen.fill((0,0,0))
        drawsquare(screen,rectPozitions,x,y,k)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()  
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run=False
            if pygame.mouse.get_pressed()[0]: 
                pos=pygame.mouse.get_pos()
                c=20/k
                pos=[int(pos[0]/c)-int(x/c),int(pos[1]/c)-int(y/c)]
                if not(pos in rectPozitions):
                    rectPozitions.append(pos)
            if pygame.mouse.get_pressed()[2]:
                pos=pygame.mouse.get_pos()
                c=20/k
                pos=[int(pos[0]/c)-int(x/c),int(pos[1]/c)-int(y/c)]
                if pos in rectPozitions:
                    rectPozitions.remove(pos)
            y += (keys[pygame.K_w]-keys[pygame.K_s])*20
            x += (keys[pygame.K_a]-keys[pygame.K_d])*20
            k +=(keys[pygame.K_o]-keys[pygame.K_l])/5
    run = True
    pygame.init()
    while run:
        pygame.display.update()
        clock.tick(30)
        screen.fill((0,0,0))
        drawsquare(screen,rectPozitions,x,y,k)                                    
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()  
            if event.type == pygame.QUIT:
                run = False
        operate(rectPozitions)
        y += (keys[pygame.K_w]-keys[pygame.K_s])*20 
        x += (keys[pygame.K_a]-keys[pygame.K_d])*20
        k +=(keys[pygame.K_o]-keys[pygame.K_l])/5             
main()