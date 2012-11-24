__author__ = 'Abel Correa, phd.abel@gmail.com'

from pybrain.rl.environments.environment import Environment
from scipy import zeros
import traci

class TrafficLights(Environment):

	#numero de acoes que o ambiente aceita
	actions = [0,1,2]
	#numero de estados possiveis de serem produzidos no ambiente
	states = [1,2,0]
	
	indim = len(actions)
	outdim = len(states)
	
	def getSensors(self, horizontal_induction_loop, vertical_induction_loop):
		loopH = traci.inductionloop.getLastStepOccupancy(horizontal_induction_loop)
		loopV = traci.inductionloop.getLastStepOccupancy(vertical_induction_loop)
		loopHp = loopH / (loopH+loopV)
		loopVp = loopV / (loopH+loopV)
		if (loopVp - loopHp) > 0.2:
			return 1
		elif (loopHp - loopVp) > 0.2:
			return 2
		else:
			return 0
	
	def performAction(self, action):
		print "Acao %i realizada" % (action)