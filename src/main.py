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
sys.path.append(os.path.join(os.path.dirname(__file__),'/net'))
from trafficlights import TrafficLights
from trafficlights.plan import Plan
from lowlevelagent import LowLevelAgent
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import BoltzmannExplorer


if __name__ == '__main__':
    print "oi"
    traci.init()
    route = Routes()
    route.setFile("net")
    prob = 0.8
    carro = []
    
    #definir action-value table
    #numero de estados e 3
    # 1 -> vertical > horizontal
    # 2 -> vertical < horizontal
    # 3 -> vertical = horizontal
    #numero de acoes 3
    # plan 0 -> 30-30 todas as direcoes
    # plan 1 -> 18v-42h
    # plan 2 -> 42v-18h
    av_table = ActionValueTable(3,3)
    av_table.initialize(0.)
    
    #definir Q-Learning Agent
    #alpha 0.5
    #gama 0.0
    #exploracao Boltzmann
    #vincula av_table com o agente
    learner = Q(0.5,0.0)
    learner._setExplorer(BoltzmannExplorer())
    agent = LowLevelAgent("B7", av_table, learner)

    #definir ambiente
    env = TrafficLights()
    #definir tarefa - interacao com ambiente
    task = Plan(env, agent)
    
    #experimentar
    experiment = Experiment(task,agent)

    for i in range(20000):
        if(random.random() <= prob):
            rota = route.getRandomRoute()
            carro.append(Vehicle(str(i), rota[0]))
            traci.simulationStep()