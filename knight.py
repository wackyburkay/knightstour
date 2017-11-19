import queue
import math
from operator import itemgetter
import timeit

def print_board(board):
    for x in range(len(board)):
        print(board[x])
        #board print edilirken board[y][x] şeklinde print ediliyor
        #origin sol üst köşe, unutma bunu.

def get_available_pos(cpos, cpath, s):

    #Optimum sonuç için, bu sırada olması gerekiyor
    avails = []
    avails.append([cpos[0]-1, cpos[1]-2])
    avails.append([cpos[0]-2, cpos[1]-1])
    avails.append([cpos[0]-2, cpos[1]+1])
    avails.append([cpos[0]-1, cpos[1]+2])
    avails.append([cpos[0]+1, cpos[1]+2])
    avails.append([cpos[0]+2, cpos[1]+1])
    avails.append([cpos[0]+2, cpos[1]-1])
    avails.append([cpos[0]+1, cpos[1]-2])

    #for loop içerisinde item silmek permitted olmadığından ikinci bir listeye atıyoruz.
    result = []
    for x in avails:
        if x[0] in range(size) and x[1] in range(size) and x not in cpath:
            result.append(x)

    return result

def h2_eval(cpos, cpath, s):

    reachable = []
    temp = get_available_pos(cpos, cpath, s)
    dist = []
    for x in temp:
        reachable.append(len(get_available_pos(x, cpath + [x], s)))
        dist.append(min([math.sqrt(x[0]**2 + x[1]**2), math.sqrt(x[0]**2 + (4-x[1])**2), math.sqrt((4-x[0])**2 + x[1]**2), math.sqrt((4-x[0])**2 + (4-x[1])**2)]))

    preresult = []

    for x in range(len(temp)):
        preresult.append([temp[x][0], temp[x][1], reachable[x], dist[x]])

    preresult = sorted(preresult, key=itemgetter(2,3))

    result = []

    for x in preresult:
       result.append([x[0], x[1]])

    return result

size = int(input("Enter size: "))
type = input("Enter mode(a = DFS, b = BFS, c = Node Selection): ")

#Gereksiz board, test amaçlı
board = [[0 for rows in range(size)] for cols in range(size)]

#Şu an atın bulunduğu pozisyon ve o pozisyona dek izlediği yol
current_position = []
current_path = []


if type == "a" or type == "c":
    frontier = queue.LifoQueue()
elif type == "b":
    frontier = queue.Queue()

frontier.put([[0, 0]])

#total counter, total move sayısını sayıyor
tctr = 1

#Frontier boş değilken sürekli dön. Hareket sayısı size^2 olduğu an çözüm bulunur. Frontier
#tamamen boşalırsa çözüm yok demektir.

start_time = timeit.default_timer()
while not frontier.empty():
    current_path = frontier.get()
    current_position = current_path[len(current_path)-1]

    if(len(current_path) == size**2):
        break

    if type == "a" or type == "b":
        prefrontier = get_available_pos(current_position, current_path, size)
    elif type == "c":
        prefrontier = h2_eval(current_position, current_path, size)

    if type != "b":
        prefrontier = list(reversed(prefrontier))

    #Yapılacak hamle varsa frontier'a pathi geri ekle. Yoksa geri eklemeye gerek yok.
    if len(prefrontier)!=0:
        for x in prefrontier:
            frontier.put(current_path + [x])

    #move counter ++
    tctr += 1

#Debug için printler
print(timeit.default_timer() - start_time, " seconds")
if(frontier.empty()):
    print("No solution.")
else:
    print(tctr, " steps")
    print("Found Path: ", current_path)
