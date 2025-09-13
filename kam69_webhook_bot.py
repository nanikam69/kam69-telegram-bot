#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot Telegram kam69 - Agent IA intelligent (version Webhook)
Créé pour fournir des réponses intelligentes et utiles aux utilisateurs
"""

import logging
import os
import asyncio
from typing import Dict, Any
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
import openai

# Configuration du logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration du bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_NAME = "kam69"

# Configuration OpenAI (utilise les variables d'environnement déjà configurées)
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

# Initialisation de l'application Flask
app = Flask(__name__)

class Kam69Bot:
    """Classe principale du bot Telegram kam69"""
    
    def __init__(self):
        self.application = None
        self.user_contexts: Dict[int, list] = {}
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Commande /start - Accueil du bot"""
        user = update.effective_user
        welcome_message = f"""
🤖 Salut {user.first_name} ! Je suis **kam69**, votre agent IA personnel !

Je peux vous aider avec :
• 💬 Conversations intelligentes
• 📚 Réponses à vos questions
• 🔍 Recherche d'informations
• 💡 Conseils et suggestions
• 🎯 Résolution de problèmes

Tapez simplement votre message et je vous répondrai !

Commandes disponibles :
/help - Afficher l'aide
/clear - Effacer l'historique de conversation
/info - Informations sur le bot
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
        # Initialiser le contexte utilisateur
        user_id = update.effective_user.id
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = []
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Commande /help - Aide du bot"""
        help_text = """
🆘 **Aide - kam69 Bot**

**Commandes disponibles :**
/start - Démarrer le bot
/help - Afficher cette aide
/clear - Effacer votre historique de conversation
/info - Informations sur le bot

**Comment utiliser le bot :**
1. Envoyez-moi simplement un message
2. Je vous répondrai avec intelligence
3. Je garde en mémoire notre conversation
4. Utilisez /clear pour recommencer à zéro

**Exemples de questions :**
• "Explique-moi la photosynthèse"
• "Comment cuisiner des pâtes parfaites ?"
• "Aide-moi à résoudre ce problème de maths"
• "Raconte-moi une blague"

Je suis là pour vous aider ! 🚀
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Commande /info - Informations sur le bot"""
        info_text = """
ℹ️ **Informations - kam69 Bot**

**Nom :** kam69
**Type :** Agent IA intelligent
**Version :** 1.0.0
**Créé :** 2025

**Fonctionnalités :**
• Intelligence artificielle avancée
• Mémoire de conversation
• Réponses contextuelles
• Support multilingue
• Disponible 24/7

**Technologie :**
• Python + python-telegram-bot
• OpenAI GPT
• Hébergement cloud

Développé avec ❤️ pour vous offrir la meilleure expérience !
        """
        
        await update.message.reply_text(info_text, parse_mode='Markdown')
    
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Commande /clear - Effacer l'historique"""
        user_id = update.effective_user.id
        self.user_contexts[user_id] = []
        
        await update.message.reply_text(
            "🗑️ Historique de conversation effacé ! Nous repartons à zéro.",
            parse_mode='Markdown'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Gestionnaire principal des messages"""
        try:
            user_id = update.effective_user.id
            user_message = update.message.text
            
            # Initialiser le contexte si nécessaire
            if user_id not in self.user_contexts:
                self.user_contexts[user_id] = []
            
            # Ajouter le message utilisateur au contexte
            self.user_contexts[user_id].append({
                "role": "user",
                "content": user_message
            })
            
            # Limiter l'historique à 20 messages pour éviter les tokens excessifs
            if len(self.user_contexts[user_id]) > 20:
                self.user_contexts[user_id] = self.user_contexts[user_id][-20:]
            
            # Envoyer un indicateur de frappe
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action="typing"
            )
            
            # Générer la réponse IA
            response = await self.generate_ai_response(user_id, user_message)
            
            # Ajouter la réponse au contexte
            self.user_contexts[user_id].append({
                "role": "assistant",
                "content": response
            })
            
            # Envoyer la réponse
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement du message: {e}")
            await update.message.reply_text(
                "❌ Désolé, j'ai rencontré une erreur. Veuillez réessayer."
            )
    
    async def generate_ai_response(self, user_id: int, message: str) -> str:
        """Génère une réponse IA basée sur le contexte de l'utilisateur"""
        try:
            # Préparer les messages pour l'API OpenAI
            messages = [
                {
                    "role": "system",
                    "content": """Tu es kam69, un agent IA intelligent et serviable intégré dans Telegram. \n                    \nTes caractéristiques :\n- Tu es amical, professionnel et utile\n- Tu réponds en français par défaut, sauf si on te demande une autre langue\n- Tu gardes le contexte de la conversation\n- Tu donnes des réponses précises et détaillées\n- Tu peux aider sur tous les sujets : éducation, technologie, vie quotidienne, etc.\n- Tu utilises des emojis avec modération pour rendre tes réponses plus engageantes\n- Tu es respectueux et bienveillant\n\nRéponds de manière naturelle et conversationnelle."""
                }
            ]
            
            # Ajouter l'historique de conversation
            messages.extend(self.user_contexts[user_id])
            
            # Appel à l'API OpenAI
            response = await asyncio.to_thread(
                openai.ChatCompletion.create,
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réponse IA: {e}")
            return "🤖 Je rencontre des difficultés techniques. Pouvez-vous reformuler votre question ?"
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Gestionnaire d'erreurs global"""
        logger.error(f"Exception lors de la mise à jour {update}: {context.error}")
    
    async def setup_bot_commands(self) -> None:
        """Configure les commandes du bot"""
        commands = [
            BotCommand("start", "Démarrer le bot"),
            BotCommand("help", "Afficher l'aide"),
            BotCommand("clear", "Effacer l'historique"),
            BotCommand("info", "Informations sur le bot")
        ]
        
        await self.application.bot.set_my_commands(commands)
    
    def run_webhook(self, webhook_url: str) -> None:
        """Lance le bot en mode webhook"""
        # Créer l'application
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Ajouter les gestionnaires
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("info", self.info_command))
        self.application.add_handler(CommandHandler("clear", self.clear_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Ajouter le gestionnaire d'erreurs
        self.application.add_error_handler(self.error_handler)
        
        # Configuration des commandes
        asyncio.create_task(self.setup_bot_commands())
        
        # Démarrer le bot en mode webhook
        logger.info("🚀 Démarrage du bot kam69 en mode webhook...")
        print("🤖 Bot kam69 démarré avec succès en mode webhook !")
        
        # Configuration du webhook
        self.application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", "8080")),
            url_path="/",
            webhook_url=webhook_url
        )

# Instance du bot
kam69_bot_instance = Kam69Bot()

@app.route("/", methods=["POST"])
async def webhook_handler():
    """Gère les requêtes webhook entrantes"""
    update = Update.de_json(request.get_json(force=True), kam69_bot_instance.application.bot)
    await kam69_bot_instance.application.process_update(update)
    return "ok"

if __name__ == '__main__':
    # Cette partie sera exécutée si le script est lancé directement (pour le développement local)
    # Pour le déploiement, le serveur web (Gunicorn, etc.) appellera l'application Flask
    logger.info("Lancement de l'application Flask...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
