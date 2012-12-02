from traci import trafficlights
from traci import lane
from traci import edge
from pybrain.rl.agents import LearningAgent


class LowLevelAgent(LearningAgent):
	
	id = None
	horizontal_edge = None
	vertical_edge = None
	horizontalLoad = 0
	verticalLoad = 0
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
		action = LearningAgent.getAction(self)		
		self.lastaction = action
		return action
	
	def setHorizontalEdge(self, horizontal_edge):
		self.horizontal_edge = horizontal_edge
	
	def setVerticalEdge(self, vertical_edge):
		self.vertical_edge = vertical_edge
	
	def verifyVerticalLoad(self):
		self.verticalLoad += edge.getLastStepHaltingNumber(self.vertical_edge)
		
	def verifyHorizontalLoad(self):
		self.horizontalLoad += edge.getLastStepHaltingNumber(self.horizontal_edge)
	
	def averageVerticalLoad(self, numSteps=1):
		avg = self.verticalLoad / numSteps
		self.verticalLoad = 0
		self.averageVertical.append(avg)
		return avg

	def averageHorizontalLoad(self, numSteps = 1):
		avg = self.horizontalLoad / numSteps
		self.horizontalLoad = 0
		self.averageHorizontal.append(avg)
		return avg
	
	def getLastAverageHorizontal(self):
		return self.averageHorizontal[self.averageHorizontal.__len__() - 1]
	
	def getLastAverageVertical(self):
		return self.averageVertical[self.averageVertical.__len__() - 1]