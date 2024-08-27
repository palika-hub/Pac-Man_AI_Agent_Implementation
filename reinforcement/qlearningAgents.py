"""
This file is submitted by:
                                Group - 3
                                1.Kailash Reddy Nandaluri - 2003123
                                2.Vishnutejesh - 2003122
""" 

# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"

        self.values = util.Counter()                                                                 # A Counter is a dictionary intialized with Q-Values 0 for all states.


    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        if (state,action) not in self.values.keys():                                                 # Checked if the state is not in the dictionary.

            return 0.0
        
        else:

            return self.values[(state, action)]                                                      # Returns Q-value of (state,action) pair.


    
    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"

        Legal_Actions = self.getLegalActions(state)                                                 # A list of all actions possible in the state.

        AllActQVals = []                                                                            # An empty list for storing the Q-values.

        if len(Legal_Actions) == 0 :                                                                # Checked if there are no legal actions.

            return 0.0                                                                              # If yes, returned 0.0

        else:                                                                                       # If no,
          
            for action in Legal_Actions:                                                            # Iterated for each possible action.
                
                get_QValue = self.getQValue(state,action)                                           # Gets the Q-value of the corresponding (state,action) pair.

                AllActQVals.append(get_QValue)                                                      # Appends the Q-value in the list.

            max_QValue = max(AllActQVals)

        return max_QValue                                                                           # Returns the max possible Q-value among all.


    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"

        Legal_Actions = self.getLegalActions(state)                                                     # A list of all actions possible in the state.

        max_QValue = self.computeValueFromQValues(state)                                                # Computed max Q-value using getQvalue() function.

        Best_Action = []                                                                                # An empty list for storing best actions.

        if len(Legal_Actions) == 0:                                                                     # Checked if there are no legal actions.

            return None                                                                                 # If yes, returned None.

        else:                                                                                           # If not,

            for action in Legal_Actions:                                                                # Iterates for each possible action.

                get_QValue = self.getQValue(state, action)                                              # Gets the Q-value of the corresponding (state,action) pair.
            
                if get_QValue == max_QValue:                                                            # Checks if the current Q-value is equal to the max Q-value for the state calculated using getQvalue() function.

                    Best_Action.append(action)                                                          # If yes, appends the corresponding action to the list.

        return random.choice(Best_Action)                                                               # Returns a random action among all the actions with same max Q-values. Broke ties randomly for better behavior.

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """

        Legal_Actions = self.getLegalActions(state)                                                     # A list of all actions possible in the state.
        
        action = None

        "*** YOUR CODE HERE ***"

        if len(Legal_Actions) == 0:                                                                     # Checked if there are no legal actions.

            return None                                                                                 # If yes, returned None.

        if util.flipCoin(self.epsilon):                                                                 # Returns True with probability 'self.epsilon' and False with probability '1-self.epsilon'.

          action = random.choice(Legal_Actions)                                                         # If True, choose a random action from all the actions possible in the state.

          return action                                                                                 # Return the random action.

        else:                                                                                           # If False, 
          
          action = self.computeActionFromQValues(state)                                                 # Computes the best action.
          
          return  action                                                                                # Returns action.

        util.raiseNotDefined()


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"

        nextstate_val = self.getValue(nextState)                                                              # Value of the next state.
        alpha = self.alpha                                                                                    # Learning rate.
        gamma = self.discount                                                                                 # Discount rate.
        Qval_old = self.values[(state,action)]                                                                # Old Q-value.
        Qval_upd = (((1 - alpha) * Qval_old) + (alpha * (reward + gamma * nextstate_val )))                   # New Q-value using formula [((1 - α) * Q(s)) + α * (reward + (γ * V(s')))]
        self.values[(state,action)] = Qval_upd                                                                # Updating Q-value.


    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):

        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"

        featureVector = self.featExtractor.getFeatures(state, action)                                                           # Feature values vector.

        Qval = 0                                                                                                                # Initialized Q-value with 0.

        w = self.weights                                                                                                        # Weights vector.

        for f in featureVector.keys():                                                                                          # Iterates for each feature.

            Qval = Qval + w[f] * featureVector[f]                                                                               # Does Q(s,a) = Σ(from i = 1 to n) [ fi(s,a) * Wi]

        return Qval                                                                                                             # Returned the Q-value.

        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"

        w = self.weights                                                                                                          # Weights vector.
        alpha = self.alpha                                                                                                        # Learning rate

        featureVector = self.featExtractor.getFeatures(state, action)                                                             # Feature values vector.
        
        gamma = self.discount                                                                                                     # Discount rate.

        nextStateQVal = self.computeValueFromQValues(nextState)                                                                   # Max Q-val of the successor state.

        Qval = self.getQValue(state, action)                                                                                      # Q-value of the current state.
        
        diff = (reward + gamma * nextStateQVal) - Qval                                                                            # Difference value found according to the formula difference = (reward + γ* max Q(s',a')) - Q(s,a)

        for f in featureVector.keys():                                                                                            # Iterates for each feature.

            w[f] = w[f] + (alpha * diff * featureVector[f])                                                                       # Update weights according to the formula Wi = Wi + α * difference * f(s,a).

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass