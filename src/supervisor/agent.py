'''
Created on 02/12/2012

@author: Abel Correa
'''
from trafficlights_env.trafficlights import TrafficLights 

class SupervisorAgent():
    '''
    classdocs
    '''
    
    id = None
    alpha = None
    lowLevelSet = []
    tmpcase = []
    cases = []


    def __init__(self, _id, _alpha=0.5):
        '''
        Constructor
        '''
        self.id = _id
        self.alpha = _alpha
        self.lowLevelSet = []
        self.tmpcase = []
        self.cases = []
    
    def addLowLevelAgent(self, _agent):
        self.lowLevelSet.append(_agent)
        
            
    #case e uma tupla [0,0],[0,0],[0,0],5
    # cada lista e o estado acao de um dos lowlevel agents e o ultimo numero e a media dos rewards
    #case[0] estado acao do lowlevel 1
    #case[1] estado acao do lowlevel 2
    #case[2] estado acao do lowlevel 3
    #case[3] media
    
    def observeLowLevel(self):
        r = 0
        
        ct = 0
        for a in self.lowLevelSet:
            maxState0 = a.module.getMaxAction(0)
            maxRew0 = max(a.module.getActionValues(0))
            maxState1 = a.module.getMaxAction(1)
            maxRew1 = max(a.module.getActionValues(1))
            maxState2 = a.module.getMaxAction(2)
            maxRew2 = max(a.module.getActionValues(2))
            lS = [maxState0, maxState1, maxState2]
            lR = [maxRew0, maxRew1, maxRew2]
            ind = lR.index(max(lR))
            
            
            self.tmpcase.append([ind, lS[ind]])
            
            
            r += lR[ind]
            ct += 1
        
        rMed = float(r) / float(len(self.lowLevelSet))
        self.tmpcase.append(rMed)
        
        
        if(len(self.cases) == 0):
            self.cases.append(self.tmpcase)
            self.tmpcase = []
            rMed = 0
            r = 0
            
        else:
            finish = 0
            for i in self.cases:
                if((self.tmpcase[0] == i[0] and self.tmpcase[1] == i[1] and self.tmpcase[2] == i[2]) and finish == 0):
                    
                    i[3] = self.alpha * rMed + (1 - self.alpha) * i[3]
                    finish = 1
                    break
            if(finish == 0):
                self.cases.append(self.tmpcase)
                
            rMed = 0
            r = 0
            self.tmpcase = []
            
        #print self.cases
        
    def getObservationAndIndicate(self):
        lastObs = []
        nextActions = []
        for a in self.lowLevelSet:
            lastObs.append(TrafficLights().getSensors(a))
        
        for i in self.cases:
            if(i[0][0] == lastObs[0] and i[1][0] == lastObs[1] and i[2][0] == lastObs[2]):
                nextActions = [i[0][1], i[1][1], i[2][1]]
                rew = i[3]
                #print nextActions
                self.lowLevelSet[0].performNextAction(nextActions[0], rew)
                self.lowLevelSet[1].performNextAction(nextActions[1], rew)
                self.lowLevelSet[2].performNextAction(nextActions[2], rew)
                break
            
        