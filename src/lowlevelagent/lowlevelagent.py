from traci import trafficlights
from traci import lane
from traci import edge
from pybrain.rl.agents import LearningAgent
from trafficlights_env.trafficlights import TrafficLights
import random
from random import choice

class LowLevelAgent(LearningAgent):
	
	id = None
	horizontal_edge = None
	vertical_edge = None
	horizontalLoad = []
	verticalLoad = []
	averageVertical = []
	averageHorizontal = []
	
	def __init__(self, _id, module, learner=None):
		#define variaveis da class
		self.id = _id
		self.horizontal_edge = lane.getEdgeID(trafficlights.getControlledLanes(self.id)[0])
		self.vertical_edge = lane.getEdgeID(trafficlights.getControlledLanes(str(_id))[2])
		#define variaveis da classe pai
		LearningAgent.__init__(self, module, learner)
		
	def getAction(self):
		#action = LearningAgent.getAction(self)
		action = random.choice(TrafficLights.actions)
		
		self.lastaction = action
		
		return action
	
	def setHorizontalEdge(self, horizontal_edge):
		self.horizontal_edge = horizontal_edge
	
	def setVerticalEdge(self, vertical_edge):
		self.vertical_edge = vertical_edge
	
	def verifyVerticalLoad(self):
		ct = edge.getLastStepHaltingNumber(self.vertical_edge)
		if(ct != 0):
			self.verticalLoad.append(ct)
		
	def verifyHorizontalLoad(self):
		ct = edge.getLastStepHaltingNumber(self.horizontal_edge)
		if(ct != 0):
			self.horizontalLoad.append(ct)
	
	def averageVerticalLoad(self):
		avg = 0
		for x in self.verticalLoad:
			avg += x
		if(len(self.verticalLoad) != 0):
			newAvg = avg / len(self.verticalLoad)
		else:
			newAvg = 0
		self.verticalLoad = []
		
		self.averageVertical.append(newAvg)
		return newAvg

	def averageHorizontalLoad(self):
		avg = 0
		for x in self.horizontalLoad:
			avg += x
		if(len(self.horizontalLoad) != 0):
			newAvg = avg / len(self.horizontalLoad)
		else:
			newAvg = 0
		
		self.horizontalLoad = []
		self.averageHorizontal.append(newAvg)
		return newAvg
	
	def getLastAverageHorizontal(self):
		return self.averageHorizontal[self.averageHorizontal.__len__() - 1]
	
	def getLastAverageVertical(self):
		return self.averageVertical[self.averageVertical.__len__() - 1]