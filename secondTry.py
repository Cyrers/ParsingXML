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


"""
def analyze_xsd_lines(xsd_lines):
    open_tags_line = []
    conteneurJson = {}  # Conteneur JSON final
    current_dict = conteneurJson  # Dictionnaire courant pour ajouter les éléments
    for line in xsd_lines:
        #print(line)
        if not line.strip().endswith("/>"):
            if not line.startswith("<"):
                #current_dict["value"] = line
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
        print(open_tags_line)

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
"""
def retourHashMapContenuLigne(ligne):
    if not ligne.startswith("</"):
        if ligne.endswith("/>"):
            copy_ligne = ligne[1:-2]
        else:
            copy_ligne = ligne[1:-1]
        copy_ligne = copy_ligne.split(" ")[1:]
        hashmap = {}
        for elem in copy_ligne:
            if elem != '':
                val = elem.split("=")
                hashmap[val[0]] = val[1]
        return hashmap
    return None


def returnLignesEnfant(lignes):
    lignes_enfant = []
    pile_tags = []
    index_children =[]
    if not lignes[0].endswith("/>"):
        for i in range(1, len(lignes)):
            if lignes[i].startswith("</"):
                if not pile_tags:
                    print(lignes_enfant, index_children)
                    return lignes_enfant, index_children
                else:
                    pile_tags.pop()
            elif lignes[i].startswith("<"):
                if not pile_tags:
                    lignes_enfant.append(lignes[i])
                    index_children.append(i)
                if not lignes[i].endswith("/>"):
                    pile_tags.append(lignes[i])
    return None, None




def add_attributes_to_json(json_dict, element_name, attributes):
    element_json = {
        "attributes": attributes,  # Liste des attributs
        "children": []  # Liste vide pour ajouter les enfants plus tard
    }
    json_dict[element_name] = element_json
    return json_dict

# def parse_element(lignes, json_dict, index=0):
#     """Fonction récursive pour parcourir et convertir chaque balise et ses enfants."""
#     while index < len(lignes):
#         ligne = lignes[index]
#
#         # Vérifier si la ligne est une balise d'ouverture (ou auto-fermante)
#         if ligne.startswith("<") and not ligne.startswith("</"):
#             element_name = ligne.split(" ")[0][1:]  # Récupère le nom de la balise
#             if element_name.endswith("/"):  # Si le nom de la balise se termine par '/', enlever cela
#                 element_name = element_name[:-1]
#
#             # Récupérer les attributs de l'élément
#             attributes = retourHashMapContenuLigne(ligne)
#
#             # Ajouter l'élément au JSON
#             json_dict = add_attributes_to_json(json_dict, element_name, attributes)
#
#             # Si la balise n'est pas auto-fermante, chercher ses enfants
#             if not ligne.endswith("/>"):
#                 enfants, next_index = returnLignesEnfant(lignes[index:])
#
#                 # Si on trouve des enfants, on les traite de manière récursive
#                 if enfants:
#                     json_dict[element_name]["children"] = []  # Initialiser la liste des enfants
#                     child_dict = {}
#                     parse_element(enfants, child_dict)  # Appel récursif
#                     json_dict[element_name]["children"].append(child_dict)  # Ajouter les enfants
#
#                 # Met à jour l'index à la fin du bloc enfant
#                 index += next_index
#
#         index += 1  # Passer à la ligne suivante
#
#     return json_dict

def convert_xsd_to_json():
    # file = ouvertureDuXSD("bidule.xsd")
    # cleaned_file = parsingXSD(file)
    # json_dict = {}

    # line_attributes = retourHashMapContenuLigne(cleaned_file[0])
    # add_attributes_to_json(json_dict, cleaned_file[0].split(" ")[0][5:], line_attributes)

    file = ouvertureDuXSD("bidule.xsd")  # Lire le fichier XSD
    cleaned_file = parsingXSD(file)  # Nettoyer le fichier (prétraitement)

    # Initialisation du dictionnaire JSON
    json_dict = {}
    element_name = cleaned_file[0].split(" ")[0][1:]  # Récupère le nom de la balise
    element_attributes = retourHashMapContenuLigne(cleaned_file[0])
    json_dict[element_name] = element_attributes
    json_dict[element_name]["children"] = {}

    # Convertir l'élément racine et ses enfants
    add_child_to_json(json_dict[element_name]["children"], cleaned_file)

    save_json_to_file(json_dict, 'output.json')


def save_json_to_file(json_data, output_filename):
    """Sauvegarde le dictionnaire JSON dans un fichier."""
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
"""
def add_child_to_json(json_dict, lignes_courantes):
    lignes_children, liste_index_children = returnLignesEnfant(lignes_courantes)
    new_dict = json_dict
    if lignes_children:
        for j in range(len(lignes_children)) :
            element_name = lignes_children[j].split(" ")[0][1:]  # Récupère le nom de la balise
            element_attributes = retourHashMapContenuLigne(lignes_children[j])
            new_dict[str(element_name + str(j))] = element_attributes
            new_dict[str(element_name + str(j))]["children"] = []
            add_child_to_json(new_dict[element_name + str(j)]["children"], lignes_courantes[liste_index_children[j]:])
    return new_dict

"""
def add_child_to_json(json_dict, lignes_courantes):
    lignes_children, liste_index_children = returnLignesEnfant(lignes_courantes)
    if lignes_children:
        for j in range(len(lignes_children)):
            element_name = lignes_children[j].split(" ")[0][1:]  # Récupère le nom de la balise
            element_attributes = retourHashMapContenuLigne(lignes_children[j])
            # On s'assure que 'json_dict' est bien un dictionnaire avant d'ajouter des éléments
            if isinstance(json_dict, dict):
                json_dict[element_name + str(j)] = element_attributes
                json_dict[element_name + str(j)]["children"] = {}
                add_child_to_json(json_dict[element_name + str(j)]["children"], lignes_courantes[liste_index_children[j]:])
    return json_dict

def parsingXSD(xsd):
    xsd = xsd.strip().split('\n')
    if xsd[0] == '<?xml version="1.0" encoding="UTF-8"?>':
        xsd = xsd[1:]
    xsd = [line.replace('\t', '') for line in xsd]
    print(xsd)
    for i in range(len(xsd)):
        while xsd[i].startswith(' '):
            xsd[i] = xsd[i][1:]
    return xsd













xsd_lines = [
    '<root>',
    '<element1>',
    '<subelement1/>',
    '<subelement2/>',
    '</element1>',
    '<element2>',
    '<subelement3>',
    '<subsubelement1/>',
    '<subsubelement2>'
    'bidule',
    '</subsubelement2>',
    '</subelement3>',
    '</element2>',
    '</root>'
]

#result, i = returnLignesEnfant(xsd_lines)
#print(result, i)"""


convert_xsd_to_json()



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


#file = ouvertureDuXSD("bidule.xsd")
