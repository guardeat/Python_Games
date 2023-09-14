import pygame

def renderColors(window,Blue=0):
    for x in range(256):
        for y in range(256):
            window.set_at((x, y), (x,y,Blue))

def renderBlue(window,selectedBlue=0):
    for x in range(256):
        pygame.draw.line(window,(0,0,x),[x,300],[x,320])
    pygame.draw.line(window,(255,255,255),[selectedBlue,300],[selectedBlue,320])

def main():
    pygame.init()
    x=1300
    y=800
    screen=pygame.display.set_mode((x,y))
    clock = pygame.time.Clock()
    run=True
    x=0
    pressing = False
    selectedBlue=0
    selectedRed=0
    selectedGreen=0
    while run:
        clock.tick(30)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()   
            if event.type == pygame.QUIT:
                run = False
            if event.type==pygame.MOUSEBUTTONDOWN or pressing:
                pos=pygame.mouse.get_pos()
                if pos[0]<256 and pos[1]>=300 and pos[1]<=320:
                    selectedBlue=pos[0]
                if pos[0]<256 and pos[1]<256:
                    selectedRed=pos[0]
                    selectedGreen=pos[1]
                pressing=True
            if event.type==pygame.MOUSEBUTTONUP:
                pressing=False
        renderColors(screen,selectedBlue)
        renderBlue(screen,selectedBlue)
        pygame.draw.circle(screen,(selectedRed,selectedGreen,selectedBlue),[400,123],100)
        pygame.draw.circle(screen,(255,255,255),[400,123],100,3)
        pygame.display.update() 

if __name__=="__main__":
    main()