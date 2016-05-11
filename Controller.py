import pipes

"""
    self.pipe = this is variable that is the pipe, you can write to it, or read to it and it will write to the file
    self.path = the location to where the dolphin folder is inside the computer
"""

class Controller:
    def __init__(self, path):
        self.path = path;
        self.__setupPipe();
    def __setupPipe(self):
        # pipeTemplate = pipes.Template()
        # pipeTemplate.append('tr a-z A-Z', '--')
        # self.pipe = pipeTemplate.open(self.path+'/Pipes/cpu-level-11', 'w')
        self.pipe = open(self.path+'/Pipes/cpu-level-11', 'w');

    #call this at the end of every script
    def releaseButtons(self):
        # if(not self.pipe): self.__setupPipe();
        # print("self.pipe: ", self.pipe );
        self.pipe.write("SET MAIN 0.5 0.5\n");
        self.pipe.write("SET C 0.5 0.5\n");
        self.pipe.write("SET L 0\n");
        self.pipe.write("SET R 0\n");
        self.pipe.write("RELEASE X\n");
        self.pipe.write("RELEASE A\n");
        self.pipe.write("RELEASE B\n");
        self.pipe.write("RELEASE Z\n");
        self.pipe.write("RELEASE L\n");
        self.pipe.write("RELEASE START\n");
        self.pipe.flush();

    """
        this function will press or release the given button for the given amount of time
        par1 = button2Press = the current button that needs to be pressed
        par2 = timeHeld = the time that the button needs to be held
        par3 = if you want the button to be released make pressOrReleased to False
    """
    def inputs(self,button2Press,pressOrRelease=True):
        # pipeTemplate = pipes.Template()
        # pipeTemplate.append('tr a-z A-Z', '--')
        # pipe = pipeTemplate.open(self.path+'/Pipes/cpu-level-11', 'w')
        action = "PRESS";
        if(not pressOrRelease): action = "RELEASE";
        self.pipe.write(action + " "+button2Press+"\n")
        # self.pipe.close();
        self.pipe.flush();

    def inputAnalog(self,action,buttonXCord,buttonYCord,pressOrRelease=True):
        # pipeTemplate = pipes.Template()
        # print (buttonXCord,buttonYCord,pressOrRelease)
        # pipeTemplate.append('tr a-z A-Z', '--')
        # pipe = pipeTemplate.open(self.path+'/Pipes/cpu-level-11', 'w')
        if(not pressOrRelease): action = "RELEASE";
        self.pipe.write("SET"+" "+action+" "+buttonXCord+" "+buttonYCord+"\n")
        # self.pipe.close();
        self.pipe.flush();

    def triggerAnalog(self,action,buttonXCord,pressOrRelease=True):
        # pipeTemplate = pipes.Template()
        # pipeTemplate.append('tr a-z A-Z', '--')
        # pipe = pipeTemplate.open(self.path+'/Pipes/cpu-level-11', 'w')
        if(not pressOrRelease): action = "RELEASE";
        self.pipe.write("SET"+" "+action+" "+buttonXCord+" "+"\n")
        self.pipe.flush();
        # self.pipe.close();

#still a work in progress
# if __name__  == "__main__":


