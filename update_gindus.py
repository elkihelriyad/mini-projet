import sqlite3
import json

DB_PATH = 'ensa_orientation.db'

# Content extracted from the GINDUS image
description = """L'objectif de cette formation est de doter les ingénieurs en génie industriel des compétences nécessaires en management industriel. Le métier de l'ingénieur en génie industriel repose sur l'amélioration continue et l'optimisation des performances des entreprises dans divers domaines (technique, financier, organisationnel, humain). La formation répond à cette polyvalence en proposant, durant les trois premiers semestres, des enseignements techniques et scientifiques (électronique, informatique, mécanique, ... etc), suivis de formations managériales et spécifiques (production, maintenance, qualité, logistique, lean manufacturing,...etc) dans les deux derniers semestres. L'enjeu est de fournir aux futurs ingénieurs les outils et méthodes pour concevoir des systèmes et gérer efficacement les aspects économiques, financiers, humains et matériels des entreprises."""

debouches = "Production industrielle, maintenance industrielle, management de projet, qualité industrielle, sécurité et environnement (QSE), logistique et supply chain, organisation et optimisation des processus, gestion des opérations, amélioration continue et lean management, conseil et ingénierie industrielle."

mots_cles = "Génie Industriel, Management Industriel, Amélioration Continue, Lean Manufacturing, Logistique, Supply Chain, Maintenance, Qualité HSE, Production, Optimisation des performances, Ingénierie des systèmes, ERP, Gestion de projet."

formation_data = [
    {
        "year": "1ère Année",
        "semesters": [
            {
                "name": "Semestre 1",
                "modules": [
                    {"name": "Conception des systèmes mécaniques", "type": "common"},
                    {"name": "Systèmes de mesure et conception expérimentale", "type": "common"},
                    {"name": "Thermodynamique appliquée et phénomènes de transfert", "type": "common"},
                    {"name": "Calcul des structures", "type": "common"},
                    {"name": "Sciences des matériaux", "type": "common"},
                    {"name": "Langues étrangères", "type": "common"},
                    {"name": "Excel avancé", "type": "common"}
                ]
            },
            {
                "name": "Semestre 2",
                "modules": [
                    {"name": "Machines électriques et électronique de puissance", "type": "common"},
                    {"name": "Procédés de fabrication mécanique", "type": "common"},
                    {"name": "Conception de circuits électroniques", "type": "common"},
                    {"name": "Automatique linéaire", "type": "common"},
                    {"name": "Recherche opérationnelle pour le génie industriel", "type": "common"},
                    {"name": "Compétences artistiques et culturelles", "type": "common"},
                    {"name": "Langues étrangères (anglais /français)", "type": "common"}
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
                    {"name": "Production et stockage de l'énergie", "type": "common"},
                    {"name": "Management de projet et de l'innovation", "type": "common"},
                    {"name": "Statistique décisionnelle", "type": "common"},
                    {"name": "Efficacité énergétique en milieu industriel", "type": "common"},
                    {"name": "Maintenance des systèmes industriels", "type": "common"},
                    {"name": "Intelligence artificielle et ses applications", "type": "common"},
                    {"name": "Langues étrangères", "type": "common"}
                ]
            },
            {
                "name": "Semestre 4",
                "modules": [
                    {"name": "Electricité industrielle et automatisme", "type": "common"},
                    {"name": "Entreprenariat et gestion des entreprises", "type": "common"},
                    {"name": "Management de production", "type": "common"},
                    {"name": "Langues étrangères", "type": "common"},
                    {"name": "Mini projet", "type": "common"},
                    {"name": "Management de projet et entrepreneuriat", "type": "common"},
                    {"name": "Management qualité", "type": "common"}
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
                    {"name": "Industrie 4.0", "type": "common"},
                    {"name": "Lean manufacturing et amélioration des processus", "type": "common"},
                    {"name": "Logistique et suply chain Management", "type": "common"},
                    {"name": "Langues étrangères", "type": "common"},
                    {"name": "Employment skills", "type": "common"},
                    {"name": "Ergonomie et HSE (Hygiène, Sécurité, Environnement)", "type": "common"},
                    {"name": "Supervision des systèmes industriels", "type": "common"}
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
        WHERE code = 'GINDUS'
    """, (description, debouches, mots_cles, formation_json))
    
    conn.commit()
    print("GINDUS filiere updated successfully.")
    conn.close()

if __name__ == "__main__":
    update_db()
