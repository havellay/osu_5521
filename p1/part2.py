#
# CSE 3521 - Programming Assignment 01 (Part2)
#
# Input - two text files containing a single integer in each line and several
#  such lines; these text files are expected to contain the ranks of the ojects
#  coming down the Conveyer Belts in our environment. The assumption is that the 
#  files are well formatted. Occurrence of two '-1' ranks in these text files
#  will denote that we have reached the end of that belt
#
# Output - a sequence of text printed to stdout that explains the values input
#  to our agent, the state of the agent and the action taken by the agent
#
#	by	Haribabu, Karpaka Vellaya (Hari)
#	email	karpakavellaya.1@osu.edu
#
# Execution - this program requires the 'sys' and 'string' python modules
#   execution syntax :
#	'python part2.py [BeltA_file BeltB_file]'
#   if the input files 'BeltA_file' and 'BeltB_file' are not specified by the
#   user, then the default files "Belt_A" and "Belt_B" that are provided with
#   this code are used as input. An alternate method of providing custom input
#   to the program would be to edit the contents of the files "Belt_A" and
#   "Belt_B". This program is governed by a parameter that denotes the energy
#   or power available to our agent; this is hardcoded to 20 units. To change
#   this, the only way is to change the line in the main() method that assigns
#   20 to current_power to any desired value
#

import sys
import string

class ConveyerBelt:
	def __init__(self, BeltFileName):
		self.RankSet = []	# Ranks are stored in a set
		self.EOB = 0		# EOB denotes the end of belt; ie., the
					# end farthest from our Agent's sensors
		self.pos = 0		# pos denotes the location on the belt
					# closest to the Agent's sensors

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

class AgentWithState:
	def __init__(self):
		self.Slot_1 = 0		# AgentState : content of slot 1
		self.Slot_2 = 0		# AgentState : content of slot 2
		self.Picked = 0		# AgentState : item picked
					#   agent only commands which is picked
		self.RelativeBeltPos = 0	# 0 means both belts are at same
						# position from where they started

	def printAgentState(self):
		print "AGENT STATE:"
		print "\tINPUT:", self.inp
		print "\tSTATE VARIABLES", self.Slot_1, self.Slot_2, self.Picked, self.RelativeBeltPos

	def reflexAgentWithState(self, belta_current, belta_next, beltb_current,
				 beltb_next, current_power):
		self.inp = [belta_current, belta_next, beltb_current,
			    beltb_next, current_power]
			# 'inp'	is a set of input values given to the agent
			# this forms a part of the agent's state though the
			# agen never uses this set for reference; it is only
			# useful for printing the agent's STATE VARIABLES
		if current_power == 0:
			return "STOP"

		if self.Picked != 0:
			if self.Slot_1 == 0:
				self.Slot_1 = self.Picked
				self.Picked = 0
				return "FILL_1"
			elif self.Slot_2 == 0:
				self.Slot_2 = self.Picked
				self.Picked = 0
				return "FILL_2"
			elif self.Picked > self.Slot_1:
				self.Slot_1 = 0
				return "DROP_1"
			elif self.Picked > self.Slot_2:
				self.Slot_2 = 0
				return "DROP_2"

			# to make sure that one belt doesn't starve, we
			# try to keep RelativeBeltPos (which is a delta
			# between the current position of the two belts)
			# at a minimum; negative RelativeBeltPos means that
			# belt B is lagging behind belt A and vice versa
		if self.RelativeBeltPos < 0:
			if beltb_current == 0 and beltb_next == -1:
				self.RelativeBeltPos += 1
				return "ADVANCE_B"
			elif beltb_current == -1:
				return "STOP"
			elif beltb_current > beltb_next:
				self.Picked = beltb_current
				return "PICKUP_B"
			else:
				self.RelativeBeltPos += 1
				return "ADVANCE_B"
		else:
			if belta_current == 0 and belta_next == -1:
				self.RelativeBeltPos -= 1
				return "ADVANCE_A"
			elif belta_current == -1:
				return "STOP"
			elif belta_current > belta_next:
				self.Picked = belta_current
				return "PICKUP_A"
			else:
				self.RelativeBeltPos -= 1
				return "ADVANCE_A"

class Slot:
	def __init__(self):
		self.value = 0		# only variable associated with a
					# slot is its value

	def drop(self):
		self.value = 0
		return

	def fill(self, val):
		self.value = val
		return

def main(argv):
	if argv == []:
		Belt_A_filename = "Belt_A"  # default filename is Belt_A, Belt_B
		Belt_B_filename = "Belt_B"
	else:
		Belt_A_filename = argv[0]
		Belt_B_filename = argv[1]

	Belt_A = ConveyerBelt(Belt_A_filename)
	Belt_B = ConveyerBelt(Belt_B_filename)
	one = Slot()
	two = Slot()
	RA = AgentWithState()
	current_power = 20	# please edit this value to make more (or less)
				# electric power available to our agent
	InHand = 0		# this variable makes it seem like the values
				# marked as 'to be picked' by our agent are
				# actually 'handled' by our Test Harness

	ranks = Belt_A.GetRanks() + Belt_B.GetRanks()

	while True:
		print "INPUT PERCEPTION:", ranks[0], ranks[1], ranks[2], ranks[3], current_power
		action = RA.reflexAgentWithState(ranks[0], ranks[1], ranks[2], ranks[3], current_power)
		print "OUTPUT ACTION:", action
		RA.printAgentState()

		current_power -= 1	# all operations after this except
					# "STOP" will result in current_power
					# reducing by 1 unit

		if action == "PICKUP_A":
			InHand = ranks[0]
			Belt_A.Pickup()
		elif action == "PICKUP_B":
			InHand = ranks[2]
			Belt_B.Pickup()
		elif action == "ADVANCE_A":
			Belt_A.Advance()
		elif action == "ADVANCE_B":
			Belt_B.Advance()
		elif action == "DROP_1":
			one.drop()
		elif action == "FILL_1":
			one.fill(InHand)
			InHand = 0
		elif action == "FILL_2":
			two.fill(InHand)
			InHand = 0
		elif action == "STOP":
			current_power += 1	# this makes no difference becasue
			return 			# the system will be stopped now
						# anyway
		ranks = Belt_A.GetRanks() + Belt_B.GetRanks()

if __name__ == "__main__":
	main(sys.argv[1:])
