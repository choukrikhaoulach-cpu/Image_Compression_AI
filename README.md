

Compression d'Images Intelligente (IA Multi-Agents)

Application web intelligente pour la compression d'images, développée avec Python et Streamlit, utilisant un système multi-agents IA.

Projet académique - démonstration de compétences en IA appliquée.

Description

Ce projet optimise automatiquement la taille des images tout en préservant leur qualité, à l'aide d'une combinaison de techniques d'analyse, de décision et de compression.

Le système intègre plusieurs agents spécialisés :

Analyseur : extrait les caractéristiques de l'image (taille, couleur, complexité, etc.).

Décisionnaire LLM : prend la décision de la méthode de compression optimale en fonction des caractéristiques de l'image (via OpenAI GPT-4o-mini).

Compresseur multi-formats : teste différents formats et niveaux de compression (JPEG, WEBP, PNG) pour choisir celui qui minimise la taille.

Évaluateur : calcule les métriques de qualité (PSNR, SSIM, MSE) pour vérifier que l'image compressée reste visuellement satisfaisante.

Fonctionnalités

Upload d'une image depuis l'interface web

Redimensionnement automatique si l'image est trop large (plus de 1280 px)

Compression multi-format avec choix automatique du format le plus léger :

JPEG (qualité 85 et 40)

WEBP (qualité 60)

PNG

Calcul automatique des métriques de qualité :

PSNR (Peak Signal-to-Noise Ratio)

SSIM (Structural Similarity Index)

MSE (Mean Squared Error)

Affichage de la taille originale et compressée

Téléchargement de l'image compressée

Rapport global JSON généré automatiquement (global\_report.json)

Barre de progression dynamique pour indiquer l'avancement de chaque agent IA

Stack technique

Python 3.10+

Streamlit - Interface web interactive

Pillow (PIL) - Traitement d'images

NumPy - Manipulation matricielle

scikit-image - Calcul des métriques (PSNR, SSIM)

OpenAI - Décision LLM (GPT-4o-mini)

python-dotenv - Chargement des variables d'environnement

Architecture

text

Image\_Compression\_AI/

├── app.py                    # Interface Streamlit

├── agents/

│   ├── analyse.py            # Agent analyseur (extraction de features)

│   ├── llm\_decision.py       # Agent décisionnaire (OpenAI)

│   ├── orchestrator.py       # Orchestrateur multi-agents

│   └── evaluation.py         # Agent évaluateur (PSNR, SSIM, MSE)

├── dataset/

│   ├── documents/            # Images de test : documents

│   ├── graphiques/           # Images de test : graphiques

│   ├── photos/               # Images de test : photos

│   └── screenshots/          # Images de test : captures d'écran

├── test\_pipeline.py          # Tests du pipeline

├── requirements.txt

├── .env.example

├── .gitignore

└── README.md

Installation

Prérequis

Python 3.10+

Une clé API OpenAI (https://platform.openai.com/api-keys)

Étapes

Cloner le dépôt

text

git clone https://github.com/choukrikhaoulach-cpu/Image\_Compression\_AI.git

cd Image\_Compression\_AI

Créer un environnement virtuel

text

python -m venv venv

venv\\Scripts\\activate       # Windows

source venv/bin/activate    # Linux / macOS

Installer les dépendances

text

pip install -r requirements.txt

Configurer l'environnement

text

copy .env.example .env      # Windows

cp .env.example .env        # macOS / Linux

Puis éditer .env et renseigner ta clé OpenAI.

Lancer l'application

text

streamlit run app.py

L'application s'ouvre dans le navigateur à l'adresse http://localhost:8501.

Utilisation

Cliquer sur Upload une image et sélectionner un fichier (JPEG, PNG, etc.)

Observer la barre de progression indiquant l'avancement de l'analyse, de la décision IA et de la compression

Vérifier les résultats :

Image originale vs Image optimisée

PSNR, SSIM, MSE

Taille originale et compressée

Télécharger l'image compressée via le bouton Télécharger

Le rapport global (global\_report.json) contient toutes les données d'analyse

Variables d'environnement

Variable	Description

OPENAI\_API\_KEY	Clé API OpenAI (obligatoire pour le LLM de décision)

Exemple de rapport généré

json

{

&#x20; "image\_name": "exemple.jpg",

&#x20; "features": {

&#x20;   "width": 1920,

&#x20;   "height": 1080,

&#x20;   "mode": "RGB",

&#x20;   "channels": 3

&#x20; },

&#x20; "decision": {

&#x20;   "format": "WEBP",

&#x20;   "quality": 60

&#x20; },

&#x20; "metrics": {

&#x20;   "PSNR": 38.12,

&#x20;   "SSIM": 0.9623,

&#x20;   "MSE": 54.7,

&#x20;   "original\_size\_kb": 2048,

&#x20;   "compressed\_size\_kb": 412

&#x20; },

&#x20; "status": "success"

}

Points forts

Multi-agents IA : chaque étape (analyse, décision, compression, évaluation) est modulable et indépendante

Compression intelligente : choix automatique du format le plus léger pour l'image uploadée

Métriques fiables : évaluation scientifique de la qualité avec PSNR, SSIM et MSE

Rapport complet : toutes les étapes sont tracées dans un fichier JSON

Interface moderne : simple, interactive et adaptée aux grands fichiers

Auteur

Khaoula Choukri

LinkedIn : https://www.linkedin.com/in/khaoula-choukri

GitHub : https://github.com/choukrikhaoulach-cpu

