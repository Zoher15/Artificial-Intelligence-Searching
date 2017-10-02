#!/usr/bin/env python
#Assignment 1 Question 2 "Assigning Groups Problem" Elements of Artificial Intelligence by David Crandall
#Author: Zoher Kachwala

'''
SET OF STATES: All the possible combinations of the given list of students in different sized groups of 1,2 or 3
Counting group combinations for 6 students (with a maximum of 3 students per group) is an extremely time consuming calculation
(thanks to Professor Crandall when he hinted that he did not have "enough time" to even mathematically formulate this counting problem)
So naturally an optimal solution will always exist but extremely hard to achieve by going through each and every possible team combination.
So after a lot of trial and error I finally gave up and focused my efforts on a local search approach.


INITIAL STATE: All students as individual groups. 
This is needed as we need to consider the possibility that, for inputs where there are very few students who all dislike each other, 
it could indeed be cheaper just to let them be in individual groups by themselves.


COST FUNCTION: This is pretty straightforward just multiplying the values of k,m,n by referencing the number of unmet requests of a particular individual.


SUCCESSOR FUNCTION: Spending hours intuitively thinking about this problem led me to the conclusion that in order to minimize the cost of a state
significantly, I will have to prioritize satisfying the costliest group first. 
Intuitively this makes a lot of sense because a student with a maximum number like dislike requests is MOST likely to take up time by emails and meetings.
To achieve this I sort(reverse with the costliest one at 0th position) the groups in a state before producing its successors. So to produce successors 
the costliest group is the first one to have a pick at merging with any other groups in the state.

These successors are returned and if the cheapest one among them costs less than its predecessor, we choose this state and pass it recursively for minization.
Again this state undergoes a reverse sorting of groups. It could be that, now having merged once with another group in the state, we have a new costliest group.\
This costliest group will now get to produce successors by merging with remaining groups on the state. Its cheapest successor is compared with the cost of
the predecessor and then passed again recursively.

This process continues until the cost of the successor is not less than the cost of the predecessor. At that point we just return the predecessor and declare
it the goal state. This could be the LOCAL MINIMA and not the GLOBAL MINIMA. But after a lot of trials upto 100 students, I believe my code achieves a fairly
high balance of running time and final cost. Afterall, time is also another cost in an NP hard problem such as this 
and I believe my code especially shines in that respect:

Taking k=160,m=31,n=10 and for test files students10.txt,students15.txt,students20.txt,students50.txt,students100.txt,students150.txt,students200.txt
 10 students:   770  0.01s
 15 students:  1218  0.02s
 20 students:  1487  0.04s
 50 students:  3707  1.1s
100 students:  7229   44s
150 students: 10563   2m
200 students: 13913   8m
'''

import sys
#Just a basic function to store data from the text file into dictionaries for team cost calculation, and lists for team manipulations
def readAndStore(file):
	with open(file,"r") as f:
		f=f.read().splitlines()
		for line in f:
			student,teamSize,prefer,notPrefer=line.split(" ")
			if prefer is not "_":
				prefer=prefer.split(",")
			else:
				prefer=[]
			if notPrefer is not "_":
				notPrefer=notPrefer.split(",")
			else:
				notPrefer=[]
			studentInfoDict[student]=[teamSize,prefer,notPrefer]
			studentGroupsList.append([student])

#This function calculates the cost of a given state that contains all the students in any combinations as part of groups/teams
def costOfState(successor):
	cost=0
	for group in successor:
		cost=cost+k+costOfGroup(group)
	return cost

#This function calculates the cost of a given group/team in a state
def costOfGroup(group):
	cost=0
	for student in group:
		teamSizeCost=countUnmetTeamSizeDemand(student,group)
		preferCost=n*countUnmetPreferDemand(student,group)
		notprefercost=m*countUnmetNotPreferDemand(student,group)
		cost=cost+teamSizeCost+preferCost+notprefercost
	return cost

#This function counts if the teamsize preference has been met or not
def countUnmetTeamSizeDemand(student,group):
	teamSize=len(group)
	demand=ord(studentInfoDict[student][0])-48
	if teamSize is not demand:
		return 1
	else:
		return 0

#This function counts the numer of unmet/unsatisfied preferred members' demands/requests
def countUnmetPreferDemand(student,group):
	i=0
	for member in group:
		if member is not student:
			for preferMember in studentInfoDict[student][1]:
				if member==preferMember:
					i=i+1
	return len(studentInfoDict[student][1])-i

#This function counts the numer of unmet/unsatisfied not-preferred members' demands/requests
def countUnmetNotPreferDemand(student,group):
	i=0
	for member in group:
		if member is not student:
			for notpreferMember in studentInfoDict[student][2]:
				if member==notpreferMember:
					i=i+1
	return i

#Using a local search methodology this function minimizes the overall cost of a state by simply checking if any of the successor states have a smaller value than the current state
def minimizeTime(state):
	successors=successorStates(state)
	if len(successors)>0:
		#Using a built-in mimimum function to find the least cost successor
		leastCostSuccessor=min(successors,key=costOfState)
		if costOfState(leastCostSuccessor)<costOfState(state):
			return minimizeTime(leastCostSuccessor)
	else:
		return state
#This function produces successors of a state by trying to merge a group/team with the remaining groups/teams in the state 
def successorStates(state):
	#Using a built-in sort function to sort the groups in a descending order.This is because making the costliest group cheaper will help produce cheaper successors
	state=sorted(state,key=costOfGroup,reverse=True)
	successors=[]
	length=len(state)
	for i in range(0,length-1):
		for j in range(i+1,length):
			if len(state[i])+len(state[j])<=3:
				successors.append(addMergedGroup(state,i,j))
	return successors
#This function produces a state format by adding the new merged group
def addMergedGroup(groups,i,j):
	return groups[0:i]+[groups[i][:]+groups[j][0:]]+groups[i+1:j]+groups[j+1:]

#First State which contains all students as individual teams
studentGroupsList=[]
#Dictionary to store the preferences of each student which will be used to calculate costs
studentInfoDict={}
file = sys.argv[1]
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])
readAndStore(file)
#print"Loading lesser TIME (in lesser TIME needed to deal with students)....."
goalState=minimizeTime(sorted(studentGroupsList,key=costOfGroup,reverse=True))
for group in goalState:
	for student in group:
		print student,
	print ""
print costOfState(goalState)
