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

# Map pour le niveau 4 (niveau plus difficile)
WAYPOINTS_NIVEAU4 = [
    (0, 350),      # Départ à gauche, position médiane
    (100, 350),    # Avance vers la droite
    (100, 200),    # Monte brusquement pour créer un virage serré
    (200, 200),    # Avance avec la trajectoire haute
    (200, 450),    # Descente rapide pour changer de direction
    (350, 450),    # Poursuite vers la droite, zone basse
    (350, 150),    # Remontée abrupte pour forcer un changement d'angle
    (500, 150),    # Avance sur la partie haute
    (500, 400),    # Descente pour revenir vers une zone centrale
    (650, 400),    # Continue à droite
    (650, 250),    # Remonte brièvement pour créer un virage
    (750, 250),    # Avance encore vers la droite
    (750, 500),    # Descente marquée pour complexifier le parcours
    (600, 500),    # Retour en arrière sur une partie pour multiplier les virages
    (600, 600),    # Descente finale pour un virage serré
    (400, 600),    # Remontée en direction de la gauche
    (400, 500),    # Petit virage final
    (0, 500)       # Arrivée finale à gauche
]

