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
    trafficlightsids = ["B2","B3","B4","B5","B6","B7",
                        "C2","C3","C4","C5","C6","C7",
                        "D2","D3","D4","D5","D6","D7",
                        "E2","E3","E4","E5","E6","E7",
                        "F2","F3","F4","F5","F6","F7",
                        "G2","G3","G4","G5","G6","G7"]
    
    agent = []
    
    for tls in trafficlightsids:
        agent.append(LowLevelAgent(tls, av_table, learner))
    #agent = LowLevelAgent("B7", av_table, learner)

    #definir ambiente
    env = TrafficLights()
    tasks = []
    #definir tarefa - interacao com ambiente
    for a in agent:
        tasks.append(Plan(env, a))
    #task = Plan(env, agent)
    
    #experimentar
    experiments = []
    for x in range(len(agent) - 1):
        experiments.append(Experiment(tasks[x], agent[x]))
    
    #experiment = Experiment(tasks,agent)
    ct = 0
    for i in range(20000):
        ct =+ 1
        if(random.random() <= prob):
            rota = route.getRandomRoute()
            carro.append(Vehicle(str(i), rota[0]))
            traci.simulationStep()
        if(ct == 60):
            ct = 0
            for i in range(500):
                for e in experiments:
                    e.doInteractions(1)
                    for a in agent:
                        a.learn()
                        a.reset()
        