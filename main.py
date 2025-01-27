from nlp import Nlp
from voice import VoiceRecognition
import time
import csv
import random
import os
from dijkstra import Dijkstra


def buildDataset(cities):

    size = len(cities)      #Calcul de la taille de la liste de villes 
    dataset = open('data/dataset.csv')
    csvreader = csv.reader(dataset, delimiter=';')
    csv_escales = open('data/escales.csv')
    escales = csv.reader(csv_escales, delimiter=';')
    next(csvreader)
    sentences = []      #Initialisation d'une liste pour stocker des phrases générées

    for row in csvreader:
        sentence = row[0]
        sentence_type = row[1]
        for i in range(50):
            city = cities[random.randrange(0, size, 1)]
            destination = cities[random.randrange(0, size, 1)]
            sentences.append([sentence.replace("first", city).replace("second", destination), sentence_type])       #Remplacement de "first" et "second" par les noms de ville 
        print(sentence)
        for escale in escales:
            new_sentence_type = sentence_type + '_by'
            new_sentence = sentence + " " + escale[0]
            print(new_sentence)
            for j in range(50):
                city = cities[random.randrange(0, size, 1)]
                destination = cities[random.randrange(0, size, 1)]
                escale_name = cities[random.randrange(0, size, 1)]
                sentences.append(
                    [new_sentence.replace("first", city).replace("second", destination).replace("third", escale_name),
                     new_sentence_type])
        csv_escales.close()
        csv_escales = open('data/escales.csv')
        escales = csv.reader(csv_escales, delimiter=';')
    dataset.close()
    with open("second_built_dataset.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["sentence", "sentence_type"])
        csvwriter.writerows(sentences)

def main():
    nlp_IA = Nlp()      #Création d'une instance de la classe Nlp
    stations = nlp_IA.get_station()     #Appel de la méthode get_station pour obtenir la liste des gares
    buildDataset(stations)
    voice = VoiceRecognition()
    first, second = [], []      #Initialisation de deux listes vides pour les gares de départ et d'arrivée 
    while (len(first) < 1 and len(second) < 1):      #Tant que les listes de gares de départ et d'arrivée sont vides
        while not os.path.exists("command.txt"):
            voice.call_me()
            time.sleep(2)
        first, second = nlp_IA.call_me()
        print(first, second)
        if (len(first) < 1 and len(second) < 1):
            print("Moin de 2 villes renseigner, reesaye\n\n")
            time.sleep(2)

    if len(first) > 1:      #Si plusieurs gares de départ sont disponibles
        print("\n\nPlusieurs possibilités de départ: ")

        for i, elem in enumerate(first):        #Affichage des options de gares de départ
            print(i + 1, " - ", elem)
        source_index = int(input("Vous avez choisi la gare : ")) - 1
        source = first[source_index]
    else:
        source = first[0]       #Si une seule gare de départ est disponible, elle est automatiquement sélectionnée

    if len(second) > 1:     #Si plusieurs gares d'arrivée sont disponibles
        print("\n\nPlusieurs possibilités de d'arrivé : ")

        for i, elem in enumerate(second):       #Affichage des options de gares d'arrivée
            print(i + 1, " - ", elem)
        destination_index = int(input("Vous avez choisi la gare : ")) - 1
        destination = second[destination_index]
    else:
        destination = second[0]     #Si une seule gare d'arrivée est disponible, elle est automatiquement sélectionnée

    file = open('data/timetables.csv')
    csvreader = csv.reader(file, delimiter='\t')
    pf = Dijkstra(stations, csvreader)

    previous_nodes, shortest_path = pf.dijkstra_algorithm(graph=pf, start_node=source)      #Application de l'algorithme de Dijkstra pour trouver le plus court chemin
    pf.print_result(previous_nodes, shortest_path, start_node=source, target_node=destination)      #Affichage du résultat du plus court chemin

    if os.path.exists("command.txt"):
        os.remove("command.txt")


if __name__ == "__main__":
    main()
