#-*- coding: iso-8859-1 -*-
'''
Created on 23/11/2012

@author: Abel Correa
'''
import traci


class Vehicle(object):
    '''
    classdocs
    '''
    id = ''
    type = ''
    route = ''
    


    def __init__(self, id, route, type=None):
        '''
        Constructor
        '''
        self.id = id
        self.type = type
        self.route = route
        self.__addCarTraci__()
    
    def __addCarTraci__(self):
        '''
            Adiciona o carro na simulação
        '''
        traci.vehicle.add(self.id, self.route)