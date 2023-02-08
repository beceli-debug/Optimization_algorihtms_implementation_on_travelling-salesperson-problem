import numpy as np
import random as rd
import copy as copy
import itertools as conbi
import math as math
data = open(r"Graphe.txt","r").read().replace("\n","").replace(" ",",").split(",")

ligne = []
graphe = []

for element in data :
    if element == "0" :
        ligne.append(int(element))
        graphe.append(ligne)
        ligne = []
    elif element.isnumeric() :
        ligne.append(int(element))

i = 0
for ligne in graphe :
    j = 0
    for element in ligne :
        
        if element != 0 :
            graphe[j].insert(i,element)
            j = 1 + j
        else :
            break
    i = i + 1

graphe = np.array(graphe, dtype=np.int16)


def permutation(solution) :
    solution0 = []
    solution0 = copy.deepcopy(solution)
    lesPermutations = []
    bornInf = 1
    bornSup = 5
    listeDesPermutations = list(conbi.permutations(solution0[bornInf:(bornSup + 1)]))
    for element in listeDesPermutations :
        element = list(element)
        element = solution0[:(bornInf)] + element + solution0[(bornSup + 1):]
        if (element != solution):
                lesPermutations.append(element)
    while bornSup <= 36 :
        bornInf = bornSup + 1
        bornSup = bornInf + 5
        listeDesPermutations = list(conbi.permutations(solution0[bornInf:(bornSup + 1)]))
        for element in listeDesPermutations :
            element = list(element)
            element = solution0[:(bornInf)] + element + solution0[(bornSup + 1):]
            if (element != solution):
                lesPermutations.append(element)

    return lesPermutations
        

def fonctionDevoisinage(solution):
    voisinage = []
    for indiceDepermutation in range(1,42):
        for i in range(1,42) :
            if indiceDepermutation  != i :
                solution0 = []
                solution0 = copy.deepcopy(solution)
                indexe1 = indiceDepermutation
                indexe2 = i
                variableIntermediaire = solution0[indexe1]
                solution0[indexe1] = solution0[indexe2]
                solution0[indexe2] = variableIntermediaire
                if solution0 != solution :
                    voisinage.append(solution0)
                solution1 = copy.deepcopy(solution0)
                k = 0
                while k != 3 :
                    indexe1 = rd.randint(1,41)
                    indexe2 = rd.randint(1,41)
                    while indexe1 == indexe2 :
                       indexe1 = rd.randint(1,41)
                       indexe2 = rd.randint(1,41) 
                    variableIntermediaire = solution0[indexe1]
                    solution0[indexe1] = solution0[indexe2]
                    solution0[indexe2] = variableIntermediaire
                    if solution0 != solution :
                        voisinage.append(solution0)
                    solution0 = []
                    solution0 = copy.deepcopy(solution1)
                    k = k + 1
    
    return voisinage

def generationDeLaSolutionInitiale(sommetInitiale):
    solution1 = []
    for i in range(43):
        solution1.append(i)
    solution1.remove(0)
    solution1.remove(sommetInitiale)
    rd.shuffle(solution1)
    solution1.insert(0,sommetInitiale)
    solution1.append(sommetInitiale)
    return solution1

def fonctionFitness(solution2,graphe):
    longueurDuCycle = 0
    for indexe in range(0,len(solution2)-1):
        sommetCourant = solution2[indexe]
        sommetSuivant = solution2[indexe+1]
        longueurDuCycle = longueurDuCycle + int(graphe[sommetCourant-1,sommetSuivant-1])
    return int(longueurDuCycle)

def min_voisinage(voisinage,solutionPrecedente,graphe) :
    min_voisin = []
    min_voisin = voisinage[0]
    while min_voisin == solutionPrecedente :
        voisinage.pop(0)
        min_voisin = voisinage[0]

    for voisin in voisinage :
        if (fonctionFitness(voisin,graphe) < fonctionFitness(min_voisin,graphe)) and (voisin != solutionPrecedente) :
            min_voisin = (copy.deepcopy(voisin))
        

    return min_voisin

temperature = pow(10,10)
temperature = float(temperature)
temperatureSaisie = temperature
temperatureSeuil = 0.1
temperatureSeuil = float(temperatureSeuil)
froid = 0.9
froid = float(froid)
sommetInitiale = int(input("Entrez le numero du sommet initiale : "))
solutionCourante = generationDeLaSolutionInitiale(sommetInitiale)
optimun_obtenu_apres_k_itteration = solutionCourante
longueurSolutionCourante = fonctionFitness(solutionCourante,graphe)
print(solutionCourante,"Longueur ==> ",longueurSolutionCourante)
voisinage = fonctionDevoisinage(solutionCourante)
print(len(voisinage))
min_voisin = min_voisinage(voisinage,solutionCourante,graphe)
longueurMin_voisin = fonctionFitness(min_voisin,graphe)
while temperature > temperatureSeuil :
    if longueurMin_voisin < longueurSolutionCourante :
        print(min_voisin,"Longueur ==> ",longueurMin_voisin)
        solutionPrecedente = solutionCourante
        solutionCourante = min_voisin
        longueurSolutionCourante = fonctionFitness(solutionCourante,graphe)
        voisinage = fonctionDevoisinage(solutionCourante)
        min_voisin = min_voisinage(voisinage,solutionPrecedente,graphe)
        #min_voisin = min_voisinage(permutation(min_voisin),solutionCourante,graphe)
        longueurMin_voisin = fonctionFitness(min_voisin,graphe)
    else:
        r = rd.random()
        if r < math.exp((longueurSolutionCourante - longueurMin_voisin) / temperature) :
            solutionCourante = min_voisin
            longueurSolutionCourante = fonctionFitness(solutionCourante,graphe)
            print(solutionCourante,"Longueur ==> ",longueurSolutionCourante)
            voisinage = fonctionDevoisinage(solutionCourante)
            min_voisin = min_voisinage(voisinage,solutionCourante,graphe)
            #min_voisin = min_voisinage(permutation(min_voisin),solutionCourante,graphe)
            longueurMin_voisin = fonctionFitness(min_voisin,graphe)
    if longueurSolutionCourante < fonctionFitness(optimun_obtenu_apres_k_itteration,graphe) :
        optimun_obtenu_apres_k_itteration = solutionCourante
    temperature = temperature * froid

print("Optimun obtenu est:",optimun_obtenu_apres_k_itteration,"Longueur ==> ",fonctionFitness(optimun_obtenu_apres_k_itteration,graphe))

    

