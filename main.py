
from memoryWatcher import MemoryWatcher;
from Controller import Controller;
import sys;
import os;
import basicCommands as bc;
import time;


def findDolphinPath():
    homePath = os.path.expanduser('~'); # this is the home path
    if sys.platform == "linux" or sys.platform == "linux2":
        path = homePath  # linux
        if (os.path.isdir(homePath + '/.local/share/dolphin-emu')): path += '/.local/share/dolphin-emu';
        else: path = homePath + '/.local/dolphin-emu';
        homePath = path;
    elif sys.platform == "darwin": homePath += "/Library/Application Support/Dolphin"
    print(homePath);
    if(not (os.path.isdir(homePath))):
        print("can not find path for dolphin, are you sure it is installed??");
        print("if it is already installed then can you please store the location to the dolphin config files in the environment variable XDG_DATA_HOME");
        print("example: export XDG_DATA_HOME='path to dolphin'");
        return "";
    ## return the home path
    return homePath;


memWatcher = None; # MemoryWatcher(findDolphinPath());
controller = None; # Controller(findDolphinPath());


def initialSetup():
    global memWatcher;
    global controller;
    memWatcher = MemoryWatcher(findDolphinPath());
    memWatcher.startSocket();
    controller = Controller(findDolphinPath());
    return;

def main():
    initialSetup();
    # bc.main();
    basicCommands = bc.BasicCommands(memWatcher, controller);

    basicCommands.test2()
    # while(True):
        # memWatcher.readMemory();

    controller.releaseButtons();


    # print("starting");
    # for i in range(3):
    #     print("in the ith: " + str(i) + " time");
    #     memWatcher.pauseForTime(100);
    #     # basicCommands.upTilt();
    #     # basicCommands.roll("right");
    #     # basicCommands.dashAttack("left");
    #     # basicCommands.waveDash("left");
    #     basicCommands.jump(2);
    #     controller.releaseButtons();
    #     memWatcher.pauseForTime(100);

    # memWatcher.pauseForTime(100);
    # controller.releaseButtons();
    # print("done");

    # while(True):
    #     # basicCommands.test2();
    #     basicCommands.recover();
    #     # basicCommands.dashDance();

        # controller.releaseButtons();
    return;




if __name__ == '__main__':
    main();
