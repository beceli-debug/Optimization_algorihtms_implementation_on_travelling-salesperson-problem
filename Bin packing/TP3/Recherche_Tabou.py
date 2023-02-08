import numpy as np
import random as rd
import copy as copy
import itertools as combi

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

def voisinage(listeSacs, listeDesTabou):
    voisinage = []
    for i in range(100):
        for i in range(round(len(listeSacs)/3)):
            sac = listeSacs[rd.randint(0, len(listeSacs) - 1 )]
            listeSacs = viderSac(sac, list(listeSacs))
        voisinage.append(list(listeSacs))

    for voisin in voisinage :
        mouvementTabou = False
        for tabou in listeDesTabou :
            if tabou == voisin :
                mouvementTabou = True
                break
        if mouvementTabou == True :
            voisinage.remove(voisin)
    return list(voisinage)

def optimumLocal(solutionInitiale ,voisinage):
    optimumLocal = solutionInitiale
    #print("SoluIni : " + " ==> " + str(fonctionCout(solutionInitiale)))
    for solution in voisinage:
        if (fonctionCout(solution) <= fonctionCout(optimumLocal)):
            optimumLocal = solution
    #print("OptimumLocal : " + str(optimumLocal) + " ==> " + str(fonctionCout(optimumLocal)))
    return list(optimumLocal)

liste_tabou = []

soluInitiale = solutionInitiale(listeObjets)
longueurSolutionInitiale = fonctionCout(soluInitiale)
longueurSolutionCourante = longueurSolutionInitiale
print(soluInitiale,"Longueur ==> ",longueurSolutionCourante)
solutionCourante = soluInitiale
optimun_globale = solutionCourante
k = 0
compteurTabou = 0
while (k != 100) :
    voisins = voisinage(solutionCourante,liste_tabou)
    min_voisin = optimumLocal(solutionCourante,voisins)
    if fonctionCout(min_voisin) < fonctionCout(solutionCourante) :
        solutionCourante = copy.deepcopy(min_voisin)
        liste_tabou.append(solutionCourante)
        print(solutionCourante,"Longueur ==> ",fonctionCout(solutionCourante))
    else :
        prob = rd.random()
        if prob > 0.6 :
            solutionCourante = copy.deepcopy(min_voisin)
            liste_tabou.append(solutionCourante)
            print(solutionCourante,"Longueur ==> ",fonctionCout(solutionCourante))
    
    if fonctionCout(optimun_globale) > fonctionCout(solutionCourante) :
        optimun_globale = copy.deepcopy(solutionCourante) 
    if compteurTabou != 5 :
        compteurTabou = compteurTabou + 1
    else :
        if len(liste_tabou) != 0 and (len(liste_tabou) != 1) :
            liste_tabou.pop(0)
        compteurTabou = 0
    k = k + 1
    
print(optimun_globale,"Longueur ==> ",fonctionCout(optimun_globale))
    

