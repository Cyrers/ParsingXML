"""
    TODO: Faire une interface graphique pour le programme
    TODO: Faire un programme pour vérifier l'intégrité des fichiers entrants
        Vérfier que les balises sont bien fermées
        Détecter qu'un fichier à été altéré

    TODO: Construire le JSON a partir du fichier entrant
    TODO: Algorithme de comparaison des JSON qui détermine si un json est compris dans un autre-> OK
    TODO: Faire en sorte de pouvoir afficher des graphes sur l'IG (avoir une représentation des éléments qui sont en commun/qui ont été rajoutés) (NETWORKX maybe ?)

"""
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

def analyze_xsd_lines(xsd_lines):
    open_tags_line = []

    for line in xsd_lines:
        #print(line)
        if not line.strip().endswith("/>"):
            if not line.startswith("<"):
                #modifier ici
                pass
            else:
                if (line.startswith("</")) & (open_tags_line != []):
                    # On ne vérifie pas l'on est en train de fermer une balise parente sur une balise enfante
                    if ( "<" + line[2:-1]) in open_tags_line:
                        open_tags_line.remove("<" + line[2:-1])
                    elif ( "<" + line[2:-1] + ">") in open_tags_line:
                        open_tags_line.remove("<" + line[2:-1] + ">")
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


file = ouvertureDuXSD("bidule.xsd")
parsingXSD(file)