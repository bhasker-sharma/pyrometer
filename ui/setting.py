from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QMessageBox, QWidget, QCheckBox,QLabel, QComboBox
)
from PyQt5.QtCore import Qt, QSize, QSize
from db.database import DeviceConfigDB


class DeviceSettingsDialog(QDialog):
    """Popup dialog for device settings"""
    def __init__(self, parent=None, db: DeviceConfigDB = None):
        super().__init__(parent)
        self.setWindowTitle("Device Settings")
        self.setGeometry(150, 150, 700, 400)

        self.db = db if db else DeviceConfigDB()

        layout = QVBoxLayout(self)

        # 🔹 COM Port selector row (above table)
        com_layout = QHBoxLayout()
        com_label = QLabel("COM Port:")
        self.combobox_comport = QComboBox()
        # Example COM ports, you can populate dynamically if needed
        self.combobox_comport.addItems(["COM1", "COM2", "COM3", "COM4"])
        com_layout.addWidget(com_label)
        com_layout.addWidget(self.combobox_comport)
        com_layout.addStretch(1)
        layout.addLayout(com_layout)


        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Device Name", "Device ID", "Baud Rate", "Enable/Disable", "Action"
        ])

        header = self.table.horizontalHeader()
        self.table.verticalHeader().setDefaultSectionSize(45)
        
        # Make all columns interactive for manual sizing
        header.setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)

        # Set initial column widths as percentages of the table width
        total_width = self.table.width() if self.table.width() > 0 else 700
        col_widths = [
            int(total_width * 0.30),  # Device Name (30%)
            int(total_width * 0.15),  # Device ID (15%)
            int(total_width * 0.15),  # Baud Rate (15%)
            int(total_width * 0.20),  # Enable/Disable (20%)
            int(total_width * 0.20),  # Action (20%)
        ]
        for i, w in enumerate(col_widths):
            self.table.setColumnWidth(i, w)

        self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        layout.addWidget(self.table, stretch=1)

        # Add first row
        self.load_from_db()

        # Save/Cancel buttons
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save")
        btn_cancel = QPushButton("Cancel")
        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addStretch(1)
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        total_width = self.table.viewport().width()
        col_widths = [
            int(total_width * 0.30),  # Device Name (30%)
            int(total_width * 0.15),  # Device ID (15%)
            int(total_width * 0.15),  # Baud Rate (15%)
            int(total_width * 0.20),  # Enable/Disable (20%)
            int(total_width * 0.20),  # Action (20%)
        ]
        for i, w in enumerate(col_widths):
            self.table.setColumnWidth(i, w)
         
    def load_from_db(self):
        """populate the settings table from db """
        self.table.setRowCount(0)  # clear any old rows

        configs = self.db.get_all()
        if configs:  # if DB has data
            for row in configs:
                _, name, device_id, baud_rate, com_port, enabled = row
                self.add_row(name, str(device_id), str(baud_rate), bool(enabled))
            # Set COM port dropdown to the first row’s com_port
            self.combobox_comport.setCurrentText(configs[0][4])
        else:
            # If no configs exist, show one default row
            self.add_row()
            
                         
    def add_row(self, name="Device", device_id="1", baud="9600", enabled=True):
        # ✅ Prevent more than 16 devices
        if self.table.rowCount() >= 16:
            QMessageBox.warning(self, "Limit Reached", 
                                "You can configure a maximum of 16 devices.")
            return
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(f"{name}"))
        self.table.setItem(row, 1, QTableWidgetItem(device_id))
        self.table.setItem(row, 2, QTableWidgetItem(baud))

        # Enable/Disable checkbox
        checkbox = QCheckBox()
        checkbox.setChecked(enabled)
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(checkbox)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.table.setCellWidget(row, 3, container)

        # Action column (+ / - small stacked buttons)
        btn_add = QPushButton("+")
        btn_add.setFixedSize(QSize(20, 20))
        btn_add.setStyleSheet("QPushButton { padding: 0; margin: 0; }")
        btn_add.clicked.connect(self.add_row)

        btn_remove = QPushButton("-")
        btn_remove.setFixedSize(QSize(20, 20))
        btn_remove.setStyleSheet("QPushButton { padding: 0; margin: 0; }")
        btn_remove.clicked.connect(lambda _, r=row: self.remove_row(r))

        action_layout = QVBoxLayout()
        action_layout.addWidget(btn_add)
        action_layout.addWidget(btn_remove)
        action_layout.setAlignment(Qt.AlignCenter)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(2)

        action_widget = QWidget()
        action_widget.setLayout(action_layout)
        self.table.setCellWidget(row, 4, action_widget)

    def remove_row(self, row):
        if self.table.rowCount() > 1:
            self.table.removeRow(row)

    def save(self):
        rows = self.table.rowCount()
        com_port = self.combobox_comport.currentText()
        
        self.db.clear()
        self.configured_devices = []
        
        for r in range(rows):
            device_name = self.table.item(r, 0).text()
            device_id = int(self.table.item(r, 1).text())
            baud_rate = int(self.table.item(r, 2).text())

            container = self.table.cellWidget(r, 3)
            checkbox = container.findChild(QCheckBox) if container else None
            enabled = checkbox.isChecked() if checkbox else False

            row_data = {
                "Device Name": device_name,
                "Device ID": device_id,
                "Baud Rate": baud_rate,
                "Com port": com_port,
                "Enable/Disable": enabled
            }
            self.configured_devices.append(row_data)

            self.db.add(device_name, device_id, baud_rate, com_port, enabled)

        QMessageBox.information(self, "Saved", "Device settings saved successfully!")
        self.accept()
