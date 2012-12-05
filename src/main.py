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
from supervisor.agent import SupervisorAgent

if __name__ == '__main__':
    
    traci.init()
    route = Routes()
    route.setFile("net")
    probH = 0.1#0.1
    probV = 0.3#0.3
    _alpha = 0.5
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
    learner = []
    supervisor = []
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
        learner.append(Q(_alpha,0.))
        learner[ct]._setExplorer(BoltzmannExplorer(500))
        av_table.append(ActionValueTable(3,3))
        av_table[ct].initialize(0.)
        agent.append(LowLevelAgent(tls, av_table[ct], learner[ct]))
        agent[ct].setTolerance(0.1)
        ct += 1
    
    
    ####
    #### adiciona os supervisores e seus supervisionados
    ct = 1
    cts = 0
    for a in agent:
        if(ct == 1):
            supervisor.append(SupervisorAgent(cts, _alpha))
            supervisor[cts].addLowLevelAgent(a)
            ct += 1
        elif(ct == 2):
            supervisor[cts].addLowLevelAgent(a)
            ct += 1  
        elif(ct == 3):
            supervisor[cts].addLowLevelAgent(a)
            ct = 1
            cts += 1
        

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
    
    rotas = route.getRoutes()
        
    for i in range(8000):
        ct += 1
        #quantidade de carros que serao adicionados durante um simulation step
        addCar = 1
        
        for r in rotas:
            if(r[0] in ['1','2','3','4','5','6','7','8']):
                if(random.random() <= probH):
                    Vehicle(str(i)+r[0], r[0])
                    carCount += 1
            else:
                if(random.random() <= probV):
                    Vehicle(str(i)+r[0], r[0])
                    carCount +=1
        
        #rota = route.getRandomRoute()
        #if( (rota[0]) in ['1','2','3','4','5','6','7','8']):
            
        #    if(random.random() <= probH):
        #        for aC in range(addCar):
        #            Vehicle(str(i)+carro[aC], rota[0])
        #        carCount += 1
        #else:
        #    if(random.random() <= probV):
        #        for aC in range(addCar):
        #            Vehicle(str(i)+carro[aC], rota[0])
        #        carCount += 1
                    
        traci.simulationStep()
        for a in agent:
            a.verifyVerticalLoad()
            a.verifyHorizontalLoad()
        
        if(ct == 60):
            for a in agent:
                a.averageVerticalLoad()
                a.averageHorizontalLoad()
                
            ct = 0
            
            if(i <= 3000):
                e.doInteractionsAndLearn(1)
                for s in supervisor:                    
                    s.observeLowLevel()
            elif(i <= 5000):
                for s in supervisor:
                    s.getObservationAndIndicate()
                e.doInteractionsAndLearn(1)
            elif(i <= 8000):
                print oi
              
        #plotagem - nao mexer e deixar no final          
        plt.addXValue(i)
        veiculosParados = 0
        totalVeiculos = 0
        for edge in traci.edge.getIDList():
            veiculosParados = veiculosParados + traci.edge.getLastStepHaltingNumber(edge)
            totalVeiculos = totalVeiculos + traci.edge.getLastStepVehicleNumber(edge)
    
        veiculos_parados.append(veiculosParados)
        total_veiculos.append(totalVeiculos)

    plt.addYValues(veiculos_parados)
    plt.addYValues(total_veiculos)
    plt.showPlot()