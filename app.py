"""
Application Flask pour la prédiction de la CAN 2025
Couleurs officielles CAN 2025: Or (#FFD700), Vert (#006B3F), Rouge (#C1272D)
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'can2025-secret-key'

# Charger le modèle et les données
try:
    MODEL_PATH = 'models/gb_model_can_2025.joblib'
    FEATURES_PATH = 'models/feature_columns.joblib'
    
    gb_model = joblib.load(MODEL_PATH)
    feature_columns = joblib.load(FEATURES_PATH)
    
    # Charger les données historiques
    matches = pd.read_csv('Africa Cup of Nations Matches.csv')
    players = pd.read_csv('Africa Cup of Nations Players.csv')
    champions = pd.read_csv('Champions.csv')
    team_stats = pd.read_csv('General Statistics For each Participated Team.csv')
    
    print("✓ Modèle et données chargés avec succès")
except Exception as e:
    print(f"⚠️ Erreur de chargement: {e}")
    gb_model = None
    feature_columns = []

# Groupes CAN 2025
# Groupes CAN 2025 (Officiels selon l'image)
CAN_2025_GROUPS = {
    'A': ['Maroc', 'Mali', 'Zambie', 'Comores'],
    'B': ['Égypte', 'Afrique du Sud', 'Angola', 'Zimbabwe'],
    'C': ['Nigeria', 'Tunisie', 'Ouganda', 'Tanzanie'],
    'D': ['Sénégal', 'RD Congo', 'Bénin', 'Botswana'],
    'E': ['Algérie', 'Burkina Faso', 'Guinée Équatoriale', 'Soudan'],
    'F': ['Côte d\'Ivoire', 'Cameroun', 'Gabon', 'Mozambique']
}

# ==================== FONCTIONS UTILITAIRES ====================

def get_default_stats():
    """Retourne les stats par défaut"""
    return {
        'goals_mean': 1.2,
        'goals_mean_l5': 1.2,
        'goals_suf_mean': 1.2,
        'goals_suf_mean_l5': 1.2,
        'game_points_mean': 1.5,
        'game_points_mean_l5': 1.5
    }

def get_team_stats_safe(team_name):
    """Récupère les stats d'une équipe en toute sécurité"""
    try:
        team_stats_clean = team_stats.copy()
        team_stats_clean.columns = team_stats_clean.columns.str.strip()
        
        if 'Team' not in team_stats_clean.columns:
            return get_default_stats()
        
        # Nettoyer le nom de l'équipe
        team_name_clean = team_name.strip()
        
        team_data = team_stats_clean[
            team_stats_clean['Team'].str.strip() == team_name_clean
        ]
        
        if len(team_data) == 0:
            return get_default_stats()
        
        row = team_data.iloc[0]
        pld = float(row.get('Pld', 1))
        
        return {
            'goals_mean': float(row.get('GF', 1.2)) / pld,
            'goals_mean_l5': float(row.get('GF', 1.2)) / pld,
            'goals_suf_mean': float(row.get('GA', 1.2)) / pld,
            'goals_suf_mean_l5': float(row.get('GA', 1.2)) / pld,
            'game_points_mean': float(row.get('Pts', 1.5)) / pld,
            'game_points_mean_l5': float(row.get('Pts', 1.5)) / pld
        }
    except Exception as e:
        print(f"Erreur stats {team_name}: {e}")
        return get_default_stats()

def calculate_kpis():
    """Calcule les KPIs principaux"""
    kpis = {}
    
    try:
        # Nettoyer les colonnes
        matches_clean = matches.copy()
        matches_clean.columns = matches_clean.columns.str.strip()
        
        # Total matches
        kpis['total_matches'] = len(matches_clean)
        
        # Moyenne buts par match
        if 'HomeTeamGoals' in matches_clean.columns and 'AwayTeamGoals' in matches_clean.columns:
            valid_matches = matches_clean.dropna(subset=['HomeTeamGoals', 'AwayTeamGoals'])
            
            if len(valid_matches) > 0:
                total_goals = (valid_matches['HomeTeamGoals'].sum() + 
                              valid_matches['AwayTeamGoals'].sum())
                kpis['avg_goals'] = total_goals / len(valid_matches)
                
                # Matchs nuls
                kpis['total_draws'] = len(
                    valid_matches[valid_matches['HomeTeamGoals'] == valid_matches['AwayTeamGoals']]
                )
                
                # Score max
                kpis['highest_score'] = int(max(
                    valid_matches['HomeTeamGoals'].max(),
                    valid_matches['AwayTeamGoals'].max()
                ))
                
                # Taux victoire domicile
                home_wins = len(valid_matches[valid_matches['HomeTeamGoals'] > valid_matches['AwayTeamGoals']])
                kpis['home_win_rate'] = (home_wins / len(valid_matches) * 100)
            else:
                kpis['avg_goals'] = 0
                kpis['total_draws'] = 0
                kpis['highest_score'] = 0
                kpis['home_win_rate'] = 0
        else:
            kpis['avg_goals'] = 0
            kpis['total_draws'] = 0
            kpis['highest_score'] = 0
            kpis['home_win_rate'] = 0
        
        # Moyenne joueurs par match
        if 'Attendance' in matches_clean.columns:
            kpis['avg_players'] = int(matches_clean['Attendance'].mean())
        else:
            kpis['avg_players'] = 22
        
        # Champion le plus titré
        if 'Champion' in champions.columns:
            champion_counts = champions['Champion'].value_counts()
            if len(champion_counts) > 0:
                kpis['top_champion'] = champion_counts.index[0]
                kpis['top_champion_titles'] = int(champion_counts.values[0])
            else:
                kpis['top_champion'] = 'N/A'
                kpis['top_champion_titles'] = 0
        else:
            kpis['top_champion'] = 'N/A'
            kpis['top_champion_titles'] = 0
        
        # Équipes participantes
        team_stats_clean = team_stats.copy()
        team_stats_clean.columns = team_stats_clean.columns.str.strip()
        if 'Team' in team_stats_clean.columns:
            kpis['total_teams'] = len(team_stats_clean)
        else:
            kpis['total_teams'] = 0
        
        # Éditions
        if 'Year' in matches_clean.columns:
            kpis['editions'] = matches_clean['Year'].nunique()
        else:
            kpis['editions'] = 0
        
    except Exception as e:
        print(f"Erreur KPIs: {e}")
        kpis = {
            'total_matches': 0,
            'avg_goals': 0,
            'total_draws': 0,
            'highest_score': 0,
            'home_win_rate': 0,
            'avg_players': 0,
            'top_champion': 'N/A',
            'top_champion_titles': 0,
            'total_teams': 0,
            'editions': 0
        }
    
    return kpis

def predict_match(home_team, away_team, is_group=True):
    """Prédit le résultat d'un match"""
    if gb_model is None or len(feature_columns) == 0:
        return {
            'home_win_prob': 0.5,
            'away_win_prob': 0.5,
            'predicted_winner': home_team,
            'confidence': 0.5
        }
    
    try:
        # Récupérer les stats des équipes
        home_stats = get_team_stats_safe(home_team)
        away_stats = get_team_stats_safe(away_team)
        
        # Créer les features
        features = {
            'goals_dif': home_stats['goals_mean'] - away_stats['goals_mean'],
            'goals_dif_l5': home_stats['goals_mean_l5'] - away_stats['goals_mean_l5'],
            'goals_suf_dif': home_stats['goals_suf_mean'] - away_stats['goals_suf_mean'],
            'goals_suf_dif_l5': home_stats['goals_suf_mean_l5'] - away_stats['goals_suf_mean_l5'],
            'game_points_dif': home_stats['game_points_mean'] - away_stats['game_points_mean'],
            'game_points_dif_l5': home_stats['game_points_mean_l5'] - away_stats['game_points_mean_l5'],
            'is_group_stage': 1 if is_group else 0
        }
        
        X_pred = pd.DataFrame([features])[feature_columns]
        
        # Prédiction
        proba = gb_model.predict_proba(X_pred.values)[0]
        
        # proba[0] = victoire home (0)
        # proba[1] = victoire away (1)
        
        # Ajouter un facteur d'avantage domicile réaliste (5%)
        home_boost = 1.05
        adjusted_home = proba[0] * home_boost
        adjusted_away = proba[1]
        total = adjusted_home + adjusted_away
        
        # Normaliser
        adjusted_home = adjusted_home / total
        adjusted_away = adjusted_away / total
        
        predicted_winner = home_team if adjusted_home > adjusted_away else away_team
        confidence = max(adjusted_home, adjusted_away)
        
        return {
            'home_win_prob': float(adjusted_home),
            'away_win_prob': float(adjusted_away),
            'predicted_winner': predicted_winner,
            'confidence': float(confidence)
        }
    except Exception as e:
        print(f"Erreur prédiction: {e}")
        return {
            'home_win_prob': 0.5,
            'away_win_prob': 0.5,
            'predicted_winner': home_team,
            'confidence': 0.5
        }

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Page d'accueil avec dashboard"""
    return render_template('index.html')

@app.route('/predict')
def predict_page():
    """Page de prédiction"""
    return render_template('predict.html', groups=CAN_2025_GROUPS)

# ==================== API ENDPOINTS ====================
@app.route('/simulate')
def simulate_page():
    """Page de simulation du tournoi complet"""
    return render_template('simulate.html', groups=CAN_2025_GROUPS)

@app.route('/api/kpis')
def get_kpis():
    """API pour récupérer les KPIs"""
    kpis = calculate_kpis()
    return jsonify(kpis)

@app.route('/api/champions')
def get_champions():
    """API pour l'historique des champions"""
    try:
        champions_clean = champions.copy()
        champions_clean.columns = champions_clean.columns.str.strip()
        
        if 'Year' in champions_clean.columns and 'Champion' in champions_clean.columns:
            data = champions_clean[['Year', 'Champion']].to_dict('records')
        else:
            data = []
    except:
        data = []
    
    return jsonify(data)

@app.route('/api/team_stats')
def get_all_team_stats():
    """API pour les statistiques des équipes"""
    try:
        team_stats_clean = team_stats.copy()
        team_stats_clean.columns = team_stats_clean.columns.str.strip()
        
        # Sélectionner les colonnes importantes
        important_cols = ['Rank', 'Team', 'Pld', 'W', 'D', 'L', 'GF', 'GA', 'Pts']
        available_cols = [col for col in important_cols if col in team_stats_clean.columns]
        
        if available_cols:
            data = team_stats_clean[available_cols].head(15).to_dict('records')
        else:
            data = []
    except:
        data = []
    
    return jsonify(data)

@app.route('/api/groups')
def get_groups():
    """API pour les groupes CAN 2025"""
    return jsonify(CAN_2025_GROUPS)

@app.route('/api/goals_distribution')
def goals_distribution():
    """Distribution des buts marqués"""
    try:
        matches_clean = matches.copy()
        matches_clean.columns = matches_clean.columns.str.strip()
        
        if 'HomeTeamGoals' in matches_clean.columns and 'AwayTeamGoals' in matches_clean.columns:
            valid_matches = matches_clean.dropna(subset=['HomeTeamGoals', 'AwayTeamGoals'])
            all_goals = pd.concat([
                valid_matches['HomeTeamGoals'],
                valid_matches['AwayTeamGoals']
            ])
            distribution = all_goals.value_counts().sort_index().to_dict()
            return jsonify(distribution)
    except:
        pass
    
    return jsonify({})

@app.route('/api/predict', methods=['POST'])
def predict():
    """API pour prédire un match"""
    try:
        data = request.json
        home = data.get('home_team')
        away = data.get('away_team')
        is_group = data.get('is_group', True)
        
        if not home or not away:
            return jsonify({'error': 'Équipes manquantes'}), 400
        
        prediction = predict_match(home, away, is_group)
        
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== LANCEMENT ====================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)