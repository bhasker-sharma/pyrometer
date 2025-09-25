import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QSplitter, QVBoxLayout, 
    QHBoxLayout, QPushButton, QFrame, QLabel, QGridLayout, QInputDialog,
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)
from PyQt5.QtCore import Qt



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PyrometerDashboard()
    window.show()
    sys.exit(app.exec_())
