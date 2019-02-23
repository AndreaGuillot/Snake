##### Projet Snake #######

import random
import matplotlib.pyplot as plt

##### Les constantes #######

#variables globales
vie=1
score=0
#taille du serpent au depart
tailleS=3   
#nombre de colonnes
nC=15       
#nombre de lignes
nL=10 
     
VIDE=0
POMME=1
TETE=2
#CORPS codé par 3,4,...
BORDURE=-1
#taille du plateau avec la bordure
NC=nC+2                
NL=nL+2

##### Les fonctions #######

def affichePlateau(M):
    MC=[]   
    for i in range(NL):
        copie = [] + M[i]
        MC.append(copie)
    for i in range(NL):
        for j in range(NC):
            if M[i][j]==BORDURE:
                MC[i][j]=[1,1,1]
            elif M[i][j]==VIDE:
                MC[i][j]=[0,0.5,1]
            elif M[i][j]==POMME:
                MC[i][j]=[1,0,0]
            elif M[i][j]==TETE:
                MC[i][j]=[0.23,0.5,0.14]
            else:
                MC[i][j]=[0.62,0.91,0.33]  
    plt.clf()
    plt.imshow(MC,interpolation="nearest");
    plt.pause(0.1)

def plateauDeJeu():
    M=[]
    for i in range(NL):
        L=[]
        for j in range(NC):
            if i==0 or i==NL-1 or j==0 or j==NC-1:
                L.append(BORDURE)
            else :
                L.append(VIDE)
        M.append(L)
    return M

def poseSerpent(M):                     
    #départ du serpent au milieu du plateau
    for r in range(tailleS):         
        M[NL//2][NC//2-r]=TETE+r

def posePomme(M):                           
    #position aléatoire de la pomme
    pp=POMME
    while pp!=VIDE:
        ip=random.randint(1,NL-2)
        jp=random.randint(1,NC-2)
        pp=M[ip][jp]
    M[ip][jp]=POMME

def deplacementCorps(M):
    #copie de M
    M2=[]   
    for i in range(NL):
        M2.append(M[i])
    for i in range(NL):
        for j in range(NC):
           if M2[i][j]>=TETE:
               #chaque partie du serpent prend la position suivante
               M2[i][j]=M2[i][j]+1
    M=M2
    
def deplacementTete(M):
    #variable TailleS, vie et score déjà définie
    global tailleS
    global vie
    global score
    M2=[]                                  
    for i in range(NL):
        M2.append(M[i])
    D=int(input("Quelle direction ? Choix possibles : haut(5), bas(2), gauche(1), droite(3) : "))
    for i in range(NL):
        for j in range(NC):
            if M2[i][j]==TETE+1:
                if D==5 :
                    X=i-1
                    Y=j
                elif D==2 :
                    X=i+1
                    Y=j
                elif D==1 :      
                    X=i
                    Y=j-1
                elif D==3 :   
                    X=i
                    Y=j+1
                #le serpent avance
                if M2[X][Y]==VIDE :
                    for k in range(NL) :
                        for l in range(NC) :
                            if M2[k][l]==tailleS+2 :
                                M2[k][l]=VIDE
                                M2[X][Y]=TETE
                #le serpent grandit
                elif M2[X][Y]==POMME :
                    M2[X][Y]=TETE
                    tailleS=tailleS+1
                    score+=1
                    posePomme(M)
                #la partie est perdue
                else :
                    vie=0
                    
def deplacementIA(M):   
    #variable TailleS, vie et score déjà définie
    global tailleS
    global vie
    global score
    M2=[]                                  
    for i in range(NL):
        M2.append(M[i])
    #recherche des coordonnées de la pomme
    for i in range(NL):
        for j in range(NC):
            if M2[i][j]==POMME:
                Xp=i
                Yp=j
    dmin=NC+NL
    for i in range (NL):
            for j in range (NC):        
                if M2[i][j]==TETE+1:
                    posPossibles=[[i-1,j],[i+1,j],[i,j-1],[i,j+1]]
                    #longueur des chemins pour atteindre la pomme
                    for k in range(len(posPossibles)) :
                        if M2[posPossibles[k][0]][posPossibles[k][1]]==VIDE or M2[posPossibles[k][0]][posPossibles[k][1]]==POMME :
                            d=abs(Xp-posPossibles[k][0])+abs(Yp-posPossibles[k][1])
                            #recherche du chemin le plus court
                            if d<=dmin :
                                dmin=d
                                X=posPossibles[k][0]
                                Y=posPossibles[k][1]
                    #la partie est perdue
                    if dmin==NC+NL:
                        vie=0    
                    #le serpent grandit
                    elif dmin==0 :
                            M2[X][Y]=TETE
                            tailleS=tailleS+1
                            score+=1
                            posePomme(M)
                            break
                    #le serpent avance
                    else :
                        for k in range(NL) :
                            for l in range(NC) :
                                if M2[k][l]==tailleS+2 :
                                    M2[k][l]=VIDE
                                    M2[X][Y]=TETE  

##### Le programme principal #######

C=int(input("Jouer manuellement (1) ou faire jouer l'intelligence artificielle (2):"))

if C==1:
    PJ=plateauDeJeu()
    posePomme(PJ)
    poseSerpent(PJ)
    affichePlateau(PJ)
    while vie==1 :
        deplacementCorps(PJ)
        deplacementTete(PJ)
        affichePlateau(PJ)
    print("BIEN JOUE !", " Votre score est de ",score,".")

else:
    PJ=plateauDeJeu()
    posePomme(PJ)
    poseSerpent(PJ)
    affichePlateau(PJ)
    print("Bougez la fenetre, sinon l'affichage bogue")
    plt.pause(5)
    while vie==1 :
        deplacementCorps(PJ)
        deplacementIA(PJ)
        affichePlateau(PJ)
    print("PARTIE TERMINEE !", " L'ordinateur a fait un score de ",score,".")