import sqlite3
import json

DB_PATH = 'ensa_orientation.db'

# Content extracted from the GPMA image
description = """La filière génie des procédés et matériaux avancés a pour objectifs de répondre au marché de l'emploi avec plus d'ouverture vers la culture projet et le monde industriel. L'ingénieur en Génie des Procédés & Matériaux Avancés est fondamentalement un manager de la production, ouvert sur l'international. Il est capable de concevoir, d'implanter et de piloter un système de production en tenant compte des caractéristiques scientifiques, technologiques, économiques et humaines. Il participe à l'organisation de l'entreprise, en respectant les principes de durabilité et de respect de l'environnement. Il exploite ses connaissances au service de la performance, de la sécurité et de la qualité. Sa compétence s'étend des installations jusqu'aux produits, en passant par les relations et les informations mises en jeu lors de la production."""

debouches = "Conduite des procédés industriels, qualité industrielle, gestion énergétique et environnementale, sécurité industrielle, production, recherche et développement (R&D), services technico-commerciaux, après-vente, vente industrielle, achats techniques."

mots_cles = "Génie des Procédés, Matériaux Avancés, Management de Production, Durabilité, R&D, Qualité HSE, Procédés Industriels, Matériaux Innovants, Digitalisation, Industrie 4.0, Simulation, Corrosion, Composites."

formation_data = [
    {
        "year": "1ère Année",
        "semesters": [
            {
                "name": "Semestre 1",
                "modules": [
                    {"name": "Opérations unitaires", "type": "common"},
                    {"name": "Physico-chimie des matériaux solides", "type": "common"},
                    {"name": "Instrumentation, mesures et plan d'expérience", "type": "common"},
                    {"name": "Résistance des matériaux et simulation numérique par éléments finis", "type": "common"},
                    {"name": "Systèmes thermiques et énergétiques", "type": "common"},
                    {"name": "Algorithmique et programmation en Python", "type": "common"},
                    {"name": "Langues étrangères", "type": "common"}
                ]
            },
            {
                "name": "Semestre 2",
                "modules": [
                    {"name": "Echangeurs de chaleur industriels et machines hydrauliques", "type": "common"},
                    {"name": "Energies renouvelables", "type": "common"},
                    {"name": "Techniques de caractérisation des matériaux", "type": "common"},
                    {"name": "Recherche opérationnelle pour le génie industriel", "type": "common"},
                    {"name": "Automatique linéaire", "type": "common"},
                    {"name": "Algorithmique et programmation en Python", "type": "common"},
                    {"name": "Langues étrangères", "type": "common"}
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
                    {"name": "Cristallisation industrielle et filtration", "type": "common"},
                    {"name": "Pilotage des performances et excellence opérationnelle", "type": "common"},
                    {"name": "Procédés de l'environnement et dessalement de l'eau de mer", "type": "common"},
                    {"name": "Statistique décisionnelle", "type": "common"},
                    {"name": "Métallurgie et traitement de surface", "type": "common"},
                    {"name": "Intelligence artificielle et ses applications", "type": "common"},
                    {"name": "Langues étrangères", "type": "common"}
                ]
            },
            {
                "name": "Semestre 4",
                "modules": [
                    # Specializations
                    {"name": "Technologie des matériaux céramiques", "type": "gi"}, # GMA
                    {"name": "Propriétés mécaniques et thermiques des matériaux", "type": "gi"}, # GMA
                    {"name": "Commande des procédés industriels", "type": "gidia"}, # GPI
                    {"name": "Génie réacteurs chimiques / Milieux poreux et dispersés", "type": "gidia"}, # GPI
                    {"name": "Théories et pratiques des fours et des sécheurs industriels", "type": "gidia"}, # GPI
                    
                    # Common
                    {"name": "Management des entreprises et de projets", "type": "common"},
                    {"name": "Management de production", "type": "common"},
                    {"name": "Management intégré qualité, sécurité et environnement", "type": "common"},
                    {"name": "Mini projet", "type": "common"},
                    {"name": "Langues étrangères", "type": "common"}
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
                    # Specializations
                    {"name": "Protection anticorrosion par revêtements", "type": "gi"}, # GMA
                    {"name": "Matériaux durables et procédés de fabrication additive", "type": "gi"}, # GMA
                    {"name": "Matériaux innovants, intelligents et nouvelles technologies", "type": "gi"}, # GMA
                    {"name": "Matériaux composites et polymères", "type": "gi"}, # GMA
                    
                    {"name": "Stockage d'énergie et audit énergétique des procédés industriels", "type": "gidia"}, # GPI
                    {"name": "Simulation des procédés industriels", "type": "gidia"}, # GPI
                    {"name": "Cycle de vie, impact environnemental et sécurité des procédés", "type": "gidia"}, # GPI
                    {"name": "Réalité virtuelle et réalité augmentée", "type": "gidia"}, # GPI
                    {"name": "Technologies hydrogène et matériaux énergétiques", "type": "gidia"}, # GPI
                    
                    # Common
                    {"name": "Industrie 4.0", "type": "common"},
                    {"name": "Employment skills", "type": "common"},
                    {"name": "Langues étrangères", "type": "common"}
                ]
            },
            {
                "name": "Semestre 6",
                "modules": [
                    {"name": "Projet de Fin d'Etudes (PFE)", "type": "common"}
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
        WHERE code = 'GPMA'
    """, (description, debouches, mots_cles, formation_json))
    
    conn.commit()
    print("GPMA filiere updated successfully with formatted module names.")
    conn.close()

if __name__ == "__main__":
    update_db()
