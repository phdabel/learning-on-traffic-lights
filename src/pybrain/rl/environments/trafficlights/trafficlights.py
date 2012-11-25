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
	
	def getSensors(self, horizontal_edge, vertical_edge):
		hLast = traci.edge.getLastStepLength(horizontal_edge)
		vLast = traci.edge.getLastStepLength(vertical_edge) 
		lastHPerCent = hLast / (hLast+vLast)
		lastVPerCent = vLast / (hLast+vLast)
		if (lastVPerCent - lastHPerCent) > 0.2:
			return 1
		elif (lastHPerCent - lastVPerCent) > 0.2:
			return 2
		else:
			return 0
	
	def performAction(self, action):
		print "Acao %i realizada" % (action)