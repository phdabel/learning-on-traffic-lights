__author__ = 'Abel Correa, phd.abel@gmail.com'

from pybrain.rl.environments.environment import Environment
#from scipy import zeros
import traci

class TrafficLights(Environment):

	#numero de acoes que o ambiente aceita
	actions = [0, 1, 2]
	#numero de estados possiveis de serem produzidos no ambiente
	states = [1, 2, 0]
	
	indim = len(actions)
	outdim = len(states)
	
	
	
	def getSensors(self, trafficlight):
		
		hLast = trafficlight.getLastAverageHorizontal()
		vLast = trafficlight.getLastAverageVertical()
		
		if(hLast == 0):
			hLast = 1
		if(vLast == 0):
			vLast = 1
		
		lastHPerCent = hLast / (hLast+vLast)
		lastVPerCent = vLast / (hLast+vLast)
		
			
		if (lastVPerCent - lastHPerCent) > 0.2:
			#print "Percentual Vertical %f e Horizontal %f" % (lastVPerCent, lastHPerCent)
			return [1,]
		elif (lastHPerCent - lastVPerCent) > 0.2:
			#print "Percentual Vertical %f e Horizontal %f" % (lastVPerCent, lastHPerCent)
			return [2,]
		else:
			#print "Percentual Vertical %f e Horizontal %f" % (lastVPerCent, lastHPerCent)
			return [0,]
	
	def performAction(self, trafficlight, action):
		acao = int(action[0])
		traci.trafficlights.setProgram(trafficlight.id,str(acao))
	