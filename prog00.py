# aaaa
# CSE 3521 - Programming Assignment 00
#
# Input - a text file (input) whose first line contains a string
#  and subsequent lines each contain a single integer; the input
#  file should be given as a command-line argument or default
#  'input' will be expected to be present
#
# Output - print a greeting addressed to the user's name (the 
#  string in the first line) in the stdout and display the integers 
#  read from the input file in ascending order to stdout
#
# 	by	Haribabu, Karpaka Vellaya (Hari)
# 	email	karpakavellaya.1@osu.edu
#
# Execution - this program requires the 'Queue' and 'string'
#   modules;
#   execution syntax
#       'python prog00.py [input_file]'
#   from the command-line in the directory that contains this code
#   and the input file
#   by default, the input_file is taken as 'input'
#   if that isn't present in the pwd, or if an argument input_file
#   is not given python throws "IOError: [Errno 2]"
# 

import sys
import Queue
import string

def main(argv):
	if argv == []:			# user didn't enter any arg
		input_file = "input"	# the default input file
	else:
		input_file = argv[0]	# user's input_file

	input = open(input_file, "r")

	text = input.readline()		# for the first line of o/p
	print "Hello", string.rstrip(text, "\n"), "!"

	pq = Queue.PriorityQueue()

	while True:
		text = input.readline()
		if text == "":		# EOF
			break
		pq.put(int(text))	# enter each number from
					# input_file

	while not pq.empty():		# print output
		print pq.get()

if __name__ == "__main__":
	main(sys.argv[1:])
