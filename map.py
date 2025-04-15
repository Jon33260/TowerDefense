WAYPOINTS = [
      (0, 50),
    (750, 50),
    (750, 150),
    (50, 150),
    (50, 550),
    (150, 550),
    (150, 230),
    (750, 230),
    (750, 400),
    (250, 400),
    (250, 550),
    (750, 550),
]

# Nouvelle map pour le niveau 2
WAYPOINTS_NIVEAU2 = [
    (0, 200),    # Point de départ en bord gauche, position verticale médiane
    (150, 200),  # Avance vers la droite
    (150, 50),   # Remontée vers le haut
    (600, 50),   # Longue traversée sur le haut de l'écran
    (600, 200),  # Descente pour créer un virage
    (750, 200),  # Poursuite vers la droite jusqu'au bord
    (750, 400),  # Descente marquée côté droit
    (500, 400),  # Retour vers la gauche pour varier le parcours
    (500, 550),  # Nouvelle descente en bas
    (250, 550),  # Remontée vers la gauche sur le bas de l'écran
    (250, 350),  # Petit déplacement vertical pour créer un virage
    (40, 350),    # Retour final vers la gauche avant de sortir (ou boucler)
]

# Map pour le niveau 3
WAYPOINTS_NIVEAU3 = [
    (0, 250),     # Début à gauche au milieu
    (150, 250),   # Vers la droite
    (150, 100),   # Monter vers le haut
    (350, 100),   # Avancer à droite sur le haut
    (350, 300),   # Redescendre pour créer un virage
    (550, 300),   # Avancer vers la droite
    (550, 150),   # Remonter pour un virage serré
    (700, 150),   # Continuer vers la droite
    (700, 400),   # Redescendre sensiblement plus bas
    (450, 400),   # Revenir vers la gauche pour un contre-virage
    (450, 550),   # Descente en bas
    (750, 550)    # Sortie à droite
]

