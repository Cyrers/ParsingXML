import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from xml_comparator import open_File, parse_to_tree, xml_to_graph, draw_graph, save_ids_to_file, get_element_id

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurer la fenêtre
        self.setWindowTitle('Comparaison de fichiers XML')
        self.setGeometry(100, 100, 400, 300)

        # Créer un layout vertical
        layout = QVBoxLayout()

        # Créer une étiquette
        self.label = QLabel('Cliquez sur un bouton ci-dessous pour charger un fichier', self)
        layout.addWidget(self.label)

        # Créer le premier bouton
        self.button1 = QPushButton('Charger fichier 1', self)
        self.button1.clicked.connect(self.load_file1)  # Connecter l'événement de clic
        layout.addWidget(self.button1)

        # Créer le deuxième bouton
        self.button2 = QPushButton('Charger fichier 2', self)
        self.button2.clicked.connect(self.load_file2)  # Connecter l'événement de clic
        layout.addWidget(self.button2)

        # Créer le bouton pour effectuer la comparaison dans un sens
        self.compare_button_1_to_2 = QPushButton('Comparer Fichier 1 → Fichier 2', self)
        self.compare_button_1_to_2.clicked.connect(self.compare_1_to_2)  # Connecter l'événement de clic
        layout.addWidget(self.compare_button_1_to_2)

        # Créer le bouton pour effectuer la comparaison dans l'autre sens
        self.compare_button_2_to_1 = QPushButton('Comparer Fichier 2 → Fichier 1', self)
        self.compare_button_2_to_1.clicked.connect(self.compare_2_to_1)  # Connecter l'événement de clic
        layout.addWidget(self.compare_button_2_to_1)

        # Créer le bouton pour fermer l'application
        self.close_button = QPushButton('Fermer l\'application', self)
        self.close_button.clicked.connect(self.close)  # Connecter l'événement de clic
        layout.addWidget(self.close_button)

        # Appliquer le layout à la fenêtre
        self.setLayout(layout)

        # Initialiser les chemins des fichiers
        self.file1_path = ''
        self.file2_path = ''

    def load_file1(self):
        # Ouvrir une boîte de dialogue pour charger un fichier
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Charger fichier 1", "", "Tous les fichiers (*)", options=options)
        if file_name:
            self.file1_path = file_name
            self.update_label()
            self.check_files_loaded()

    def load_file2(self):
        # Ouvrir une boîte de dialogue pour charger un fichier
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Charger fichier 2", "", "Tous les fichiers (*)", options=options)
        if file_name:
            self.file2_path = file_name
            self.update_label()
            self.check_files_loaded()

    def update_label(self):
        # Mettre à jour le texte de l'étiquette avec les chemins des fichiers chargés
        self.label.setText(f'Fichier 1 chargé: {self.file1_path}\nFichier 2 chargé: {self.file2_path}')

    def check_files_loaded(self):
        # Vérifier si les deux fichiers sont chargés
        if self.file1_path and self.file2_path:
            self.enable_comparison_buttons()

    def enable_comparison_buttons(self):
        # Activer les boutons de comparaison si les deux fichiers sont chargés
        self.compare_button_1_to_2.setEnabled(True)
        self.compare_button_2_to_1.setEnabled(True)

    def compare_1_to_2(self):
        # Logique pour la comparaison du fichier 1 avec le fichier 2
        file1_content = open_File(self.file1_path)
        file2_content = open_File(self.file2_path)

        if file1_content and file2_content:
            root1 = parse_to_tree(file1_content)
            root2 = parse_to_tree(file2_content)

            if root1 and root2:
                reference_elements = list(root2.iter())
                compared_elements = list(root1.iter())

                save_ids_to_file(reference_elements, "reference_ids.json")
                save_ids_to_file(compared_elements, "compared_ids.json")

                reference_dict = {get_element_id(e): e for e in reference_elements if get_element_id(e)}
                graph, compared_dict = xml_to_graph(root1, reference_elements, compared_elements, reference_dict=reference_dict)
                draw_graph(graph)

    def compare_2_to_1(self):
        # Logique pour la comparaison du fichier 2 avec le fichier 1
        file1_content = open_File(self.file1_path)
        file2_content = open_File(self.file2_path)

        if file1_content and file2_content:
            root1 = parse_to_tree(file1_content)
            root2 = parse_to_tree(file2_content)

            if root1 and root2:
                reference_elements = list(root1.iter())
                compared_elements = list(root2.iter())

                save_ids_to_file(reference_elements, "reference_ids.json")
                save_ids_to_file(compared_elements, "compared_ids.json")

                reference_dict = {get_element_id(e): e for e in reference_elements if get_element_id(e)}
                graph, compared_dict = xml_to_graph(root2, reference_elements, compared_elements, reference_dict=reference_dict)
                draw_graph(graph)

if __name__ == '__main__':
    # Créer l'application
    app = QApplication(sys.argv)

    # Créer la fenêtre principale
    window = MainWindow()
    window.show()

    # Lancer la boucle principale de l'application
    sys.exit(app.exec_())
