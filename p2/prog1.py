#
# This code is as though the robots are on the left side of the chasm and the
# base station is on the right side of the chasm; all naming will follow this
#
# ABCDP
#

import sys
import Queue

def ExpandNode(sLeft, sRight):
    # sLeft, sRight = Agent.sLeft, Agent.sRight
    Direction = 0               # direction is from left to right by default

    RightLen = len(sRight)
    idx = 0
    while idx < RightLen:
        if sRight[idx] == 'P':
           Direction = 1        # direction is from right to left
        idx += 1

    if Direction == 0:
        sFrom, sTo = sLeft, sRight
    else:
        sFrom, sTo = sRight, sLeft

    idx = 0
    lenFrom = len(sFrom)
    MovingList = []

    while idx < lenFrom-2:
        print "idx is",idx
        Moving = ""
        if Direction == 0:
            PendingRobot, PendingPack  = 2, 1
        else:
            PendingRobot, PendingPack  = 1, 1

        if sFrom[idx] == 'P':
            Moving = Moving+sFrom[idx]
            PendingPack -= 1
        else:
            Moving = Moving+sFrom[idx]
            PendingRobot -= 1

        idx2 = idx+1
        while idx2 < lenFrom-1:
            if PendingPack != 0 && sFrom[idx2] == 'P':
                Moving = Moving+sFrom[idx2]
                PendingPack -= 1
            else if PendingRobot != 0
                Moving = Moving+sFrom[idx2]
                PendingRobot -= 1

            idx3 = idx2+1
            while idx3 < lenFrom && (PendingPack != 0 
            initial_idx2 = idx2
            print "idx2 is", idx2
            if sFrom[idx2] == 'P' and PendingPack != 0:
                Moving = Moving+sFrom[idx2]
                PendingPack -= 1
            elif sFrom[idx2] != 'P' and PendingRobot != 0:
                Moving = Moving+sFrom[idx2]
                PendingRobot -= 1

            if PendingPack == 0 and PendingRobot == 0:
                # Moving is now a good set
                MovingList = MovingList + [Moving]
                Moving = sFrom[idx]
                if Direction == 0:
                    PendingRobot, PendingPack = 2, 1
                else:
                    PendingRobot, PendingPack = 1, 1
                if sFrom[idx] == 'P':
                    PendingPack -= 1
                else:
                    PendingRobot -= 1
            idx2 = initial_idx2+1
        idx += 1
    print MovingList
    return MovingList

#class DFSAgent:
#    def __init__(self):
#
#    def findPath(self, sLeft, sRight)
#        self.sLeft, self.sRight = sLeft, sRight
#        listExpanded = ExpandNode(self)

#class BFSAgent:
#    def __init__(self):
#
#    def findPath(self, sLeft, sRight)
#        self.sLeft  = sLeft
#        self.sRight = sRight

#class UCAgent:
#    def __init__(self):
#
#    def findPath(self, sLeft, sRight)
#        self.sLeft  = sLeft
#        self.sRight = sRight

#class AStarAgent:
#    def __init__(self):
#
#    def findPath(self, sLeft, sRight)
#        self.sLeft  = sLeft
#        self.sRight = sRight

def main(argv):
    ExpandNode("ABCDP", "")

if __name__ == "__main__":
    main(sys.argv[1:])
