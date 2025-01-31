import networkx as nx
import matplotlib.pyplot as plt
from lxml import etree
from networkx.drawing.nx_agraph import graphviz_layout

def open_File(path):
    with open(path) as f:
        xsd = f.read()
        # xsd = xsd[:69]
    return xsd


def parse_to_tree(xml_string):
    tree = etree.fromstring(xml_string.encode('utf-8'))
    return tree


def print_tree(tree_root):
    print(etree.tostring(tree_root, pretty_print=True))


def get_element_id(element):
    return element.attrib.get('id', id(element))


def elements_equal(e1, e2):
    return get_element_id(e1) == get_element_id(e2) and e1.tag == e2.tag and e1.attrib == e2.attrib

# TODO: Pour détecter les éléments supprimés on fait comme un ajout mais on colore les noeuds en rouge ca devrais aller vu que l'ajout marche en dernière nouvelle.
def xml_to_graph(element, reference=None, graph=None, parent=None, reference_dict=None, compared_dict=None):
    if graph is None:
        graph = nx.DiGraph()
    if reference_dict is None:
        reference_dict = {get_element_id(e): e for e in reference} if reference else {}
    if compared_dict is None:
        compared_dict = {}

    node_id = get_element_id(element)
    node_label = element.attrib.get('name', element.tag)

    color = 'lightblue'  # Par défaut
    if node_id not in reference_dict:
        color = 'green'  # Nouvel élément
    elif not elements_equal(element, reference_dict[node_id]):
        color = 'orange'  # Élément existant mais modifié

    graph.add_node(node_id, label=node_label, color=color)
    compared_dict[node_id] = element  # Ajout au dictionnaire des nœuds comparés

    if parent is not None:
        graph.add_edge(parent, node_id)

    for child in element:
        xml_to_graph(child, reference, graph, node_id, reference_dict, compared_dict)

    return graph, compared_dict


def mark_deleted_nodes(graph, reference_dict, compared_dict):
    for ref_id, ref_element in reference_dict.items():
        if ref_id not in compared_dict:
            node_label = ref_element.attrib.get('name', ref_element.tag)
            graph.add_node(ref_id, label=node_label, color='red')


def draw_graph(graph):
    pos = graphviz_layout(graph, prog="dot")
    labels = nx.get_node_attributes(graph, 'label')
    colors = [nx.get_node_attributes(graph, 'color')[node] for node in graph.nodes()]

    plt.figure(figsize=(10, 6))
    nx.draw(graph, pos, with_labels=True, labels=labels, node_size=2500,
            node_color=colors, edge_color='gray', font_size=10, font_weight='bold')
    plt.show()


# root = parse_to_tree(open_File("Test_fichiers/SmokeDetector_M1.capella"))
# graph = xml_to_graph(root)
# draw_graph(graph)


file1_content = open_File("Test_fichiers/SmokeDetector_M1.capella")
file2_content = open_File("Test_fichiers/SmokeDetectorM1''.capella")  # Fichier de référence
if file1_content and file2_content:
    root1 = parse_to_tree(file1_content)
    root2 = parse_to_tree(file2_content)
    if root1 and root2:
        reference_elements = list(root2.iter())
        reference_dict = {get_element_id(e): e for e in reference_elements}
        graph, compared_dict = xml_to_graph(root1, reference_elements, reference_dict=reference_dict)
        mark_deleted_nodes(graph, reference_dict, compared_dict)
        draw_graph(graph)
