# -*- coding: utf-8 -*-

# Installer la librairie SpaCy
# pip install spacy OU pip3 install spacy

# Télécharger les modèles français.
# python3 -m spacy download fr_core_news_sm

import csv

import numpy as np
import spacy
from nltk.corpus import stopwords

from sklearn.utils import Bunch
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import os
from os.path import isfile, join, dirname, realpath
import pandas as pd

from os import listdir
import re


class Nlp:

    # Chargement du modèle SpaCy pour le français
    spacy_french_model = spacy.load("fr_core_news_sm")

    # Initialisation des objets pour la vectorisation du texte et la classification bayésienne
    count_vector = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    clf = MultinomialNB()
    label_classes = []



    #
    # Méthode pour charger le fichier second_built_dataset.csv
    def load_dataset(self):
        dataset_path = 'second_built_dataset.csv'
        df = pd.read_csv(dataset_path, delimiter=',')
        return df['sentence'], df['sentence_type']
    # Méthode pour entraîner le modèle bayésien avec le dataset
    def train_classifier(self, sentences, labels):
        X_train_counts = self.count_vector.fit_transform(sentences)
        X_train_tfidf = self.tfidf_transformer.fit_transform(X_train_counts)
        self.clf.fit(X_train_tfidf, labels)
        self.label_classes = set(labels)


    # Méthode pour exécuter le traitement NLP
    def call_me(self):
        text = self.read_from_file()
        return self.launch_nlp(text)
    
    # Méthode pour lire le texte à partir du fichier 'command.txt'
    def read_from_file(self):
        file = open('command.txt')
        text = file.read()
        file.close()
        return text

    # Méthode pour obtenir les noms de gares à partir du fichier CSV 'timetables'
    def get_station(self):
        file = open('data/timetables.csv')
        csvreader = csv.reader(file, delimiter='\t')
        next(csvreader)
        rows = []
        for row in csvreader:
            trajet = row[1].split(" - ")

            if not trajet[0].startswith("Gare de"):
                trajet[0] = "Gare de " + trajet[0]
            if not trajet[1].startswith("Gare de"):
                trajet[1] = "Gare de " + trajet[1]

            departure = trajet[0].split("Gare de ")[1]
            destination = trajet[1].split("Gare de ")[1]

            rows.append(departure)
            rows.append(destination)

        return list(set(rows))

    # Méthode principale pour exécuter le traitement NLP sur le texte donné
    def launch_nlp(self, text):

        print("Command received : " + text)

        #DATASET
        sentences, labels = self.load_dataset()
        self.train_classifier(sentences, labels)

        # Utiliser le modèle bayésien pour faire des prédictions
        sentence_type_predictions_bayesian = self.clf.predict(self.count_vector.transform([str(text)]))
        to_from_relation = sentence_type_predictions_bayesian[0]

        # Reconnaissance d’entités nommées (NER)
        spacyText = self.spacy_french_model(text)
        location = []

        # Récupération des gares existantes
        stations = self.get_station()

        stopWords = set(stopwords.words('french'))
        clean_words = []
        for token in [X.text for X in spacyText]:
            if token not in stopWords:
                clean_words.append(token)

        for word in clean_words:
            text = self.spacy_french_model(word)
            for ent in text.ents:
                if ent.label_ == 'LOC':
                    location.append(ent.text)

        # Identifier la gare de départ et la gare d'arrivée en fonction de la relation
        if to_from_relation == 'first':
            first, second = location[0], location[1]
        elif to_from_relation == 'second':
            first, second = location[1], location[0]
        else:
            # Gérer d'autres relations si nécessaire
            first, second = None, None

        if len(location) < 2:
            return [], []


        #cleaned_text = " ".join(clean_words)

       

        print("Bayesian Predictions:", sentence_type_predictions_bayesian)
        print(location)
        print("To/From Relation:", to_from_relation)
        print("Extracted Clean Words:", clean_words)

        # Récupére la bonne gare en fonction de la ville
        first = []
        second = []
        for station in stations:
            if sentence_type_predictions_bayesian[0] == "from_to":
                if location[0] in station and (
                        print("Before Association - from_to: first =", first, "second =", second, "location =", location),

                        location[0] == station or (location[0] + "-") in station or (location[0] + ".") in station or (
                        location[0] + " ") in station):
                    first.append(station)
                    print("After Association - from_to: first =", first, "second =", second)
                

                if location[1] in station and (
                        location[1] == station or (location[1] + "-") in station or (location[1] + ".") in station or (
                        location[1] + " ") in station):
                    second.append(station)
            elif sentence_type_predictions_bayesian[0] == "to_from":
                if location[0] in station and (
                        print("Before Association - to_from: first =", first, "second =", second, "location =", location),

                        location[0] == station or (location[0] + "-") in station or (location[0] + ".") in station or (
                        location[0] + " ") in station):
                    second.append(station)
                    print("After Association - to_from: first =", first, "second =", second)


                if location[1] in station and (
                        location[1] == station or (location[1] + "-") in station or (location[1] + ".") in station or (
                        location[1] + " ") in station):
                    first.append(station)

        # Combinez les prédictions des deux modèles
        combined_predictions = sentence_type_predictions_bayesian
        

        return first, second

