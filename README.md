# Étapes du projet
Phase 1 : Modélisation

    Représentation des règles du Futoshiki avec des variables booléennes.
    Traduction des contraintes du jeu en formules logiques sous CNF.

Phase 2 : Génération du format DIMACS

    Développement d’un programme en Python qui convertit une instance du problème en fichier DIMACS (format standard pour les solveurs SAT).

Phase 3 : Résolution et Affichage

    Utilisation d’un SAT-solveur (ex: MiniSat, Z3) pour résoudre le problème.
    Extraction et affichage de la solution lisible à partir de la trace générée.
