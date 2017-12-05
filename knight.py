import queue
import math
from operator import itemgetter
import timeit

#------------------------------------------------------
#Function to get positions that knight can move to from current position. Takes
#three arguments: cpos for current position, cpath for currently expanded path
#and s for board size (board is s by s)
def get_available_pos(cpos, cpath, s):

    #This ordering of the available destination checking is
    #from the related project article. It's clockwise.
    avails = []
    avails.append([cpos[0]-1, cpos[1]-2])
    avails.append([cpos[0]-2, cpos[1]-1])
    avails.append([cpos[0]-2, cpos[1]+1])
    avails.append([cpos[0]-1, cpos[1]+2])
    avails.append([cpos[0]+1, cpos[1]+2])
    avails.append([cpos[0]+2, cpos[1]+1])
    avails.append([cpos[0]+2, cpos[1]-1])
    avails.append([cpos[0]+1, cpos[1]-2])

    #Python does not allow deletion of list elements while iterating with for.
    #So a new list is way to go.
    result = []
    for x in avails:
        if x[0] in range(size) and x[1] in range(size) and x not in cpath:
            result.append(x)

    return result

#------------------------------------------------------
#Function to create the list of available destinations, and the order of list
#depends on available node amount from nodes found, and minimum distance to a corner
#from that node.
def h2_eval(cpos, cpath, s):

    reachable = []
    temp = get_available_pos(cpos, cpath, s)
    dist = []

    #Get number of reachable squares from available squares. Also get distance
    # between them and nearest corner.
    for x in temp:
        reachable.append(len(get_available_pos(x, cpath + [x], s)))
        dist.append(min([math.sqrt(x[0]**2 + x[1]**2), math.sqrt(x[0]**2 + ((s-1)-x[1])**2), math.sqrt(((s-1)-x[0])**2 + x[1]**2), math.sqrt(((s-1)-x[0])**2 + ((s-1)-x[1])**2)]))

    preresult = []

    #Merdge lists into type [x coordinate, y coordinate, number of nodes available from that one, distance to corner]
    for x in range(len(temp)):
        preresult.append([temp[x][0], temp[x][1], reachable[x], dist[x]])

    #Sort the list. This puts nodes with least available destinations into first places. As tiebreaker,
    #distance is used.
    preresult = sorted(preresult, key=itemgetter(2,3))

    result = []

    for x in preresult:
       result.append([x[0], x[1]])

    return result

#------------------------------------------------------
#Required inputs to program
size = int(input("Enter size: "))
type = input("Enter mode(a = DFS, b = BFS, c = Node Selection): ")
tlimit = float(input("Enter time limit(seconds): "))
limitreach = 0

#Current knight position and currently expanded path
current_position = []
current_path = []

#DFS uses LIFO queue and BFS uses FIFO queue.
if type == "a" or type == "c":
    frontier = queue.LifoQueue()
elif type == "b":
    frontier = queue.Queue()

#Initial position of knight is put into frontier. Because we did this, expanded node
#counter starts from 1 instead of 0.
frontier.put([[0, 0]])

#Total expanded node counter
tctr = 1

start_time = timeit.default_timer()
#If frontier is empty, this means we tried every combination and there is no solution.
while not frontier.empty():

    #Get first element of frontier queue as current path. Current position is last node on current path.
    current_path = frontier.get()
    current_position = current_path[len(current_path)-1]

    #If current path length is equal to number of squares on board, we have found a solution.
    if(len(current_path) == size**2):
        break

    #On DFS and BFS, next available nodes are directly appended to the (maximum) first eight paths on queue.
    #On Node Selection, evaluation function builds the set of nodes that will be appended.
    if type == "a" or type == "b":
        prefrontier = get_available_pos(current_position, current_path, size)
    elif type == "c":
        prefrontier = h2_eval(current_position, current_path, size)

    #If it's not BFS, revert the incoming list order because it's LIFO.
    if type != "b":
        prefrontier = list(reversed(prefrontier))

    #If there are remaining moves to do, add new path to frontier, otherwise no need to do this.
    if len(prefrontier)!=0:
        for x in prefrontier:
            frontier.put(current_path + [x])

    tctr += 1

    #If time limit is reached, break the loop.
    if timeit.default_timer() - start_time > tlimit:
        limitreach = 1
        break

#Final results printed to screen for the sake of testing.
if(frontier.empty()):
    print("No solution.")
elif limitreach == 1:
    print("Timeout.")
else:
    print(tctr, " nodes expanded")
    print("Found Path: ", current_path)
    print("in ", timeit.default_timer() - start_time, " seconds")
