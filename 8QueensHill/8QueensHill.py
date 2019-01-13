#-*- coding: utf-8 -*-
# Solution for eight queens problem using the hill climbing algorithm

import random
import time

possibleStatements = 0 # The number of analyzed possible statements
changeStatements = 0 # The number of statement changes
randomRestarts = 0 # The number of random restarts

def randomState():
	# Initialize the board
	items = [0, 1, 2, 3, 4, 5, 6, 7]
	random.shuffle(items)
	return items

	
def stateValue(state):
	# The number of illegal statements
	value = 0
	
	for i in range(8):
		for j in range(8):
			if i != j and (abs(i-j) == abs(state[i]-state[j]) or state[i] == state[j]):
				value += 1
	
	return value/2 # For duplicate statements
	

def selectNextMove(currentState, iteration):
	# Calculate value for every position of queen where same column
	tempState = list(currentState)
	passIt = tempState[iteration] # For same statement; current and next.
	bestValue = 28 # Worst-case
	global possibleStatements
	
	for i in range(8):
		
		if i != passIt: # Don't control to same statement
		
			tempState[iteration] = i
			currentValue = stateValue(tempState) # The number of illegal statements
			print "i:",i, " currentValue:",currentValue," tempState:", tempState 
			
			if currentValue < bestValue: # Choose the best statement
				bestValue = currentValue
				bestState = list(tempState)
				print "change i:",i," bestValue:",bestValue," bestState:",bestState
			
			possibleStatements += 1
			
	return bestState, bestValue
					

def hillClimbing(initState, selectNextMove, stateValue):
	
	currentState = initState
	currentValue = stateValue(currentState)
	
	global changeStatements
	global randomRestarts
	iteration = 0
	
	while True:
		
		print "iteration:", iteration," currentValue:",currentValue," currentState:",currentState
			
		nextState, nextValue = selectNextMove(currentState, iteration) # Find the best next statement
		print "iteration:", iteration," nextValue:",nextValue," nextState:",nextState,"\n\n"
        
		if nextValue < currentValue: # Compare number of illegal statements
			currentState = list(nextState)
			currentValue = nextValue
			print "statement changed  currentState:",currentState," currentValue:",currentValue,"\n\n"
			
			changeStatements += 1
			
			if currentValue == 0: # Problem was solved?
				return currentState

		elif iteration == 7: # If algorithm doesn't climb and all columns finished, board refresh
			print "Problem didn't solve. Restarting..\n\n"
			randomRestarts += 1
			return hillClimbing(randomState(), selectNextMove, stateValue)
			break;
					
		iteration = (iteration+1)%8 # When 8 columns finish, iteration restarts

        
		
if __name__=='__main__':
	
	start = time.time()
	
	initState = randomState()
	resultStatement = hillClimbing(initState, selectNextMove, stateValue)
	print "Result Statement:",resultStatement
	
	elapsed = (time.time() - start)
	print "\nTotal processing time:",elapsed,"seconds"
	print "\nThe number of analyzed possible statements:",possibleStatements
	print "\nThe number of statement changes:",changeStatements
	print "\nThe number of random restarts:",randomRestarts
