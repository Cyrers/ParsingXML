"""
    TODO: Faire une interface graphique pour le programme -> OK
    TODO: Faire un programme pour vérifier l'intégrité des fichiers entrants -> OSEF
        Vérfier que les balises sont bien fermées
        Détecter qu'un fichier à été altéré

    TODO: Construire le JSON a partir du fichier entrant  -> OK
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

def convert_xsd_to_json(filename='bidule.xsd', output_file='output.json'):
    # file = ouvertureDuXSD("bidule.xsd")
    # cleaned_file = parsingXSD(file)
    # json_dict = {}

    # line_attributes = retourHashMapContenuLigne(cleaned_file[0])
    # add_attributes_to_json(json_dict, cleaned_file[0].split(" ")[0][5:], line_attributes)

    file = ouvertureDuXSD(filename)  # Lire le fichier XSD
    cleaned_file = parsingXSD(file)  # Nettoyer le fichier (prétraitement)

    # Initialisation du dictionnaire JSON
    json_dict = {}
    element_name = cleaned_file[0].split(" ")[0][1:]  # Récupère le nom de la balise
    element_attributes = retourHashMapContenuLigne(cleaned_file[0])
    json_dict[element_name] = element_attributes
    json_dict[element_name]["children"] = {}

    # Convertir l'élément racine et ses enfants
    add_child_to_json(json_dict[element_name]["children"], cleaned_file)

    save_json_to_file(json_dict, output_file)
    return json_dict

def save_json_to_file(json_data, output_filename):
    """Sauvegarde le dictionnaire JSON dans un fichier."""
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    
def add_child_to_json(json_dict, lignes_courantes):
    lignes_children, liste_index_children = returnLignesEnfant(lignes_courantes)
    if lignes_children:
        for j, ligne in enumerate(lignes_children):
            element_name = ligne.split(" ")[0][1:]  # Récupère le nom de la balise
            element_attributes = retourHashMapContenuLigne(ligne)
            
            # Utiliser un defaultdict pour stocker plusieurs occurrences d'un même élément
            if element_name not in json_dict:
                json_dict[element_name] = []
            
            child_dict = {"attributes": element_attributes, "children": {}}
            json_dict[element_name].append(child_dict)
            
            add_child_to_json(child_dict["children"], lignes_courantes[liste_index_children[j]:])
    
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


# def main():
#     convert_xsd_to_json("bidule.xsd", "output1.json")
#     convert_xsd_to_json("bidule2.xsd", "output2.json")
#     convert_xsd_to_json("biduleMinux.xsd", "output3.json")
#     convert_xsd_to_json("bidulefalse.xsd", "output4.json")
#     with open("output1.json") as file1:
#         json1 = json.load(file1)
#     with open("output2.json") as file2:
#         json2 = json.load(file2)
#     with open("output3.json") as file3:
#         json3 = json.load(file3)
#     with open("output4.json") as file4:
#         json4 = json.load(file4)
#     print(is_subset(json2, json1))
#     assert(is_subset(json2, json1))
#     print(is_subset(json3, json1))
#     assert(is_subset(json3, json1))
#     print(is_subset(json4, json1))
#     assert(not is_subset(json4, json1))
# if __name__ == "__main__":
#     main()