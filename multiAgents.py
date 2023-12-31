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
        bestIndices = [
            index for index in range(len(scores)) if scores[index] == bestScore
        ]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        return successorGameState.getScore()


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

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
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
        value, action = self.MaxValue(gameState, 0, None)
        return action

    def MaxValue(self, gameState, depth, prevAction):
        # If the game is terminal, return the evaluation function
        if gameState.isWin() or gameState.isLose() or self.depth == depth:
            return self.evaluationFunction(gameState), prevAction
        # Set best value to negative infinity and best action to None
        bestValue = -float("inf")
        bestAction = None
        # For each action in the legal actions of the current agent
        for action in gameState.getLegalActions(0):
            value, move = self.MinValue(
                gameState.generateSuccessor(0, action), depth, action, 1
            )
            # If the new value is greater than the best value, update the best value and best action
            if value > bestValue:
                bestValue = value
                bestAction = action
        return bestValue, bestAction

    def MinValue(self, gameState, depth, prevAction, i):
        # If the game is terminal, return the evaluation function
        if gameState.isWin() or gameState.isLose() or self.depth < depth:
            return self.evaluationFunction(gameState), prevAction
        # Set best value to infinity and best action to None
        bestValue = float("inf")
        bestAction = None
        # For each action in the legal actions of the current agent
        for action in gameState.getLegalActions(i):
            # If the current agent is the last agent, call MaxValue for the next depth
            if i == gameState.getNumAgents() - 1:
                value, move = self.MaxValue(
                    gameState.generateSuccessor(i, action), depth + 1, action
                )
            # Else, call MinValue for the next agent
            else:
                value, move = self.MinValue(
                    gameState.generateSuccessor(i, action), depth, action, i + 1
                )
            # If the new value is less than the best value, update the best value and best action
            if value < bestValue:
                bestValue = value
                bestAction = action
        return bestValue, bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    This agent uses the Minimax algorithm with alpha-beta pruning to make decisions.
    Alpha-beta pruning is a technique to avoid searching through branches of the game 
    tree that won't be selected.
    """

    def getAction(self, gameState):
        """
        Given a gameState, this method returns the best action to take based on 
        the evaluation function, tree depth, and alpha-beta pruning. 
        
        :param gameState: The current game state.
        :return: The best action to take from the current state.
        """
        value, action = self.MaxValue(gameState, 0, None, -float('inf'), float('inf'))
        return action

    def MaxValue(self, gameState, depth, prevAction, alpha, beta):
        """
        Calculate the maximum value for Pacman (agent 0) given a game state.
        
        :param gameState: The current game state.
        :param depth: The current depth in the search tree.
        :param prevAction: The action that led to the current state.
        :param alpha: The best score so far for Pacman at the current depth or above.
        :param beta: The best score so far for the ghost at the current depth or above.
        :return: The maximum value and the action leading to it.
        """
        
        # If terminal state or max depth is reached, return evaluated score.
        if gameState.isWin() or gameState.isLose() or self.depth == depth:
            return self.evaluationFunction(gameState), prevAction

        v = -float('inf')
        tempAction = None
        
        for action in gameState.getLegalActions(0):
            tempValue, temp = self.MinValue(gameState.generateSuccessor(0, action), depth, action, 1, alpha, beta)
            if tempValue > v:
                v = tempValue
                tempAction = action
            # Prune the branch if current value is greater than beta
            if v > beta:
                return v, tempAction
            alpha = max(alpha, v)  # Update alpha for next iterations

        return v, tempAction
    
    def MinValue(self, gameState, depth, prevAction, i, alpha, beta):
        """
        Calculate the minimum value for a ghost agent given a game state.
        
        :param gameState: The current game state.
        :param depth: The current depth in the search tree.
        :param prevAction: The action that led to the current state.
        :param i: The index of the current ghost agent.
        :param alpha: The best score so far for Pacman at the current depth or above.
        :param beta: The best score so far for the ghost at the current depth or above.
        :return: The minimum value and the action leading to it.
        """
        
        # If terminal state or max depth is reached, return evaluated score.
        if gameState.isWin() or gameState.isLose() or self.depth < depth:
            return self.evaluationFunction(gameState), prevAction

        v = float('inf')
        tempAction = None
        
        for action in gameState.getLegalActions(i):
            if i == gameState.getNumAgents() - 1:  # If it's the last ghost, go to MaxValue next
                tempValue, temp = self.MaxValue(gameState.generateSuccessor(i, action), depth + 1, action, alpha, beta)
            else:  # Otherwise, continue with the next ghost agent
                tempValue, temp = self.MinValue(gameState.generateSuccessor(i, action), depth, action, i + 1, alpha, beta)

            if tempValue < v:
                v = tempValue
                tempAction = action

            # Prune the branch if current value is less than alpha
            if v < alpha:
                return v, tempAction
            beta = min(beta, v)  # Update beta for next iterations

        return v, tempAction


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
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
