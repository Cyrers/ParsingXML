import networkx as nx
import matplotlib.pyplot as plt
import json
from lxml import etree
from networkx.drawing.nx_agraph import graphviz_layout

def open_File(path):
    with open(path) as f:
        xsd = f.read()
        # xsd = xsd[:69]
    return xsd

def parse_to_tree(xml_string):
    try:
        parser = etree.XMLParser(recover=True)  # Active la récupération des erreurs
        return etree.fromstring(xml_string.encode('utf-8'), parser=parser)
    except etree.XMLSyntaxError as e:
        print(f"Erreur de syntaxe XML : {e}")
        return None


def get_element_id(element):
    return element.attrib.get('id')  # Utilisation stricte de l'ID XML


def elements_equal(e1, e2):
    return get_element_id(e1) == get_element_id(e2) and e1.tag == e2.tag and e1.attrib == e2.attrib


def xml_to_graph(element, reference=None, compared=None, graph=None, parent=None, reference_dict=None, compared_dict=None):
    if graph is None:
        graph = nx.DiGraph()
    if reference_dict is None:
        reference_dict = {get_element_id(e): e for e in reference if get_element_id(e)} if reference else {}
    if compared_dict is None:
        compared_dict = {get_element_id(e): e for e in compared}  # ou les éléments du fichier comparé

    node_id = get_element_id(element)
    if node_id is None:
        return graph, compared_dict  # Ignorer les éléments sans ID

    node_label = element.attrib.get('name', element.tag)

    color = 'lightblue'  # Par défaut
    # Si l'élément existe dans le fichier comparé mais pas dans le fichier de référence, c'est un ajout
    if node_id not in reference_dict and node_id in compared_dict:
        color = 'green'  # Ajout
        print(f"[DEBUG] Nouvel élément détecté dans le fichier comparé : ID={node_id}, Label={node_label}")
    # Si l'élément existe dans les deux fichiers mais diffère, c'est une modification
    elif node_id in reference_dict and node_id in compared_dict and not elements_equal(element, reference_dict[node_id]):
        color = 'orange'  # Modification
        print(f"[DEBUG] Élément modifié : ID={node_id}, Label={node_label}")

    # Ajouter le nœud avec la couleur appropriée
    graph.add_node(node_id, label=node_label, color=color)
    compared_dict[node_id] = element  # Marquer comme comparé

    if parent is not None:
        graph.add_edge(parent, node_id)

    # Traiter les enfants
    for child in element:
        xml_to_graph(child, reference, compared, graph, node_id, reference_dict, compared_dict)

    return graph, compared_dict


def draw_graph(graph):
    pos = graphviz_layout(graph, prog="dot")
    labels = nx.get_node_attributes(graph, 'label')
    colors = [nx.get_node_attributes(graph, 'color')[node] for node in graph.nodes()]

    plt.figure(figsize=(10, 6))
    nx.draw(graph, pos, with_labels=True, labels=labels, node_size=2500,
            node_color=colors, edge_color='gray', font_size=10, font_weight='bold')
    plt.show()

def save_ids_to_file(elements, filename):
    ids = {get_element_id(e): e.tag for e in elements}
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(ids, f, indent=4)


