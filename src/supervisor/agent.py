'''
Created on 02/12/2012

@author: Abel Correa
'''


class SupervisorAgent(object):
    '''
    classdocs
    '''
    
    alpha = 0
    lowLevelSet = []
    tmpcase = {}
    cases = []


    def __init__(self, _alpha=0.5):
        '''
        Constructor
        '''
        self.alpha = _alpha
    
    def addLowLevelAgent(self, agent):
        self.lowLevelSet.append(agent)
        
            
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
            
            self.tmpcase[ct] = [ind, lS[ind]]
            
            r += lR[ind]
            ct += 1
        
        rMed = float(r) / float(len(self.lowLevelSet))
        self.tmpcase['reward'] = rMed
        
        
        if(len(self.cases) == 0):
            self.cases.append(self.tmpcase)
            self.tmpcase = {}
            rMed = 0
            r = 0
        else:
            finish = 0
            for i in self.cases:
                if((self.tmpcase[0] == i[0] and self.tmpcase[1] == i[1] and self.tmpcase[2] == i[2]) and finish == 0):
                    i['reward'] = self.alpha * rMed + (1 - self.alpha) * i['reward']
                    finish = 1
                    break
            if(finish == 0):
                self.cases.append(self.tmpcase)
                
            rMed = 0
            r = 0
            self.tmpcase = {}
            
        #print self.cases
        
    def getBestObservation(self):
        x = []
        for i in self.cases:
            x.append(i['reward'])
        return x.index(max(x))
