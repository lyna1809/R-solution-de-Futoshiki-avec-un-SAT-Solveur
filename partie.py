import os
import random
import inquirer
from test import *

def recherche_bool (liste , el) :
    for p in liste :
        if (p[0]== el[0] and p[1] == el [1]) :
            return True
    return False
def recherche (liste ,f_li, el) :
    
    for p in liste :
        if (p[0]== el[0] and p[1] == el [1]) :
            if  p in f_li :
                return liste
            liste.remove(p)
            (liste.append(el))
            return liste
    return liste 
def verifi2 (listes,a,b,n) :
    if (  (  (   ( a[0] == b[0] and (a[1] == (b[1]-1)) ) or ( ( ( a[0] == b[0] and a[1] == (b[1]+1)) ) ) ) or  ( ( ( a[1] == b[1] and (a[0] == ( b[0]-1))) ) or ( ( a[1] == b[1] and (a[0] == ( b[0]-1))) )  ) ) ):
        if n== 0 :
            if [a,'<',b] not in listes :
                return True
            else :
                return False
        else :
            if [a,'>',b] not in listes :
                return True
            else :
                return False
    return False

def verificati (liste,e) :
    
    for p in liste :
        if p[0] == e[0] and p[1] == e[1] :
            return True
        if p[0] == e[0] and p[2] == e[2] :
            return True
        if p[1] == e[1] and p[2] == e[2] :
            return True        
    return False

def verificati2 (liste,e) :
    l = liste[-1]
    if len(liste) == 0 :
        return False
    
    for p in liste :
        if p[0] == l[0] and p[2] == l[2]  and p[1] !=l[1]:
            return True
        if p[1] == l[1] and p[2] == l[2] and p[0] !=l[0]:
            return True        
    return False


def clear_screen():
    """Efface l'écran de la console"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def display_puzzle(f_puzzle,puzzle, n, l):
    # clear_screen()
    # Définir les codes  pour les couleurs
    RED = '\033[91m'
    GREEN = '\033[92m'
    END = '\033[0m'
    Cyan = '\033[96m'
    
    
    print(Cyan+"\n      1   2   3   4   5"+END)
    for i in range(1, n + 1):
        # Afficher la ligne supérieure de la case
        
        print("    +---+---+---+---+---+")

        for j in range(1, n + 1):
            # Afficher le bord gauche de la case
            if j== 1 :
                print(Cyan,i,END,"| ", end="")
            else :
                print("| ", end="")

            # Rechercher la valeur k pour le tuple (i, j, k)
            k = 0
            for t in puzzle:
                if t[0] == i and t[1] == j:
                    k = t[2]
                    break
            color = GREEN
            if verificati2 (puzzle,(i,j,k)) :
                    color = RED
            if (i,j,k)   in f_puzzle :

                color = Cyan
            

            # else :
            #     color = GREEN
           
            # Afficher la valeur k, ou un espace si la case est vide
            if k != 0:
                # Choisir la couleur en fonction de la valeur de k
                if k in range(1, n+1):
                    color = color
                else:
                    color = RED
                print(color + str(k) + END + " ", end="")
            else:
                print("  ", end="")

        # Afficher le bord droit de la ligne
        print("|")
        

    # Afficher la ligne inférieure de la grille
    print("    +---+---+---+---+---+")
    
    print (GREEN+"\nListe des contraintes : \n"+END)
    for p in l  :
        print (Cyan,p[0],END,RED+p[1]+END,Cyan,p[2],END)

    print ("\n\n")



def generate_puzzle(n,nb):
    """Génère une grille de taille n x n avec des nombres aléatoires"""
    puzzle = []
    while (len (puzzle )!= nb):
            i,j,k = (random.randint(1, n), random.randint(1, n), random.randint(1, n))
            # if not (verificati (puzzle,(i,j,k)) ) :
            puzzle.append((i,j,k))
    return puzzle


def generate_contraintes(n,nb):
    """Génère une grille de taille n x n avec des nombres aléatoires"""
    listes = []
    while (len (listes )!= nb):
            a = (random.randint(1, n), random.randint(1, n))
            b = (random.randint(1, n), random.randint(1, n))
            x = random.randint(0, 1)
            if  (verifi2 (listes,a,b,x) ) :
                if x == 0 :
                   listes.append([a,'<',b])
                else :
                    listes.append([a,'>',b])
    return listes

def load_game (f_puzzle,l) :


        n = 5
        #  generation des clauses 


        clauses = []

        for p in l  :
            clauses += constraints_05(5,p[0],p[2],p[1])

        
        for p in f_puzzle :
            clauses += constraints_04 (p[0],p[1],p[2],n)

        ma_liste = constraints_01(n) + constraints_02(n) + constraints_03(n)  + clauses 

        with open('clause.cnf', 'w') as fichier:
            fichier.write("p  cnf "  +str (n*n*n) +" "+ str(len (ma_liste))  + '\n')
            for element in ma_liste:
                cc =""
                for p in element :
                    cc += p
                fichier.write(cc + '\n')


        resCmd = subprocess.run(["z3",  "clause.cnf"], capture_output=True, text=True).stdout
        # Ecrit le resultat de la commande dans un fichier
        file = open("solution.cnf", "w")
        file.write(str(resCmd))

        solution = resCmd.split("v")[0].split()
        solution = list(filter(delNegNumbers, solution))
        solution.pop(0)
        sss = solution

        puzzle = []
        for tupl in sss :
            puzzle.append((to_tuple(int(tupl),n)))

        return puzzle,resCmd





def play_game():

    leve = 2

    while True :
        
        clear_screen()
        questions = [
        inquirer.List('choice',
                        message="BIENVENU DANS LE JEU FUTOSHIKI ",
                        choices=['JOUE', 'NIVEAU', 'EXIT']
                    ),
        ]
        answers = inquirer.prompt(questions)
        clear_screen()

        if answers['choice'] == 'NIVEAU' :
            questions = [
                inquirer.List('NIVEAU',
                        message="NIVEAU",
                        choices=['FACILE', 'NORMAL', 'DIFFICILE']
                    ),
            ]
            
            answers1 = inquirer.prompt(questions)
            if answers1['NIVEAU']  == 'FACILE' :
        
                leve =   1
            elif answers1['NIVEAU']  == 'DIFFICILE' :
                 
                leve = 3

        if answers['choice'] == "JOUE" :

        # f_puzzle contient les cases daja defini  dans le jeu 
            # f_puzzle = generate_puzzle(5,leve*3)


            n = 5 
            res= ["aa","ll"]
            # l = generate_contraintes(n,leve*2) 

            clear_screen()
            # copie du puzzel ou on va avoir toute les cases 

            # res = load_game (f_puzzle,l)
            # s_puzzle  = res[0]
            while len(res[1]) < 24  :

                    f_puzzle = generate_puzzle(5,leve*2)

                    l = generate_contraintes(n,leve*2) 
                    res = load_game (f_puzzle,l)

            puzzle = f_puzzle.copy()
            # solution du puzzle 
            s_puzzle  = res[0]
            a = True
            while a : 




                clear_screen()
                
                display_puzzle(f_puzzle,puzzle, n,l)
                questions = [
                inquirer.List('JOUE',
                        message="Choisissez   ",
                        choices=['SOLVE','JOUE']
                    ),
                ]
                clear_screen()
                display_puzzle(f_puzzle,puzzle, n,l)


                choice = inquirer.prompt(questions)

                choice = (choice['JOUE'])

                if choice == 'SOLVE' :
                        clear_screen()
                        display_puzzle(f_puzzle,s_puzzle, n,l)
                        questions = [
                        inquirer.List('REJOUE',
                        message= "VOULEZ VOUS   ",
                                    choices=['REJOUE','MENU', 'QUITTER']
                                 ),
                                    ]
                        choice = inquirer.prompt(questions)
                        choice = (choice['REJOUE'])
                        if choice == 'REJOUE' :
                            a = True
                        elif choice == 'QUITTER' :
                            print("Merci d'avoir joue a notre jeu .")
                            exit()
                        elif choice == 'MENU' :

                              a = False  
                else :



                    clear_screen()
                    
                    display_puzzle(f_puzzle,puzzle, n,l)
                    questions = [
                    inquirer.List('ligne',
                            message="Choisissez la ligne de la case  ",
                            choices=['1','2','3','4','5']
                        ),
                    ]
                    clear_screen()
                    display_puzzle(f_puzzle,puzzle, n,l)

                    ligne = inquirer.prompt(questions)
                    ligne = int(ligne['ligne'])
                    questions = [
                    inquirer.List('colonne',
                            message="Choisissez la colonne de la case  ",
                            choices=['1','2','3','4','5']
                        ),
                    ]
                    
                    colonne = inquirer.prompt(questions)
                    colonne = int(colonne['colonne'] )
                    clear_screen()
                    
                    display_puzzle(f_puzzle,puzzle, n,l)

                    questions = [
                    inquirer.List('valeur',
                            message="Choisissez la valeur de la case  ",
                            choices=['1','2','3','4','5']
                        ),
                    ]
                    
                    valeur = inquirer.prompt(questions)
                    valeur = int(valeur['valeur'] )

                    if  recherche_bool(puzzle,(ligne,colonne,valeur)) :
                        puzzle = recherche(puzzle,f_puzzle,(ligne,colonne,valeur))
                    else :
                        puzzle.append((int(ligne),int(colonne),int(valeur)))
                    
        if answers['choice'] == 'EXIT' :
            print("Le programme va maintenant se terminer.")
            exit()







if __name__ == '__main__':
    play_game()
