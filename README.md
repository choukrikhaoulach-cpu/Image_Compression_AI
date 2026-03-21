 Compression d’Images Intelligente (IA Multi-Agents)


Illustration : Image avant et après compression

- Description du Projet

Ce projet est une application web intelligente pour la compression d’images, développée avec Python et Streamlit, utilisant un système de multi-agents IA. L’objectif est d’optimiser automatiquement la taille des images tout en préservant leur qualité, à l’aide d’une combinaison de techniques d’analyse, de décision et de compression.

Le système intègre plusieurs agents spécialisés :

Analyseur : extrait les caractéristiques de l’image (taille, couleur, complexité, etc.).
Décisionnaire LLM : prend la décision de la méthode de compression optimale en fonction des caractéristiques de l’image.
Compresseur multi-formats : teste différents formats et niveaux de compression (JPEG, WEBP, PNG) pour choisir celui qui minimise la taille.
Évaluateur : calcule les métriques de qualité (PSNR, SSIM, MSE) pour vérifier que l’image compressée reste visuellement satisfaisante.

Ce projet est destiné à être utilisé par des étudiants, chercheurs ou développeurs souhaitant réduire la taille des images sans perte significative de qualité, et fournit en parallèle un rapport global sur les performances de compression.

⚙️ Fonctionnalités
Upload d’une image depuis l’interface web.
Redimensionnement automatique si l’image est trop large (> 1280 px).
Compression multi-format avec choix automatique du format le plus léger :
JPEG (qualité 85 et 40)
WEBP (qualité 60)
PNG
Calcul automatique des métriques de qualité :
PSNR (Peak Signal-to-Noise Ratio)
SSIM (Structural Similarity Index)
MSE (Mean Squared Error)
Affichage de la taille originale et compressée.
Téléchargement de l’image compressée.
Rapport global JSON généré automatiquement (global_report.json) avec toutes les informations d’analyse, décision IA, compression et métriques.
Barre de progression dynamique pour indiquer l’avancement de chaque agent IA.


🖥️ Technologies et Librairies Utilisées
Python 3.10+
Streamlit – Interface web interactive
Pillow (PIL) – Traitement d’images
NumPy – Manipulation matricielle
scikit-image – Calcul des métriques d’images (PSNR, SSIM)
Git – Gestion de version
Agents IA personnalisés pour l’orchestration et la décision intelligente


📂 Structure du Projet

compression_web_app/
│

├── app.py                  # Script principal Streamlit

├── agents/

│   └── orchestrator.py     # Orchestrateur multi-agents (analyse, décision, compression, évaluation)

├── web_results/            # Dossier pour les images originales et compressées

├── global_report.json      # Rapport global généré automatiquement

├── requirements.txt        # Dépendances Python

└── README.md               # Ce fichier


🚀 Instructions d’Installation
Cloner le dépôt GitHub :
git clone https://github.com/KHAOULA_DEV/image-compression-ai.git
cd image-compression-ai
Créer un environnement virtuel (optionnel mais recommandé) :
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux / macOS
Installer les dépendances :
pip install -r requirements.txt
Lancer l’application Streamlit :
streamlit run app.py
Ouvrir le navigateur à l’adresse indiquée (généralement http://localhost:8501).


📝 Utilisation
Cliquer sur Upload une image et sélectionner votre fichier (JPEG, PNG, etc.).
Observer la barre de progression indiquant l’avancement de l’analyse, de la décision IA et de la compression.
Vérifier les résultats :
Image originale vs Image optimisée
PSNR, SSIM, MSE
Taille originale et compressée
Télécharger l’image compressée via le bouton ⬇️ Télécharger.
Le rapport global (global_report.json) contient toutes les données d’analyse et peut être utilisé pour documentation ou évaluation académique.


📊 Exemple de global_report.json
{
  "image_name": "exemple.jpg",
  "features": {
    "width": 1920,
    "height": 1080,
    "mode": "RGB",
    "channels": 3
  },
  "decision": {
    "format": "WEBP",
    "quality": 60
  },
  "metrics": {
    "PSNR": 38.12,
    "SSIM": 0.9623,
    "MSE": 54.7,
    "original_size_kb": 2048,
    "compressed_size_kb": 412
  },
  "status": "success"
}


🌟 Points Forts du Projet
Multi-agents IA : Chaque étape (analyse, décision, compression, évaluation) est modulable et indépendante.
Compression intelligente : Choix automatique du format le plus léger pour l’image uploadée.
Métriques fiables : Évaluation scientifique de la qualité avec PSNR, SSIM et MSE.
Rapport complet : Toutes les étapes sont tracées dans un fichier JSON pour transparence et reproductibilité.
Interface utilisateur moderne : Simple, interactive et adaptée aux grands fichiers.


📌 Notes Importantes
Les images trop volumineuses peuvent prendre quelques minutes à être analysées et compressées, surtout si elles dépassent 5–10 Mo.
Le redimensionnement automatique permet de réduire le temps de traitement et d’améliorer la compression sans perte visible.
Les fichiers PNG peuvent parfois être plus lourds que JPEG ou WEBP selon le contenu de l’image.
📚 Références et Ressources
Streamlit Documentation
Pillow Documentation
scikit-image Metrics
Techniques de compression d’images et mesure de qualité PSNR/SSIM.


-Auteur

Khaoula Choukri – Étudiante en Informatique, FST Mohammedia, Maroc.
GitHub : KHAOULA_DEV
