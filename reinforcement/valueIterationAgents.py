"""
This file is submitted by:
                                Group - 3
                                1.Kailash Reddy Nandaluri - 2003123
                                2.Vishnutejesh - 2003122
""" 

# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        States = self.mdp.getStates()                         # A list of states.

        for iter in range (self.iterations):                  # Iterated k times based on the given value of k. 
            UpdatedVal = self.values.copy()                   # Made a copy of Counter dictionary (with default 0).
            for state in States:                              # Iterated for each state.
                if self.mdp.isTerminal(state):                # Checked if the state is a terminal state, if yes, continued with next iteration (next state).
                    continue
                Actions = self.mdp.getPossibleActions(state)        # If the state is not a terminal state, gets a list of all actions possible in the state.
                AllActQVals = []                                    # Temporary list to store all Q-values.
                for action in Actions:                              # Iterated for each possible action.
                    QVal = self.computeQValueFromValues(state, action)     # Found Q-value of the (state, action) pair.
                    AllActQVals.append(QVal)                               # Appended the Q-value in the temporary list.  
                bestActionVal = max(AllActQVals)                           # After considering all action, found the highest possible Q-value among all.
                UpdatedVal[state] = bestActionVal                          # Updated the value (by the value obtained in this iteration) of the state in the dictionary.

            self.values = UpdatedVal                                       # After considering all the states, replaced the dictionary.


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        QVal= 0                                                                                 # Initiazed Qval variable with value 0.
        dis_fact = self.discount                                                                # Variable having supplied discount value factor.
        AllQVals = self.values.copy()                                                           # Made a copy of Counter dictionary (with default 0). 
        for nextstate, Probability in self.mdp.getTransitionStatesAndProbs(state, action):      # Iterated over a list of (nextstate, Probability) pairs representing the states reachable from state 'state' by taking action 'action' along with their transition probabilities.
            Reward = self.mdp.getReward(state, action, nextstate)                               # Found the reward earned for ending up in the nextstate from state by .
            temp = Probability * (Reward + dis_fact * (AllQVals[nextstate]))                    # Found the Q value using formula Σ(all states reachable from 'state' by taking 'action') P(s,a,s') * [R(s,a,s') +  γ*(V*(s'))]
            QVal = QVal + temp                                                                  # Did Σ(for all states) here.
 
        return QVal                                                                             # Returned Q-value of the action in state.

        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        self.values

        if self.mdp.isTerminal(state):                                                          # Checks if the given state is a terminal state.
          return None                                                                           # If yes, returns nothing.

        Actions = self.mdp.getPossibleActions(state)                                            # If the state is not a terminal state, gets a list of all actions possible in the state.
        actionVal = util.Counter()                                                              # Made a copy of Counter dictionary (with default 0).             
        for action in Actions:                                                                  # Iterated over all actions possible in the state.
            actionVal[action] = self.computeQValueFromValues(state, action)                     # Calculated Q value using given state and action.

        BestactionVal = actionVal.argMax()                                                      # Finds the best action based on highest Q value in the dictionary.

        return BestactionVal                                                                    # Returns best action.

        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        States = self.mdp.getStates()                                               # A list of states.

        for iter in range (self.iterations):                                        # Iterated k times based on the given value of k. 
            index = iter % len(States)                                              # Deciding the state whose value will be updated in a particular iteration.
            state = States[index]                                                   # State assigned.

            if self.mdp.isTerminal(state):                                          # Checked if the state is a terminal state, if yes, continued with next iteration (next state).
                continue
            else:
                Actions = self.mdp.getPossibleActions(state)                        # If the state is not a terminal state, gets a list of all actions possible in the state.
                AllActQVals = []                                                    # Temporary list to store all Q-values.

                for action in Actions:                                              # Iterated for each possible action.
                    QVal = self.computeQValueFromValues(state, action)              # Found Q-value of the (state, action) pair.
                    AllActQVals.append(QVal)                                        # Appended the Q-value in the temporary list.
                bestActionVal = max(AllActQVals)                                    # After considering all action, found the highest possible Q-value among all.

                self.values[state] = bestActionVal                                  # Updated the value (by the value obtained in this iteration) of the state in the dictionary.


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        predecessors = self.predecessors()                                          # Computed predecessors of all states.
        PQ = util.PriorityQueue()                                                   # Initialized an empty priority queue.
        AllActQVals = []                                                            # Temporary list to store all Q-values.

        for state in self.mdp.getStates():                                          # Iterated over all possible states.
            if self.mdp.isTerminal(state):                                          # If the state is a terminal state, continue with next iteration.
                continue
            else:                                                                   # If the state is not a terminal state,
                for action in self.mdp.getPossibleActions(state):                   # Iterated for each possible action.
                    QVal = self.computeQValueFromValues(state, action)              # Found Q-value of the (state, action) pair.
                    AllActQVals.append(QVal)                                        # Appended the Q-value in the temporary list.
                
                bestActionVal = max(AllActQVals)                                    # After considering all action, found the highest possible Q-value among all.
                AllActQVals.clear()
                diff = abs(self.values[state] - bestActionVal)                      # Found the absolute value of the difference between the current value of the given state in self.values and the highest Q-value across all possible actions from the given state.
                PQ.push(state, -diff)                                               # Pushed the given state into the priority queue with priority '-diff'.

        for iter in range(self.iterations):                                         # Iterated k times based on the given value of k. 
            if PQ.isEmpty():                                                        # Checked if the priority queue is empty, if yes, terminate.
                break
            state = PQ.pop()                                                        # Popped the state with the highest priority from the priority queue.
          
            if self.mdp.isTerminal(state):                                          # If the state is a terminal state, continue with next iteration.
                continue
            
            else:                                                                   # If the state is not a terminal state,
                for action in self.mdp.getPossibleActions(state):                   # Iterated for each possible action.
                    QVal = self.computeQValueFromValues(state, action)              # Found Q-value of the (state, action) pair.
                    AllActQVals.append(QVal)                                        # Appended the Q-value in the temporary list.
                
                bestActionVal = max(AllActQVals)                                    # After considering all action, found the highest possible Q-value among all.
                AllActQVals.clear()
                self.values[state] = bestActionVal                                  # Update the value of the state.


            for predecessor in predecessors[state]:                                 # Iterated for each predecessor of the state.
                for action in self.mdp.getPossibleActions(predecessor):             # Iterated for each possible action.
                    QVal = self.computeQValueFromValues(predecessor, action)        # Found Q-value of the (state, action) pair.
                    AllActQVals.append(QVal)                                        # Appended the Q-value in the temporary list.
                
                bestActionVal = max(AllActQVals)                                    # After considering all action, found the highest possible Q-value among all.
                AllActQVals.clear()
                diff = abs(self.values[predecessor] - bestActionVal)                # Found the absolute value of the difference between the current value of the given predecessor in self.values and the highest Q-value across all possible actions from the given predecessor.
                if diff > self.theta:                                               # Checked if diff > theta,
                    PQ.update(predecessor, -diff)                                   # If yes, pushed predecessor into the priority queue with priority -diff.



    def predecessors(self):                                                         # Helper function to find all states that have a nonzero probability of reaching s by taking some action a.

        States = self.mdp.getStates()                                               # A list of states.
        predecessors = {}                                                           # An empty set for storing predecessors of each state.
        for state in States:                                                                                               
            predecessors[state] = set()                                            

        for state in States:                                                                        # Iterated over all possible states.
            for action in self.mdp.getPossibleActions(state):                                       # Iterated for each possible legal action from that state. 
                for successor, probability in self.mdp.getTransitionStatesAndProbs(state, action):  # Iterated over a list of (Successor, Probability) pairs representing the successors reachable from state 'state' by taking action 'action' along with their transition probabilities.
                    if probability > 0:                                                             # Checked if the probability is non-zero. 
                        predecessors[successor].add(state)                                          # If yes, added the state in the predecessors subset for the successor.  

        # print("PREDECESSORS:\n")
        # print(predecessors)
        return predecessors                                                                         # Returned the set of the predecessors.
        

    

