import sys
import forzero
from timeit import default_timer as timer
from collections import deque
import time


def run(path,timez):
    ####**********--- since A* with zero hueristic is bfs so we thought it would be better studying experience for us to do bfs algorythm as we understand it
    #instead of just ignoring the values of board and give all states (boards ) same priority
    def breadthfs(board, max_time=1000000000000,max_depth=25):
        visited = set()
        solutions = list()
        depth_states = dict()
        # deque our data structure list like but pop and inserts are much faster o(1)vs o(n)~ and from both ends
        queue = deque()
        queue.appendleft((board, tuple()))
        start = time.time()
        runtime=0
        lasttime=0
        while len(queue) != 0:
            board, path = queue.pop()
            new_path = path + tuple([board])
            depth_states[len(new_path)] = depth_states.get(len(new_path), 0) + 1
            #we check here either the depth is too large (max depth = 25 gave good results) so we exit or if chosen time for one puzzle passed
            if len(new_path) >= max_depth :
                break
            if board in visited:
                continue
            else:
                visited.add(board)

            if board.solved():

                solutions.append(new_path)
            else:
                queue.extendleft((move, new_path) for move in board.moves())
            end = time.time()
            runtime = end - start
        return {'visited': visited,
                'solutions': solutions,
                'depth_states': depth_states}

    #getting the moves and preparing steps in string
    def solution_steps(solution):
        steps = []
        for i in range(len(solution) - 1):
            x, y = solution[i], solution[i + 1]
            car1 = list(x.vehicles - y.vehicles)[0]
            car2 = list(y.vehicles - x.vehicles)[0]
            if car1.x < car2.x:
                steps.append('{0}R'.format(car1.id))
            elif car1.x > car2.x:
                steps.append('{0}L'.format(car1.id))
            elif car1.y < car2.y:
                steps.append('{0}D'.format(car1.id))
            elif car1.y > car2.y:
                steps.append('{0}U'.format(car1.id))
        return steps


    numpuzzle = 0
    f = open("bfs_zeroblocking_output.txt", "w+")
    path = path
    problems = open(path, "r")
    for line in problems:
        rushhour =forzero.load_file(line)
        start = timer()
        results = breadthfs(rushhour, max_time=timez,max_depth=100)
        end = timer()
        timez = end - start
        numpuzzle += 1
        f.write("\npuzzle #%d" % (numpuzzle))
        f.write("\nmoves: ")
        #we get more than 1 solution so we print the first one
        for solution in results['solutions']:
            f.write('{0}'.format(', '.join(solution_steps(solution))))
            break
        f.write('\n{0} Nodes visited'.format(len(results['visited'])))
        f.write("\ntime: %f" % (timez))
    f.close()