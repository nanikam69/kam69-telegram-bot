#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration du bot Telegram kam69
"""

import os

# Configuration du bot Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_NAME = "kam69"

# Configuration OpenAI
OPENAI_API_KEY = os.getenv(\'OPENAI_API_KEY\')
OPENAI_API_BASE = os.getenv(\'OPENAI_API_BASE\')

# Configuration du logging
LOG_LEVEL = "INFO"
LOG_FORMAT = \'%(asctime)s - %(name)s - %(levelname)s - %(message)s\'

# Configuration de l\\\'IA
MAX_CONTEXT_MESSAGES = 20  # Nombre maximum de messages dans l\\\'historique
MAX_TOKENS = 1000  # Nombre maximum de tokens pour les réponses
TEMPERATURE = 0.7  # Créativité de l\\\'IA (0.0 à 1.0)

# Messages système
SYSTEM_PROMPT = """Tu es kam69, un agent IA intelligent et serviable intégré dans Telegram. \n\nTes caractéristiques :\n- Tu es amical, professionnel et utile\n- Tu réponds en français par défaut, sauf si on te demande une autre langue\n- Tu gardes le contexte de la conversation\n- Tu donnes des réponses précises et détaillées\n- Tu peux aider sur tous les sujets : éducation, technologie, vie quotidienne, etc.\n- Tu utilises des emojis avec modération pour rendre tes réponses plus engageantes\n- Tu es respectueux et bienveillant\n\nRéponds de manière naturelle et conversationnelle."""
