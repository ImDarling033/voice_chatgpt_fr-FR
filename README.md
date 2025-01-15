# VoiceGPT

VoiceGPT est un assistant vocal qui exploite le puissant chatbot ChatGPT pour répondre à vos questions. Vous énoncez les demandes et VoiceGPT répond avec une parole synthétique réaliste.

![](https://raw.githubusercontent.com/nickbild/voice_chatgpt/main/media/voicegpt_title.jpg)

## Comment ça marche

![](https://raw.githubusercontent.com/nickbild/voice_chatgpt/main/media/voicegpt_overview.jpg)

J'ai choisi un ordinateur monocarte Raspberry Pi 4 pour héberger le projet, car il exécute Linux et offre une grande polyvalence. Un [script Python](https://github.com/nickbild/voice_chatgpt/blob/main/voice_chat.py) personnalisé collecte l'audio de la voix d'un orateur à l'aide d'un microphone USB. L'API Google Cloud Speech-to-Text est ensuite utilisée pour convertir ce fichier audio en texte. Le texte est ensuite interrogé sur ChatGPT à l'aide d'une [API non officielle](https://github.com/acheong08/ChatGPT-lite) qui renvoie une chaîne de texte de la réponse de ChatGPT. Cette réponse est ensuite traitée par l'API Text-to-Speech de Google Cloud pour la transformer en parole synthétique réaliste que le Raspberry Pi peut diffuser via un haut-parleur.

Le concept d'assistant vocal est bien établi (par exemple Google Home, Amazon Alexa), mais cette preuve de concept montre comment un assistant vocal peut utiliser ChatGPT, ce qui, à mon avis, offre une expérience bien meilleure que tout ce qui existe actuellement sur le marché.

À l'avenir, j'ajouterai peut-être un algorithme de repérage de mots-clés au projet afin qu'il puisse toujours s'exécuter en arrière-plan, en attendant qu'un mot-clé (par exemple « Hey, ChatGPT ») se réveille. Avant d'avoir la chance de faire quoi que ce soit d'autre, il y aura probablement un produit commercial incluant ChatGPT sur le backend — alors je l'achèterai simplement parce qu'il sera plus petit et meilleur. :)

## Média

[Vidéo de démonstration](https://www.youtube.com/watch?v=ajUCMu7de80)

![](https://raw.githubusercontent.com/nickbild/voice_chatgpt/main/media/voicegpt_sm.jpg)

## Liste des matériaux

- 1 x Raspberry Pi 4
- 1 x microphone USB (j'utilise une webcam avec un microphone intégré)
- 1 x haut-parleur

## À propos de l'auteur

[Nick A. Bild, MS](https://nickbild79.firebaseapp.com/#!/)
