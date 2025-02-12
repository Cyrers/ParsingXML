import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit
from xml_comparator import open_File, parse_to_tree, xml_to_graph, draw_graph, save_ids_to_file, get_element_id
import json


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurer la fenêtre
        self.setWindowTitle('Comparaison de fichiers XML')
        self.setGeometry(100, 100, 800, 600)  # Fenêtre plus grande

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

        # Créer un bouton unique pour comparer les fichiers
        self.compare_button = QPushButton('Comparer les fichiers', self)
        self.compare_button.clicked.connect(self.compare_files)  # Connecter l'événement de clic
        layout.addWidget(self.compare_button)

        # Créer la zone de texte pour afficher les IDs détectés
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)  # Ne pas permettre la modification du texte
        self.text_area.setStyleSheet("background-color: white;")  # Fond blanc
        self.text_area.setPlaceholderText("Les IDs ajoutés seront affichés ici.")  # Texte par défaut
        layout.addWidget(self.text_area)

        # Créer le bouton pour fermer l'application
        self.close_button = QPushButton('Fermer l\'application', self)
        self.close_button.clicked.connect(self.close)  # Connecter l'événement de clic
        layout.addWidget(self.close_button)

        # Bouton pour exporter les résultats en JSON
        self.export_button = QPushButton('Exporter en JSON', self)
        self.export_button.clicked.connect(self.export_results)
        self.export_button.setEnabled(False)  # Désactivé tant qu'il n'y a pas de résultats
        layout.addWidget(self.export_button)

        # Appliquer le layout à la fenêtre
        self.setLayout(layout)

        # Initialiser les chemins des fichiers
        self.file1_path = ''
        self.file2_path = ''

        self.comparison_results = ''

    def load_file1(self):
        # Ouvrir une boîte de dialogue pour charger un fichier
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Charger fichier 1", "", "Tous les fichiers (*)",
                                                   options=options)
        if file_name:
            self.file1_path = file_name
            self.update_label()
            self.check_files_loaded()

    def load_file2(self):
        # Ouvrir une boîte de dialogue pour charger un fichier
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Charger fichier 2", "", "Tous les fichiers (*)",
                                                   options=options)
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
            self.compare_button.setEnabled(True)  # Activer le bouton de comparaison

    def compare_files(self):
        # Comparer les fichiers dans les deux sens (1 → 2 et 2 → 1)
        file1_content = open_File(self.file1_path)
        file2_content = open_File(self.file2_path)

        if file1_content and file2_content:
            root1 = parse_to_tree(file1_content)
            root2 = parse_to_tree(file2_content)

            if root1 and root2:
                # Comparer le fichier 1 avec le fichier 2
                reference_elements_1_to_2 = list(root2.iter())  # Fichier de référence
                compared_elements_1_to_2 = list(root1.iter())  # Fichier comparé

                # Comparer le fichier 2 avec le fichier 1
                reference_elements_2_to_1 = list(root1.iter())  # Fichier de référence
                compared_elements_2_to_1 = list(root2.iter())  # Fichier comparé

                save_ids_to_file(reference_elements_1_to_2, "reference_ids_1_to_2.json")
                save_ids_to_file(compared_elements_1_to_2, "compared_ids_1_to_2.json")

                save_ids_to_file(reference_elements_2_to_1, "reference_ids_2_to_1.json")
                save_ids_to_file(compared_elements_2_to_1, "compared_ids_2_to_1.json")

                reference_dict_1_to_2 = {get_element_id(e): e for e in reference_elements_1_to_2 if get_element_id(e)}
                graph_1_to_2, compared_dict_1_to_2 = xml_to_graph(root1, reference_elements_1_to_2,
                                                                  compared_elements_1_to_2,
                                                                  reference_dict=reference_dict_1_to_2)

                reference_dict_2_to_1 = {get_element_id(e): e for e in reference_elements_2_to_1 if get_element_id(e)}
                graph_2_to_1, compared_dict_2_to_1 = xml_to_graph(root2, reference_elements_2_to_1,
                                                                  compared_elements_2_to_1,
                                                                  reference_dict=reference_dict_2_to_1)

                # Identifier les éléments ajoutés dans les deux sens
                added_ids_1_to_2 = [get_element_id(e) for e in compared_elements_1_to_2 if
                                    get_element_id(e) not in reference_dict_1_to_2]
                added_ids_2_to_1 = [get_element_id(e) for e in compared_elements_2_to_1 if
                                    get_element_id(e) not in reference_dict_2_to_1]

                # Afficher les résultats dans la zone de texte
                if added_ids_1_to_2:
                    self.text_area.setText(f"IDs ajoutés (Fichier 1 → Fichier 2) :\n" + "\n".join(added_ids_1_to_2))
                    self.comparison_results = added_ids_1_to_2
                    draw_graph(graph_1_to_2)  # Afficher le graph du sens 1 → 2
                elif added_ids_2_to_1:
                    self.text_area.setText(f"IDs ajoutés (Fichier 2 → Fichier 1) :\n" + "\n".join(added_ids_2_to_1))
                    self.comparison_results = added_ids_2_to_1
                    draw_graph(graph_2_to_1)  # Afficher le graph du sens 2 → 1
                else:
                    self.text_area.setText("Les deux fichiers sont identiques !")  # Afficher ce message si aucun ajout
                    self.text_area.setStyleSheet(
                        "background-color: lightgray;")  # Change le fond pour indiquer que les fichiers sont identiques.
                self.export_button.setEnabled(True)

    def export_results(self):
        if not self.comparison_results:
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier", "",
                                                   "Fichiers JSON (*.json);;Tous les fichiers (*)")

        if file_name:
            # S'assurer que l'extension .json est bien présente
            if not file_name.lower().endswith(".json"):
                file_name += ".json"

            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(self.comparison_results, f, indent=4, ensure_ascii=False)
                self.text_area.append(f"\nRésultats exportés : {file_name}")
            except Exception as e:
                self.text_area.append(f"\nErreur lors de l'exportation : {e}")


if __name__ == '__main__':
    # Créer l'application
    app = QApplication(sys.argv)

    # Créer la fenêtre principale
    window = MainWindow()
    window.show()

    # Lancer la boucle principale de l'application
    sys.exit(app.exec_())
