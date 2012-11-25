# -*- coding: iso-8859-1 -*-

'''
Created on 24/11/2012

@author: Abel
'''
import traci

class Edges(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def getTrafficLength(self, edge):
        '''
            Mostra número de carros numa via
        '''
        return traci.edge.getLastStepLength(edge)