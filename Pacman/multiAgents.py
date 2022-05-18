# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        # First calculate the minimum distance and real distance to the fartherst food pellet
        foodList = newFood.asList()
        min_food_distance = -9999
        for food in foodList:
            distance = util.manhattanDistance(newPos, food)
            if min_food_distance == -9999:
                min_food_distance = distance

            elif min_food_distance >= distance:
                min_food_distance = distance

        # then calculate the distance from the pacman to the ghosts
        distance_from_ghosts = 1
        proximity_from_ghosts = 0
        for ghost_state in successorGameState.getGhostPositions():
            distance = util.manhattanDistance(newPos, ghost_state)
            distance_from_ghosts = distance_from_ghosts + distance
            if distance <= 1:
                proximity_from_ghosts = proximity_from_ghosts + 1

        # add new data
        return (successorGameState.getScore() + ((1 /min_food_distance) - (1 /distance_from_ghosts) - proximity_from_ghosts))

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def minimax(agent, depth, gameState):
            if depth == self.depth:   # return the utility if the depth has been reached
                return self.evaluationFunction(gameState)

            elif gameState.isLose():  # return the utility value if the game is lost
                return self.evaluationFunction(gameState)

            elif gameState.isWin(): # return the utility value if the game is won
                return self.evaluationFunction(gameState)

            # begin to maximize for the pacman agent
            if agent == 0:  
                return max(minimax(1, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))
            else:  # do the opposite for the ghosts
                nextAgent = agent + 1  # calculate the next agent value
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = 0

                if nextAgent == 0:
                    depth = depth + 1   # increase depth

                return min(minimax(nextAgent, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))

        # complete max function for pacman agent
        maximum = -9999
        action = Directions.WEST
        for agentState in gameState.getLegalActions(0):
            utility = minimax(1, 0, gameState.generateSuccessor(0, agentState))
            if utility > maximum:
                maximum = utility
                action = agentState
            
            elif maximum == -9999:
                maximum = utility
                action = agentState

        return action

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def Maximizer(agent, depth, game_state, a, b): 
            v = -9999
            for newState in game_state.getLegalActions(agent):
                v = max(v, AlphaBetaPrune(1, depth, game_state.generateSuccessor(agent, newState), a, b))
                if v > b:
                    return v
                a = max(a, v)
            return v

        def Minimizer(agent, depth, game_state, a, b):
            v = 9999

            next_agent = agent + 1  # calculate the next agent value
            if game_state.getNumAgents() == next_agent:
                next_agent = 0
            if next_agent == 0:
                depth = depth + 1   # increase depth for search

            for newState in game_state.getLegalActions(agent):
                v = min(v, AlphaBetaPrune(next_agent, depth, game_state.generateSuccessor(agent, newState), a, b))
                if v < a:
                    return v
                b = min(b, v)
            return v

        def AlphaBetaPrune(agent, depth, game_state, a, b):
            if depth == self.depth:   # return utility value in case the depth is reached
                return self.evaluationFunction(game_state)

            elif game_state.isLose():  # return the utility in case the defined depth is reached or the game is won/lost.
                return self.evaluationFunction(game_state)
            
            elif game_state.isWin():    # return utility value in case its won
                return self.evaluationFunction(game_state)
            
        
            # maximize for the pacman agent
            if agent == 0: 
                return Maximizer(agent, depth, game_state, a, b)
            # do the opposite for the ghosts
            else:  
                return Minimizer(agent, depth, game_state, a, b)

        # same as before but this time for the alpha beta pruning
        utility = -9999
        action = Directions.WEST
        alpha = -9999
        beta = 9999
        for agentState in gameState.getLegalActions(0):
            ghostValue = AlphaBetaPrune(1, 0, gameState.generateSuccessor(0, agentState), alpha, beta)
            if ghostValue > utility:
                utility = ghostValue
                action = agentState

            if utility > beta:
                return utility
            alpha = max(alpha, utility)
        return action

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def Expectimax(agent, depth, gameState):
            if depth == self.depth:   # return the utility value if the depth is reached
                return self.evaluationFunction(gameState)

            elif gameState.isLose():  # return the utility value if the game is lost
                return self.evaluationFunction(gameState)

            elif gameState.isWin(): # return the utility value if the game is won
                return self.evaluationFunction(gameState)

            if agent == 0:
                return max(Expectimax(1, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))
            else:
                nextAgent = agent + 1 
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = 0

                if nextAgent == 0:
                    depth = depth + 1 
                return sum(Expectimax(nextAgent, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent)) / float(len(gameState.getLegalActions(agent)))

        # creates the max for the root node
        maximum = -9999
        action = Directions.WEST
        for agentState in gameState.getLegalActions(0):
            utility = Expectimax(1, 0, gameState.generateSuccessor(0, agentState))
            if utility > maximum:
                maximum = utility
                action = agentState

            elif maximum == -9999:
                maximum = utility
                action = agentState

        return action


        util.raiseNotDefined()

