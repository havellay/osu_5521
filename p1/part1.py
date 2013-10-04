#
# CSE 3521 - Programming Assignment 01 (Part1)
#
# Input - one text file containing a single integer in each line and several
#  such lines; this text files is expected to contain the ranks of the ojects
#  coming down the Conveyer Belt in this environment. The assumption is that the 
#  file is well formatted. Occurrence of two '-1' ranks in this text file
#  will denote that we have reached the end of the belt
#
# Output - a sequence of text printed to stdout that explains the values input
#  to this agent, the state of the agent and the action taken by the agent
#
#	by	Haribabu, Karpaka Vellaya (Hari)
#	email	karpakavellaya.1@osu.edu
#
# Execution - this program requires the 'sys' and 'string' python modules
#   execution syntax :
#	'python part2.py [Belt_file]'
#   if the input file 'Belt_file' is not specified by the user, then the
#   default file "inp" that is provided with this code is used as input.
#   An alternate method of providing custom input to the program would be 
#   to edit the contents of the file "inp".
#
# For the last element in the belt, this agent always decides to PICKUP the item;
# This is so that this program behaves in the same way as the example shown in
# the Question
#

import sys
import string

class ConveyerBelt:
	def __init__(self, BeltFileName):
		self.RankSet = []	# Ranks are stored in a set
		self.EOB = 0		# EOB denotes the end of belt; ie., the
					# end farthest from this Agent's sensors
		self.pos = 0		# pos denotes the location on the belt
					# closest to the agent's sensors

		BeltFile = open(BeltFileName, "r")
		while True:
			val = string.rstrip(BeltFile.readline(), "\n")
			if val == "":
				break
			self.RankSet = self.RankSet + [int(val)]
					# all ranks are read and stored in the
					# set RankSet
			self.EOB+=1

	def GetRanks(self):
		Ranks = self.RankSet[self.pos : self.pos+2]
		return Ranks

	def Advance(self):
		self.pos+=1

	def Pickup(self):
		self.RankSet[self.pos] = 0

class Agent:
	def ReflexAgent(self, percept1, percept2):
		# percept1 is Rank of EOB and percept2 is Rank of EOB+1
		# this agent has no set variables and so, no member variables
		# in this implementation of this class Agent
		if percept1 == 0 and percept2 == -1:
			return "ADVANCE"
		elif percept1 == -1:
			return "STOP"
		elif percept1 > percept2:
			return "PICKUP"
		else:
			return "ADVANCE"

def main(argv):
	if argv == []:
		belt_filename = "inp"
	else:
		belt_filename = argv[0]

	CB = ConveyerBelt(belt_filename)
	RA = Agent()

	ranks = CB.GetRanks()
	while True:
		print "INPUT PERCEPTION:", ranks[0], ranks[1]
		action = RA.ReflexAgent(ranks[0], ranks[1])
		print "OUTPUT ACTION:", action

		if action == "PICKUP":
			CB.Pickup()
		elif action == "ADVANCE":
			CB.Advance()
		elif action == "STOP":
			return 

		ranks = CB.GetRanks()

if __name__ == "__main__":
	main(sys.argv[1:])
