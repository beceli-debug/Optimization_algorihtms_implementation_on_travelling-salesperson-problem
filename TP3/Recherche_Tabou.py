import numpy as np
import random as rd
import copy as copy
import itertools as combi

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
    listeDesPermutations = list(combi.permutations(solution0[bornInf:(bornSup + 1)]))
    for element in listeDesPermutations :
        element = list(element)
        element = solution0[:(bornInf)] + element + solution0[(bornSup + 1):]
        lesPermutations.append(element)
    while bornSup <= 36 :
        bornInf = bornSup + 1
        bornSup = bornInf + 5
        listeDesPermutations = list(combi.permutations(solution0[bornInf:(bornSup + 1)]))
        for element in listeDesPermutations :
            element = list(element)
            element = solution0[:(bornInf)] + element + solution0[(bornSup + 1):]
            lesPermutations.append(element)

    return lesPermutations

liste_tabou = []
def fonctionDevoisinage(solution,liste_tabou):
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
                voisinage.append(solution0)
                solution01 = copy.deepcopy(solution0)
                k = 0
                while k != 10 :
                    indexe1 = rd.randint(1,41)
                    indexe2 = rd.randint(1,41)
                    while indexe1 == indexe2 :
                       indexe1 = rd.randint(1,41)
                       indexe2 = rd.randint(1,41) 
                    variableIntermediaire = solution0[indexe1]
                    solution0[indexe1] = solution0[indexe2]
                    solution0[indexe2] = variableIntermediaire
                    voisinage.append(solution0)
                    solution0 = []
                    solution0 = copy.deepcopy(solution01)
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
    for indexe in range(0,len(solution2)-2):
        sommetCourant = solution2[indexe]
        sommetSuivant = solution2[indexe+1]
        longueurDuCycle = longueurDuCycle + int(graphe[sommetCourant-1,sommetSuivant-1])
    return int(longueurDuCycle)

def min_voisinage(voisinage,listeDesTabou,graphe) :
    min_voisin = copy.deepcopy(voisinage[0])
    mouvementTabou = False
    for tabou in listeDesTabou :
        if tabou == min_voisin :
            mouvementTabou = True
            break
    while mouvementTabou == True :
        voisinage.pop(0)
        min_voisin = copy.deepcopy(voisinage[0])
        mouvementTabou = False
        for tabou in listeDesTabou :
            if tabou == min_voisin :
                mouvementTabou = True
                break
                    
    for voisin in voisinage :
        if fonctionFitness(voisin,graphe) < fonctionFitness(min_voisin,graphe) :
            mouvementTabou = False
            for tabou in listeDesTabou :
                if tabou == voisin :
                    mouvementTabou = True
                    break
            if mouvementTabou == False :
                min_voisin = copy.deepcopy(voisin)

    return min_voisin

sommetInitiale = int(input("Entrez le numero du sommet initiale : "))
solutionInitiale = generationDeLaSolutionInitiale(sommetInitiale)
longueurSolutionInitiale = fonctionFitness(solutionInitiale,graphe)
longueurSolutionCourante = longueurSolutionInitiale
print(solutionInitiale,"Longueur ==> ",longueurSolutionCourante)
solutionCourante = solutionInitiale
optimun_globale = solutionCourante
k = 0
compteurTabou = 0
while (k != 100) :
    voisinage = fonctionDevoisinage(solutionCourante,liste_tabou)
    min_voisin = min_voisinage(voisinage,liste_tabou,graphe)
    if fonctionFitness(min_voisin, graphe) < fonctionFitness(solutionCourante, graphe) :
        solutionCourante = copy.deepcopy(min_voisin)
        liste_tabou.append(solutionCourante)
        print(solutionCourante,"Longueur ==> ",fonctionFitness(solutionCourante, graphe))
    else :
        prob = rd.random()
        if prob > 0.6 :
            solutionCourante = copy.deepcopy(min_voisin)
            liste_tabou.append(solutionCourante)
            print(solutionCourante,"Longueur ==> ",fonctionFitness(solutionCourante,graphe))
    
    if fonctionFitness(optimun_globale,graphe) > fonctionFitness(solutionCourante,graphe) :
        optimun_globale = copy.deepcopy(solutionCourante) 
    if compteurTabou != 5 :
        compteurTabou = compteurTabou + 1
    else :
        if len(liste_tabou) != 0 and (len(liste_tabou) != 1) :
            liste_tabou.pop(0)
        compteurTabou = 0
    k = k + 1
    
print(optimun_globale,"Longueur ==> ",fonctionFitness(optimun_globale,graphe))
    

