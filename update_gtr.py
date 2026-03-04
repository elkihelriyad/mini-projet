import sqlite3
import json

DB_PATH = 'ensa_orientation.db'

# Content extracted from the GTR image
description = """La filière Génie de Télécommunication et Réseaux (GTR) de l'ENSA-Safi forme des ingénieurs spécialisés en télécommunications et réseaux pour répondre aux besoins croissants des industries et services. Les étudiants y acquièrent des compétences en conception, implantation et gestion des réseaux, ainsi qu'en traitement du signal et protocoles de communication. La formation met un accent particulier sur la sécurité des réseaux et de l'Internet des objets (IoT), face aux défis croissants en cybersécurité. Structurée sur les quatre derniers semestres, elle combine enseignements techniques et matières spécifiques pour préparer des professionnels polyvalents et hautement qualifiés dans le domaine des TIC."""

debouches = "Ingénieur réseaux, ingénieur télécommunications, administrateur systèmes et réseaux, ingénieur cybersécurité, spécialiste en sécurité des réseaux, ingénieur IoT, développeur et intégrateur de solutions, consultant en réseaux et télécoms, entrepreneur technologique, chercheur en nouvelles technologies."

mots_cles = "Télécommunications, Réseaux, Cybersécurité, Internet des Objets (IoT), Ingénieur télécoms, Administration des réseaux, Sécurité des systèmes, Cloud Computing, Infrastructure réseau, Optimisation des réseaux mobiles, Consultant en cybersécurité, Développement et intégration, Virtualisation, Entrepreneuriat, Intelligence artificielle appliquée aux réseaux, Startups technologiques, Sociétés de services numériques (ESN), Innovation technologique, Infrastructure critique, Recherche et développement (R&D)."

formation_data = [
    {
        "year": "1ère Année",
        "semesters": [
            {
                "name": "Semestre 1",
                "modules": [
                    {"name": "Théorie de l'information et codage", "type": "common"},
                    {"name": "Signaux et systèmes", "type": "common"},
                    {"name": "Electronique analogique", "type": "common"},
                    {"name": "Mathématiques Appliquées pour l'ingénieur", "type": "common"},
                    {"name": "Système d'information", "type": "common"},
                    {"name": "Langues Etrangères (Anglais /Français)", "type": "common"},
                    {"name": "Systèmes de Gestion de Contenu (CMS)", "type": "common"}
                ]
            },
            {
                "name": "Semestre 2",
                "modules": [
                    {"name": "Architecture des Systèmes", "type": "common"},
                    {"name": "Systèmes de Communications Analogiques", "type": "common"},
                    {"name": "Propagation et Antennes", "type": "common"},
                    {"name": "Probabilités et Processus stochastiques", "type": "common"},
                    {"name": "Introduction aux réseaux informatiques", "type": "common"},
                    {"name": "Culture and Art skills", "type": "common"},
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
                    {"name": "Electronique numérique", "type": "common"},
                    {"name": "Réseaux optiques et sécurité des données", "type": "common"},
                    {"name": "Ingénierie de la Décision et Optimisation par la Recherche Opérationnelle (IDORO)", "type": "common"},
                    {"name": "Transmission Numérique en Bande de Base", "type": "common"},
                    {"name": "Techniques de Modulations Numériques", "type": "common"},
                    {"name": "Langues Etrangères (Français /Anglais)", "type": "common"},
                    {"name": "Intelligence artificielle et ses applications", "type": "common"}
                ]
            },
            {
                "name": "Semestre 4",
                "modules": [
                    {"name": "Administration Avancée des Systèmes et Réseaux sous GNU/Linux", "type": "common"},
                    {"name": "Réseaux cellulaires et planification mobile", "type": "common"},
                    {"name": "Systèmes de communication radio", "type": "common"},
                    {"name": "Traitement d'images (TI)", "type": "common"},
                    {"name": "Génie logiciel et systèmes intelligents", "type": "common"},
                    {"name": "Langues Etrangères (Français /Anglais)", "type": "common"},
                    {"name": "Management de Projet et entrepreneuriat", "type": "common"}
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
                    {"name": "Cryptographie et sécurité des systèmes d'information et réseaux (CSSIR)", "type": "common"},
                    {"name": "Automatisation robotisée des processus (RPA)", "type": "common"},
                    {"name": "Sécurité des objets connectés (IOT)", "type": "common"},
                    {"name": "Cloud Computing", "type": "common"},
                    {"name": "technologie de réseau étendu", "type": "common"},
                    {"name": "Langues Etrangères (Anglais /Français)", "type": "common"},
                    {"name": "Employment Skills", "type": "common"}
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
        WHERE code = 'GTR'
    """, (description, debouches, mots_cles, formation_json))
    
    conn.commit()
    print("GTR filiere updated successfully.")
    conn.close()

if __name__ == "__main__":
    update_db()
