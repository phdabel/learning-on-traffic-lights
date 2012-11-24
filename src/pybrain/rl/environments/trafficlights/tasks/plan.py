__author__ = 'Abel Correa, phd.abel@gmail.com'

from scipy import clip, asarray
from numpy import *
from pybrain.rl.environments.task import Task
import traci

class Plan(Task):

	#penalidades
	bangPenalty = -1
	defaultPenalty = 0
	finalReward = 1
	#dados do induction_loop vertical e horizontal
	horizontal_induction_loop = None
	vertical_induction_loop = None
	#dados do trafficlight
	trafficlight = None

	def __init__(self, environment, horizontal_induction_loop, vertical_induction_loop, trafficlight):
		#atribui o ambiente que deve ser passado como parametro apos ser instanciado
		#juntamente com os ids do induction loop vertical e horizontal
		self.env = environment
		self.horizontal_induction_loop  = horizontal_induction_loop
		self.vertical_induction_loop = vertical_induction_loop
		self.trafficlight = trafficlight
		
	
	def performAction(self, action):
		return self.env.performAction(action)
	
	def getObservation(self):
		#retorna estado do ambiente
		sensors = self.env.getSensors(self.horizontal_induction_loop, self.vertical_induction_loop)
		return sensors
	
	def getReward(self):
		currentAction = traci.trafficlights.getPhase(self.trafficlight)
		if(self.getObservation() == 0 and currentAction == 0):
			cur_reward = self.finalReward
		elif(self.getObservation() == 2 and currentAction == 1):
			cur_reward = self.finalReward
		elif(self.getObservation() == 1 and currentAction == 2):
			cur_reward = self.finalReward
		elif(self.getObservation() == 2 and currentAction == 2):
			cur_reward = self.bangPenalty
		elif(self.getObservation() == 1 and currentAction == 1):
			cur_reward = self.bangPenalty
		else:
			cur_reward = self.defaultPenalty		
		return cur_reward