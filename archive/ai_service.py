import os
import json
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

SYSTEM_PROMPT = """Tu es l'assistant IA officiel de l'ENSA Safi, spécialisé dans l'orientation des étudiants du cycle préparatoire (2ème année).
Ton rôle est d'aider les étudiants à choisir leur spécialité parmi les 6 filières d'excellence :
- GIIA : Génie Informatique et Intelligence Artificielle (Développement logiciel, Data Science, IA)
- GINDUS : Génie Industriel (Optimisation de production, Logistique, Qualité)
- GTR : Génie des Télécommunications et Réseaux (5G, Cybersécurité, IoT, Cloud, Systèmes)
- GMSI : Génie Mécatronique et Systèmes Intelligents (Robotique, Systèmes embarqués, Mécanique)
- GATE : Génie Aéronautique et Technologies de l'Espace (Aéronautique, Spatial, Maintenance usinage)
- GPMA : Génie des Procédés et Matériaux Avancés (Chimie industrielle, Matériaux finis, Environnement)

RÈGLES STRICTES :
1. Réponds toujours poliment, de manière empathique, naturelle, et très concise (2 à 3 phrases maximum).
2. N'utilise PAS de formatage Markdown agressif (pas d'étoiles, pas de texte en gras). Garde le texte normal et épuré.
3. Si un étudiant mentionne ses passions ou ses doutes, écoute-le et propose-lui formellement 1 ou 2 filières les plus adaptées en justifiant selon le contexte professionnel.
4. Si la question n'est PAS en rapport avec les études académiques, l'ENSA Safi, ou le choix de filière, recadre aimablement vers le sujet de l'orientation.
5. Utilise 1 emoji maximum par message (ex: 🎓 ou 🚀).
"""

def get_mistral_response(user_message, api_key):
    """
    Sends the user message directly to Mistral AI along with the ENSA Safi context
    and returns a clean, reliable response, handling any connection timeouts.
    """
    if not api_key:
        return "Configuration manquante: clé API Mistral absente."
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "model": "mistral-tiny",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.35, # Slightly low to be deterministic and serious but conversational
        "max_tokens": 300
    }
    
    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        content = data['choices'][0]['message']['content']
        
        # Post-process response to ensure no bold/asterisk markdown creeps into simple UI 
        content = content.replace('**', '').replace('*', '')
        return content.strip()
        
    except requests.exceptions.Timeout:
        logger.error("Mistral API call timed out.")
        return "Le service d'assistance prend trop de temps à répondre. Réessayez dans un instant."
        
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Mistral HTTP error: {http_err}")
        return "Mon service d'IA rencontre un problème temporaire. Veuillez réessayer plus tard."
        
    except Exception as e:
        logger.error(f"Mistral API unexpected error: {e}")
        return "Une erreur technique m'empêche de vous répondre pour le moment."
