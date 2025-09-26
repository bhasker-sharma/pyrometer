from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QGridLayout, QDialog, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox
)
from PyQt5.QtCore import Qt
from ui.setting import DeviceSettingsDialog
from ui.device_cell import DeviceCell


class MainWindow(QMainWindow):
    def __init__(self, config_db = None, readings_db = None):
        super().__init__()
        self.setWindowTitle("Pyrometer Software")
        self.setGeometry(100, 100, 1100, 600)

        self.config_db = config_db
        self.readings_db = readings_db
        
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

        self.load_devices()
        
    def init_navbar(self):
        navbar = QHBoxLayout()

        btn_settings = QPushButton("Settings")
        btn_settings.clicked.connect(self.open_settings_dialog)

        navbar.addStretch(1)  # pushes settings button to right
        navbar.addWidget(btn_settings)

        self.main_layout.addLayout(navbar)

    def open_settings_dialog(self):
        dialog = DeviceSettingsDialog(self, db =self.config_db)
        if dialog.exec_():
            self.load_devices()

    def load_devices(self):
        # Clear old cells
        for cell in self.devices:
            self.device_grid.removeWidget(cell)
            cell.deleteLater()
        self.devices.clear()

        # Remove any old placeholder widget
        if hasattr(self, "no_device_widget") and self.no_device_widget:
            self.device_grid.removeWidget(self.no_device_widget)
            self.no_device_widget.deleteLater()
            self.no_device_widget = None

        # Load configs directly from DB
        configs = self.config_db.get_all()
        enabled_configs = [row for row in configs if row[5]]  # row[5] = enabled column
        
        if not enabled_configs:

            self.no_device_widget = QWidget()
            layout = QVBoxLayout(self.no_device_widget)
            layout.setAlignment(Qt.AlignCenter)

            # Message
            message = QLabel("⚠ No devices configured yet.\nOpen Settings to add devices.")
            message.setAlignment(Qt.AlignCenter)
            message.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #666666;
                    padding: 15px;
                }
            """)

            # Button
            btn_add = QPushButton("➕ Add Device")
            btn_add.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    padding: 8px 16px;
                    color: white;
                    background-color: #0078D7;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #005A9E;
                }
            """)
            btn_add.clicked.connect(self.open_settings_dialog)

            layout.addWidget(message)
            layout.addWidget(btn_add)

            # Add placeholder widget spanning 4 columns
            self.device_grid.addWidget(self.no_device_widget, 0, 0, 1, 4)
            return

        # Otherwise create DeviceCells
        for i, row in enumerate(enabled_configs):

            cell = DeviceCell(row)
            self.devices.append(cell)

            # place in grid (4 columns layout)
            row_idx = i // 4
            col_idx = i % 4
            self.device_grid.addWidget(cell, row_idx, col_idx)