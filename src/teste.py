'''
Created on 29/11/2012

@author: Abel Correa
'''
from numpy import *
from pylab import *
from matplotlib import rc, rcParams
from plotting.lineplot import LinePlot

x = LinePlot()
x.addLabelPlot(['x1']) #,'x2','x3'])
x.addTitle("Plot Teste")
x.addXValue([1,2,3,4,5,6,7,8,9])
x.addYValues([2,3,4,5,6,4,6,4,4])
x.addYValues([6,5,3,6,3,4,6,8,3])
x.addYValues([7,5,2,3,4,3,4,5,2])
x.labelX("tempo")
x.labelY("grana")
x.showPlot()

print x.labels
print x.labels[0]
print x.labels[1]
print x.labels[2]
