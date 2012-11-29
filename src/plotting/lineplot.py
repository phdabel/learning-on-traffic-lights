'''
Created on 29/11/2012

@author: Abel Correa
'''
from numpy import *
import pylab
from matplotlib import rc, rcParams

class LinePlot(object):
    '''
    classdocs
    '''
    
    #list
    x_axis = []
    #string
    label_x = None
    #list or list os lists
    y_axis = []
    #string
    label_y = None
    #list
    labels = []
    #string
    title = None
    
    
    def __init__(self):
        '''
        Constructor
        '''
        
    #seta o rotulo do eixo x
    def labelX(self, label):
        
        self.label_x = label 
    
    #seta o rotulo do eixo y
    def labelY(self, label):
        self.label_y = label
    
    #recebe um valor ou uma lista de valores para o eixo X
    def addXValue(self, dado):
        if(type(dado)==int):
            self.x_axis.append(dado)
        if(type(dado)==list):
            self.x_axis = dado

    # adiciona uma lista de valores para o eixo y
    def addYValues(self, dados):
        if(type(dados)==list):
            self.y_axis.append(array(dados))
    
    #adiciona rotulos um a um ou todos, para cada valor de y
    def addLabelPlot(self, label):
        if(type(label)==list):
            self.labels = label
        else:
            self.labels.append(label)
    
    
    #adiciona titulo ao plot
    def addTitle(self, title):
        self.title = title
    
    def __testPlot__(self):
        if(type(self.x_axis)==list and self.x_axis!=[]):
            if(type(self.y_axis==list) and self.y_axis!=[]):
                if(self.label_x != None):
                    if(self.label_y != None):
                        if(self.labels != []):
                            return True
                        else:
                            print "As variaveis nao tem rotulo"
                            return False
                    else:
                        print "O Eixo Y nao tem rotulo"
                        return False
                else:
                    print "O Eixo X nao tem rotulo"
                    return False
            else:
                print "O Eixo Y nao tem dados"
                return False
        else:
            print "O Eixo X nao tem dados"
            return False
    
    #plota o grafico
    def showPlot(self):
        ct = 0
        if(self.__testPlot__()):
            pylab.title(self.title)
            pylab.xlabel(self.label_x)
            pylab.ylabel(self.label_y)
            
            x = array(self.x_axis)
            if(len(self.y_axis)==1):
                y = self.y_axis[0]
                labelY = self.labels[ct]
                pylab.plot(x,y, label=r'%s' % (labelY))
            else:
                for yLists in self.y_axis:
                    y = yLists
                    labelY = self.labels[ct]
                    pylab.plot(x,y, label=r'%s' % (labelY))
                    #pylab.legend([pylab.plot(x,y)], loc=1) 
                    pylab.hold(True)
                    ct += 1
            pylab.legend(loc=1)
            pylab.show()