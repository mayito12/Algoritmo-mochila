
from random import randint, uniform, sample
import math
import numpy as np 
from matplotlib import pyplot as plt
import sys
from PyQt5 import uic
from PyQt5 import  QtWidgets
from package import Package
from individuo import Individuo

minimo = []
maximo = []
best_ind = []
packages = []
amount = [5,9,5,6,9]
avarage = []

class Inicialization():
    count = 0
    def create_packages(self):
        for i in range(amount[self.count]):
            packages.append(Package(type_package+str(i+1),space_package,cost_package,price_package, (price_package-cost_package)))
        self.count += 1
        print(packages)

class Seleccion():
    def create_population(self, po):
        for i in range(po):
            aleatorios = sample(range(1,35), 34)
            population.append(Individuo(aleatorios))
        print('')
        print(population)
        print(len(population))

    def evaluacion(self):
        for ind in population:
            valid_space = 0
            aux_profit = 0
            for i in range(len(ind.packages)):
                valid_space += packages[ind.packages[i]-1].space
                aux_profit += packages[ind.packages[i]-1].profit
                if valid_space <= container: 
                    ind.total_space = valid_space
                    ind.valid_space = i
                    ind.profit_ind = aux_profit
            print(ind)
    
    def create_couples(self):
        couples = []
        num_of_best = 0
        num_of_best = math.ceil(len(population)/2)
        for i in range(num_of_best):
            for x in range(i+1,len(population)):
                couples.append((population[i],population[x]))
        return couples

class Cruza_and_mutacion():
    
    def evaluate(self,child):
        for ind in population:
            if child != ind.packages:
                print('no es repetible')
                return True
            else:
                print('si es repetible')
                return False
    
    def mutacion(self,child):
        rand_mut_ind = uniform(0,1)
        rand_mut_gen = uniform(0,1)
        if rand_mut_ind >= prob_mut_ind:
            print('va mutar')
            for i in range(len(child)-1):
                if rand_mut_gen >= prob_mut_gen:
                    print('va mutar gen')
                    rand_position = randint(0,len(child)-1)
                    aux = child[i]
                    child[i] = child[rand_position]
                    child[rand_position] = aux
        return child
    
    def create_children(self, couples):
        pattern_1, pattern_2 = couples[0].packages, couples[1].packages
        position = randint(0,len(packages)-1)
        half1 = pattern_1[position:]
        half2 = pattern_2[:position]
        child_1 = pattern_1[position:] + half2
        child_2 = pattern_2[:position] + half1
        print('Este es el hijo1:' )
        print(child_1)
        print('Este es el hijo2:' )
        print(child_2)

        for gen in [child_1, child_2]:
            if self.evaluate(gen):
                print('quiere mutar')
                population.append(Individuo(self.mutation(gen)))

class Poda():
    def ordering_max(self, Pmax):
        aux = sorted(population, key=lambda x: x.profit_ind, reverse=True)
        
        return aux[:Pmax]
    
    def auxMax(self):
        maximo.append(population[0].profit_ind)

    def auxMin(self):
        minimo.append(population[len(population)-1].profit_ind)

    def auxAvarage(self):
        
        avarage.append(sum(population[i].profit_ind for i in range(len(population)))/len(population))

    def poda_best(self):
        x = self.ordering_max(Pmax)
        return x
            
def tabla_historial():
    x = []
    fig = plt.figure(figsize=(10, 5))
    fig.tight_layout()
    plt.style.use('_mpl-gallery')
    for i in range(len(maximo)):
        x.append(i+1)
    ax = plt.subplot(1, 1, 1)
    ax.plot(x, maximo, label='Caso Máximo')
    ax.plot(x, avarage, label='Caso Promedio')
    ax.plot(x, minimo, label='Caso Mínimo')
    ax.legend(loc='upper right')
    plt.savefig(f'img/historico.png')
    plt.show()

def tables( x):
    fig2 = plt.figure(figsize=(10, 5))  
    fig2.tight_layout()
    plt.style.use('_mpl-gallery')
    plt.subplots_adjust(left=0.06, right=0.95, bottom=0.06, top=0.95)
    aptitud_x = []
    aptitud_generacion = []
    for i in range(len(population)):
        aptitud_x.append(i+1)
        aptitud_generacion.append(population[i].profit_ind)
    ax_2 = plt.subplot(1, 1, 1)
    ax_2.barh(aptitud_x, aptitud_generacion)
    ax_2.set_xlabel("Ganancia Total")
    ax_2.set_ylabel("Paquetes")
    ax_2.set_title("Generacion "+str(x+1) + "°")
    num_gen = x + 1
    if num_gen < 10:
        name = f'0{num_gen}'
    elif num_gen >= 10 and num_gen < 100:
        name = f'{x+1}'
    elif num_gen >= 100 and num_gen < 1000:
        name = f'c_{num_gen}'
    plt.savefig(f'img/{name}.png')

def main(PoI, iterations):
    global population
    population = []
    seleccion = Seleccion()
    cruza = Cruza_and_mutacion()
    poda = Poda()
    seleccion.create_population(PoI)
    seleccion.evaluacion()
    for i in range(iterations):
        print("Iteracion: ",i)
        total_couples = seleccion.create_couples()
        for couple in total_couples:
            cruza.create_children(couple)
        seleccion.evaluation()
        population = poda.poda_best()
        poda.auxMax()
        poda.auxMin()
        poda.auxAvarage()
        tables(i)
    print(maximo)
    print(avarage)
    print(minimo)
    tabla_historial()

class iniciar():
    def __init__(self):
        app = QtWidgets.QApplication([])
        self.window = uic.loadUi('Interfaz.ui')
        self.window.findMax.clicked.connect(self.fin_Max)
        self.window.createPackage.clicked.connect(self.create)
        self.window.show()
        app.exec()
    
    initial = Inicialization()
    
    def create(self):
        global type_package
        global space_package
        global cost_package
        global price_package
        global iterations
        iterations = int(self.window.generations.text())
        type_package = self.window.typePackage.text()
        space_package =  int(self.window.spacePackage.text())
        cost_package = float(self.window.costPackage.text())
        price_package = float(self.window.pricePackage.text())

        self.initial.create_packages()

    def fin_Max(self):
        maximo.clear()
        minimo.clear()
        avarage.clear()

        global PoI
        global Pmax
        global prob_mut_ind
        global prob_mut_gen
        global iterations
        global container

        iterations = int(self.window.generations.text())
        PoI = int(self.window.poInitial.text())
        Pmax = int(self.window.poMax.text())
        prob_mut_ind = float(self.window.mutInd.text())
        prob_mut_gen = float(self.window.mutGen.text())
        container = int(self.window.tamContenedor.text())

        main(PoI, iterations)

if __name__ == "__main__":
    iniciar()

