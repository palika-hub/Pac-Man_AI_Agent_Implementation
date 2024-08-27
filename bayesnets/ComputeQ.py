'''
            Group - 3
            Kailash Reddy Nandaluri - 2003123
            Vishnu Tejesh - 2003122
'''

from collections import defaultdict
import string
import random
from decimal import Decimal

#Reading from bayes net file
f = open("example_bayesnet.txt", "r", encoding='utf-8')
content = f.readlines()       #Reads contents of file
variables = []

#number of variables
n = content[0][0]
n = int(n)

for i in range(n):
    variables.append(content[0][3*(i+1)])   # Gives variables present in Network

print("variables are :",variables)
d = defaultdict(list)
for i in range(n):       #In this loop we add possible values of the variables
    empty = ""
    empty = empty + (content[i+1][3])
    empty =  empty + (content[i+1][4])
    d[variables[i]].append(empty)
    empty = ""
    empty = empty + (content[i+1][7])
    empty = empty + (content[i+1][8])
    d[variables[i]].append(empty)

print("values of variables : ",d)

#CPT tables
Cpt = defaultdict(list)
line = n + 1
while line < len(content)-1:
    temp = content[line]
    temp2 = ""
    for ch in temp :
        if ch.isalpha() :
            temp2 = temp2 + ch
    for i in range(2 ** len(temp2)):
        templist = []
        temp3 = ""
        for j in range(2 *len(temp2) + 2 * (len(temp2)-1)):
            if content[line+1+i][j] != " ":
                temp3 = temp3 + content[line+1+i][j]
        templist.append(temp3)
        #Cpt[content[line]].append(temp3)
        #print(Cpt[content[line]])
        
        temp4 = ""
        for j in range(2 *len(temp2) + 2 * (len(temp2)-1)+2,len(content[line+1+i])-1):
            temp4 = temp4 + content[line+1+i][j]
        temp4 = float(temp4)
        templist.append(temp4)
        Cpt[content[line]].append(templist)
        
    line += 2 ** len(temp2) +1
print(Cpt)
        


#Generating samples
def univariate_sample_from_fixed_distribution(prob_dist, num_samples):
    samples = []
    keyset =  prob_dist.keys() 
    num_keyset = len(keyset)

    for i in range(num_samples):
        u = random.random()
        init_val = 0

        for k in keyset:
            
            if (u <= (init_val+ (prob_dist[k][0][1]))) and u>init_val: 
                
                samples.append(prob_dist[k][0][0])
                break
            init_val =  init_val+ (prob_dist[k][0][1])
    #print(samples)
    return samples

            

univariate_sample_from_fixed_distribution(Cpt, 5)
                

def prior_sampling(num_samples,Cpt):
    sample_set = []
    #for s in range(num_samples):
        #curr_sample = []
        #for 
    '''
    Randomly sample from bn's full joint distribution.
    '''
    return 0

def rejection_sampling(num_sampling,Cpt):
    '''
    Estimate the probability distribution of variable X given
    evidence e in BayesNet bn, using N samples. 
    Raises a ZeroDivisionError if all the N samples are rejected,
    '''

    return 0

def likelihood_weighing(num_sampling,Cpt):
    '''
    Sample an event from bn that's consistent with the evidence e;
    return the event and its weight, the likelihood that the event
    accords to the evidence.
    '''

    return 0

def gibbs_sampling(num_samples,Cpt):
    '''
    In likelihood sampling, it is possible to obtain low weights in cases where the evidence variables reside at the bottom of the Bayesian Network. 
    This can happen because influence only propagates downwards in likelihood sampling.
    Gibbs Sampling solves this.
    '''

    return 0
