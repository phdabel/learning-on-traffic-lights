import sys, os
import traci
import random
from random import choice
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.environments.trafficlights import TrafficLights


class LowLevelAgent(LearningAgent):
	
	id = None
	horizontal_edge = None
	vertical_edge = None
	
	def __init__(self, id, module, learner=None):
		#define variaveis da class
		self.id = id
		self.horizontal_edge = traci.lane.getEdgeID(traci.trafficlights.getControlledLanes(str(self.id))[0])
		self.vertical_edge = traci.lane.getEdgeID(traci.trafficlights.getControlledLanes(str(self.id))[2])
		#define variaveis da classe pai
		LearningAgent.__init__(self, module, learner)
		
	def getAction(self):
		action = random.choice(TrafficLights.actions)
		traci.trafficlights.setPhase(self.id,action)
		traci.simulationStep()
		self.lastaction = action
		return action
	
	def setHorizontalEdge(self, horizontal_edge):
		self.horizontal_edge = horizontal_edge
	
	def setVerticalEdge(self, vertical_edge):
		self.vertical_edge = vertical_edge