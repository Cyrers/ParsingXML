import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from secondTry import convert_xsd_to_json, is_subset

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurer la fenêtre
        self.setWindowTitle('Interface PyQt5')
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
            self.process_files()

    def process_files(self):
        # Convertir les fichiers XSD en JSON
        json1 = convert_xsd_to_json(self.file1_path)
        json2 = convert_xsd_to_json(self.file2_path)

        # Vérifier si le premier XSD est inclus dans le deuxième XSD
        result = is_subset(json1, json2)

        # Afficher le résultat dans l'interface
        self.label.setText(f'Fichier 1 chargé: {self.file1_path}\nFichier 2 chargé: {self.file2_path}\nRésultat: {result}')


if __name__ == '__main__':
    # Créer l'application
    app = QApplication(sys.argv)

    # Créer la fenêtre principale
    window = MainWindow()
    window.show()

    # Lancer la boucle principale de l'application
    sys.exit(app.exec_())
