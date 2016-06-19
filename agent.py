import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from collections import defaultdict

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        #https://www.accelebrate.com/blog/using-defaultdict-python/
        self.qTable = defaultdict(int)
        self.alpha = 0.9
        self.gamma = 0.5
        self.trial = 0

        
        
        

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.trial = self.trial+1
        
        
        if self.trial < 91:
            self.rewardSum = 0
            self.violationCounter = 0
            self.numberOfMoves = 0
        else:
            self.rewardSum = self.rewardSum
            self.violationCounter = self.violationCounter
            self.numberOfMoves = self.numberOfMoves
        
        print self.trial
        print self.rewardSum
        print self.violationCounter
        print self.numberOfMoves
        

    def update(self, t):
        #https://discussions.udacity.com/t/for-those-who-are-completely-new-and-completely-lost/168240
        #https://discussions.udacity.com/t/question-about-q-learning-implementation/168810/8
        #https://discussions.udacity.com/t/next-state-action-pair/44902
        #Q(s,a) = (1 - alpha) * Q(s,a) + alpha * ( r + gamma * max_over_a'[ Q(s', a') ] )
    
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = tuple((inputs['light'],inputs['oncoming'],inputs['left'],inputs['right'],self.next_waypoint))
        
        print self.next_waypoint
        
        # TODO: Select action according to your policy
        actionRandom = random.choice(self.env.valid_actions)
        #print 'The trial number is '
        #print self.trial
        if self.trial < 91:
            epsilon = 1
        else:
            epsilon = 0
 
        actionDictionary = {'left': self.qTable[(self.state,'left')],'right': self.qTable[(self.state,'right')],'forward': self.qTable[(self.state,'forward')],None: self.qTable[(self.state,None)]}     
        actionMax = sorted(actionDictionary, key=actionDictionary.__getitem__, reverse=True)[0]

        
        #Set Epsilon value by trial - learn as much as possible at first, then exploit when it counts.
        if random.random() <= epsilon:
            action = actionRandom
        else:
            action = actionMax
            

        # Execute action and get reward
        reward = self.env.act(self, action)
        self.rewardSum = self.rewardSum + reward
        
        if reward < 0:
            self.violationCounter = self.violationCounter + 1
            
            
        self.numberOfMoves = self.numberOfMoves + 1
            
            
        print 'Trial'
        print self.trial
        print 'Reward Sum'
        print self.rewardSum
        print 'Violation Count'
        print self.violationCounter
        print 'Number of Moves'
        print self.numberOfMoves

        

        # TODO: Learn policy based on state, action, reward
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        self.state_2 = tuple((inputs['light'],inputs['oncoming'],inputs['left'],inputs['right'],self.next_waypoint))

        #pass a value to the qTable
        prime_1 = self.qTable[(self.state_2,'left')]
        prime_2 = self.qTable[(self.state_2,'right')]
        prime_3 = self.qTable[(self.state_2,'forward')]
        prime_4 = self.qTable[(self.state_2,None)]
        maxPrime = max(prime_1,prime_2,prime_3,prime_4)
        self.qTable[(self.state,action)] = (1-self.alpha) * self.qTable[(self.state,action)] + self.alpha * (reward + self.gamma * maxPrime)

        

        

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
        





def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=0.000)  # reduce update_delay to speed up simulation
    sim.run(n_trials=100)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
