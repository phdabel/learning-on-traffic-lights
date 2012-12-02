#-*- coding: iso-8859-1 -*-
'''
Created on 23/11/2012

@author: Abel Correa
'''
from traci import *
import random

class Vehicle(object):
    '''
    classdocs
    '''
    id = ''
    type = ''
    route = ''
    accel = None
    decel = None
    speed = None


    def __init__(self, _id, route, **kwargs):
        '''
        Constructor
        '''
        self.id = _id
        self.route = route
        for key in kwargs:
            if(key == "accel"):
                self.accel = kwargs[key]
            if(key == "decel"):
                self.decel = kwargs[key]
            if(key == 'type'):
                self.type = kwargs[key]
            if(key == 'speed'):
                self.speed = kwargs[key]
        self.__addCarTraci__()
    
    def __addCarTraci__(self):
        '''
            Adiciona o carro na simulação
        '''      
          
        vehicle.add(self.id, self.route)
        #define velocidade padrao para 70
        #aceleracao aleatoria
        #deceleracao aleatoria
        if(self.speed == None):
            self.speed = 70
        if(self.accel == None):
            self.accel = random.uniform(0,4)
        #if(self.decel == None):
            #self.decel = random.random()
        
        if(self.accel != None):
            vehicle.setAccel(self.id, self.accel)
        if(self.decel != None):
            vehicle.setDecel(self.id, self.decel)
        if(self.speed != None):
            vehicle.setMaxSpeed(self.id, self.speed)