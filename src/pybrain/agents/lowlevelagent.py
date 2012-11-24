import sys, os
import traci
import random
from random import choice
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.environments.trafficlights import TrafficLights


class LowLevelAgent(LearningAgent):
	id = None
	horizontal_sensor = None
	vertical_sensor = None
	
	def __init__(self, id, horizontal_sensor, vertical_sensor, module, learner=None):
		#define variaveis da class
		self.id = id
		self.horizontal_sensor = horizontal_sensor
		self.vertical_sensor = vertical_sensor
		#define variaveis da classe pai
		LearningAgent.__init__(self, module, learner)
		
	def getAction(self):
		action = random.choice(TrafficLights.actions)
		traci.trafficlights.setPhase(self.id,action)
		traci.simulationStep()
		self.lastaction = action
		return action