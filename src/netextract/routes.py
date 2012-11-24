#-*- coding: iso-8859-1 -*-
"""
Created on 21/11/2012

@author: Abel Corrêa
"""
from xml.dom import minidom
from netextract.constants import *
import traci
import random
from random import choice
import sys, os

class Routes(object):

    xmlDoc = ''
    file = ''
    listaRotas = []
    
    def __init__(self):
        """
        Constructor
        """
        
    def setFile(self, nomeArquivo):
        '''
            Configura um arquivo passado como parametro para a variavel file
            e executa a funcao _setRoutes_
        '''
        try:
            self.file = open(NETWORK_DIR + nomeArquivo + ".rou.xml", "r").read()
        except:
            self.file = 'Arquivo invalido'
        self.xmlDoc = minidom.parseString(self.file)
        self._setRoutes_()
        self._setTraciRoutes_()
    
    
    def _setRoutes_(self):
        '''
            Pega as rotas do arquivo adiciona no vetor listaRotas e no traci
            requer o traci ligado
        '''
        i = 0
        for r in self.xmlDoc.getElementsByTagName("route"):
            try:
                self.listaRotas.append(list(r.getAttribute("id").encode('utf8')))
                self.listaRotas[i].append(list(r.getAttribute("edges").encode('utf8').split(" ")))
                i += 1
            except:
                print "Problema ao pegar rotas"
                
    def _setTraciRoutes_(self):
        '''
            Seta as rotas no simulador utilizando TRACI
        '''
        for n in self.listaRotas:
            traci.route.add(str(n[0]), n[1])
    
    def getRoutes(self):
        '''
            retorna vetor de rotas
        '''
        return self.listaRotas
    
    def getRandomRoute(self):
        '''
            escolhe, aleatoriamente, uma rota
        '''
        return random.choice(self.listaRotas)