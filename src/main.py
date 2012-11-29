# -*- coding: iso-8859-1 -*-

'''
Created on 22/11/2012

@author: Abel Correa
'''
from netextract.routes import Routes
from netextract.vehicle import Vehicle
import traci
import random
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__),'/net'))
from trafficlights_env.trafficlights import TrafficLights
from trafficlights_env.plan_env.plan import Plan
from lowlevelagent import LowLevelAgent
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.learners import Q
from pybrain.rl.experiments import ContinuousExperiment
from pybrain.rl.explorers import BoltzmannExplorer
import pylab
from math import *

if __name__ == '__main__':
    print "oi"
    traci.init()
    route = Routes()
    route.setFile("net")
    prob = 0.7
    
    #definir action-value table
    #numero de estados e 3
    # 1 -> vertical > horizontal
    # 2 -> vertical < horizontal
    # 3 -> vertical = horizontal
    #numero de acoes 3
    # plan 0 -> 30-30 todas as direcoes
    # plan 1 -> 18v-42h
    # plan 2 -> 42v-18h
    agent = []
    learner = Q(0.5,0.0)
    learner._setExplorer(BoltzmannExplorer())

    #definir Q-Learning Agent
    #alpha 0.5
    #gama 0.0
    #exploracao Boltzmann
    #vincula av_table com o agente
    
    trafficlightsids = ["B2","B3","B4","B5","B6","B7",
                        "C2","C3","C4","C5","C6","C7",
                        "D2","D3","D4","D5","D6","D7",
                        "E2","E3","E4","E5","E6","E7",
                        "F2","F3","F4","F5","F6","F7",
                        "G2","G3","G4","G5","G6","G7"]
        
    ct = 0
    
    av_table = []
    #av_table = ActionValueTable(3,3)
    #av_table.initialize(0.)
    
    for tls in trafficlightsids:
        av_table.append(ActionValueTable(3,3))
        av_table[ct].initialize(0.)
        agent.append(LowLevelAgent(tls, av_table[ct], learner))
        ct += 1
        

    #definir ambiente
    env = TrafficLights()
    tasks = []
    
    #definir tarefa - interacao com ambiente
    for a in agent:
        tasks.append(Plan(env, a))
    
    #experimentar
    experiments = []
    for a in range(36):
        experiments.append(ContinuousExperiment(tasks[a],agent[a]))
    
    ct = 0
    media_aprendizagem = []
    qtd = []
    carro = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    for i in range(2000):
        ct += 1
        #quantidade de carros que serao adicionados durante um simulation step
        addCar = 2
        if(random.random() <= prob):
            for aC in range(addCar):
                rota = route.getRandomRoute()
                Vehicle(str(i)+carro[aC], rota[0])
            traci.simulationStep()
            
        if(ct == 60):
            ct = 0
            for y in range(36):
                print "Experimento: %i com agente %i - %s" % (i, y, agent[y].id)
                #print experiments[y].agent.module.getActionValues(0)
                #print experiments[y].agent.module.getActionValues(1)
                #print experiments[y].agent.module.getActionValues(2)
                experiments[y].doInteractionsAndLearn(1)
                agent[y].learn()
                agent[y].reset()
                print av_table[y].params.reshape(3,3)
                
                pylab.plot(x,y)
                pylab.draw()
                #pylab.pcolor(av_table[y].params.reshape(3,3).max(1).reshape(1,3))