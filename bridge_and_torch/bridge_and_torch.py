"""

    Bridge and Torch Problem:
    Four people come to a river in the night. 
    There is a narrow bridge, but it can only hold two people at a time. 
    They have one torch and, because it's night, the torch has to be used 
    when crossing the bridge. Person A can cross the bridge in one minute, 
    B in two minutes, C in five minutes, and D in eight minutes. 
    When two people cross the bridge together, they must move at the 
    slower person's pace. The question is, can they all get across 
    the bridge in 15 minutes or less? (From Wikipedia)
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
    
    Copyright (C) 2012 Enes Ates
    
    Authors: Enes Ates - enes@enesates.com

"""

left_side  = [1, 2, 5, 8] # people in left side of the river
right_side = []  # people in right side of the river
solution   = []  # solution steps
time       = 0   # total cost

# pass from left side to right side
def to_right(left_side, right_side, i, j, time, solution):
    
    # two people pass at a time
    right_side.append(left_side[i])
    right_side.append(left_side[j])
    
    # slower person's pace
    if(left_side[i] > left_side[j]):
        time += left_side[i]
    else:
        time += left_side[j]
    
    # add to solution step
    solution.append("to_right: "+str(left_side[i])+","+str(left_side[j])+" (time: "+str(time)+")")
    
    left_side.remove(left_side[i])
    left_side.remove(left_side[j-1])
    
    print left_side, right_side, time, solution
    return left_side, right_side, time, solution

# pass from right side to left side
def to_left(left_side, right_side, k, time, solution):
    
    # one person pass at a time
    left_side.append(right_side[k])
     
    time += right_side[k]
    
    # add to solution step
    solution.append("to_left: "+str(right_side[k])+" (time: "+str(time)+")")
        
    right_side.remove(right_side[k])
    
    print left_side, right_side, time, solution 
    return left_side, right_side, time, solution

# main function
def bridge_and_torch(left_side, right_side, time, solution):
    
    # temporary variables for recursive function
    left1 = left2 = right1 = right2 = []
    time1 = time2 = 0
    solution1 = solution2 = []
    
    # possibility for all people 
    for a in range (0, len(left_side)-1):  
        for b in range (a+1, len(left_side)):
            
            left1, right1, time1, solution1  = to_right(list(left_side), list(right_side), a, b, time, list(solution))
            
            # if there is no person in the left side, it is finished
            if len(left1) == 0:
                if time1 <= 15: # if total cost <= 15, problem is solved 
                    print "\nSolution:", solution1,"\n"
                return
            
            for c in range (0, len(right1)):
                
                left2, right2, time2, solution2 = to_left(list(left1), list(right1), c, time1, list(solution1))
                
                # recursive function for subtree
                bridge_and_torch(left2, right2, time2, solution2)
 
                
bridge_and_torch(left_side, right_side, time, solution)