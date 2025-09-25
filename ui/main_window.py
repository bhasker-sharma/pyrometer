from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QGridLayout, QDialog, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox
)
from PyQt5.QtCore import Qt
from ui.setting import DeviceSettingsDialog
from ui.device_cell import DeviceCell


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pyrometer Software")
        self.setGeometry(100, 100, 1100, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)

        # Navbar (Settings on top-right)
        self.init_navbar()

        # Device grid
        self.device_grid = QGridLayout()
        self.device_grid.setSpacing(10)
        self.devices = []
        self.max_devices = 16
        self.main_layout.addLayout(self.device_grid, stretch=3)

        # Bottom placeholder
        self.bottom_label = QLabel("Bottom Section (Logs / Graphs etc.)")
        self.bottom_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.bottom_label, stretch=1)

    def init_navbar(self):
        navbar = QHBoxLayout()

        btn_settings = QPushButton("Settings")
        btn_settings.clicked.connect(self.open_settings_dialog)

        navbar.addStretch(1)  # pushes settings button to right
        navbar.addWidget(btn_settings)

        self.main_layout.addLayout(navbar)

    def open_settings_dialog(self):
        dialog = DeviceSettingsDialog(self)
        if dialog.exec_():
            configured_devices = dialog.configured_devices
            self.load_devices(configured_devices)

    def load_devices(self, configs):
        # Clear old cells
        for cell in self.devices:
            self.device_grid.removeWidget(cell)
            cell.deleteLater()
        self.devices.clear()

        # Create new cells
        for i, cfg in enumerate(configs):
            device_id = cfg["Device ID"]
            cell = DeviceCell(device_id)
            self.devices.append(cell)

            # place in grid (4 columns layout)
            row = i // 4
            col = i % 4
            self.device_grid.addWidget(cell, row, col)