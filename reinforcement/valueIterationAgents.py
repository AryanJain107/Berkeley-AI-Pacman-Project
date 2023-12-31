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
        for i in range(self.iterations):
            val = util.Counter()
            for state in self.mdp.getStates():
                max_val = float('-inf')
                for action in self.mdp.getPossibleActions(state):
                    # This calculation is done in the ComputeQValueFromValues function
                    # sum = 0
                    # for s in self.mdp.getTransitionStatesAndProbs(state, action):
                    #     sum += (s[1]) * (self.mdp.getReward(state, action, s[0]) + self.discount * self.values[s[0]])
                    sum = self.computeQValueFromValues(state, action)    
                    max_val = max(max_val, sum)
                    val[state] = max_val
            self.values = val


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
        sum = 0
        for s in self.mdp.getTransitionStatesAndProbs(state, action):
            sum += (s[1]) * (self.mdp.getReward(state, action, s[0]) + self.discount * self.values[s[0]])
        return sum
        # util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        best_action = None
        if self.mdp.isTerminal(state):
            return best_action
        max_val = float('-inf')
        for action in self.mdp.getPossibleActions(state):
            sum = self.computeQValueFromValues(state, action)
            if max_val < sum:
                max_val = max(max_val, sum)
                best_action = action
        return best_action
        # util.raiseNotDefined()

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
        for i in range(self.iterations):
            val = util.Counter()
            # for state in self.mdp.getStates():
            state = self.mdp.getStates()[i % len(self.mdp.getStates())]
            max_val = float('-inf')
            if self.mdp.isTerminal(state):
                continue
            for action in self.mdp.getPossibleActions(state):
                # This calculation is done in the ComputeQValueFromValues function
                sum = 0
                # for s in self.mdp.getTransitionStatesAndProbs(state, action):
                #     sum += (s[1]) * (self.mdp.getReward(state, action, s[0]) + self.discount * self.values[s[0]])
                sum = self.computeQValueFromValues(state, action)    
                max_val = max(max_val, sum)
                val[state] = max_val
            self.values[state] = val[state]

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
    # def getQVals(self, state):
    #     possibleActions = self.mdp.getPossibleActions(state)  
    #     countQVals = util.Counter()  

    #     for action in possibleActions:
    #         countQVals[action] = self.computeQValueFromValues(state, action)
    #     return countQVals
    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        predecessors = {}
        for state in self.mdp.getStates():
            for action in self.mdp.getPossibleActions(state):
                for s in self.mdp.getTransitionStatesAndProbs(state, action):
                    if s[0] in predecessors:
                        predecessors[s[0]].add(state)
                    else:
                        predecessors[s[0]] = {state}

        queue = util.PriorityQueue()
        for state in self.mdp.getStates(): 
            val = util.Counter()  
            for action in self.mdp.getPossibleActions(state):
                val[action] = self.computeQValueFromValues(state, action)
            q_val = val
            max_value_key = q_val.argMax();
            queue.push(state, -1 * (abs(self.values[state] - q_val[max_value_key])))

        for i in range(self.iterations):
            if not queue.isEmpty():
                removed_state = queue.pop()
                if not self.mdp.isTerminal(removed_state):
                    val = []
                    for action in self.mdp.getPossibleActions(removed_state):
                        val.append(self.computeQValueFromValues(removed_state, action))
                    self.values[removed_state] = max(val)
                for p in predecessors[removed_state]:
                    if self.mdp.isTerminal(p):
                        continue;
                    val = []
                    for action in self.mdp.getPossibleActions(p):
                        val.append(self.computeQValueFromValues(p, action))
                    diff = abs(self.values[p] - max(val))
                    if diff > self.theta:
                        queue.update(p, -diff)
