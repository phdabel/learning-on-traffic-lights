# -*- coding: iso-8859-1 -*-

'''
Created on 22/11/2012

@author: Abel Correa
'''
from netextract.routes import Routes
from netextract.vehicle import Vehicle
from netextract.edges import Edges
import traci
import random
from random import choice
import sys, os

#if __name__ == '__main__':
print "oi"
traci.init()
route = Routes()
route.setFile("net")
traci.route.getIDList()
#
#print route.getRoutes()
carro = []
for i in range(2000):
    rota = route.getRandomRoute()
    carro.append(Vehicle(str(i), rota[0]))
    traci.simulationStep()