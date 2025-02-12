from Interface import MainWindow
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    # Créer l'application
    app = QApplication(sys.argv)

    # Créer la fenêtre principale
    window = MainWindow()
    window.show()

    # Lancer la boucle principale de l'application
    sys.exit(app.exec_())