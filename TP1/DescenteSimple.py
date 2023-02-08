import numpy as np
import random as rd
import copy as copy

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


def fonctionDeVoisinage(solution):
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
    for indexe in range(0,len(solution2)-2):
        sommetCourant = solution2[indexe]
        sommetSuivant = solution2[indexe+1]
        longueurDuCycle = longueurDuCycle + int(graphe[sommetCourant-1,sommetSuivant-1])
    return int(longueurDuCycle)

def min_voisinage(voisinage, graphe) :
    min_voisin = copy.deepcopy(voisinage[0])

    for voisin in voisinage :
        if fonctionFitness(voisin,graphe) < fonctionFitness(min_voisin,graphe) :
            min_voisin = copy.deepcopy(voisin)

    return min_voisin

sommetInitiale = int(input("Entrez le numero du sommet initiale : "))
solutionCourante = generationDeLaSolutionInitiale(sommetInitiale)
longueurSolutionCourante = fonctionFitness(solutionCourante,graphe)
print(solutionCourante,"Longueur ==> ",fonctionFitness(solutionCourante,graphe))
voisinage = fonctionDeVoisinage(solutionCourante)
print(len(voisinage))
min_voisin = min_voisinage(voisinage,graphe)
longueurMin_voisin = fonctionFitness(min_voisin,graphe)
k = 0
optimun_obtenu_apres_k_itteration = solutionCourante
while k <= 10 :
    while longueurMin_voisin < longueurSolutionCourante :
        print(min_voisin,"Longueur ==> ",longueurMin_voisin)
        solutionCourante = min_voisin
        voisinage = fonctionDeVoisinage(solutionCourante)
        min_voisin = min_voisinage(voisinage,graphe)
        longueurSolutionCourante = fonctionFitness(solutionCourante,graphe)
        longueurMin_voisin = fonctionFitness(min_voisin,graphe)

    if longueurSolutionCourante < fonctionFitness(optimun_obtenu_apres_k_itteration,graphe) :
        optimun_obtenu_apres_k_itteration = solutionCourante
    
    k = k + 1

    solutionCourante = generationDeLaSolutionInitiale(sommetInitiale)
    longueurSolutionCourante = fonctionFitness(solutionCourante,graphe)
    voisinage = fonctionDeVoisinage(solutionCourante)
    min_voisin = min_voisinage(voisinage,graphe)
    longueurMin_voisin = fonctionFitness(min_voisin,graphe)

print("Optimun obtenu apres:",k,'itteration',optimun_obtenu_apres_k_itteration,"Longueur ==> ",fonctionFitness(optimun_obtenu_apres_k_itteration,graphe))