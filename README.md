# 🏆 CAN 2025 - Système de Prédiction ML

![CAN 2025](https://img.shields.io/badge/CAN-2025-gold?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=for-the-badge&logo=flask)
![ML](https://img.shields.io/badge/ML-Gradient_Boosting-red?style=for-the-badge)

Application web de prédiction et simulation pour la Coupe d'Afrique des Nations 2025 utilisant le Machine Learning.

---

## 📋 Table des matières

- [Aperçu](#-aperçu)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies](#-technologies)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Modèle ML](#-modèle-ml)
- [API Endpoints](#-api-endpoints)
- [Screenshots](#-screenshots)
- [Contribuer](#-contribuer)
- [Licence](#-licence)

---

## 🎯 Aperçu

Ce projet utilise l'intelligence artificielle pour prédire les résultats des matchs de la CAN 2025. Il s'appuie sur des données historiques de toutes les éditions précédentes de la Coupe d'Afrique des Nations pour entraîner un modèle de **Gradient Boosting** capable de prédire avec précision les résultats des matchs.

### 🌟 Points forts

- ✅ **Modèle ML entraîné** sur l'historique complet de la CAN
- ✅ **Dashboard interactif** avec statistiques et graphiques
- ✅ **Simulation match par match** avec animations
- ✅ **Simulation complète du tournoi** (phase de groupes → finale)
- ✅ **Interface moderne** avec design aux couleurs de la CAN (Or, Vert, Rouge)
- ✅ **API REST** pour intégration externe

---

## 🚀 Fonctionnalités

### 1. 📊 Dashboard Statistiques
- **KPIs principaux** : Total matchs, éditions, moyenne de buts, équipes
- **Graphiques interactifs** :
  - Historique des champions
  - Distribution des buts
  - Top 15 équipes
- **Groupes CAN 2025** avec composition officielle
- **Statistiques détaillées** par équipe

### 2. ⚽ Simulation Match par Match
- Sélection de 2 équipes
- Choix de la phase (Groupes / Élimination)
- **Animation du match** en temps réel
- Affichage des **probabilités de victoire**
- **Historique** des matchs simulés
- Confiance du modèle en pourcentage

### 3. 🏆 Simulation Tournoi Complet
- **Phase de groupes** : 36 matchs (6 groupes × 6 matchs)
- Calcul automatique des **classements**
- **Qualification** : 16 équipes (12 + 4 meilleurs 3èmes)
- **Phases à élimination** :
  - Huitièmes de finale (16 → 8)
  - Quarts de finale (8 → 4)
  - Demi-finales (4 → 2)
  - Finale (2 → 1 champion)
- Révélation spectaculaire du **champion**

---

## 🛠 Technologies

### Backend
- **Python 3.8+**
- **Flask 2.0+** - Framework web
- **Pandas** - Manipulation de données
- **NumPy** - Calculs numériques
- **Scikit-learn** - Machine Learning
  - Gradient Boosting Classifier
  - GridSearchCV pour optimisation
- **Joblib** - Sauvegarde du modèle

### Frontend
- **HTML5 / CSS3**
- **JavaScript ES6+**
- **Bootstrap 5** - Framework CSS
- **Chart.js** - Graphiques interactifs
- **Font Awesome** - Icônes

### Données
- Historique complet de la CAN
- 4 datasets CSV :
  - Matchs (dates, scores, équipes)
  - Joueurs
  - Champions
  - Statistiques des équipes

---

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/Maaly22240/SBI-Challenge.git
cd can-2025-prediction
```

2. **Créer un environnement virtuel** (recommandé)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Vérifier la structure des fichiers**
```
SBI CHALLENGE/
├── models/
│   ├── gb_model_can_2025.joblib
│   └── feature_columns.joblib
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── predict.html
│   └── simulate.html
├── static/
├── *.csv (fichiers de données)
└── app.py
```

5. **Lancer l'application**
```bash
python app.py
```

6. **Ouvrir dans le navigateur**
```
http://localhost:5000
```

---

## 📖 Utilisation

### Dashboard
1. Accédez à la page d'accueil
2. Consultez les KPIs et statistiques
3. Explorez les graphiques interactifs
4. Visualisez les groupes de la CAN 2025

### Simulation Match par Match
1. Cliquez sur **"Match par Match"** dans le menu
2. Sélectionnez la phase (Groupes ou Élimination)
3. Choisissez l'équipe domicile
4. Choisissez l'équipe extérieur
5. Cliquez sur **"Lancer la Simulation"**
6. Observez l'animation et les résultats

### Simulation Tournoi Complet
1. Cliquez sur **"Tournoi Complet"** dans le menu
2. Cliquez sur **"Simuler le Tournoi Complet"**
3. Patientez pendant la simulation automatique
4. Suivez la progression :
   - Phase de groupes
   - Huitièmes de finale
   - Quarts de finale
   - Demi-finales
   - Finale
5. Découvrez le champion prédit !

---

## 📁 Structure du projet

```
SBI CHALLENGE/
│
├── 📂 models/                          # Modèles ML entraînés
│   ├── gb_model_can_2025.joblib       # Modèle Gradient Boosting
│   └── feature_columns.joblib         # Colonnes des features
│
├── 📂 templates/                       # Templates HTML
│   ├── base.html                      # Template de base
│   ├── index.html                     # Dashboard
│   ├── predict.html                   # Simulation match par match
│   └── simulate.html                  # Simulation tournoi complet
│
├── 📂 static/                          # Fichiers statiques (si nécessaire)
│
├── 📄 Africa Cup of Nations Matches.csv           # Historique des matchs
├── 📄 Africa Cup of Nations Players.csv           # Données des joueurs
├── 📄 Champions.csv                               # Liste des champions
├── 📄 General Statistics For each Participated Team.csv  # Stats équipes
├── 📄 General Statistics For each Tournaments.csv        # Stats tournois
│
├── 📓 CAN 2025.ipynb                   # Notebook d'entraînement ML
├── 🐍 app.py                           # Application Flask principale
├── 📋 requirements.txt                 # Dépendances Python
└── 📖 README.md                        # Ce fichier
```

---

## 🤖 Modèle ML

### Architecture
Le modèle utilise **Gradient Boosting Classifier** de Scikit-learn, optimisé via **GridSearchCV**.

### Features utilisées
```python
features = [
    'goals_dif',           # Différence de buts marqués (moyenne)
    'goals_dif_l5',        # Différence de buts (5 derniers matchs)
    'goals_suf_dif',       # Différence de buts encaissés (moyenne)
    'goals_suf_dif_l5',    # Différence de buts encaissés (5 derniers)
    'game_points_dif',     # Différence de points (moyenne)
    'game_points_dif_l5',  # Différence de points (5 derniers)
    'is_group_stage'       # Indicateur phase de groupes
]
```

### Target
```python
target = 'result'
# 0 = Victoire domicile
# 1 = Victoire extérieur
# 2 = Match nul (converti en victoire domicile)
```

### Performance
- **Accuracy** : ~70-75% sur le test set
- **AUC-ROC** : ~0.75-0.80
- **Validation croisée** : 5-fold CV

### Entraînement
Le notebook `CAN 2025.ipynb` contient :
1. Chargement et nettoyage des données
2. Feature engineering
3. Entraînement avec GridSearchCV
4. Évaluation (confusion matrix, ROC curve)
5. Sauvegarde du modèle

---

## 🔌 API Endpoints

### Endpoints disponibles

#### **GET /**
- Page d'accueil (Dashboard)

#### **GET /predict**
- Page de simulation match par match

#### **GET /simulate**
- Page de simulation tournoi complet

#### **GET /api/kpis**
- Récupère les KPIs principaux
- **Response** : JSON
```json
{
  "total_matches": 826,
  "editions": 34,
  "avg_goals": 2.42,
  "total_teams": 54,
  "top_champion": "Égypte",
  "top_champion_titles": 7,
  "total_draws": 189,
  "highest_score": 6,
  "avg_players": 22,
  "home_win_rate": 45.2
}
```

#### **GET /api/champions**
- Récupère l'historique des champions
- **Response** : JSON (liste)

#### **GET /api/team_stats**
- Récupère les statistiques des 15 meilleures équipes
- **Response** : JSON (liste)

#### **GET /api/groups**
- Récupère les groupes de la CAN 2025
- **Response** : JSON (objet)

#### **GET /api/goals_distribution**
- Distribution des buts marqués
- **Response** : JSON (objet)

#### **POST /api/predict**
- Prédit le résultat d'un match
- **Body** :
```json
{
  "home_team": "Maroc",
  "away_team": "Égypte",
  "is_group": true
}
```
- **Response** :
```json
{
  "home_win_prob": 0.65,
  "away_win_prob": 0.35,
  "predicted_winner": "Maroc",
  "confidence": 0.65
}
```

---

## 📸 Screenshots

### Dashboard
<img width="587" height="372" alt="image" src="https://github.com/user-attachments/assets/4479d002-a25f-4ed3-902f-d955aaafc2bd" />
<img width="573" height="379" alt="image" src="https://github.com/user-attachments/assets/1a6ed039-9de4-4914-b9e8-8de87de901d7" />

### Simulation Match par Match
<img width="551" height="390" alt="image" src="https://github.com/user-attachments/assets/ab4e6926-1b0d-4cdf-b4b7-45b3b41a9835" />

### Simulation Tournoi
<img width="559" height="254" alt="image" src="https://github.com/user-attachments/assets/e3ee0404-a92a-4e36-953d-0a6163398c07" />

---



## 📞 Contact

**Auteur** : Moulay El Hassen Maasly 

**Email** : moulayelymaaly@gmail.com 

**GitHub** : [@Maaly22240](https://github.com/Maaly22240)  

**LinkedIn** : [linkedin](https://www.linkedin.com/in/maaly-moulay-el-hassan-65552a27b/)

---





## 🎉 CAN 2025

**Dates** : 21 décembre 2025 - 18 janvier 2026  
**Lieu** : Maroc 🇲🇦  
**Équipes** : 24 équipes participantes  
**Format** : 6 groupes de 4 → 16 qualifiés → Phase finale  

---

<div align="center">

### ⚽ Que le meilleur gagne ! 🏆

**Made with ❤️ for African Football**


</div>


