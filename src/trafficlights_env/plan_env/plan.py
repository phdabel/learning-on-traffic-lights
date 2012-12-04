__author__ = 'Abel Correa, phd.abel@gmail.com'

#from scipy import clip, asarray
#from numpy import *
from pybrain.rl.environments.task import Task
from lowlevelagent.lowlevelagent import LowLevelAgent
import traci

class Plan(Task):

	#penalidades
	bangPenalty = -1
	defaultPenalty = 0
	finalReward = 1
	
	#dados do trafficlight
	trafficlight = None

	def __init__(self, environment, trafficlight):
		#atribui o ambiente que deve ser passado como parametro apos ser instanciado
		#juntamente com os ids do induction loop vertical e horizontal
		self.env = environment
		if(isinstance(trafficlight, LowLevelAgent)):
			self.trafficlight = trafficlight
	
	def performAction(self, action):
		return self.env.performAction(self.trafficlight, action)
	
	def getObservation(self):
		#retorna estado do ambiente
		sensors = self.env.getSensors(self.trafficlight)
		#print "observacao %d" % sensors
		return sensors
	
	def getReward(self):
		currentAction = traci.trafficlights.getProgram(self.trafficlight.id)
		currentAction = int(currentAction)
		#plan 1 - vertical > horizontal
		#plan 2 - horizontal > vertical
		#plan 0 - horizontal = vertical
		
		if(self.getObservation() == 0 and currentAction == 0):
			#cur_reward = self.finalReward
			return 1 - self._calcReward()
		elif(self.getObservation() == 2 and currentAction == 1):
			#cur_reward = self.finalReward
			return 1 - self._calcReward()
		elif(self.getObservation() == 1 and currentAction == 2):
			#cur_reward = self.finalReward
			return 1 - self._calcReward()
		elif(self.getObservation() == 2 and currentAction == 2):
			#cur_reward = self.bangPenalty
			return 1 - self._calcReward()
		elif(self.getObservation() == 1 and currentAction == 1):
			#cur_reward = self.bangPenalty
			return 1 - self._calcReward()
		else:
			#cur_reward = self.defaultPenalty
			return 1 - self._calcReward()

		#return cur_reward
		return 1 - self._calcReward()
	
	def _calcReward(self):
		
		horizontal = self.trafficlight.getLastAverageHorizontal()
		vertical = self.trafficlight.getLastAverageVertical()
	
		if(horizontal == 0):
			horizontal = 1
		if(vertical == 0):
			vertical = 1
		#print "Horizontal - %f Vertical - %f" % (horizontal, vertical)
			
		if(horizontal > vertical):
			return vertical / horizontal
		elif(vertical > horizontal):
			return horizontal / vertical
		else:
			return 0