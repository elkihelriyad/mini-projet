import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json
import logging
import re

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleChatbot:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.vectorizer = TfidfVectorizer()
        # Knowledge Base: (Question/Pattern, Answer)
        self.knowledge_base = [
            ("Bonjour salut coucou", "Bonjour ! Je suis l'assistant virtuel de l'ENSA Safi. Comment puis-je vous aider dans votre orientation ?"),
            ("C'est quoi GIIA ?", "GIIA signifie Génie Informatique et Intelligence Artificielle. C'est une filière axée sur le développement logiciel, la Data Science et l'IA."),
            ("Quels sont les débouchés de GIIA ?", "Les lauréats GIIA deviennent souvent Développeurs Fullstack, Data Scientists, ou Ingénieurs DevOps."),
            ("C'est quoi GTR ?", "GTR (Génie Réseaux et Télécoms) forme des experts en 5G, cybersécurité, IoT et administration des réseaux."),
            ("Débouchés GTR ?", "Ingénieur Réseaux, Consultant Cybersécurité, Architecte Cloud."),
            ("C'est quoi GINDUS ?", "GINDUS (Génie Industriel) se concentre sur l'optimisation de la production, la logistique et la qualité."),
            ("C'est quoi GMSI ?", "GMSI (Génie Mécatronique et Systèmes Intelligents) combine mécanique, électronique et informatique pour la robotique et les systèmes embarqués."),
            ("C'est quoi GATE ?", "GATE (Génie Aéronautique) est dédié aux technologies de l'espace et à la maintenance aéronautique."),
            ("C'est quoi GPMA ?", "GPMA (Génie des Procédés et Matériaux Avancés) concerne la chimie industrielle, l'environnement et l'étude des matériaux."),
            ("Comment choisir ma filière ?", "Vous pouvez passer notre test d'orientation intelligent via le menu 'Faire le Test' !"),
            ("Combien de temps dure la formation ?", "Le cycle ingénieur dure 3 ans après les 2 années préparatoires."),
            ("Merci", "Je vous en prie ! Bon courage pour votre orientation.")
        ]
        
        self.questions = [q for q, a in self.knowledge_base]
        self.answers = [a for q, a in self.knowledge_base]
        
        # Train TF-IDF on startup
        self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)
        
        self.greetings = ['bonjour', 'salut', 'coucou', 'salam', 'selem', 'slm', 'hello', 'hi', 'hey', 'yo', 'salam alaykoum']
        # Vague inputs list
        self.vague_inputs = ['oui', 'non', 'ok', 'd\'accord', 'yep', 'no', 'yes', 'cool', 'super']
        
        # Synonym Mapping for Query Expansion
        self.synonyms = {
            'génie info': 'GIIA', 'informatique': 'GIIA', 'ia': 'GIIA', 'dev': 'GIIA', 'développement': 'GIIA', 'info': 'GIIA',
            'réseaux': 'GTR', 'télécom': 'GTR', 'cybersécurité': 'GTR', '5g': 'GTR',
            'industriel': 'GINDUS', 'logistique': 'GINDUS', 'qualité': 'GINDUS',
            'mécanique': 'GMSI', 'électronique': 'GMSI', 'robotique': 'GMSI', 'systèmes embarqués': 'GMSI',
            'chimie': 'GPMA', 'matériaux': 'GPMA', 'procédés': 'GPMA',
            'aéronautique': 'GATE', 'espace': 'GATE', 'avion': 'GATE'
        }

    def expand_query(self, user_input):
        """Expands user input with relevant major codes to improve TF-IDF retrieval."""
        expanded_input = user_input.lower()
        for keyword, code in self.synonyms.items():
            if keyword in expanded_input:
                expanded_input += f" {code}"
        return expanded_input

    def retrieve(self, user_input, top_k=5, threshold=0.05):
        """Retrieve top_k relevant Q/A pairs using Cosine Similarity on expanded query."""
        expanded_query = self.expand_query(user_input)
        user_vec = self.vectorizer.transform([expanded_query])
        similarities = cosine_similarity(user_vec, self.tfidf_matrix).flatten()
        
        # Get indices of top_k results
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            score = similarities[idx]
            if score >= threshold:
                results.append({
                    "question": self.questions[idx],
                    "answer": self.answers[idx],
                    "score": float(score)
                })
        
        return results

    def generate_with_mistral(self, user_input, retrieved_items):
        """Generates a response using Mistral API based on retrieved context."""
        if not self.api_key:
            return "Erreur de configuration : Clé API Mistral manquante."

        # Build Context
        context_str = "\n".join([f"Q: {item['question']}\nR: {item['answer']}" for item in retrieved_items])
        
        # Advanced Persona System Prompt
        system_prompt = (
            "Tu es un assistant IA d'orientation universitaire pour l'ENSA Safi. "
            "Ton rôle est d'aider les étudiants à comprendre les filières, l'orientation et la vie académique. "
            "Ton ton est SÉRIEUX, CALME et NATUREL. "
            
            "\n\nAnalysez l'intention de l'utilisateur et adaptez ta réponse selon ces catégories :"
            "\n1. ENSA_INFO (Filières/École) : Donne un résumé clair (c'est quoi, modules, débouchés). "
            "Si l'info est absente, dis-le et propose une alternative."
            "\n2. ORIENTATION (Choix) : Pose 2-3 questions simples pour cerner le profil, puis propose 1-2 filières avec justification. Ne force jamais le choix."
            "\n3. OFF_TOPIC (Hors sujet) : Réponds calmement et redirige vers un sujet académique pertinent (ambiance, projets, débouchés)."
            "\n4. AMBIGUOUS (Vague) : Demande une clarification actionnable avec 2 exemples concrets."

            "\n\nRÈGLES DE FORMAT :"
            "\n- Langue : Français."
            "\n- TEXTE SIMPLE UNIQUEMENT : PAS DE MARKDOWN (ni **, ni *, ni listes à tirets)."
            "\n- 0 à 2 Emojis maximum (si pertinent)."
            "\n- Ne JAMAIS afficher de section 'Sources' ou de scores."
            "\n- Limite : 1 seule question de suivi maximum."
            "\n- EMOJIS : Utilise UNIQUEMENT des emojis sobres et professionnels (🙂 🎓 🤝). Règle STRICTE : 1 emoji MAXIMUM par message, toujours à la fin d'une phrase."
            
            "\n\nRÈGLE ANTI-HALLUCINATION ABSOLUE :"
            "\nSi l'information demandée n'est PAS dans le CONTEXTE ci-dessous, réponds : "
            "'Je n'ai pas cette information dans les données disponibles. Tu peux préciser ta question ou contacter l'administration de l'ENSA Safi.'"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"CONTEXTE:\n{context_str}\n\nMESSAGE UTILISATEUR: {user_input}"}
        ]

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            payload = {
                "model": "mistral-tiny", 
                "messages": messages,
                "temperature": 0.3, # Lower temperature for more consistent/serious tone
                "max_tokens": 450
            }
            
            response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            # Post-processing to enforce rules
            content = content.replace('**', '').replace('*', '') # Remove Markdown
            
            lines = content.split('\n')
            clean_lines = [l for l in lines if not l.lower().strip().startswith('sources:')]
            content = "\n".join(clean_lines).strip()
            
            return content

        except Exception as e:
            logger.error(f"Mistral API Error: {e}")
            return "Une erreur technique est survenue. Veuillez reformuler votre demande."

    def get_response(self, user_input):
        clean_input = user_input.strip().lower()
        
        # 1. Check Greetings (Local & Fast) - Category 1 handling
        is_greeting = any(clean_input == g or clean_input.startswith(g + ' ') for g in self.greetings)
        
        if is_greeting:
            return (
                "Bonjour 🙂\n"
                "Je peux t'aider sur :\n"
                "• une filière (ex : “C'est quoi GIIA ?”)\n"
                "• l'orientation (ex : “Quelle filière me correspond ?”)\n"
                "Écris simplement ta question."
            )

        # 2. Check Vague Inputs
        if clean_input in self.vague_inputs:
            return (
                "D'accord 🙂\n"
                "Dis-moi simplement ce que tu veux savoir, par exemple :\n"
                "“Débouchés GTR” ou “Comment choisir ma filière ?”"
            )

        # 3. Retrieve Context (Use Expanded Query)
        retrieved = self.retrieve(clean_input, top_k=5, threshold=0.1)
        
        # 4. Fallback (No Context)
        if not retrieved:
             return "Je n'ai pas cette information dans les données disponibles. Tu peux préciser ta question ou contacter l'administration de l'ENSA Safi."
        
        # 5. Generate with Mistral
        if self.api_key:
            return self.generate_with_mistral(user_input, retrieved)
        
        # 6. Fallback (No API Key)
        return retrieved[0]['answer']
