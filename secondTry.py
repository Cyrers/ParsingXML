"""
    TODO: Faire une interface graphique pour le programme
    TODO: Faire un programme pour vérifier l'intégrité des fichiers entrants
        Vérfier que les balises sont bien fermées
        Détecter qu'un fichier à été altéré

    TODO: Construire le JSON a partir du fichier entrant
    TODO: Algorithme de comparaison des JSON qui détermine si un json est compris dans un autre-> OK
    TODO: Faire en sorte de pouvoir afficher des graphes sur l'IG (avoir une représentation des éléments qui sont en commun/qui ont été rajoutés) (NETWORKX maybe ?)

"""

import json

def ouvertureDuXSD(path):
    with open(path) as f:
        xsd = f.read()
    return xsd

def print_hex_values(strings):
    for string in strings:
        hex_values = [hex(ord(char)) for char in string]
        print(f"String: {string}")
        print("Hex values:", ' '.join(hex_values))
        print()  # For spacing between each string's output



"""def analyze_xsd_lines(xsd_lines):
    open_tags_line = []
    conteneurJson = {}
    for line in xsd_lines:
        #print(line)
        if not line.strip().endswith("/>"):
            if not line.startswith("<"):
                # call une fonction affecte la value a l'élément courant
                pass
            else:
                if (line.startswith("</")) & (open_tags_line != []):
                    # On ne vérifie pas l'on est en train de fermer une balise parente sur une balise enfante
                    open_tags_line.pop()
                    # modifier ici
                else:
                    open_tags_line.append(line.split(" ")[0])
                    #modifier ici
            for i in range(len(open_tags_line)):
                if open_tags_line[i] == '':
                    open_tags_line.pop(i)
        else:
            print("Balise Autofermée")
            #modifier ici
        print(open_tags_line)"""

def analyze_xsd_lines(xsd_lines):
    open_tags = []  # Stack des balises ouvertes
    conteneurJson = {}  # Conteneur JSON final
    current_dict = conteneurJson  # Dictionnaire courant pour ajouter les éléments
    for line in xsd_lines:
        line = line.strip()

        if not line.endswith("/>"):  # Si la ligne n'est pas une balise autofermante
            if line.startswith("</"):  # Balise fermante
                tag = line[2:-1].split()[0]  # Récupère le nom de la balise sans le '/'
                if open_tags:
                    open_tags.pop()  # Supprime la balise ouverte correspondante
                if len(open_tags) > 0:
                    current_dict = conteneurJson
                    for open_tag in open_tags:
                        current_dict = current_dict[open_tag]  # Retour à la balise parente
            else:  # Balise ouvrante
                tag = line[1:].split()[0]  # Récupère le nom de la balise sans '<'
                if tag not in current_dict:  # Si la balise n'existe pas, on la crée
                    current_dict[tag] = {}  # Crée un dictionnaire pour cette balise
                open_tags.append(tag)  # Ajoute la balise ouverte à la pile
                current_dict = current_dict[tag]  # Passe au sous-dictionnaire de la balise

        else:  # Balise auto-fermante
            tag = line[1:-2].split()[0]  # Récupère le nom de la balise sans '<' et '/>'
            current_dict[tag] = None  # Ajoute la balise autofermée avec une valeur nulle

        # Affichage de l'état de la pile de balises (optionnel)
        print(f"Pile des balises: {open_tags}")

    return conteneurJson


# Exemple d'utilisation
xsd_lines = [
    '<root>',
    '  <element1>',
    '    <subelement1/>',
    '    <subelement2/>',
    '  </element1>',
    '  <element2>',
    '    <subelement3>',
    '      <subsubelement1/>',
    '      <subsubelement2>'
    '        bidule',
    '      </subsubelement2>',
    '    </subelement3>',
    '  </element2>',
    '</root>'
]

result = analyze_xsd_lines(xsd_lines)
print(result)




def parsingXSD(xsd):
    xsd = xsd.strip().split('\n')
    if xsd[0] == '<?xml version="1.0" encoding="UTF-8"?>':
        xsd = xsd[1:]
    xsd = [line.replace('\t', '') for line in xsd]
    print(xsd)
    for i in range(len(xsd)):
        while xsd[i].startswith(' '):
            xsd[i] = xsd[i][1:]

    analyze_xsd_lines(xsd)
    return 0

def is_subset(json1, json2):
    """
        Vérifie si json1 est un sous-ensemble de json2.
    """
    if isinstance(json1, dict) and isinstance(json2, dict):
        for key in json1:
            if key not in json2:
                return False
            if not is_subset(json1[key], json2[key]):
                return False
        return True

    elif isinstance(json1, list) and isinstance(json2, list):
        for item in json1:
            if not any(is_subset(item, elem) for elem in json2):
                return False
        return True

    else:
        return json1 == json2


"""file = ouvertureDuXSD("bidule.xsd")
parsingXSD(file)"""