import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurer la fenêtre
        self.setWindowTitle('Interface PyQt5')
        self.setGeometry(100, 100, 400, 300)

        # Créer un layout vertical
        layout = QVBoxLayout()

        # Créer une étiquette
        self.label = QLabel('Cliquez sur le bouton ci-dessous', self)
        layout.addWidget(self.label)

        # Créer un bouton
        self.button = QPushButton('Cliquez-moi', self)
        self.button.clicked.connect(self.on_button_click)  # Connecter l'événement de clic
        layout.addWidget(self.button)

        # Appliquer le layout à la fenêtre
        self.setLayout(layout)

    def on_button_click(self):
        # Ce qui se passe quand le bouton est cliqué
        self.label.setText('Bouton cliqué !')


if __name__ == '__main__':
    # Créer l'application
    app = QApplication(sys.argv)

    # Créer la fenêtre principale
    window = MainWindow()
    window.show()

    # Lancer la boucle principale de l'application
    sys.exit(app.exec_())
