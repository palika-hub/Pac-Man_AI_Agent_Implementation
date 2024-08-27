"""
This file is submitted by:
                                Group - 3
                                1.Kailash Reddy Nandaluri - 2003123
                                2.Vishnutejesh - 2003122
""" 

# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0.001                             # Very low noise value will make sure that agent rarely ends up in an unintended successor state when they perform an action.
    return answerDiscount, answerNoise

def question3a():                                   # Prefers the close exit (+1), risking the cliff (-10)

    answerDiscount = 0.2                            # Discount factor = 0.2: Rewards value decay faster, hence, close exit preferred.
    answerNoise = 0                                 # Noise value = 0: chance of ending up in an unintended successor state is 0, hence, risking cliff is preferred.
    answerLivingReward = -1                         # Reward of Living = -1: Living longer results in more loss, hence agent tries to complete game in least steps (close exit preferred).

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():                                   # Prefers the close exit (+1), but avoiding the cliff (-10)

    answerDiscount = 0.2                            # Discount factor = 0.2: Rewards value decay faster, hence, close exit preferred.
    answerNoise = 0.2                               # Noise value = 0.2: chance of ending up in an unintended successor state is there, hence avoids cliff.
    answerLivingReward = -1                         # Reward of Living = -1: Living longer results in more loss, hence agent tries to complete game in least steps (close exit preferred).

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():                                   # Prefers the distant exit (+10), risking the cliff (-10)

    answerDiscount = 0.8                            # Discount factor = 0.8: Rewards value decay slower, hence, distant exit preferred.
    answerNoise = 0                                 # Noise value = 0: chance of ending up in an unintended successor state is 0, hence, risking cliff is preferred.
    answerLivingReward = 0                          # Reward of Living = 0: Agents can take as much step as it wants.

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():                                   # Prefers the distant exit (+10), avoiding the cliff (-10)

    answerDiscount = 0.8                            # Discount factor = 0.8: Rewards value decay slower, hence distant exit preferred.
    answerNoise = 0.4                               # Noise value = 0.4: chance of ending up in an unintended successor state is bit high, hence, avoids cliff.
    answerLivingReward = 0                          # Reward of Living = 0: Agents can take as much step as it wants.

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():                                   # Avoiding both exits and the cliff (so an episode should never terminate)

    answerDiscount = 1                              # Discount factor = 1: Rewards value remains same forever, hence both exits are avoided (Living forever will yeild more and more rewards).
    answerNoise = 0                                 # Noise value = 0: chance of ending up in an unintended successor state is 0, hence risking cliff is preferred.
    answerLivingReward = 1                          # Reward of Living = 1: Infinite steps yields infinite reward, hence, agent lives forever and never exits.

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question8():
    answerEpsilon = None
    answerLearningRate = None

    """
    There are no values of epsilon and learning rate for which it is highly likely (greater than 99%) that the optimal policy 
    will be learned after 50 iterations.
    """
    
    return 'NOT POSSIBLE'

    # return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
