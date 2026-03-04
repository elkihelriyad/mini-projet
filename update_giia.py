import sqlite3
import json

DB_PATH = 'ensa_orientation.db'

# Define the new structure
formation_data = [
  {
    "year": "1ère Année",
    "semesters": [
      {
        "name": "Semestre 1",
        "modules": [
          {"name": "Ingénierie Financière", "type": "common"},
          {"name": "Mathématiques pour l'Ingénieur", "type": "common"},
          {"name": "Python pour la Data Science et le Machine Learning", "type": "common"},
          {"name": "Systèmes d'Information", "type": "common"},
          {"name": "Modélisation Stochastique", "type": "common"},
          {"name": "Systèmes de Gestion de Contenu", "type": "common"},
          {"name": "LC 1", "type": "common"}
        ]
      },
      {
        "name": "Semestre 2",
        "modules": [
          {"name": "Transition Écologique et Dynamiques Culturelles", "type": "common"},
          {"name": "Techniques d'Optimisation Avancées", "type": "common"},
          {"name": "Systèmes d'Exploitation et Environnements de Développement", "type": "common"},
          {"name": "Modélisation UML", "type": "common"},
          {"name": "Architecture des Systèmes", "type": "common"},
          {"name": "Machine Learning", "type": "common"},
          {"name": "LC 2", "type": "common"}
        ]
      }
    ]
  },
  {
    "year": "2ème Année",
    "semesters": [
      {
        "name": "Semestre 3",
        "modules": [
          {"name": "Développement Backend en JS", "type": "gi"},
          {"name": "Marketing et Développement Durable", "type": "common"},
          {"name": "Bases de Données Avancées", "type": "common"},
          {"name": "Méthodes Heuristiques et Méta-Heuristiques", "type": "gidia"},
          {"name": "Projets Tutorés", "type": "common"},
          {"name": "Analyse des Données", "type": "gidia"},
          {"name": "Programmation Java Avancée", "type": "gi"},
          {"name": "Développement Web Dynamique", "type": "gi"},
          {"name": "LC 3", "type": "common"}
        ]
      },
      {
        "name": "Semestre 4",
        "modules": [
          {"name": "Gouvernance des Systèmes d'Information", "type": "gi"},
          {"name": "Génie Logiciel", "type": "gi"},
          {"name": "Systèmes Intelligents Flous", "type": "gidia"},
          {"name": "Traitement d'Image / Vision Artificielle", "type": "common"},
          {"name": "Internet des Objets", "type": "common"},
          {"name": "Cloud Computing et Virtualisation", "type": "common"},
          {"name": "Introduction à la Sécurité des Réseaux et Systèmes", "type": "common"},
          {"name": "Management de Projet et Entrepreneuriat", "type": "common"},
          {"name": "LC 4", "type": "common"}
        ]
      }
    ]
  },
  {
    "year": "3ème Année",
    "semesters": [
      {
        "name": "Semestre 5",
        "modules": [
          {"name": "Architectures Réparties JEE", "type": "gi"},
          {"name": "Ingénierie des Données Massives et Big Data", "type": "gidia"},
          {"name": "Anglais", "type": "common"},
          {"name": "Traitement Automatique du Langage Naturel", "type": "gidia"},
          {"name": "Théorie des Jeux et Systèmes Multi-Agents", "type": "gidia"},
          {"name": "Web Sémantique et Développement Mobile", "type": "common"}
        ]
      },
      {
        "name": "Semestre 6",
        "modules": [
          {"name": "Intégration et Solutions Métiers", "type": "common"},
          {"name": "E-Management et Innovation / Innovation et Entrepreneuriat", "type": "common"},
          {"name": "Sécurité des Systèmes d'Information et Technologie Blockchain", "type": "common"},
          {"name": "Factory Management / Usine de Développement Logiciel", "type": "gi"},
          {"name": "Projet de Fin d'Études", "type": "common"}
        ]
      }
    ]
  }
]

def update_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    json_str = json.dumps(formation_data, ensure_ascii=False)
    
    cursor.execute("UPDATE filieres SET formation_json = ? WHERE code = 'GIIA'", (json_str,))
    conn.commit()
    print("GIIA formation data updated successfully.")
    conn.close()

if __name__ == "__main__":
    update_db()
