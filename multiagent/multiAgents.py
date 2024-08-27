"""
        ##########################################
                        Group - 3
        Vishnu Tejesh Movva         2003122    CSE
        Nandaluri Kailash Reddy     2003123    CSE
        ##########################################
""" 






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


from argparse import Action
from hashlib import new
from math import inf
from multiprocessing import Value
from turtle import distance
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
        #newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = float(0)
        currentFood = currentGameState.getFood().asList()
        
        for i in range(len(newGhostStates)):
            ## Used manhattan to find distance from food
            distGhost = manhattanDistance(newPos, newGhostStates[i].getPosition())
            
            ## If ghost is near
            if distGhost < 2:
                score -= 5
            
            if distGhost < 3:
                score -= 1
            
            ## If Food is near
            if newPos in currentFood:
                score += 2
        
        closestFoodDist = float(inf)
        for i in range(len(currentFood)) :
            closestFoodDist = min(closestFoodDist, manhattanDistance(newPos, currentFood[i]))
        score -= closestFoodDist
        return score

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

        """
        Using 3 Helper Functions
        1. Value()
        2. maxValue()
        3. minValue()
        """

        Actions = gameState.getLegalActions(0)                                      # Gives the list of all legal actions associated with the state
        Successors = [gameState.generateSuccessor(0, Action) for Action in Actions] # Generating Successor States for each and every action

        maxScore = -float(inf)                                                      # Initializing score to -infinity
        maxScoreAction = Actions[0]

        for Index in range(len(Actions)):                                           # Iterating through all the possible actions
            score = self.value(Successors[Index], 1, 0)                             # Calling Helper Function
            if score > maxScore:                                                    # Taking maximum possible score
                maxScore = score
                maxScoreAction = Actions[Index]                                     # Taking maximum possible action
        
        return maxScoreAction                                                       # Returning the action corresponding to max Score

    def minValue(self, gameState, agentIndex, depthSoFar) :
        """
        Value function for minAgents
        Takes/Returns the minimum possible value 
        """
        Actions = gameState.getLegalActions(agentIndex)                             # Gives the list of all legal actions for the selected minAgent
        Successors = [gameState.generateSuccessor(agentIndex, Action) for Action in Actions] # Generating Successor States for each and every action
        minValue = float(inf)                                                       # Initializing score to +infinity
        total_minAgents = gameState.getNumAgents()-1

        for Successor in Successors:                                                # Iterating through all the possible Actions
            if agentIndex < total_minAgents:                                        # Reccursive Call for next minAgent
                minValue = min(minValue, self.value(Successor, agentIndex + 1, depthSoFar))
            else :                                                                  # Increasing the depth after all minAgents are covered
                minValue = min(minValue, self.value(Successor, 0, depthSoFar+1))
        
        return minValue

    def maxValue(self, gameState, depthSoFar) :
        """
        Value function for maxAgents
        Takes/Returns the maximum possible value 
        """
        Actions = gameState.getLegalActions(0)                                      # Gives the list of all legal actions for maxAgent/Pacman
        Successors = [gameState.generateSuccessor(0, Action) for Action in Actions] # Generating Successor States for each and every action
        maxValue = -float(inf)                                                      # Initializing score to -infinity

        for Successor in Successors:                                                # Iterating through all the possible Actions/States
            maxValue = max(maxValue, self.value(Successor, 1, depthSoFar))          # Recursive calling for MinAgent
        
        return maxValue
            

    def value(self, gameState, agentIndex, depthSoFar) :
        """
        Generalized Value function for both maxAgents and minAgents
        Calls the corresponding value function
        """
        if (gameState.isWin() or gameState.isLose() or depthSoFar == self.depth) :  # Base Case
            return self.evaluationFunction(gameState)

        if agentIndex == 0:                                                         # If Agent is Max Agent
            return self.maxValue(gameState, depthSoFar)
        if agentIndex  > 0:                                                         # If Agent is Min Agent
            return self.minValue(gameState, agentIndex, depthSoFar)     

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        Using 3 Helper Functions
        1. Value()
        2. maxValue()
        3. minValue()
        """

        Actions = gameState.getLegalActions(0)                                      # Gives the list of all legal actions associated with the state.
        Successors = [gameState.generateSuccessor(0, Action) for Action in Actions] # Generating Successor States for each and every action
        
        alpha = -float(inf)                                                         # Best score for Max Agent initialized to -infinity
        beta = float(inf)                                                           # Best score for Min Agent initialized to +infinity
        maxScore = -float(inf)                                                      # Initializing value to -infinity
        maxScoreAction = Actions[0]

        for Index in range(len(Actions)):                                           # Iterating through all the possible Actions/States
            score = self.value(Successors[Index], 1, alpha, beta, 0)                # Calling Helper Function
            if score > maxScore :
                maxScore = score                                                    # Taking maximum possible score
                maxScoreAction = Actions[Index]                                     # Taking maximum possible action
                alpha = score
        
        return maxScoreAction                                                       # Returning the action corresponding to max Score

    def minValue(self, gameState, agentIndex, alpha, beta, depthSoFar) :
        """
        Value function for minAgents
        Takes/Returns the minimum possible value
        """
        Actions = gameState.getLegalActions(agentIndex)                             # Gives the list of all legal actions for the selected minAgent
        minValue = float(inf)                                                       # Initializing score to +infinity
        ## Here we do generate successor state when needed because in alpha beta pruning we don't check all the possible successor states
        
        total_minAgents = gameState.getNumAgents() - 1
        for Action in Actions:                                                      # Iterating through all the possible Actions/States
            Successor = gameState.generateSuccessor(agentIndex, Action)             # Generating Successor State for the considered action
            if agentIndex < total_minAgents:                                        # Recursive Call for next minAgent
                minValue = min(minValue, self.value(Successor, agentIndex + 1, alpha, beta, depthSoFar))
            else :                                                                  # Increasing the depth after all minAgents are covered
                minValue = min(minValue, self.value(Successor, 0, alpha, beta, depthSoFar+1))
        
            ## Pruning the Tree ##
            if minValue < alpha :
                return minValue
            if minValue < beta :
                beta = minValue
        return minValue

    def maxValue(self, gameState, alpha, beta, depthSoFar) :
        Actions = gameState.getLegalActions(0)                                      # Gives the list of all legal actions for the maxAgent/Pacman
        maxValue = -float(inf)                                                      # Initializing score to -infinity
        ## Here we do generate successor state when needed because in alpha beta pruning we don't check all the possible successor states
        
        for Action in Actions:                                                      # Iterating through all the possible Actions/States
            Successor = gameState.generateSuccessor(0, Action)                      # Generating Successor State for the considered action
            maxValue = max(maxValue, self.value(Successor, 1, alpha, beta, depthSoFar)) # Recursive calling for MinAgent
            # Pruning the Tree #
            if maxValue > beta :
                return maxValue
            if maxValue > alpha :
                alpha = maxValue

        return maxValue

    def value(self, gameState, agentIndex, alpha, beta, depthSoFar) :
        if (gameState.isWin() or gameState.isLose() or depthSoFar == self.depth) :  # Base Case
            return self.evaluationFunction(gameState)

        if agentIndex == 0:                                                         # If Agent is Max Agent
            return self.maxValue(gameState, alpha, beta, depthSoFar)
        if agentIndex  > 0:                                                         # If Agent is Min Agent
            return self.minValue(gameState, agentIndex, alpha, beta, depthSoFar)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        
        Using 3 Helper Functions
        1. Value()
        2. maxValue()
        3. minValue()
        """
        
        Actions = gameState.getLegalActions(0)                                      # Gives the list of all legal actions associated with the state
        Successors = [gameState.generateSuccessor(0, Action) for Action in Actions] # Generating Successor States for each and every action

        maxScore = -float(inf)                                                      # Initializing score to -infinity
        ExpectiMaxAction = Actions[0]

        for Index in range(len(Actions)):                                           # Iterating through all the possible Actions/States
            score = self.value(Successors[Index], 1, 0)                             # Calling the Helper Function
            if score > maxScore:
                maxScore = score                                                    # Taking maximum possible score
                ExpectiMaxAction = Actions[Index]                                   # Taking maximum possible action
        
        return ExpectiMaxAction                                                     # Returning the action corresponding to max Score

    def minValue(self, gameState, agentIndex, depthSoFar) :
        """
        Value function for minAgents
        Takes/Returns the average of all possible values
        """
        Actions = gameState.getLegalActions(agentIndex)                             # Gives the list of all legal actions for the selected minAgent
        Successors = [gameState.generateSuccessor(agentIndex, Action) for Action in Actions]# Generating Successor States for each and every action
        Values = []                                                                 # Array to store values of all possible successor states
        total_minAgents = gameState.getNumAgents()-1

        for Successor in Successors:                                                # Iterating through all the possible Actions/States
            if agentIndex < total_minAgents:                                        # Recursive Call for next minAgent
                Values.append(self.value(Successor, agentIndex + 1, depthSoFar))
            else :                                                                  # Increasing the depth after all minAgents are covered
                Values.append(self.value(Successor, 0, depthSoFar+1))
        
        return sum(Values)/len(Values)                                              # Returning the average of values of  all possible successor states
    
    def maxValue(self, gameState, depthSoFar) :
        """
        Value function for minAgents
        Takes/Returns the maximum of all possible values
        """
        Actions = gameState.getLegalActions(0)                                      # Gives the list of all legal actions for the MaxAgent/Pacman
        Successors = [gameState.generateSuccessor(0, Action) for Action in Actions] # Generating Successor States for each and every action
        maxValue = -float(inf)                                                      # Initializing score to +infinity

        for Successor in Successors:                                                # Iterating through all the possible Actions/States
            maxValue = max(maxValue, self.value(Successor, 1, depthSoFar))          # Recursive calling for MinAgent
        
        return maxValue

    def value(self, gameState, agentIndex, depthSoFar) :
        if (gameState.isWin() or gameState.isLose() or depthSoFar == self.depth) :  # Base Case
            return self.evaluationFunction(gameState)

        if agentIndex == 0:                                                         # If Agent is Max Agent
            return self.maxValue(gameState, depthSoFar)
        if agentIndex  > 0:                                                         # If Agent is Min Agent
            return self.minValue(gameState, agentIndex, depthSoFar)     

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    The 'betterEvaluationFunction' function takes in the current GameState 
    and returns a number, where higher numbers are better.

    The functions takes into account :

    (i)     Reciprocal of the distance of pacman from closest food position.
    (ii)    10 times the Reciprocal of the distance of pacman from closest capsule position.
            (This times is actually decided after testing the evaluation function for some values)
    (iii)   Reciprocal of distance of pacman from each ghost.
    (iv)    The ScaredTimer for each ghost.
    
    """
    
    #just some variables declared for main files.
    x = currentGameState.getPacmanPosition()
    foodpos = currentGameState.getFood()
    foodlist = foodpos.asList()
    capspos = currentGameState.getCapsules()
    ghoststates = currentGameState.getGhostStates()


    score = currentGameState.getScore()

    temp1 = [] #for storing distances of food
    temp2 = []

    for Food in foodlist:
        dist = (manhattanDistance(x, Food))  #used manhattan to find distance from food
        temp1.append(dist)

    
    if len(temp1) != 0:
        score = score + (1/min(temp1))     #using reciprocal of the min distance of food in evaluation function


    for Ghost in ghoststates:
        ghostpos = Ghost.getPosition()
        Rem_scare_time = Ghost.scaredTimer
        dist = manhattanDistance(x, ghostpos) #manhattan distance of ghost


# Checks if that distance is greater than 0. If yes, then checks if the time/moves for which the ghost will remain scared is greater than 0                                                     # If yes, adds 100 to the score, to make the currentGameState a good state to be in.
        if (dist > 0):
            if (Rem_scare_time != 0):
                score = score + 100 #if yes adds 100 to score

            else:
                score = score - (1/(dist)) #else we use reciprocal of distance of ghost in EF

        else:
            score = score - 100000  #negate the score large enough so that we dont go to this stage.


    for Cap in capspos:
        dist = (manhattanDistance(x, Cap)) #manhattan distance of capseuls
        temp2.append(dist)

    if len(temp2) != 0:
        score = score + 10/min(temp2)   #10 times sthe manhattan distance used in EF


    return score    #return score
    

# Abbreviation
better = betterEvaluationFunction
