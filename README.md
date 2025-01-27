
# Système de Recherche de Trajets Ferroviaires avec Reconnaissance Vocale

Ce projet est une application Python utilisant la reconnaissance vocale et des techniques de traitement du langage naturel (NLP) pour identifier les gares de départ et d'arrivée. Ensuite, il calcule et propose le plus court chemin entre ces gares en se basant sur un fichier CSV contenant les distances entre les gares.

## Fonctionnalités Principales

### 1. **Reconnaissance Vocale**
- Utilisation de la reconnaissance vocale pour identifier les gares de départ et d'arrivée demandées par l'utilisateur.

### 2. **Traitement du Langage Naturel (NLP)**
- Extraction et reconnaissance des noms de gares dans une commande textuelle.
- Utilisation de SpaCy pour la reconnaissance d'entités nommées (NER).
- Classification bayésienne pour la correspondance des noms de villes.

### 3. **Calcul de l'itinéraire optimal**
- Implémentation de l'algorithme de Dijkstra pour trouver le chemin le plus court entre deux gares, en tenant compte des horaires des trains.

### 4. **Génération de Dataset**
- Construction dynamique de phrases pour entraîner ou tester des modèles NLP.
- Intégration d'escales pour enrichir le dataset.

---

## Structure du Projet

### **main.py**
Le fichier principal qui orchestre les étapes suivantes : 
1. Utilisation de la reconnaissance vocale pour saisir les gares.
2. Traitement des données pour identifier et valider les gares.
3. Calcul du plus court chemin à l'aide de l'algorithme de Dijkstra.
4. Gestion et suppression de fichiers temporaires.

### **nlp.py**
Responsable du traitement du langage naturel :
- Lecture de texte et extraction des noms de gares depuis un fichier CSV.
- Correspondance entre les noms de villes et les gares existantes.
- Génération d'une liste des gares identifiées.

### **dijkstra.py**
Implémentation de l'algorithme de Dijkstra pour :
- Calculer l'itinéraire optimal en minimisant le temps de trajet.
- Intégrer des critères personnalisés comme des escales ou des préférences de voyage.

---

## Fonctionnement de l'application

1. **Saisie de l'utilisateur :**
   - L'utilisateur utilise sa voix pour indiquer les gares de départ et d'arrivée.
   
2. **Identification des gares :**
   - Le programme traite les commandes vocales pour extraire les noms de gares.
   - Il propose des correspondances si plusieurs options sont disponibles.

3. **Calcul du trajet optimal :**
   - Le programme applique l'algorithme de Dijkstra pour déterminer le chemin le plus court, en utilisant les horaires contenus dans un fichier CSV.

4. **Résultat :**
   - Affichage du trajet optimal avec les détails des gares intermédiaires et du temps de trajet.

---

## Technologies Utilisées

- **Python** : Langage principal.
- **SpaCy** : Reconnaissance d'entités nommées (NER).
- **SpeechRecognition** : Bibliothèque pour la reconnaissance vocale.
- **CSV** : Manipulation de fichiers contenant les horaires de train.
- **Algorithme de Dijkstra** : Calcul de l'itinéraire optimal.

---

## Points Forts de l'algorithme de Dijkstra
1. **Flexibilité :** Personnalisation des itinéraires en fonction de divers critères (temps, coût, escales).
2. **Efficacité :** Recherche rapide du plus court chemin dans des réseaux complexes.
3. **Adaptabilité :** Large compatibilité avec les systèmes de recommandation et de réservation en ligne.

---

## Installation et Exécution

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/username/repo.git
   cd repo
   ```

2. Installez les dépendances nécessaires :
   ```bash
   pip install -r requirements.txt
   ```

3. Assurez-vous que les fichiers suivants sont présents dans le dossier `data` :
   - `timetables.csv` : Horaires des trains.
   - `escales.csv` : Données sur les escales.

4. Exécutez le programme :
   ```bash
   python main.py
   ```

---

## Contributions
Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour signaler des bogues ou proposer des améliorations.

---

## Auteurs
- **Votre Nom**  
- Contact : [email@example.com](mailto:email@example.com)

---

## Licence
Ce projet est sous licence [MIT](LICENSE).

--- 

Ajoutez ce fichier à la racine de votre projet pour présenter efficacement votre application sur GitHub. Si vous souhaitez des ajustements ou des précisions supplémentaires, faites-le-moi savoir !
