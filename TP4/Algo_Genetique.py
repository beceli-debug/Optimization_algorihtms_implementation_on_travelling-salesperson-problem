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

def Generation_Population(sommetInitiale,taille):
    population = []
    k = 1
    while k <= taille :
        individu = []
        for i in range(43):
            individu.append(i)
        individu.remove(0)
        individu.remove(sommetInitiale)
        rd.shuffle(individu)
        individu.insert(0,sommetInitiale)
        individu.append(sommetInitiale)
        population.append(individu)
        k = k + 1
               
    return population

def evaluation_et_evaluation(population,NbIndividuSelectionnee,graphe) :
    copy_population = []
    copy_population = copy.deepcopy(population)
    listeIndividuSelectionnes = []
    while len(copy_population) != 0 and len(listeIndividuSelectionnes) != NbIndividuSelectionnee :
        k = 0
        posMeilleur_individu = 0
        meilleur_individu = copy_population[0]
        for individu in copy_population :
            if fonctionFitness(individu,graphe) < fonctionFitness(meilleur_individu,graphe) :
                meilleur_individu = individu
                posMeilleur_individu = k
            k = k + 1
        listeIndividuSelectionnes.append(meilleur_individu)
        copy_population.pop(posMeilleur_individu)

    return listeIndividuSelectionnes

def fonctionDeMutationControlle(solution,NbDePermutation,graphe):
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
                #solution0 = min_voisinage(permutation(solution0),graphe)
                if solution0 != solution :
                    voisinage.append(solution0)
                solution1 = copy.deepcopy(solution0)
                nbIndividu = 0
                while nbIndividu != 10 :
                    k = 0
                    while k != NbDePermutation :
                        indexe1 = rd.randint(1,41)
                        indexe2 = rd.randint(1,41)
                        while indexe1 == indexe2 :
                            indexe1 = rd.randint(1,41)
                            indexe2 = rd.randint(1,41) 
                        variableIntermediaire = solution0[indexe1]
                        solution0[indexe1] = solution0[indexe2]
                        solution0[indexe2] = variableIntermediaire
                        k = k + 1
                    if solution0 != solution :
                        voisinage.append(solution0)
                    solution0 = copy.deepcopy(solution1)
                    nbIndividu = nbIndividu + 1          

    mutant = min_voisinage(voisinage,graphe)
    
    return mutant   

def mutation(population_selectionner,NbDeGeneMutant) :
    liste_des_individu_mutant = []
    for individu in  population_selectionner :
        if rd.random() > 0.6 :
            liste_des_individu_mutant.append(fonctionDeMutationControlle(individu,NbDeGeneMutant,graphe))
        else :
            liste_des_individu_mutant.append(individu)

    return liste_des_individu_mutant

def croisement(population_selectionner) :
    liste_des_individus_issuent_de_croisement = []
    sommetInitiale = population_selectionner[0][0]
    for individu_a in population_selectionner :
        if rd.random() > 0.3 :
            for individu_b in population_selectionner :
                if (rd.random() > 0.3) and (individu_a != individu_b) :
                    cassure = rd.randint(10,21)
                    nouvelleIndividu_n1 = individu_a[:cassure]
                    nouvelleIndividu_n2 = individu_b[:cassure]
                    for sommet_b in individu_b :
                        repetition = False
                        for sommet_a in nouvelleIndividu_n1 :
                            if sommet_a == sommet_b :
                                repetition = True
                                break
                        if repetition == False :
                            nouvelleIndividu_n1.append(sommet_b)
                    for sommet_a in individu_a :
                        repetition = False
                        for sommet_b in nouvelleIndividu_n2 :
                            if sommet_a == sommet_b :
                                repetition = True
                                break
                        if repetition == False :
                            nouvelleIndividu_n2.append(sommet_a)
                    nouvelleIndividu_n1.append(sommetInitiale)
                    nouvelleIndividu_n2.append(sommetInitiale)
                    liste_des_individus_issuent_de_croisement.append(nouvelleIndividu_n1)
                    liste_des_individus_issuent_de_croisement.append(nouvelleIndividu_n2)
                    
    return liste_des_individus_issuent_de_croisement

def fonctionFitness(solution2,graphe):
    longueurDuCycle = 0
    for indexe in range(0,len(solution2)-1):
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
population = Generation_Population(sommetInitiale,500)
min_voisin = min_voisinage(population,graphe)
solutionCourante = min_voisin
print(solutionCourante,"Longueur ==> ",fonctionFitness(solutionCourante, graphe))
optimun_obtenu_apres_k_itteration = min_voisin
k = 1
while (k < 1000) :
    population = evaluation_et_evaluation(population,10,graphe)
    population = mutation(population,1) + croisement(population)
    min_voisin = min_voisinage(population,graphe)
    solutionCourante = min_voisin
    print(solutionCourante,"Longueur ==> ",fonctionFitness(solutionCourante, graphe))
        
    k = k + 1
    
    if fonctionFitness(solutionCourante,graphe) < fonctionFitness(optimun_obtenu_apres_k_itteration,graphe) :
        optimun_obtenu_apres_k_itteration = copy.deepcopy(solutionCourante) 

    
print("Optimun obtenu apres",k,"generation est:",optimun_obtenu_apres_k_itteration,"Longueur ==> ",fonctionFitness(optimun_obtenu_apres_k_itteration,graphe))
    


