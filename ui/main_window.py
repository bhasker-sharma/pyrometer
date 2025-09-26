from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt
from ui.setting import DeviceSettingsDialog
from ui.device_cell import DeviceCell
from ui.graph_section import GraphSection


class MainWindow(QMainWindow):
    def __init__(self, config_db=None, readings_db=None):
        super().__init__()
        self.setWindowTitle("Pyrometer Software")
        self.setGeometry(100, 100, 1100, 600)

        self.config_db = config_db
        self.readings_db = readings_db

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout (vertical stack)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Navbar
        self.init_navbar()

        # 🔹 Top section: Device Grid
        self.device_grid = QGridLayout()
        self.device_grid.setSpacing(10)
        self.devices = []
        self.max_devices = 16

        self.top_widget = QWidget()
        self.top_widget.setLayout(self.device_grid)
        self.main_layout.addWidget(self.top_widget, stretch=2)

        # 🔹 Divider line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(line)

        # 🔹 Bottom section: Graph / Logs (new widget)
        self.bottom_widget = GraphSection()
        self.main_layout.addWidget(self.bottom_widget, stretch=2)

        # Load devices from DB
        self.load_devices()

    def init_navbar(self):
        navbar = QHBoxLayout()

        btn_settings = QPushButton("Settings")
        btn_settings.clicked.connect(self.open_settings_dialog)

        navbar.addStretch(1)
        navbar.addWidget(btn_settings)

        self.main_layout.addLayout(navbar)

    def open_settings_dialog(self):
        dialog = DeviceSettingsDialog(self, db=self.config_db)
        if dialog.exec_():
            self.load_devices()

    def load_devices(self):
        """Reload device cells dynamically from DB"""
        # Clear old cells
        for cell in self.devices:
            self.device_grid.removeWidget(cell)
            cell.deleteLater()
        self.devices.clear()

        if hasattr(self, "no_device_widget") and self.no_device_widget:
            self.device_grid.removeWidget(self.no_device_widget)
            self.no_device_widget.deleteLater()
            self.no_device_widget = None

        configs = self.config_db.get_all()
        enabled_configs = [row for row in configs if row[5]]  # row[5] = enabled column

        if not enabled_configs:
            # 🔹 Show message + Add Device button
            self.no_device_widget = QWidget()
            layout = QVBoxLayout(self.no_device_widget)
            layout.setAlignment(Qt.AlignCenter)

            message = QLabel("⚠ No devices configured yet.\nOpen Settings to add devices.")
            message.setAlignment(Qt.AlignCenter)
            message.setStyleSheet("font-size: 16px; color: #666; padding: 15px;")

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

            self.device_grid.addWidget(self.no_device_widget, 0, 0, 1, 1)
            return

        device_count = len(enabled_configs)

        # 🔹 Decide grid size dynamically (square-ish layout)
        cols = int(device_count ** 0.5)  # start with sqrt for balance
        if cols * cols < device_count:
            cols += 1
        rows = (device_count + cols - 1) // cols  # ceil division

        # ✅ Clear old stretches
        for r in range(self.device_grid.rowCount()):
            self.device_grid.setRowStretch(r, 0)
        for c in range(self.device_grid.columnCount()):
            self.device_grid.setColumnStretch(c, 0)

        # 🔹 Add cells into grid
        for i, row in enumerate(enabled_configs[:self.max_devices]):
            cell = DeviceCell(row)
            self.devices.append(cell)

            r = i // cols
            c = i % cols
            self.device_grid.addWidget(cell, r, c)

        # 🔹 Make each row/col expand equally (fresh stretches)
        for r in range(rows):
            self.device_grid.setRowStretch(r, 1)
        for c in range(cols):
            self.device_grid.setColumnStretch(c, 1)
