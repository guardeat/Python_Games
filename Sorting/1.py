import pygame
import random

SIZE_X=1300
SIZE_Y=700

def sorter(screen,list):
    clock = pygame.time.Clock()
    for i in range(len(list)-1):
        min_index=i
        for i2 in range(i+1,len(list)):
            if(list[min_index]>list[i2]):
                min_index=i2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False              
        temp=list[i]
        list[i]=list[min_index]
        list[min_index]=temp
        clock.tick(15)          
        drawer(screen,list,min_index,i)
        pygame.display.update() 
        screen.fill((0,0,0))


def drawer(screen,list,number1,number2):
    for i in range(len(list)):
        pygame.draw.rect(screen,(255,255,255),pygame.Rect(5*i,SIZE_Y-list[i], 4, SIZE_Y))
    pygame.draw.rect(screen,(255,0,0),pygame.Rect(5*number1,SIZE_Y-list[number1], 4, SIZE_Y))
    pygame.draw.rect(screen,(255,0,0),pygame.Rect(5*number2,SIZE_Y-list[number2], 4, SIZE_Y))


def main():
    pygame.init()
    screen=pygame.display.set_mode((SIZE_X,SIZE_Y))
    clock = pygame.time.Clock()
    numberList=[]
    for i in range(SIZE_X//5):
        numberList.append(random.randint(0,SIZE_Y-100))

    sorter(screen,numberList) 
    sorter(screen,numberList)     

if __name__=="__main__":
    main() 