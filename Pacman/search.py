# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # print("Start: ", problem.getStartState()) # returns (5,5)
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState())) # returns true
    # print("Start's successors:", problem.getSuccessors(problem.getStartState())) # returns south and west coordinates for the successors of starts

    fringe = util.Stack()   # creates the fringe
    visited_nodes = []  # creates the list of nodes that have already been visited, since we are using a graph search
    fringe.push((problem.getStartState(),[], 0))    # pushes the first state onto the fringe

    # check for failure condition
    if fringe.isEmpty():
        failure = "There was a failure, most likely due to an empty fringe"
        return failure

    else:
        while not fringe.isEmpty():
            node = fringe.pop()
            state = node[0]
            actions = node[1]

            # the goal-test
            if problem.isGoalState(state):
                return actions
            
            # if the state has not been expanded
            if state not in visited_nodes:
                visited_nodes.append(state)
                # visit all child nodes
                successors = problem.getSuccessors(state)
                for child in successors:
                    # store state, action and cost as a value of 1
                    child_state = child[0]
                    child_action = child[1]
                    while child_state not in visited_nodes:
                        # add the remaining child nodes
                        child_action = actions + [child_action]
                        fringe.push((child_state, child_action, 1))
                        break

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # almost identical to the DFS, only main difference is the QUEUE use instead of a STACK

    fringe = util.Queue()   # initializa the fringe as a Queue
    visited_nodes = []  # create list for nodes that have been expanded 
    fringe.push((problem.getStartState(),[], 0))    # pushes the first state onto the fringe

    # check for failure condition
    if fringe.isEmpty():
        failure = "There was a failure, most likely due to an empty fringe."
        return failure

    else:
        while not fringe.isEmpty():
            node = fringe.pop()
            state = node[0]
            actions = node[1]

            # the goal-test
            if problem.isGoalState(state):
                return actions

            # if state has not yet been expanded  
            if state not in visited_nodes:
                visited_nodes.append(state)
                # visit all child nodes
                successors = problem.getSuccessors(state)
                for child in successors:
                    # store state, action and cost as a value of 1
                    child_state = child[0]
                    child_action = child[1]
                    while child_state not in visited_nodes:
                        # add the remaining child nodes
                        child_action = actions + [child_action]
                        fringe.push((child_state, child_action, 1))
                        break

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()   # initialize the fringe as a Prioroty Queue
    visited_nodes = []  # create list for the expanded or visited nodes of the fringe
    fringe.push((problem.getStartState(), [], 0), 0) # push the start state onto the fringe but with a priority of 0

    # check for the failure condition
    if fringe.isEmpty():
        failure = "There is a failure, most likely due to an empty fringe."
        return failure
    
    else: 
        while not fringe.isEmpty():
            node = fringe.pop()
            state = node[0]
            actions = node[1]

            # the goal-test
            if problem.isGoalState(state):
                return actions
            
            # if state has not yet been expanded
            if state not in visited_nodes:
                visited_nodes.append(state)
                # visit all child nodes
                successors = problem.getSuccessors(state)
                for child in successors:
                    # store the state, action and cost as a value of 1
                    child_state = child[0]
                    child_action = child[1]
                    while child_state not in visited_nodes:
                        # add the remaining child nodes
                        child_action = actions + [child_action]
                        cost = problem.getCostOfActions(child_action)   # get the cost value for the priority value of the queue
                        fringe.push((child_state, child_action, 1), 0 + cost) # push the node with the priority value as the cost
                        break

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()   # initialize the fringe as a Prioroty Queue
    visited_nodes = []  # create list for the expanded or visited nodes of the fringe
    fringe.push((problem.getStartState(), [], 0), heuristic(problem.getStartState(), problem))

    # check for the failure condition
    if fringe.isEmpty():
        failure = "There is a failure, most likely due to an empty fringe."
        return failure
    
    else: 
        while not fringe.isEmpty():
            node = fringe.pop()
            state = node[0]
            actions = node[1]

            # the goal-test
            if problem.isGoalState(state):
                return actions
            
            # if state has not yet been expanded
            if state not in visited_nodes:
                visited_nodes.append(state)
                # visit all child nodes
                successors = problem.getSuccessors(state)
                for child in successors:
                    # store the state, action and cost as a value of 1
                    child_state = child[0]
                    child_action = child[1]
                    while child_state not in visited_nodes:
                        # add the remaining child nodes
                        child_action = actions + [child_action]
                        cost = problem.getCostOfActions(child_action) # get the cost value that will be used to calculate the priority 
                        fringe.push((child_state, child_action, 0), cost + heuristic(child_state, problem)) # add the cost value to the heuristic value for the priority 
                        break

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
