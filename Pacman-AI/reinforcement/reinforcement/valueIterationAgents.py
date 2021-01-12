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
        k=0
        for k in range(self.iterations):
            newValue = util.Counter()
            states = self.mdp.getStates()
            
            for s in states:
                value_iteration = []
                action  = self.mdp.getPossibleActions(s)
                maxVal = float('-inf')
                if self.mdp.isTerminal(s):
                    newValue[s] = 0
                    value_iteration.append(newValue)
                
                else:
                    for a in action:
                        transtionsFunction = self.mdp.getTransitionStatesAndProbs(s,a)
                        qValue = 0
                        for transitionData in transtionsFunction:
                            n,tf = transitionData
                            R = self.mdp.getReward(s,a,n)
                            qValue += tf*(R + self.discount*self.values[n])
                            
                            if(qValue > maxVal):
                                maxVal = qValue
                        value_iteration.append(qValue)
                    newValue[s] = max(value_iteration)
                    #value_iteration.append(newValue)
                    
                
            self.values = newValue#value_iteration.pop()
                        
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
        transitionFunction = self.mdp.getTransitionStatesAndProbs(state,action)
        qValue = 0
        for transitionData in transitionFunction:
            n,tf = transitionData
            R = self.mdp.getReward(state,action,n)
            qValue += tf*(R + self.discount*self.values[n])
        return qValue
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
        maxVal = float('-inf')
        if self.mdp.isTerminal(state):
            return None
        else:
            actions = self.mdp.getPossibleActions(state)
            #print(actions)
            states = self.mdp.getStates()
            #print(states)
            
            for a in actions:
                transitionFunction = self.mdp.getTransitionStatesAndProbs(state,a)
                qValue = 0
                for transitionData in transitionFunction:
                    n,tf = transitionData
                    R = self.mdp.getReward(state,a,n)
                    qValue += tf*(R + self.discount*self.values[n])
                
                if(qValue > maxVal):
                    maxAction = a
                    maxVal = qValue
                    
            return maxAction
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
        k=0
        i=0
        states = self.mdp.getStates()
        size = len(states)
        newValue = util.Counter()
        for k in range(self.iterations):
            states = self.mdp.getStates()
            new_state =[]
            new_state.append(states[i])
            for s in new_state:
                value_iteration = []
                action  = self.mdp.getPossibleActions(s)
                maxVal = float('-inf')
                if self.mdp.isTerminal(s):
                    newValue[s] = 0
                
                else:
                    
                    for a in action:
                        transtionsFunction = self.mdp.getTransitionStatesAndProbs(s,a)
                        qValue = 0
                        for transitionData in transtionsFunction:
                            n,tf = transitionData
                            R = self.mdp.getReward(s,a,n)
                            qValue += tf*(R + self.discount*self.values[n])
                        
                        value_iteration.append(qValue)
                    newValue[s] = max(value_iteration)
                    #value_iteration.append(newValue)
                
                i+=1
                if(i>=size):
                    i=0
                
                
            self.values = newValue#value_iteration.pop()

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
        pq = util.PriorityQueue()
        
        state = self.mdp.getStates()
        predescessor = {}
        #predecessorList = { [] for state in self.mdp.getStates()}
        for s in state:
            predescessor[s] = set()
            
        for s in state:
            actions = self.mdp.getPossibleActions(s)
            maxVal = float('-inf')
            for a in actions:
                transtionsFunction = self.mdp.getTransitionStatesAndProbs(s,a)
                qValue = 0
                for transitionData in transtionsFunction:
                    n,tf = transitionData
                    if tf!=0:
                        predescessor[n].add(s)
                    R = self.mdp.getReward(s,a,n)
                    qValue += tf*(R + self.discount*self.values[n])
                if(qValue > maxVal):
                    maxAction = a
                    maxVal = qValue
                            
                        
            if not self.mdp.isTerminal(s):
                diff = abs(self.values[s] - maxVal)
                pq.update(s,-diff)
        
        #print("Priority Queue")
        #print(pq)
                
        #print(predescessor)
        for k in range(self.iterations):
            if pq.isEmpty():
                return
            
            s = pq.pop()

            if not self.mdp.isTerminal(s):
                actions = self.mdp.getPossibleActions(s)
                maxVal = float('-inf')
                for a in actions:
                    transtionsFunction = self.mdp.getTransitionStatesAndProbs(s,a)
                    qValue = 0
                    for transitionData in transtionsFunction:
                        n,tf = transitionData
                        R = self.mdp.getReward(s,a,n)
                        qValue += tf*(R + self.discount*self.values[n])
                    if(qValue > maxVal):
                        maxAction = a
                        maxVal = qValue           
                            
                self.values[s] = maxVal
                #print(self.values)
            
            for p in predescessor[s]:
                actions = self.mdp.getPossibleActions(p)
                maxVal = float('-inf')
                for a in actions:
                    transtionsFunction = self.mdp.getTransitionStatesAndProbs(p,a)
                    qValue = 0
                    for transitionData in transtionsFunction:
                        n,tf = transitionData
                        R = self.mdp.getReward(p,a,n)
                        qValue += tf*(R + self.discount*self.values[n])
                    #print("qValue ",qValue)
                    if(qValue > maxVal):
                        maxAction = a
                        maxVal = qValue

                #print("MaxVal ",maxVal)
                diff = abs(self.values[p] - maxVal)
            #print("State ",s)
            #print("Difference ",diff)
                if diff > self.theta:
                    #print("p ",p)
                    #print("Diff ",diff)
                    pq.update(p,-diff) 
              
        
        

