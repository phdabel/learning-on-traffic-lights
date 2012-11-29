from traci import trafficlights
from traci import lane
from pybrain.rl.agents import LearningAgent


class LowLevelAgent(LearningAgent):
	
	id = None
	horizontal_edge = None
	vertical_edge = None
	
	def __init__(self, _id, module, learner=None):
		#define variaveis da class
		self.id = _id
		self.horizontal_edge = lane.getEdgeID(trafficlights.getControlledLanes(self.id)[0])
		self.vertical_edge = lane.getEdgeID(trafficlights.getControlledLanes(str(_id))[2])
		#define variaveis da classe pai
		LearningAgent.__init__(self, module, learner)
		
	def getAction(self):
		action = LearningAgent.getAction(self)
		#action = random.choice(TrafficLights().actions)
		
		self.lastaction = action
		return action
	
	def setHorizontalEdge(self, horizontal_edge):
		self.horizontal_edge = horizontal_edge
	
	def setVerticalEdge(self, vertical_edge):
		self.vertical_edge = vertical_edge