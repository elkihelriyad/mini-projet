import sqlite3
import json

DB_PATH = 'ensa_orientation.db'

# Content extracted from the GMSI image
description = """La filière "Mécatronique et Systèmes Intelligents" combine la mécanique, l'électronique, l'informatique et l'automatique pour concevoir des systèmes intégrés et intelligents. Elle forme des ingénieurs capables de développer des robots, des machines autonomes, et des dispositifs embarqués. Les étudiants apprennent à maîtriser la modélisation, la programmation, et l'optimisation des systèmes complexes. Cette formation prépare à des carrières dans l'automobile, l'aéronautique, la robotique et les technologies de pointe. A la fin de cette formation, les lauréats doivent être capables de : Maîtriser le fonctionnement et augmenter les performances des systèmes mécatroniques. Concevoir et mettre au point des solutions mécatroniques. Conduire une équipe d'innovation dans le domaine de la mécatronique. Superviser, maintenir et développer un système mécatronique. Développer des solutions en mécatronique de l'automobile, de l'avion et des systèmes de production des énergies renouvelables. Systèmes robotisés et intelligents. Concevoir et augmenter la performance des systèmes embarqués. Concevoir, développer et maintenir des Optimiser une chaîne de production et améliorer la productivité. Conduire un changement et gérer les contraintes technologiques. Faire partie d'une équipe mixte de conception et de fabrication intégrées de systèmes mécatroniques."""

debouches = "Chef de projet en systèmes mécatroniques, gestion de maintenance et sûreté de fonctionnement, ingénieur en conception et développement mécatronique, bureaux d’études, industrie automobile, industrie aéronautique, énergies renouvelables, robotique industrielle, ingénieur-conseil."

mots_cles = "Mécatronique, Systèmes Intelligents, Robotique, Automatique, Systèmes Embarqués, Mécanique, Electronique, Informatique, Automobile, Aéronautique, Energies Renouvelables, Maintenance, IA. "

formation_data = [
    {
        "year": "1ère Année",
        "semesters": [
            {
                "name": "Semestre 1",
                "modules": [
                    {"name": "Electronique Numérique", "type": "common"},
                    {"name": "Conception des Systèmes Mécaniques", "type": "common"},
                    {"name": "Systèmes Analogiques Avancés", "type": "common"},
                    {"name": "Programmation Orientée Objet en C++", "type": "common"},
                    {"name": "Systèmes de Mesure et Conception Expérimentale", "type": "common"},
                    {"name": "Algorithmique et Programmation en Python", "type": "common"},
                    {"name": "Langues Étrangères (Anglais/Français)", "type": "common"}
                ]
            },
            {
                "name": "Semestre 2",
                "modules": [
                    {"name": "Programmation des microcontrôleurs CORTEX M4", "type": "common"},
                    {"name": "Mécanique des Milieux Continues et Mécanique des Fluides", "type": "common"},
                    {"name": "Électronique de Puissance", "type": "common"},
                    {"name": "Électrotechnique", "type": "common"},
                    {"name": "Propriétés Mécaniques et Thermiques des Matériaux", "type": "common"},
                    {"name": "Créativité visuelle et innovation numérique", "type": "common"},
                    {"name": "Traitement du signal et simulation de circuits électroniques", "type": "common"},
                    {"name": "Langues Etrangères (Anglais /Français)", "type": "common"}
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
                    {"name": "Base de Données et Réseaux Informatiques", "type": "common"},
                    {"name": "Systèmes Hydrauliques et Pneumatiques", "type": "common"},
                    {"name": "Calcul des Structures et RDM", "type": "common"},
                    {"name": "Systèmes Embarqués pour l'Automobile et Automate Programmable", "type": "common"},
                    {"name": "Systèmes Asservis", "type": "common"},
                    {"name": "Intelligence Artificielle et ses Applications", "type": "common"},
                    {"name": "Langues Étrangères (Anglais/Français)", "type": "common"}
                ]
            },
            {
                "name": "Semestre 4",
                "modules": [
                    {"name": "Informatique Embarquée", "type": "common"},
                    {"name": "Circuits programmables", "type": "common"},
                    {"name": "Capteurs intelligents industriels et chaine d'acquisition", "type": "common"},
                    {"name": "Maintenance 4.0", "type": "common"},
                    {"name": "Management de projet et entrepreneuriat", "type": "common"},
                    {"name": "Management intégré qualité, sécurité et environnement", "type": "common"},
                    {"name": "Mini projets", "type": "common"},
                    {"name": "Langues étrangères (français /anglais)", "type": "common"}
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
                    {"name": "Pilotage des performances et excellence opérationnelle", "type": "common"},
                    {"name": "Systèmes mécatroniques de l'automobile", "type": "common"},
                    {"name": "Robotique et systèmes intelligents", "type": "common"},
                    {"name": "Employment skills", "type": "common"},
                    {"name": "Outils de modélisation et simulation automobile", "type": "common"},
                    {"name": "Internet des objets", "type": "common"},
                    {"name": "Commande intelligente", "type": "common"},
                    {"name": "Langues étrangères (français /anglais)", "type": "common"}
                ]
            },
            {
                "name": "Semestre 6",
                "modules": [
                    {"name": "Projet de fin d'étude (PFE)", "type": "common"}
                ]
            }
        ]
    }
]

def update_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    formation_json = json.dumps(formation_data, ensure_ascii=False)
    
    cursor.execute("""
        UPDATE filieres 
        SET description = ?, debouches = ?, mots_cles = ?, formation_json = ?
        WHERE code = 'GMSI'
    """, (description, debouches, mots_cles, formation_json))
    
    conn.commit()
    print("GMSI filiere updated successfully.")
    conn.close()

if __name__ == "__main__":
    update_db()
