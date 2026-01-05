# 📊 Application Web d’Analyse Exploratoire des Données (EDA)

## 1. Présentation générale

Ce projet consiste à concevoir une **application web interactive d’analyse exploratoire des données (Exploratory Data Analysis – EDA)** à l’aide du framework **Streamlit**.
L’application permet à un utilisateur de charger un jeu de données au format CSV, d’en explorer la structure, de visualiser les variables, de traiter les valeurs manquantes, de transformer les données et d’exporter un jeu de données nettoyé.

L’objectif principal est de fournir un **outil intuitif, structuré et professionnel**, respectant les bonnes pratiques en data science.

---

## 2. Objectifs du projet

L’application répond aux objectifs suivants :

* Comprendre la structure générale d’un jeu de données
* Identifier les problèmes de qualité des données
* Visualiser les distributions et relations entre variables
* Traiter les valeurs manquantes
* Transformer les variables pour l’analyse
* Exporter les données nettoyées pour une utilisation ultérieure

---

## 3. Technologies utilisées

* **Python 3.10+**
* **Streamlit** : interface web interactive
* **Pandas** : manipulation et analyse des données
* **NumPy** : calcul numérique
* **Plotly** : visualisations interactives
* **Scikit-learn** : prétraitement (encodage, normalisation, standardisation)
* **XlsxWriter / OpenPyXL** : export Excel

---

## 4. Structure du projet

```
ApplicationStreamlite/
│
├── app.py
├── requirements.txt
├── rapport.md
│
├── .streamlit/
│   └── config.toml
│
├── modules/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_overview.py
│   ├── visualization.py
│   ├── missing_values.py
│   ├── preprocessing.py
│   ├── insights.py
│   └── export.py
│
└── data/
```

---

## 5. Fonctionnalités de l’application

### 5.1 Chargement et aperçu des données

* Importation d’un fichier CSV
* Affichage des 5 premières lignes
* Nombre de lignes et de colonnes
* Types des variables
* Nombre et pourcentage de valeurs manquantes
* Comparaison entre données originales et données nettoyées

---

### 5.2 Visualisation des données

* Histogrammes pour les variables numériques
* Boxplots pour la détection des valeurs aberrantes
* Bar charts pour les variables catégorielles
* Scatter plots pour analyser les relations entre variables
* Graphiques interactifs (zoom, hover, export)

---

### 5.3 Analyse des valeurs manquantes

* Nombre et pourcentage de valeurs manquantes par colonne
* Visualisation de la distribution des valeurs manquantes
* Classification des variables selon leur niveau d’impact :

  * Faible
  * Moyen
  * Critique
* Identification des variables les plus affectées

---

### 5.4 Traitement des valeurs manquantes

Méthodes disponibles :

* Remplacement par une valeur fixe
* Remplacement par la moyenne
* Remplacement par la médiane
* Remplacement par la valeur la plus fréquente
* Forward fill
* Backward fill

---

### 5.5 Encodage des variables catégorielles

* One-Hot Encoding
* Label Encoding

---

### 5.6 Normalisation et standardisation

* Normalisation Min–Max
* Standardisation Z-score

---

### 5.7 Analyse automatique (Insights)

* Détection des corrélations fortes entre variables
* Identification des variables à forte variance
* Détection simple des valeurs aberrantes (méthode IQR)

---

### 5.8 Export des données

* Aperçu des données finales
* Choix du nom du fichier
* Export au format CSV
* Export au format Excel
* Historique des transformations appliquées

---

## 6. Interface utilisateur

* Interface claire et moderne
* Navigation simple via une barre latérale
* Thème visuel professionnel
* Actions explicites, sans modification automatique des données
* Conservation des données originales

---

## 7. Lancement de l’application

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Lancement

```bash
streamlit run app.py
```

---

## 8. Conformité au cahier des charges

| Exigence                                            | Statut |
| --------------------------------------------------- | ------ |
| Aperçu des données                                  | ✔      |
| Visualisations (histogramme, boxplot, bar, scatter) | ✔      |
| Détection des valeurs manquantes                    | ✔      |
| Traitement des valeurs manquantes                   | ✔      |
| Encodage catégoriel                                 | ✔      |
| Normalisation / standardisation                     | ✔      |
| Export CSV                                          | ✔      |
| Interface graphique conviviale                      | ✔      |

---

## 9. Conclusion

Cette application constitue un **outil complet d’analyse exploratoire des données**, répondant strictement aux exigences du projet tout en intégrant des fonctionnalités avancées et une interface professionnelle.
Elle peut être utilisée comme base pour des projets de data science, de machine learning ou d’analyse statistique.

---
