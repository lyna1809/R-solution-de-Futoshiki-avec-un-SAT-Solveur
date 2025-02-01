import subprocess

#===========================  affichage  ============================
def display_puzzle(puzzle, n):
    # Définir les codes ANSI pour les couleurs
    RED = '\033[91m'
    GREEN = '\033[92m'
    END = '\033[0m'
    print("\n\n")
    for i in range(1, n + 1):
        # Afficher la ligne supérieure de la case
        print("+---" * n + "+")

        for j in range(1, n + 1):
            # Afficher le bord gauche de la case
            print("| ", end="")

            # Rechercher la valeur k pour le tuple (i, j, k)
            k = 0
            for t in puzzle:
                if t[0] == i and t[1] == j:
                    k = t[2]
                    break

            # Afficher la valeur k, ou un espace si la case est vide
            if k != 0:
                # Choisir la couleur en fonction de la valeur de k
                if k in range(1, n+1):
                    color = GREEN
                else:
                    color = RED
                print(color + str(k) + END + " ", end="")
            else:
                print("  ", end="")

        # Afficher le bord droit de la ligne
        print("|")

    # Afficher la ligne inférieure de la grille
    print("+---" * n + "+")
    print("\n\n")
#=======================================================================


#=======================================================================
def delNegNumbers(number: str):
    return not list(number)[0] == '-'
#======================================================================= 

#======================================================================= 
def ijk_to_num_case (a,b,c,n) :
    v = 1
    for i in range (1,n+1) :
        for j in range (1,n+1) :
            for k in range (1, n + 1) :
                if (a == i and b == j and k == c) :
                    return v 
                else :
                    v += 1

#======================================================================= 

#=======================================================================
def to_tuple (a,n) :
    v = 1
    for i in range (1,n+1) :
        for j in range (1,n+1) :
            for k in range (1, n + 1) :
                if (a == v) :
                    return  (i,j,k)
                else :
                    v += 1
#=======================================================================

#====================        01      =================================== 
def constraints_01 (n) :
    constraints = []
    
    for i in range (1,n+1) :
        for j in range (1,n+1) :
            constraint = []
            for k in range (1, n + 1) :
                constraint.append(f"{ijk_to_num_case (i,j,k,n)} " )
            constraint.append (" 0 ")
            constraints.append(constraint )
    return constraints
#======================================================================= 

#=====================        02        ================================ 
def constraints_02 (n) :
    constraints = []

    clauses = []
    clause = []
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(1, n + 1):
                clause = []
                for p in range(1, n + 1):
                    if (i != p) :
                        clause.append(f"-{ijk_to_num_case (i,j,k,n)}  -{ijk_to_num_case (p,j,k,n)} " )
                        clause.append (" 0 ")
                        clauses.append(clause)
                        clause = []

    return clauses
#======================================================================= 


#==========================        03      =============================
def constraints_03 (n) :
    constraints = []

    clauses = []
    clause = []
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(1, n + 1):
                
                for p in range(1, n + 1):
                    if (j != p) :
                        clause.append(f"-{ijk_to_num_case (i,j,k,n)}  -{ijk_to_num_case (i,p,k,n)} " )
                        clause.append (" 0 ")
                        clauses.append(clause)
                        clause = []

    return clauses
#======================================================================= 


#==========================        04      =============================
def constraints_04 (i,j,k,n) :
    return [(str(ijk_to_num_case (i,j,k,n)) )+ " 0 "]
#======================================================================= 


#==========================        05      =============================
def constraints_05 (n,case1,case2,ch) :
    if ch == '<' :
        case3 = case2
        case2 = case3
        case1 = case3
    
    clauses = []
    clause = []
    for i in range(1, n ):
        for j in range(i, n + 1):
                        clause.append(f"-{ijk_to_num_case (case1[0],case2[1],i,n)}  -{ijk_to_num_case (case1[0],case2[1],j,n)} " )
                        clause.append (" 0 ")
                        clauses.append(clause)
                        clause = []

    return clauses
#======================================================================= 




#=====================        main       =============================== 
def principale () :
    n = 8

    ma_liste = constraints_01(n) + constraints_02(n) + constraints_03(n)  + constraints_05 (n,(1,1),(2,1),'<') + constraints_04(1,1,4,n) 


    with open('f.cnf', 'w') as fichier:
        fichier.write("p  cnf "  +str (n*n*n) +" "+ str(len (ma_liste))  + '\n')
        for element in ma_liste:
            cc =""
            for p in element :
                cc += p
            fichier.write(cc + '\n')


    resCmd = subprocess.run(["z3",  "f.cnf"], capture_output=True, text=True).stdout
    # Ecrit le resultat de la commande dans un fichier
    file = open("s.cnf", "w")
    file.write(str(resCmd))

    solution = resCmd.split("v")[0].split()
    solution = list(filter(delNegNumbers, solution))
    solution.pop(0)
    sss = solution

    puzzle = []
    for tupl in sss :
        puzzle.append((to_tuple(int(tupl),n)))


    display_puzzle(puzzle, n)
    return

if __name__ == '__main__':
    principale ()
