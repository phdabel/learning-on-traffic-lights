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
from pybrain.rl.experiments import Experiment
from maexperiment.multiagentexperiment import MultiAgentExperiment
from pybrain.rl.explorers import BoltzmannExplorer
import pylab
from math import *
from plotting.lineplot import LinePlot

if __name__ == '__main__':
    print "oi"
    traci.init()
    route = Routes()
    route.setFile("net")
    prob = 0.7
    
    #definicao do plot
    plt = LinePlot()
    plt.addLabelPlot(['Veiculos Parados', 'Total'])
    plt.addTitle("Veiculos durante a Simulacao")
    plt.labelX("Tempo")
    plt.labelY("Veiculos")
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
    learner = [] #Q(0.8,0.4)
    
    #learner._setExplorer(BoltzmannExplorer())

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
    
    
    av_table = [] #ActionValueTable(3,3)
    #av_table.initialize(0.)
    #agent = LowLevelAgent(trafficlightsids[35], av_table, learner)
    #av_table = ActionValueTable(3,3)
    #av_table.initialize(0.)
    
    for tls in trafficlightsids:
        learner.append(Q(0.5,0.))
        learner[ct]._setExplorer(BoltzmannExplorer())
        av_table.append(ActionValueTable(3,3))
        av_table[ct].initialize(0.)
        agent.append(LowLevelAgent(tls, av_table[ct], learner[ct]))
        ct += 1
        

    #definir ambiente
    env = TrafficLights()
    tasks = []
    
    #definir tarefa - interacao com ambiente
    for a in agent:
        tasks.append(Plan(env, a))
    #task = Plan(env,agent)
    #experimentar
    #experiments = []
    #for a in range(36):
    #    experiments.append(Experiment(tasks[a],agent[a]))
    e = MultiAgentExperiment(tasks, agent)
    
    ct = 0
    veiculos_parados = []
    total_veiculos = []
    qtd = []
    carro = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    
    carCount = 0
    
    for i in range(1000):
        ct += 1
        #quantidade de carros que serao adicionados durante um simulation step
        addCar = 1
        if(random.random() <= prob):
            for aC in range(addCar):
                rota = route.getRandomRoute()
                Vehicle(str(i)+carro[aC], rota[0])
                carCount += 1
        traci.simulationStep()
        for a in agent:
            a.verifyVerticalLoad()
            a.verifyHorizontalLoad()
        
        if(ct == 60):
            for a in agent:
                a.averageVerticalLoad(ct)
                a.averageHorizontalLoad(ct)
                
            ct = 0
            e.doInteractionsAndLearn(1)

            plt.addXValue(i)
            veiculosParados = 0
            totalVeiculos = 0
            for i in traci.edge.getIDList():
                veiculosParados = veiculosParados + traci.edge.getLastStepHaltingNumber(i)
                totalVeiculos = totalVeiculos + traci.edge.getLastStepVehicleNumber(i)
    
            veiculos_parados.append(veiculosParados)
            total_veiculos.append(totalVeiculos)

    plt.addYValues(veiculos_parados)
    plt.addYValues(total_veiculos)
    plt.showPlot()