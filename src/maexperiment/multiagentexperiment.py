'''
Created on 01/12/2012

@author: Abel Correa
'''
from pybrain.rl.experiments import Experiment


class MultiAgentExperiment(Experiment):
    '''
    classdocs
    '''
    tasks = []
    agents = []
    stepid = None

    def __init__(self, tasks, agents):
        '''
        Constructor
        '''
        self.tasks = tasks
        self.agents = agents
        self.stepid = 0

    def doInteractionsAndLearn(self, number = 1):
        """ The default implementation directly maps the methods of the agent and the task.
            Returns the number of interactions done.
        """
        for _ in range(number):
            self._oneInteraction()
        return self.stepid

    def _oneInteraction(self):
        """ Give the observation to the agent, takes its resulting action and returns
            it to the task. Then gives the reward to the agent again and returns it.
        """
        self.stepid += 1
        for i in range(len(self.agents)):
            self.agents[i].integrateObservation(self.tasks[i].getObservation())
            self.tasks[i].performAction(self.agents[i].getAction())
            reward = self.tasks[i].getReward()
            
            self.agents[i].giveReward(reward)
            self.agents[i].learn()
            self.agents[i].reset()
            
            print self.agents[i].id
            print self.agents[i].module.getActionValues(0)
            print self.agents[i].module.getActionValues(1)
            print self.agents[i].module.getActionValues(2)
            

        