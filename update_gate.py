import sqlite3
import json

DB_PATH = 'ensa_orientation.db'

# Content extracted from the GATE image
description = """L’écosystème aéronautique marocain représente l’un des plus beaux cas de réussite industrielle dans un pays en développement avec un important besoin en ingénieurs diplômés. Ainsi le Maroc est devenu un important acteur dans ce secteur industriel. Avec la présence des leaders du secteur aéronautique sur son sol, tels que Bombardier, EADS, Boeing, Safran, Thalès, le Maroc a fait du secteur aéronautique un des plus importants dans son Plan d’accélération industriel 2014-2020. Le métier d’ingénieur aéronautique fait appel à des qualifications issues de multiples disciplines : physique, matériaux, informatique, mécanique, hydraulique, pneumatique, électronique, armement…Il travaille donc en équipe multidisciplinaire et internationalisée( anglais requis). Notre filière de spécialisation met la théorie en pratique de façon équilibrée et mène à un diplôme d’ingénierie en techniques aéronautique et aérospatiale, en Techniques de maintenance d'aéronefs ou en Techniques d'avionique, en plus, la formation est dotée de reconnaissance des codes et des normes de l'aviation civile nationales, européennes et de l'UAE. Par ailleurs Notre diplôme offre la possibilité à ses étudiants de passer les examens PART-66 de l’Agence européenne de sécurité aérienne (EASA) afin d’obtenir une licence de maintenance d’aéronefs (LMA) européenne en collaboration avec le NOVAe Aerospace. Cette filière est bien appuyée par des professionnels du domaines aéronautiques et spatiales à l’échelle nationale (CE3M, GIMAS…) et aussi internationale (NOVAE ,HCT …). Et dans son opérationnalisation plusieurs intervenants du monde de l’industrie vont animer et assister les apprentissages aux futures ingénieurs."""

debouches = "ingénieur aéronautique, ingénieur interface client aéronautique, ingénieur études aéronautiques, consultant aerospace, ingénieur systèmes aéronautiques, ingénieur logiciel embarqué aéronautique, ingénieur assistance technique."

mots_cles = "Aéronautique, Technologies spatiales, maintenance aéronautique, manufacturing aéronautique, smart-manufacturing."

formation_data = [
    {
        "year": "1ère Année",
        "semesters": [
            {
                "name": "Semestre 1",
                "modules": [
                    {"name": "Structures des avions, Technologies des aéronefs", "type": "common"},
                    {"name": "Fonctions électroniques", "type": "common"},
                    {"name": "Mécanique des fluides appliquée", "type": "common"},
                    {"name": "Matériaux plastiques et composites", "type": "common"},
                    {"name": "Thermopropulsion", "type": "common"},
                    {"name": "Langues étrangères 1 (Anglais/Français)", "type": "common"},
                    {"name": "Algorithmique et Programmation en Python", "type": "common"}
                ]
            },
            {
                "name": "Semestre 2",
                "modules": [
                    {"name": "Conception aéronautique et Design Industriel", "type": "common"},
                    {"name": "Systèmes embarqués 1", "type": "common"},
                    {"name": "Système d'information", "type": "common"},
                    {"name": "Programmation pour l'ingénieur", "type": "common"},
                    {"name": "Analyse numérique / Equations Différentielles", "type": "common"},
                    {"name": "Langues étrangères 2 (Anglais/Français)", "type": "common"},
                    {"name": "Culture and Art Skills", "type": "common"}
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
                    {"name": "Commande des systèmes électriques des aéronefs", "type": "common"},
                    {"name": "Systèmes embarqués II", "type": "common"},
                    {"name": "Technologie des hélices", "type": "common"},
                    {"name": "Mécanique du vol et aérodynamique appliquée", "type": "common"},
                    {"name": "Technologies propulseurs et Moteurs à piston", "type": "common"},
                    {"name": "Langues étrangères 3 (Anglais/Français)", "type": "common"},
                    {"name": "Intelligence Artificielle et ses Applications", "type": "common"}
                ]
            },
            {
                "name": "Semestre 4",
                "modules": [
                    {"name": "Hydraulique, Pneumatique / Météorologie aéronautique", "type": "common"},
                    {"name": "Calcul des structures en aéronautique", "type": "common"},
                    {"name": "CFAO et Machines Outils à commande", "type": "common"},
                    {"name": "Lean six sigma et Manufacturing", "type": "common"},
                    {"name": "Recherche opérationnelle, Optimisation et Modélisation", "type": "common"},
                    {"name": "Langues étrangères 4 (Anglais/Français)", "type": "common"},
                    {"name": "Management de projet et Entrepre- nariat", "type": "common"}
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
                    {"name": "Management Organisationnel et Management de Projets Complexes", "type": "common"},
                    {"name": "Smart manufacturing : Industrie 4.0", "type": "common"},
                    {"name": "Logistique Industrielle", "type": "common"},
                    {"name": "Aircraft Maintenance Practices", "type": "common"},
                    {"name": "Qualité, Sécurité et Environnement et réglementation aéronautique", "type": "common"},
                    {"name": "Langues étrangères 5 (Anglais/Français)", "type": "common"},
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
        WHERE code = 'GATE'
    """, (description, debouches, mots_cles, formation_json))
    
    conn.commit()
    print("GATE filiere updated successfully.")
    conn.close()

if __name__ == "__main__":
    update_db()
