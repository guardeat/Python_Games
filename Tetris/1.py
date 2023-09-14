from random import randint
from msvcrt import kbhit,getch
import time
from os import system


class gamemap():

    def __init__(self,x,y):

        self.maplist=[[" " for i in range(x)].copy() for i2 in range(y)]
        self.height=y
        self.weight=x


    def remover(self):

        control=0

        for y in range(self.height):
            if self.maplist[y].count("o")==self.weight:
                control+=1
                self.maplist[y]=[" " for x in range(self.weight)].copy()

        return control


    def mover(self,control):
        
        for i in range(control):
            templist=[i[::] for i in self.maplist]
            for y in range(1,self.height):
                if self.maplist[y].count(" ")==self.weight and "o" in sum(self.maplist[:y+1],[]):
                    for y2 in range(1,y+1):
                        self.maplist[y2]=templist[y2-1].copy()
                    break
    

    def blockreturner(self,block):

        blockdict={"L1":[[int(self.weight/2),0],[int(self.weight/2),1],[int(self.weight/2),2],[int(self.weight/2)-1,2]],
        "L2":[[int(self.weight/2)-1,0],[int(self.weight/2)-1,1],[int(self.weight/2),1],[int(self.weight/2)+1,1]],
        "L3":[[int(self.weight/2),0],[int(self.weight/2)+1,0],[int(self.weight/2),1],[int(self.weight/2),2]],
        "L4":[[int(self.weight/2)-1,0],[int(self.weight/2),0],[int(self.weight/2)+1,0],[int(self.weight/2)+1,1]],
        "Z1":[[int(self.weight/2),0],[int(self.weight/2)+1,0],[int(self.weight/2)+1,1],[int(self.weight/2)+2,1]],
        "Z2":[[int(self.weight/2)+1,0],[int(self.weight/2)+1,1],[int(self.weight/2),1],[int(self.weight/2),2]],
        "Z3":[[int(self.weight/2),0],[int(self.weight/2)+1,0],[int(self.weight/2)+1,1],[int(self.weight/2)+2,1]],
        "Z4":[[int(self.weight/2)+1,0],[int(self.weight/2)+1,1],[int(self.weight/2),1],[int(self.weight/2),2]],
        "z1":[[int(self.weight/2),1],[int(self.weight/2)+1,1],[int(self.weight/2)+1,0],[int(self.weight/2)+2,0]],
        "z2":[[int(self.weight/2),0],[int(self.weight/2),1],[int(self.weight/2)+1,1],[int(self.weight/2)+1,2]],
        "z3":[[int(self.weight/2),1],[int(self.weight/2)+1,1],[int(self.weight/2)+1,0],[int(self.weight/2)+2,0]],
        "z4":[[int(self.weight/2),0],[int(self.weight/2),1],[int(self.weight/2)+1,1],[int(self.weight/2)+1,2]],
        "B1":[[int(self.weight/2),0],[int(self.weight/2)+1,0],[int(self.weight/2),1],[int(self.weight/2)+1,1]],
        "B2":[[int(self.weight/2),0],[int(self.weight/2)+1,0],[int(self.weight/2),1],[int(self.weight/2)+1,1]],
        "B3":[[int(self.weight/2),0],[int(self.weight/2)+1,0],[int(self.weight/2),1],[int(self.weight/2)+1,1]],
        "B4":[[int(self.weight/2),0],[int(self.weight/2)+1,0],[int(self.weight/2),1],[int(self.weight/2)+1,1]],
        "I1":[[int(self.weight/2),0],[int(self.weight/2),1],[int(self.weight/2),2],[int(self.weight/2),3]],
        "I2":[[int(self.weight/2),0],[int(self.weight/2)+1,0],[int(self.weight/2)+2,0],[int(self.weight/2)+3,0]],
        "I3":[[int(self.weight/2),0],[int(self.weight/2),1],[int(self.weight/2),2],[int(self.weight/2),3]],
        "I4":[[int(self.weight/2),0],[int(self.weight/2)+1,0],[int(self.weight/2)+2,0],[int(self.weight/2)+3,0]],
        "V1":[[int(self.weight/2)+1,0],[int(self.weight/2),1],[int(self.weight/2)+1,1],[int(self.weight/2)+2,1]],
        "V2":[[int(self.weight/2),0],[int(self.weight/2),1],[int(self.weight/2)+1,1],[int(self.weight/2),2]],
        "V3":[[int(self.weight/2),0],[int(self.weight/2)+1,0],[int(self.weight/2)+1,1],[int(self.weight/2)+2,0]],
        "V4":[[int(self.weight/2)+1,0],[int(self.weight/2),1],[int(self.weight/2)+1,1],[int(self.weight/2)+1,2]],
        "l1":[[int(self.weight/2),0],[int(self.weight/2),1],[int(self.weight/2),2],[int(self.weight/2)+1,2]],
        "l2":[[int(self.weight/2),0],[int(self.weight/2),1],[int(self.weight/2)+1,0],[int(self.weight/2)+2,0]],
        "l3":[[int(self.weight/2),0],[int(self.weight/2)+1,0],[int(self.weight/2)+1,1],[int(self.weight/2)+1,2]],
        "l4":[[int(self.weight/2),1],[int(self.weight/2)+1,1],[int(self.weight/2)+2,1],[int(self.weight/2)+2,0]],
        }

        return blockdict[block]
    

    def mapupdatechecher(self,blocklist):

        for y in range(len(blocklist)):
            if blocklist[y][1]>=self.height-1:
                return 1
        for y in blocklist:
            if self.maplist[y[1]+1][y[0]]=="o" and [y[1]+1,y[0]] not in blocklist:
                return 1 
        return 0
    

    def randomblock(self):
        return ["L1","Z1","z1","B1","I1","V1","l1"][randint(0,6)]


    def blockturner(self,block,char):

        if char =="e":
            if block[1]=="4":
                block=block[:-1]+"1"
            else:
                block=block[:-1]+str(int(block[-1])+1)
        else:
            if block[1]=="1":
                block=block[:-1]+"4"
            else:
                block=block[:-1]+str(int(block[-1])-1)

        return block
    

    def mapupdater(self,blocklist):

        for y in range(self.height):
            for x in range(self.weight):
                if [x,y] in blocklist:
                    self.maplist[y][x]="o"
    

def blockrightleft(blocklist,attempt,attempt2):
        
    blocklist1=[i[::] for i in blocklist]
    for y in range(len(blocklist1)):
        blocklist1[y]=[blocklist1[y][0]+attempt,blocklist1[y][1]+attempt2]
        
    return blocklist1


def timed_input(timeout=0.5): 
    start = time.time()
    while time.time() - start < timeout:
        if kbhit():
            char = getch().decode("utf-8")
            if char != None:
                return char
            else:
                time.sleep(timeout)


def mappresser(maplist,blocklist):
        templist=[i[:] for i in maplist]
        if blocklist:
            for y in range(len(templist)):
                for x in range(len(templist[0])):
                    if [x,y] in blocklist:
                        templist[y][x]="o"
        print((2*(len(templist[0])+1)*"-"))
        for y in range(1,len(templist)):
            print("|",end="")
            for x in templist[y]:
                if x=="o":
                    print(2*"o",end="")
                else:
                    print(2*" ",end="")
            print("|")
        print((2*(len(templist[0])+1)*"-"))


def blockcheck(blocklist,gamemap,oldblock,blockrightleft,rightleftattemp,attempt):

    for control in range(4):
        for block1 in blocklist:
            if block1[1]>gamemap.height-1:
                for i in range(len(blocklist)):
                    blocklist[i][1]=blocklist[i][1]-1
            if block1[0]>gamemap.weight-1:
                for i in range(len(blocklist)):
                    blocklist[i][0]=blocklist[i][0]-1
            if block1[1]<0:
                for i in range(len(blocklist)):
                    blocklist[i][1]=blocklist[i][1]+1
            if block1[0]<0:
                for i in range(len(blocklist)):
                    blocklist[i][0]=blocklist[i][0]+1
    for y in blocklist:
        if gamemap.maplist[y[1]][y[0]]=="o":
            return blockrightleft(gamemap.blockreturner(oldblock),rightleftattemp,attempt)
    return blocklist

    
def main(gamemap):
    blocklist=0
    attempt=0
    rightleftattemp=0
    while True:
        if blocklist==0:
            block=gamemap.randomblock()
            blocklist=gamemap.blockreturner(block)
            oldblock=block
        started=time.time()
        attempt+=1
        userinput=timed_input()
        if gamemap.maplist[1].count("o") !=0:
            print("Game over")
            break
        if userinput in ["q","e"]:
            oldblock=block
            block=gamemap.blockturner(block,userinput)
            blocklist=gamemap.blockreturner(block)
            blocklist=blockcheck(blocklist,gamemap,oldblock,blockrightleft,rightleftattemp,attempt)

        elif userinput in ["a","d"]:
            controlrightleft=1
            temp1=blockrightleft(blocklist,rightleftattemp,attempt)
            if userinput=="a":
                for c in temp1:
                    if not (c[1]+1==gamemap.height or c[0]-1 >=0):
                        if gamemap.maplist[c[1]+1][c[0]-1]=="o" or c[0]-1==-1:
                            controlrightleft =0
                    else:
                        if gamemap.maplist[c[1]][c[0]-1]=="o" or c[0]-1==-1:
                            controlrightleft =0
                if controlrightleft:
                    rightleftattemp-=1

            else:  
                for c in temp1:
                    if not c[1]+1==gamemap.height:
                        if c[0]+1==gamemap.weight or gamemap.maplist[c[1]+1][c[0]+1]=="o":
                            controlrightleft=0
                            break
                    else:
                        if c[0]+1==gamemap.weight or gamemap.maplist[c[1]][c[0]+1]=="o" :
                            controlrightleft =0
                            break
                if controlrightleft:
                    rightleftattemp+=1  

        elif userinput =="s":
            pass
        elif userinput=="r":
            break
        else:
            time.sleep(0.6-(time.time()-started))

        blocklist=blockcheck(blocklist,gamemap,oldblock,blockrightleft,rightleftattemp,attempt)
        blocklist=blockrightleft(blocklist,rightleftattemp,attempt)
        blocklist=blockcheck(blocklist,gamemap,oldblock,blockrightleft,rightleftattemp,attempt)
        system("cls")
        mappresser(gamemap.maplist,blocklist)

        if gamemap.mapupdatechecher(blocklist):
            gamemap.mapupdater(blocklist)
            control=gamemap.remover()
            gamemap.mover(control)
            attempt=0
            rightleftattemp=0
            blocklist=0
        if blocklist !=0:
            blocklist=gamemap.blockreturner(block)

map1=gamemap(10,20)
main(map1)