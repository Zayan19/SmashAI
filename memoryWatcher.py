import os;
import struct;
import socket as sc;
import debugger as dgr;

"""
    This is how dolphines memory watcher uses the data
    MemoryWatcher reads a file containing in-game memory addresses and outputs
    changes to those memory addresses to a unix domain socket as the game runs.

    The input file is a newline-separated list of hex memory addresses, without
    the "0x". To follow pointers, separate addresses with a space. For example,
    "ABCD EF" will watch the address at (*0xABCD) + 0xEF.
    The output to the socket is two lines. The first is the address from the
    input file, and the second is the new value in hex.
"""

class MemoryWatcher:
    """
        create a socket
        unix domain socket
        flags = 0
        socket type = SOCK_DGRAM, other options include SOCK_STREAM, SOCK_RAW, SOCK_RDM, SOCK_SEQPACKET
        SOCK_DGRAM = faster, data might not always reach its destination.
        SOCK_STREAM = garuntees order, and relative garuntee that message was successfully sent,
    """
    def __init__(self, path):
        self.socket = sc.socket(sc.AF_UNIX, sc.SOCK_DGRAM, 0);
        self.path = path; # the path to where dolphin emulator is stored
        self.createEmptyState();
    def createEmptyState(self):
        self.state = {
            "p1":{
                "action":0,
                "actionCounter":0,
                "actionFrame":0,
                "invulnerable":False,
                "hitlagFramesLeft":0,
                "hitStunFramesLeft":0,
                "isChargingSmash":False,
                "jumpsRemaining":0,
                "isOnGround":True,
                "speedAirX":0,
                "speedAirY":0,
                "speedXAttack":0,
                "speedYAttack":0,
                "speedGroundX":0,
                "damage":100,
                "stocks":4,
                "facingLeft":True,
                "character":0,
                "x":0,
                "y":0
            },
            "p2":{
                "action":0,
                "actionCounter":0,
                "actionFrame":0,
                "invulnerable":False,
                "hitlagFramesLeft":0,
                "hitStunFramesLeft":0,
                "isChargingSmash":False,
                "jumpsRemaining":0,
                "isOnGround":True,
                "speedAirX":0,
                "speedAirY":0,
                "speedXAttack":0,
                "speedYAttack":0,
                "speedGroundX":0,
                "damage":100,
                "stocks":4,
                "facingLeft":True,
                "character":0,
                "x":0,
                "y":0,
                "cursorX":0,
                "cursorY":0
            },
            "frame":0,
            "menuState":0,
            "stage":0
        };

    def startSocket(self):
        socketPath =  self.path + "/MemoryWatcher" + '/MemoryWatcher' # this is the path to the socket
        ### make sure the socket does not already exist
        try: os.unlink(socketPath);
        except OSError:
            if os.path.exists(socketPath): raise

        ## bind the socket to its path
        self.socket.bind(socketPath);
        # dgr.dprint("binded the socket waiting for input");
    def test(self):
        while True:
            dgr.dprint("starting to read from socket");
            datagram = self.socket.recv( 1024 ) # get the information from the socket
            if not datagram: break # break out if the information is null

            dgr.dprint("-" * 20) ## print a line just to make it easier to read
            dgr.dprint(datagram) ## print the information

        self.socket.close();
        return;

    """
        this function will delay for the number of frames that is given by the user
        @param 1 = delay, the amount that you want to delay it.
    """
    def pauseForTime(self, delay):
        if(not self.socket):
            print("the socket has not been created yet please create it before calling the pauseForTime function");
            return;
        # print("inside the pause for delay");
        numberOfFramesPassed = 0;
        startingFrame = -1;
        while(True):
            datagram = self.socket.recv( 1024 ) # get the information from the socket
            # print (datagram)
            datagram = datagram.splitlines();
            region = datagram[0].decode('ascii');
            value = int(datagram[1][0:-1],16); ## remove the last null character
            self.adjustValue(region, datagram[1]);
            if(region != "00479D60"): continue; #current updated frame

            numberOfFramesPassed += 1;
            if(startingFrame == -1):
                startingFrame = value;

            # print("number of frames passed: " + str(numberOfFramesPassed), "delay: ", delay, "value: ", value, "startingFrame: ", startingFrame)
            if(value >= startingFrame + delay): return;
            if(numberOfFramesPassed >= delay): return;

    def getX(self,address):
            while(True):
                datagram = self.socket.recv( 1024 )
                datagram = datagram.splitlines();
                region = datagram[0].decode('ascii');


                if address in region:
                    x=((int(datagram[1].decode('ascii')[:-1],16)))
                    print(x)
                    return(x)


    def getHitStun(self):
            datagram = self.socket.recv( 1024 )
            datagram = datagram.splitlines();
            region = datagram[0].decode('ascii');

            if region == "00453FC0 23a0":
                x=((int(datagram[1].decode('ascii')[:-1],16)))
                # x=((int(datagram[1].decode('ascii'),16)))
                # print("hexcode value: " + str(datagram[1]));
                # print("hitStun value: " + str(x))
                # return(x)
                return x;
            else:
                return -1

    def adjustValueForPlayer(self, region, value, player, ptrInt):
        def convertToInt(value, shiftVal): return int(value, 16) >> shiftVal;
        def convertToBool(value, shiftVal): return bool(int(value, 16) >> shiftVal);
        def convertToFloat(value): struct.unpack('f',struct.pack('I',int(value,16)))[0];

        if(ptrInt == 0x70): self.state[player]["action"] = convertToInt(value,0);
        elif(ptrInt == 0x20CC): self.state[player]["actionCounter"] = convertToInt(value,0);
        elif(ptrInt == 0x8F4): self.state[player]["actionFrame"] = convertToFloat(value);
        elif(ptrInt == 0x19EC): self.state[player]["invulnerable"] = convertToBool(value,0);
        elif(ptrInt == 0x19BC): self.state[player]["hitlagFramesLeft"] = convertToFloat(value);
        elif(ptrInt == 0x23A0): self.state[player]["hitstunFramesLeft"] = convertToFloat(value);
        elif(ptrInt == 0x2174): self.state[player]["isChargingSmash"] = convertToBool(value,0);
        elif(ptrInt == 0x19C8): self.state[player]["jumpsRemaining"] = (0 if convertToInt(value, 24) > 1 else convertToInt(value, 24)); ## this wont work for characters with multiple jumps
        elif(ptrInt == 0x140): self.state[player]["isOnGround"] = convertToBool(value, 0);
        elif(ptrInt == 0xE0): self.state[player]["speedAirX"] = convertToFloat(value);
        elif(ptrInt == 0xE4): self.state[player]["speedAirY"] = convertToFloat(value);
        elif(ptrInt == 0xEC): self.state[player]["speedAttackX"] = convertToFloat(value);
        elif(ptrInt == 0xF0): self.state[player]["speedAttackY"] = convertToFloat(value);
        elif(ptrInt == 0x14C): self.state[player]["speedGroundX"] = convertToFloat(value);
        else: print("WARNING: got an expected memory address", ptrInt);

    def adjustValue(self, region, value):
        def convertToInt(valShift, shiftVal): return int(valShift, 16) >> shiftVal;
        def convertToBool(valShift, shiftVal): return bool(int(valShift, 16) >> shiftVal);
        def convertToFloat(valShift): return struct.unpack('f',struct.pack('I',int(valShift,16)))[0];
        value = value[0:-1];
        # print("region: ", region);
        inputAddressList = region.split(" ");
        # print("region: ", region, "value", value);
        baseInt = int(inputAddressList[0],16);
        if(len(inputAddressList) == 1): ## its a direct pointer
            region = baseInt;
            if(region == 0x479D60): self.state["frame"] = convertToInt(value, 0)
            elif(region == 0x4530E0): self.state["p1"]["damage"] = convertToInt(value, 16);
            elif(region == 0x453F70): self.state["p2"]["damage"] = convertToInt(value, 16);
            elif(region == 0x45310E): self.state["p1"]["stock"] = convertToInt(value, 24);
            elif(region == 0x453F9E): self.state["p2"]["stock"] = convertToInt(value, 24);
            elif(region == 0x4530C0): self.state["p1"]["facing"] = convertToBool(value, 31);
            elif(region == 0x453F50): self.state["p2"]["facing"] = convertToBool(value, 31);
            elif(region == 0x453090): self.state["p1"]["x"] = convertToFloat(value);
            elif(region == 0x453F20): self.state["p2"]["x"] = convertToFloat(value);
            elif(region == 0x453094): self.state["p1"]["y"] = convertToFloat(value);
            elif(region == 0x453F24): self.state["p2"]["y"] = convertToFloat(value);
            elif(region == 0x3F0E0A): self.state["p1"]["character"] = convertToInt(value, 24);
            elif(region == 0x3F0E0A): self.state["p2"]["character"] = convertToInt(value, 24);
            elif(region == 0x479d30): self.state["menu"] = convertToInt(value, 0);
            elif(region == 0x4D6CAD): self.state["stage"] = convertToInt(value, 16);
            elif(region == 0x0111826C): self.state["p2"]["curosrX"] = convertToFloat(value);
            elif(region == 0x01118270): self.state["p2"]["curosrX"] = convertToFloat(value);
            # elif(value == 0x003F0E08): print("i dont know what this is ");
        elif(baseInt == 0x453FC0): ## player two
            self.adjustValueForPlayer(region, value, "p1", int(inputAddressList[1], 16));
        elif(baseInt == 0x453130): ## player one
            self.adjustValueForPlayer(region, value, "p2", int(inputAddressList[1], 16));
        # self.state.printState();

    def readMemory(self):
        if(not self.socket):
            print("the socket has not been created yet please create it before calling the pauseForTime function");
            return;
        datagram = self.socket.recv( 1024 ) # get the information from the socket
        # print (datagram)
        datagram = datagram.splitlines();
        region = datagram[0].decode('ascii');
        value = datagram[1];
        self.adjustValue(region, value);









# if __name__ == '__main__':
#     main();


