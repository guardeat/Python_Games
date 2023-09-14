import pygame
import math
import random

bullets = []

class Direction:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3 
    UPRIGHT = 4
    UPLEFT = 5
    DOWNRIGHT = 6
    DOWNLEFT = 7

class vec2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __add__(self,aim):
        return vec2(self.x + aim.x, self.y + aim.y)
    
    def __sub__(self,aim):
        return vec2(self.x - aim.x, self.y - aim.y)
    
    def __mult__(self,aim):
        return vec2(self.x * aim.x, self.y * aim.y)
    
    def __truediv__(self,aim):
        return vec2(self.x / aim.x, self.y / aim.y)
    
    def lenght(self):
        return (self.x**2 + self.y**2)**(1/2)


class Bullet:
    def __init__(self,startPos,speed,owner):
        self.pos = startPos
        self.speed = speed
        self.owner = owner

    def update(self):
        self.pos[0] += self.speed.x
        self.pos[1] += self.speed.y

    def draw(self,screen):
        pygame.draw.circle(screen,[255,255,255],self.pos,3)


class Player:
    def __init__(self,buttonSet,startPos,color,id):
        self.buttonSet = buttonSet
        self.pos = startPos
        self.direction = Direction.DOWN
        self.speed = vec2(3,3)
        self.color = color
        self.id = id
        self.oldPos = startPos.copy()

    def draw(self, screen):
        pygame.draw.circle(screen,self.color,self.pos,10)

    def handleInput(self, inputs):
        self.oldPos = self.pos.copy()

        self.pos[0] += (inputs[self.buttonSet[1]]-inputs[self.buttonSet[3]]) * self.speed.x
        self.pos[1] -= (inputs[self.buttonSet[0]]-inputs[self.buttonSet[2]]) * self.speed.y

        self.calculateDirection()
        
        if inputs[self.buttonSet[4]] == True:
            self.createBullet()

    def createBullet(self):
        if self.direction == Direction.UP:
            bullets.append(Bullet(self.pos.copy(),vec2(0,-10),self.id))
        if self.direction == Direction.RIGHT:
            bullets.append(Bullet(self.pos.copy(),vec2(10,0),self.id))
        if self.direction == Direction.DOWN:
            bullets.append(Bullet(self.pos.copy(),vec2(0,10),self.id))
        if self.direction == Direction.LEFT:
            bullets.append(Bullet(self.pos.copy(),vec2(-10,0),self.id))
        if self.direction == Direction.UPLEFT:
            bullets.append(Bullet(self.pos.copy(),vec2(-6,-6),self.id))
        if self.direction == Direction.UPRIGHT:
            bullets.append(Bullet(self.pos.copy(),vec2(6,-6),self.id))
        if self.direction == Direction.DOWNRIGHT:
            bullets.append(Bullet(self.pos.copy(),vec2(6,6),self.id))
        if self.direction == Direction.DOWNLEFT:
            bullets.append(Bullet(self.pos.copy(),vec2(-6,6),self.id))

    def calculateDirection(self):
        if self.pos[0] > self.oldPos[0]:
            if self.pos[1] > self.oldPos[1]:
                self.direction = Direction.DOWNRIGHT
            elif self.pos[1] == self.oldPos[1]:
                self.direction = Direction.RIGHT
            else:
                self.direction = Direction.UPRIGHT

        elif self.pos[0] < self.oldPos[0]:
            if self.pos[1] > self.oldPos[1]:
                self.direction = Direction.DOWNLEFT
            elif self.pos[1] == self.oldPos[1]:
                self.direction = Direction.LEFT
            else:
                self.direction = Direction.UPLEFT

        else:
            if self.pos[1] > self.oldPos[1]:
                self.direction = Direction.DOWN
            else:
                self.direction = Direction.UP



class Physics:
    def solveCollision(posList,radius):
        for i in range(len(posList)):
            for i2 in range(i + 1,len(posList)):
                Physics.checkCollision(posList[i],posList[i2],radius)

    def checkCollision(pos1,pos2,radius):

        y=pos1[1]-pos2[1]
        x=pos1[0]-pos2[0]

        distance = math.sqrt(x**2 + y**2)

        if distance > 2*radius:
            return

        try:
            signx=abs(x)/(x)
            signy=abs(y)/(y)
        except:
            signx=1
            signy=1
        if(x==0):
            x=0.01        
        m=abs(y/x)
        k=(radius+radius-distance)/1.2
        x2=k/math.sqrt(m**2+1)*signx
        y2=abs(m*x2)*signy
        pos1[0] = pos1[0]+x2
        pos1[1] = pos1[1]+y2
        pos2[0]=pos2[0]-x2
        pos2[1]=pos2[1]-y2

    def drawBullets(bulletList, screen):
        for bullet in bulletList:
            bullet.draw(screen)

    def updateBullets(bulletList):
        for bullet in bulletList:
            bullet.update()

    def checkBulletCollision(playerList,bulletList):
        for bullet in bulletList:
            for player in playerList:
                y=player.pos[1]-bullet.pos[1]
                x=player.pos[0]-bullet.pos[0]

                distance = math.sqrt(x**2 + y**2)

                if distance < 13 and player.id != bullet.owner:
                    return False
                
        return True
    

class Border:
    def __init__(self,screenX,screenY):
        self.radius = min(screenX,screenY)
        self.center = [screenX/2 , screenY/2]
        self.bombed = [-1000,-1000]
        self.bombedAge = 0

    def call(self,playerList):
        global bullets

        self.bombedAge += 1

        self.createBombed()

        removeIndices = []
        for i,bullet in enumerate(bullets):
            x = bullet.pos[0] - self.center[0]
            y = bullet.pos[1] - self.center[1]
            if math.sqrt(x**2 + y**2) > self.radius:
                removeIndices.append(i)

        temp = [i for j, i in enumerate(bullets) if j not in removeIndices]

        bullets = temp

        for player in playerList:
            x = player.pos[0] - self.center[0]
            y = player.pos[1] - self.center[1]
            if math.sqrt(x**2 + y**2) > self.radius:
                return False
            
        if self.bombedAge > 50:    
            for player in playerList:
                x = player.pos[0] - self.bombed[0]
                y = player.pos[1] - self.bombed[1]
                if math.sqrt(x**2 + y**2) < self.radius/10:
                    return False
            
        self.radius -= 0.5
        return True    
    
    def draw(self,screen):
        pygame.draw.circle(screen,(255,255,255),self.center,self.radius,3)
        pygame.draw.circle(screen,(self.bombedAge*2 + 30,255 - self.bombedAge * 2 - 30,255 - self.bombedAge * 2 - 30),self.bombed,self.radius/10,3) 

    def createBombed(self):
        if self.bombedAge >= 100:
            randomX = random.randint(self.center[0] - int(self.radius),self.center[0] + int(self.radius))
            randomY = random.randint(self.center[1] - int(self.radius),self.center[1] + int(self.radius))
            self.bombed = [randomX,randomY]
            self.bombedAge = 0
            print(self.bombed)


def main():
    pygame.init()

    SCREEN_X = 1200
    SCREEN_Y = 800

    screen=pygame.display.set_mode((SCREEN_X,SCREEN_Y))
    clock = pygame.time.Clock()
    run=True
    con = True
    pressing = False

    player1 = Player([pygame.K_w,pygame.K_d,pygame.K_s,pygame.K_a,pygame.K_f],[300,300],[0,255,0],0)
    player2 = Player([pygame.K_UP,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_LEFT,pygame.K_l],[600,400],[255,0,0],1)

    border = Border(SCREEN_X,SCREEN_Y)

    while run and con:
        screen.fill((0,0,0))
        clock.tick(30)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()  
            if event.type == pygame.QUIT:
                run = False

        player1.handleInput(keys)
        player2.handleInput(keys)

        Physics.updateBullets(bullets)

        Physics.solveCollision([player1.pos,player2.pos],10)
        con = Physics.checkBulletCollision([player1,player2],bullets) and border.call([player1,player2])
        
        border.draw(screen)
        player1.draw(screen) 
        player2.draw(screen)     
        Physics.drawBullets(bullets,screen)
        
        pygame.display.update()    
    

if __name__=="__main__":
    main()             