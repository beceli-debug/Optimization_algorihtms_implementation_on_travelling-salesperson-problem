import numpy as np
import random as rd
import copy as copy
import itertools as conbi
import math as math

data = open(r"poidsObjets.txt","r").read().replace("\n","").replace(" ",",").split(",")
listeObjets = list(data)

listeSacs = []

def poids(sac):
    poids = 0
    for objet in sac:
        poids = poids + int(objet)
    return poids

def ajoutObjet(sac, listeObjets):
    if(len(listeObjets) != 0):
        objet = listeObjets[rd.randint(0, len(listeObjets) - 1 )]
        if ((poids(sac) + int(objet)) <= 150):
            sac.append(objet)
            listeObjets.remove(objet)
            return listeObjets, sac, False
        else:
            return listeObjets, sac, True
    else:
        return listeObjets, sac, True

def viderSac(sac, listeSacs):
    listeSacs.remove(sac)
    solution = list(listeSacs)
    for element in listeSacs:
        index_element = listeSacs.index(element)
        if (len(sac) != 0):
            for objet in sac:
                if ((poids(element) + int(objet)) <= 150):
                    element.append(objet)
                    sac.remove(objet)
        else:
            break
        solution[index_element] = list(element)
    if(len(sac) != 0):
        solution.append(sac)
    
    return list(solution)

def solutionInitiale(listeObjets):
    while(len(listeObjets) != 0):
        echecAjout = False
        sac = []
        while(not(echecAjout)):
            listeObjets, sac, echecAjout = ajoutObjet(sac, listeObjets)
        listeSacs.append(sac)
    return list(listeSacs)

def fonctionCout(listeSacs):
    return len(listeSacs)

def fonctionDeVoisinage(listeSacs):
    voisinage = []
    for i in range(100):
        for i in range(round(len(listeSacs)/3)):
            sac = listeSacs[rd.randint(0, len(listeSacs) - 1 )]
            listeSacs = viderSac(sac, list(listeSacs))
        voisinage.append(list(listeSacs))
    return voisinage

def optimumLocal(solutionInitiale ,voisinage):
    optimumLocal = solutionInitiale
    #print("SoluIni : " + " ==> " + str(fonctionCout(solutionInitiale)))
    for solution in voisinage:
        if (fonctionCout(solution) <= fonctionCout(optimumLocal)):
            optimumLocal = solution
    #print("OptimumLocal : " + str(optimumLocal) + " ==> " + str(fonctionCout(optimumLocal)))
    return list(optimumLocal)


temperature = pow(10,2)
temperature = float(temperature)
temperatureSaisie = temperature
temperatureSeuil = 0.1
temperatureSeuil = float(temperatureSeuil)
froid = 0.9
froid = float(froid)
solutionCourante = solutionInitiale(listeObjets)
optimun_obtenu_apres_k_itteration = solutionCourante
longueurSolutionCourante = fonctionCout(solutionCourante)
print(solutionCourante,"Longueur ==> ",longueurSolutionCourante)
voisinage = fonctionDeVoisinage(solutionCourante)
print(len(voisinage))
min_voisin = optimumLocal(solutionCourante, voisinage)
longueurMin_voisin = fonctionCout(min_voisin)
while temperature > temperatureSeuil :
    if longueurMin_voisin < longueurSolutionCourante :
        print(min_voisin,"Longueur ==> ",longueurMin_voisin)
        solutionPrecedente = solutionCourante
        solutionCourante = min_voisin
        longueurSolutionCourante = fonctionCout(solutionCourante)
        voisinage = fonctionDeVoisinage(solutionCourante)
        min_voisin = optimumLocal(solutionPrecedente,voisinage)
        #min_voisin = optimumLocal(permutation(min_voisin),solutionCourante,graphe)
        longueurMin_voisin = fonctionCout(min_voisin)
    else:
        r = rd.random()
        if r < math.exp((longueurSolutionCourante - longueurMin_voisin) / temperature) :
            solutionCourante = min_voisin
            longueurSolutionCourante = fonctionCout(solutionCourante)
            print(solutionCourante,"Longueur ==> ",longueurSolutionCourante)
            voisinage = fonctionDeVoisinage(solutionCourante)
            min_voisin = optimumLocal(solutionCourante,voisinage)
            #min_voisin = optimumLocal(permutation(min_voisin),solutionCourante,graphe)
            longueurMin_voisin = fonctionCout(min_voisin)
    if longueurSolutionCourante < fonctionCout(optimun_obtenu_apres_k_itteration) :
        optimun_obtenu_apres_k_itteration = solutionCourante
    temperature = temperature * froid

print("Optimun obtenu est:",optimun_obtenu_apres_k_itteration,"Longueur ==> ",fonctionCout(optimun_obtenu_apres_k_itteration))

    

