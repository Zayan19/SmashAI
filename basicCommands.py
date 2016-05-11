from memoryWatcher import MemoryWatcher;
from random import *;
from math import *;



class BasicCommands:
    def __init__(self, memoryWatcher, controller):
        self.memoryWatcher = memoryWatcher;
        self.controller = controller;
        self.p2x="00453F20"
        self.p2y="00453F24"
        self.rightlock = False
        self.leftlock = False
    def dashDance(self):
        self.memoryWatcher.pauseForTime(12)

        self.controller.inputAnalog("MAIN","0.5","0.5")
        x=15;
        while (x>0):
            self.memoryWatcher.pauseForTime(11)
            self.controller.inputAnalog("MAIN","0","0.5")
            self.memoryWatcher.pauseForTime(11)
            self.controller.inputAnalog("MAIN","1","0.5")
            x=x-1
    # def walk (self):
    # def run (self):
    # def jab (self):
    def upB(self,xCord,yCord):

        # self.memoryWatcher.pauseForTime(10)
        self.controller.inputAnalog("MAIN","0.5","1")

        self.memoryWatcher.pauseForTime(15)

        self.controller.inputs("B")
        self.memoryWatcher.pauseForTime(2)
        self.controller.inputAnalog("MAIN",xCord,yCord)
        self.memoryWatcher.pauseForTime(70)


    def sideB(self,Shorten,dirr):
        self.memoryWatcher.pauseForTime(3)
        if (dirr=="left"):
            self.controller.inputAnalog("MAIN","0","0.5")
        else: self.controller.inputAnalog("MAIN","1","0.5")
        self.memoryWatcher.pauseForTime(2)
        self.controller.inputs("B",1)
        self.memoryWatcher.pauseForTime(1)
        if Shorten is True:
            self.controller.releaseButtons()
            self.memoryWatcher.pauseForTime(19)
            self.controller.inputs("B")
        self.memoryWatcher.pauseForTime(1)

    #performs a jump cancelled up Smash
    def upSmash(self):
        self.controller.inputAnalog("MAIN","0.5","1")
        self.memoryWatcher.pauseForTime(2)
        self.controller.inputs("A",1)
        self.memoryWatcher.pauseForTime(1)


    def upTilt(self):
        self.controller.inputAnalog("MAIN","0.5","0.6")
        self.memoryWatcher.pauseForTime(2)
        self.controller.inputs("A",1)
        self.memoryWatcher.pauseForTime(3)

    def shield(self):
        self.controller.triggerAnalog("L","1")
        self.memoryWatcher.pauseForTime(2);
        self.controller.releaseButtons();

    def roll(self,dir):
        self.shield()
        self.memoryWatcher.pauseForTime(9)
        print (dir)
        if dir=="right":
            self.controller.inputAnalog("MAIN","1","0.5")
        elif dir is "left":
            self.controller.inputAnalog("MAIN","0","0.5")
        self.memoryWatcher.pauseForTime(1)

    def dashAttack(self,dir):
        if (dir=="right"):
            self.controller.inputAnalog("MAIN","1","0.5")
        elif (dir=="left"):
            self.controller.inputAnalog("MAIN","0","0.5")
        self.memoryWatcher.pauseForTime(9)
        self.controller.inputs("A")
        self.memoryWatcher.pauseForTime(1)

    def waveDash(self,dir):
        # timer = self.memoryWatcher;
        if dir=="left": self.controller.inputAnalog("MAIN","0","0.3")
        elif dir=="right": self.controller.inputAnalog("MAIN","1","0.3")
        self.controller.inputs("X")
        self.memoryWatcher.pauseForTime(4)
        self.controller.inputs("L")
        self.memoryWatcher.pauseForTime(7)


    #pass in 2 frames for short hop, 3 or more for full hop
    def jump(self,pauseTime,dirr):
        if (dirr=="right"): self.controller.inputAnalog("MAIN","1","0.5")
        elif (dirr=="left"): self.controller.inputAnalog("MAIN","0","0.5")
        self.controller.inputs("X");
        timer = self.memoryWatcher;
        self.controller.inputs("X");
        timer.pauseForTime(pauseTime)
        self.controller.releaseButtons();
        # print("not okay!!!!!!!!!!!")


    def recover(self):
       while (True):
           # self.memoryWatcher.getHitStun()
           # print ("This is the X please print",self.memoryWatcher.getX())
           if (self.memoryWatcher.getHitStun()==0):
                # currentX = self.memoryWatcher.getX();
                if ( 1120447161< self.memoryWatcher.getX() <1124447162 ):
                    # print ("this is the one:",self.memoryWatcher.getX())
                    # print ("This is the other branch")
                    self.upB("0","1")
                    self.controller.releaseButtons()
                elif (self.memoryWatcher.getX() > 3268000000):
                    # print ("This is the X",currentX)
                    self.upB("1","1")
                    self.controller.releaseButtons()

    def test3(self):
               value = self.memoryWatcher.getHitStun();
               x=0
               counter = 0
               while (x<20):

                    if (self.memoryWatcher.getHitStun()!=-1):
                        # print (value)
                        counter=counter+1
                    else:
                        # print("no")
                        counter=counter-1
                    x=x+1
               # print ("This is the counter",counter)
               return counter



    def recover2(self):
               value = self.memoryWatcher.getHitStun();
               self.controller.inputAnalog("MAIN","0.5","0.7")
               if ( self.test3()>= -16):
                        print (value)
                        self.controller.releaseButtons()
                        self.controller.inputAnalog("MAIN","0","0.5")
                        self.memoryWatcher.pauseForTime(2)
                        self.controller.inputAnalog("MAIN","1","0.5")
                        self.controller.releaseButtons()

               else:
                    # currentX = self.memoryWatcher.getX(self.p2x);
                    # currentY = self.memoryWatcher.getX(self.p2y);

                    curX = self.memoryWatcher.state['p2']['x'];
                    print("curX: ",curX)
                    if ( curX>81 ):
                        # self.recoveryHelper("left","left")
                        self.jump(2,"left")
                        self.memoryWatcher.pauseForTime(10)
                        curY = self.memoryWatcher.state['p2']['y'];
                        if (curY>-10):
                            if (randint(0,10)<7):self.sideB(False,"left")
                            else: self.upB("0","0.8")
                        else: self.upB("0","1")
                    elif (curX < -81):
                        self.jump(2,"right")
                        self.memoryWatcher.pauseForTime(10)
                        curY = self.memoryWatcher.state['p2']['y'];
                        if (curY>-10):
                            if (randint(0,10)<7):self.sideB(False,"right")
                            else: self.upB("1","0.8")
                        else: self.upB("1","1")

                    self.controller.releaseButtons();


    def recoveryHelper(self,jumpDir,upBdir):
                self.memoryWatcher.pauseForTime(10)
                self.jump(2,jumpDir)
                # if (currentY>1000000000): self.sideB(False,"left")
                # else: self.upB("0","1")
                if upBdir=="left":self.upB("0","1")
                else: self.upB("1","1")
                self.controller.releaseButtons()

    def shdl(self):
            self.jump(2, "")
            self.controller.releaseButtons();
            self.memoryWatcher.pauseForTime(2);
            self.controller.inputs("B",True);
            self.memoryWatcher.pauseForTime(1);
            self.controller.releaseButtons();
            self.memoryWatcher.pauseForTime(5);
            self.controller.inputs("B",True);
            self.memoryWatcher.pauseForTime(5);
            self.controller.releaseButtons();
            self.memoryWatcher.pauseForTime(13)


















    def facePlayer(self,curXPlayer,curXCPU):
                # rightlock = False;
                # leftlock  = False;

                # while True:

                    # curXPlayer = self.memoryWatcher.state['p1']['x'];
                    # curXCPU = self.memoryWatcher.state['p2']['x'];
                    self.memoryWatcher.pauseForTime(1)

                    if (curXPlayer > curXCPU and self.rightlock == False):
                        self.controller.inputAnalog("MAIN","0.6","0.5")
                        self.memoryWatcher.pauseForTime(2)
                        self.controller.releaseButtons()
                        self.rightlock = True
                        self.leftlock = False
                    elif (curXPlayer < curXCPU and self.leftlock == False):
                        self.controller.inputAnalog("MAIN","0.4","0.5")
                        self.memoryWatcher.pauseForTime(2)
                        self.controller.releaseButtons()
                        self.leftlock = True
                        self.rightlock = False




    def SHAerial(self,x):
        #check to see when AI can move
              actionFrame = self.memoryWatcher.state['p1']['action'];
              while (actionFrame!=14):  #when this address reaches 14, the AI is actionable
                self.memoryWatcher.readMemory() # update the addresses
                actionFrame = self.memoryWatcher.state['p1']['action'];
                print ("not 14 yet")


              print("starting the SHAerial function y value: ", self.memoryWatcher.state['p2']['y']);
              #do a short hop and then immediately do a neutral air
              self.jump(2,"")#the short hop is done here
              self.memoryWatcher.pauseForTime(2); #wait 2 frames
              self.controller.inputs("A",True)  #then press A while in the air causing a neutral air attack
              self.memoryWatcher.pauseForTime(2); #the A must be pressed for 2 frames for it to register in the game
              self.controller.releaseButtons();

              print("SHAerial, y value: ", self.memoryWatcher.state['p2']['y']);
              while True:
                #check if Fox is falling, done by checking when Y starts decreasing, we do this using two Y values
                curYCPU = self.memoryWatcher.state['p2']['y']; #the first Y address
                self.memoryWatcher.readMemory() # update the addresses
                curYCPU2 = self.memoryWatcher.state['p2']['y']; #the second Y address
                #when Y starts decreasing do a fast all and get ready to L cancel
                if (curYCPU>curYCPU2):
                        self.controller.inputAnalog("MAIN","0.5","0") #press down to start the fastfall
                        self.memoryWatcher.pauseForTime(2)  #need to press down for at least 2 frames for it to register
                        self.controller.releaseButtons();
                        self.LCancel() #function that waits for the right time to L cancel
                        break;
                print("ending the SHAerial function ");

#this function waits until Fox is just about to land
#then it presses L to reduce the landing lag of the aerial by half
#right now it's hard coded to work for only his neutral aerial
    def LCancel(self):
            curY = self.memoryWatcher.state['p2']['y'];
            #if Y is >2 as Fox is falling down, wait as it's not time to L cancel yet
            while ( curY>2 ):
                curY = self.memoryWatcher.state['p2']['y'];
                self.memoryWatcher.readMemory();
                print ("L cancel while loop")
            self.shield()  #do the L cancel
            # self.memoryWatcher.pauseForTime(6); #waits until the landing lag of the neutral air ends

    def test2(self):
        self.memoryWatcher.pauseForTime(97)
        self.controller.releaseButtons()

        # self.SHAerial(1);
        # self.shdl()
        # self.dashDance()
        # self.shortHopAerial()
        # self.controller.releaseButtons()
        # self.memoryWatcher.pauseForTime(13)
        # self.sideB(True,"left");
        # self.shield()
        # self.recover2()
        # self.roll("right")
        # self.upTilt()
        # self.upB("0","0")
        # self.dashAttack("right")
        # self.waveDash("right")
        # self.dashDance()


#basic loop to demonstrate the AI
#Fox will short hop and double laser if the opponent is far
#will neutral air if they come close
#will recover if offstage
        while True:
            x=1
            curXPlayer = self.memoryWatcher.state['p1']['x'];
            curXCPU = self.memoryWatcher.state['p2']['x'];
            # print ("this is curXCPU",curXCPU)
            self.memoryWatcher.pauseForTime(1)
            self.facePlayer(curXPlayer,curXCPU)
            if (curXCPU>61 or curXCPU <-61): self.recover2()
            else:
                self.memoryWatcher.pauseForTime(1)
                distance = (abs(curXPlayer-curXCPU))
                if (distance>40):
                    self.shdl()
                else:
                    if (curXPlayer > curXCPU and curXCPU<=62 and curXCPU>=-62):
                        self.controller.inputAnalog("MAIN","1","0.5")
                        self.memoryWatcher.pauseForTime(3)
                        self.controller.releaseButtons()
                        self.SHAerial(x)
                        self.controller.releaseButtons()
                    if (curXPlayer < curXCPU and curXCPU>=-62 and curXCPU<=62):
                        self.controller.inputAnalog("MAIN","0","0.5")
                        self.memoryWatcher.pauseForTime(3)
                        self.controller.releaseButtons()
                        self.SHAerial(x)
                        self.controller.releaseButtons()

        self.controller.releaseButtons()
        return;




# def main():
#     print("inside the basic commands file");
# if __name__ == '__main__':
    # main();
