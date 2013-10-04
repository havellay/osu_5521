# submitted by Karpaka Vellaya Haribabu
#   karpakavellaya.1@osu.edu
#
# This code shows the different methods to transport robots across a cliff
# given the limitations of battery power.
# A limitation of the program is that it doesn't explicitly always tell the
# cost of the complete transportation activity - However, the number should
# be easily apparent from the output.
#
# for A* search, the heuristic employed is that each robot travels at the 
# speed of the fastest robot in the bunch which is A
#
# the program should be executable through stdlinux
#
# to provide different output, the function FindTrueCost() would have to be
# modified and different input would have to be supplied from the main()
# method.
#
# This code is as though the robots are on the left side of the chasm and the
# base station is on the right side of the chasm; all naming will follow this
#
# ABCDP
#
        # A -> 1 min
        # B -> 2 min
        # C -> 5 min
        # D -> 10 min

import sys
from Queue import PriorityQueue

def ExpandNode(Agent, sLeft, sRight):
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
    ReturnSet=[]

    if Direction == 0:
        for x in list(sFrom):
            idx+=1
            listy=list(sFrom[idx:])
            for y in listy:
                for z in ['P']:
                    if x!=y and x!=z and y!=z:
                        cost = Agent.FindCost([x,y,z])
                        ReturnSet+=[[cost,sLeft,sRight,x,y,z]]
    else:
        for x in list(sFrom):
            for y in ['P']:
                if x!=y:
                    cost = Agent.FindCost([x,y])
                    ReturnSet+=[[cost,sLeft,sRight,x,y]]

    return ReturnSet

class DFSAgent:
    def __init__(self):
        self.PQ = PriorityQueue();
        self.CurDepth = 9999
        self.MinCurDepth = 9998
        self.PathFound = False
        self.NodeCount = 1
        self.SolutionSet = []

    def FindCost(self, Action):
        return self.CurDepth-1

    def FindTrueCost(self, Action):
        cost = 0
        for ch in Action:
            if ch == 'A' and cost < 1:
                cost = 1
            elif ch == 'B' and cost < 2:
                cost = 2
            elif ch == 'C' and cost < 5:
                cost = 5
            elif ch == 'D' and cost < 10:
                cost = 10
        return cost

    def FindPath(self, sLeft, sRight):
        while self.PathFound == False:
            listExpanded = ExpandNode(self, sLeft, sRight)
            x_set = []
            for x in listExpanded:
                x = x[0:1]+[self.NodeCount]+[0]+x[1:]
                self.NodeCount+=1
                x_set = x_set+[x]
            listExpanded = x_set
            self.PushAndPop(listExpanded)
            if self.PathFound == True:
                print "Solution found through DFS"
                return self.SolutionSet
            else:
                print "Adjusting MinCurDepth and reset CurDepth"
                print "\tPrevious MinCurDepth was "+str(self.MinCurDepth)
                self.MinCurDepth = self.MinCurDepth-1
                print "\tCurrent MinCurDepth is "+str(self.MinCurDepth)
                self.CurDepth = 9999
                self.NodeCount = 0
                self.PQ = PriorityQueue()

    def PushAndPop(self, listExpanded):
        print "Nodes Added to Tree",listExpanded
        for Action in listExpanded:
            self.PQ.put(Action)
        if self.PQ.empty() == True:
            return
        BestAction = self.PQ.get()
        while BestAction[0] < self.MinCurDepth:
            if self.PQ.empty() == True:
                return
            BestAction = self.PQ.get()
        self.CurDepth = BestAction[0]
        print "Node Going to be expanded",BestAction
        if BestAction[3] == "":
            self.PathFound = True
            self.LookingFor = BestAction[2]
            self.SolutionSet = self.SolutionSet+[[BestAction, "cost", 0]]
            return
        else:
            sLeft = BestAction[3]
            sRight = BestAction[4]
            for x in BestAction[5:]:
                if type(x) != str:
                    continue
                if sLeft.find(x) != -1:
                    sLeft = sLeft.replace(x,"")
                    sRight = sRight+x
                else:
                    sRight=sRight.replace(x,"")
                    sLeft=sLeft+x
            new_listExpanded = ExpandNode(self, sLeft, sRight)
            x_set = []
            for x in new_listExpanded:
                x = x[0:1]+[self.NodeCount]+[BestAction[1]]+x[1:]
                self.NodeCount+=1
                x_set = x_set+[x]
            new_listExpanded = x_set
            self.PushAndPop(new_listExpanded)
            if self.PathFound == True and self.LookingFor == BestAction[1]:
                self.LookingFor = BestAction[2]
                cost = self.FindTrueCost(BestAction[5:])
                self.SolutionSet = self.SolutionSet+[[BestAction, "cost", cost]]
                return
        
class BFSAgent:
    def __init__(self):
        self.PQ = PriorityQueue();
        self.CurDepth = 1
        self.PathFound = False
        self.NodeCount = 1
        self.SolutionSet = []

    def FindCost(self, Action):
        return self.CurDepth+1

    def FindTrueCost(self, Action):
        cost = 0
        for ch in Action:
            if ch == 'A' and cost < 1:
                cost = 1
            elif ch == 'B' and cost < 2:
                cost = 2
            elif ch == 'C' and cost < 5:
                cost = 5
            elif ch == 'D' and cost < 10:
                cost = 10
        return cost

    def FindPath(self, sLeft, sRight):
        while self.PathFound == False:
            listExpanded = ExpandNode(self, sLeft, sRight)
            x_set = []
            for x in listExpanded:
                x = x[0:1]+[self.NodeCount]+[0]+x[1:]
                self.NodeCount+=1
                x_set = x_set+[x]
            listExpanded = x_set
            self.PushAndPop(listExpanded)
            if self.PathFound == True:
                print "Solution found using BFS"
                return self.SolutionSet

    def PushAndPop(self, listExpanded):
        print "Nodes Added to Tree",listExpanded
        print listExpanded
        for Action in listExpanded:
            self.PQ.put(Action)
        if self.PQ.empty() == True:
            return
        BestAction = self.PQ.get()
        self.CurDepth = BestAction[0]
        print "Node Going to be expanded",BestAction
        if BestAction[3] == "":
            self.PathFound = True
            self.LookingFor = BestAction[2] # parent
            self.SolutionSet = self.SolutionSet+[[BestAction, "cost", 0]]
            return
        else:
            sLeft = BestAction[3]
            sRight = BestAction[4]
            for x in BestAction[5:]:
                if type(x) != str:
                    continue
                if sLeft.find(x) != -1:
                    sLeft = sLeft.replace(x,"")
                    sRight = sRight+x
                else:
                    sRight=sRight.replace(x,"")
                    sLeft=sLeft+x
            new_listExpanded = ExpandNode(self, sLeft, sRight)
            x_set = []
            for x in new_listExpanded:
                x = x[0:1]+[self.NodeCount]+[BestAction[1]]+x[1:]
                self.NodeCount+=1
                x_set = x_set+[x]
            new_listExpanded = x_set
            self.PushAndPop(new_listExpanded)
            if self.PathFound == True and self.LookingFor == BestAction[1]:
                self.LookingFor = BestAction[2]
                cost = self.FindTrueCost(BestAction[5:])
                self.SolutionSet = self.SolutionSet + [[BestAction, "cost", cost]]

class UCSAgent:
    def __init__(self):
        self.PQ = PriorityQueue();
        self.PathFound = False
        self.NodeCount = 1
        self.SolutionSet = []
        self.CurrentCost = 0

    def FindCost(self, Action):
        return self.CurrentCost+self.FindTrueCost(Action)

    def FindTrueCost(self, Action):
        cost = 0
        for ch in Action:
            if ch == 'A' and cost < 1:
                cost = 1
            elif ch == 'B' and cost < 2:
                cost = 2
            elif ch == 'C' and cost < 5:
                cost = 5
            elif ch == 'D' and cost < 10:
                cost = 10
        return cost

    def FindPath(self, sLeft, sRight):
        while self.PathFound == False:
            listExpanded = ExpandNode(self, sLeft, sRight)
            x_set = []
            for x in listExpanded:
                x = x[0:1]+[self.NodeCount]+[0]+x[1:]
                self.NodeCount+=1
                x_set = x_set+[x]
            listExpanded = x_set
            self.PushAndPop(listExpanded)
            if self.PathFound == True:
                print "Solution found using UCS"
                return self.SolutionSet

    def PushAndPop(self, listExpanded):
        print "Nodes Added to Tree",listExpanded
        for Action in listExpanded:
            self.PQ.put(Action)
        if self.PQ.empty() == True:
            return
        BestAction = self.PQ.get()
        self.CurrentCost = BestAction[0]
        print "Node Going to be expanded",BestAction
        if BestAction[3] == "":
            self.PathFound = True
            self.LookingFor = BestAction[2]
            self.SolutionSet = self.SolutionSet+[[BestAction, "cost", 0]]
            return
        else:
            sLeft = BestAction[3]
            sRight = BestAction[4]
            for x in BestAction[5:]:
                if type(x) != str:
                    continue
                if sLeft.find(x) != -1:
                    sLeft = sLeft.replace(x,"")
                    sRight = sRight+x
                else:
                    sRight=sRight.replace(x,"")
                    sLeft=sLeft+x
            new_listExpanded = ExpandNode(self, sLeft, sRight)
            x_set = []
            for x in new_listExpanded:
                x = x[0:1]+[self.NodeCount]+[BestAction[1]]+x[1:]
                self.NodeCount+=1
                x_set = x_set+[x]
            new_listExpanded = x_set
            self.PushAndPop(new_listExpanded)
            if self.PathFound == True and self.LookingFor == BestAction[1]:
                self.LookingFor = BestAction[2]
                cost = self.FindCost(BestAction[5:])
                self.SolutionSet = self.SolutionSet + [[BestAction, "cost", cost]]

class AStarAgent:
    def __init__(self):
        self.PQ = PriorityQueue();
        self.PathFound = False
        self.NodeCount = 1
        self.SolutionSet = []
        self.CurrentCost = 0

    def FindCost(self, Action):
        return self.CurrentCost+self.FindTrueCost(Action)+self.HeuristicCost(Action)

    def HeuristicCost(self, Action):
        return 1

    def FindTrueCost(self, Action):
        cost = 0
        for ch in Action:
            if ch == 'A' and cost < 1:
                cost = 1
            elif ch == 'B' and cost < 2:
                cost = 2
            elif ch == 'C' and cost < 5:
                cost = 5
            elif ch == 'D' and cost < 10:
                cost = 10
        return cost

    def FindPath(self, sLeft, sRight):
        while self.PathFound == False:
            listExpanded = ExpandNode(self, sLeft, sRight)
            x_set = []
            for x in listExpanded:
                x = x[0:1]+[self.NodeCount]+[0]+x[1:]
                self.NodeCount+=1
                x_set = x_set+[x]
            listExpanded = x_set
            self.PushAndPop(listExpanded)
            if self.PathFound == True:
                print "Solution found through AStar"
                return self.SolutionSet

    def PushAndPop(self, listExpanded):
        print "Nodes Added to Tree",listExpanded
        for Action in listExpanded:
            self.PQ.put(Action)
        if self.PQ.empty() == True:
            return
        BestAction = self.PQ.get()
        self.CurrentCost = BestAction[0]
        print "Node Going to be expanded",BestAction
        if BestAction[3] == "":
            self.PathFound = True
            self.LookingFor = BestAction[2]
            self.SolutionSet = self.SolutionSet+[[BestAction, "cost", 0]]
            return
        else:
            sLeft = BestAction[3]
            sRight = BestAction[4]
            for x in BestAction[5:]:
                if type(x) != str:
                    continue
                if sLeft.find(x) != -1:
                    sLeft = sLeft.replace(x,"")
                    sRight = sRight+x
                else:
                    sRight=sRight.replace(x,"")
                    sLeft=sLeft+x
            new_listExpanded = ExpandNode(self, sLeft, sRight)
            x_set = []
            for x in new_listExpanded:
                x = x[0:1]+[self.NodeCount]+[BestAction[1]]+x[1:]
                self.NodeCount+=1
                x_set = x_set+[x]
            new_listExpanded = x_set
            self.PushAndPop(new_listExpanded)
            if self.PathFound == True and self.LookingFor == BestAction[1]:
                self.LookingFor = BestAction[2]
                cost = self.FindCost(BestAction[5:])
                self.SolutionSet = self.SolutionSet + [[BestAction, "cost", cost]]

def PrintSolution(SolutionSet):
    print "\tsolution from last node to first"
    for x in SolutionSet:
        print "\t\tCurrent Node Number", x[0][1]
        print "\t\tParent of Current Node", x[0][2]
        print "\t\tString representing Robots on left side of cliff", x[0][3]
        print "\t\tString representing Robots on right side of cliff", x[0][4]
        print "\t\tUnits to be moved (Robot / Battery Pack to side without Battery)", x[0][5:]
        print "\t\tCost to make the move", x[2]

def main(argv):
    DFSA = DFSAgent()
    DFSASolution = DFSA.FindPath("ABCDP","")

    BFSA = BFSAgent()
    BFSASolution = BFSA.FindPath("ABCDP","")

    UCSA = UCSAgent()
    UCSASolution = UCSA.FindPath("ABCDP","")

    ASA = AStarAgent()
    ASASolution = ASA.FindPath("ABCDP","")

    print "Solution through Depth First Search :"
    PrintSolution(DFSASolution)
    print ""

    print "Solution through Breadth First Search :"
    PrintSolution(BFSASolution)
    print ""

    print "Solution through Uniform Cost Search :"
    PrintSolution(UCSASolution)
    print ""

    print "Solution through AStarSearch :"
    PrintSolution(ASASolution)
    print ""

if __name__ == "__main__":
    main(sys.argv[1:])
