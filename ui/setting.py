from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QMessageBox, QWidget, QCheckBox
)
from PyQt5.QtCore import Qt


class DeviceSettingsDialog(QDialog):
    """Popup dialog for device settings"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Device Settings")
        self.setGeometry(150, 150, 700, 400)

        layout = QVBoxLayout(self)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Device Name", "Device ID", "Baud Rate", "Enable/Disable", "Action"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        layout.addWidget(self.table)

        # Add first row
        self.add_row()

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

    def add_row(self, name="Device", device_id="1", baud="9600", enabled=True):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(f"{name} {row+1}"))
        self.table.setItem(row, 1, QTableWidgetItem(device_id))
        self.table.setItem(row, 2, QTableWidgetItem(baud))

        # Enable/Disable checkbox (wrapped in QWidget for centering)
        checkbox = QCheckBox()
        checkbox.setChecked(enabled)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(checkbox)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table.setCellWidget(row, 3, container)

        # Action column (+ / -)
        btn_add = QPushButton("+")
        btn_add.clicked.connect(self.add_row)

        btn_remove = QPushButton("-")
        btn_remove.clicked.connect(lambda _, r=row: self.remove_row(r))

        action_layout = QHBoxLayout()
        action_layout.addWidget(btn_add)
        action_layout.addWidget(btn_remove)
        action_layout.setContentsMargins(0, 0, 0, 0)

        action_widget = QWidget()
        action_widget.setLayout(action_layout)
        self.table.setCellWidget(row, 4, action_widget)

    def remove_row(self, row):
        if self.table.rowCount() > 1:
            self.table.removeRow(row)

    def save(self):
        rows = self.table.rowCount()
        self.configured_devices = []
        for r in range(rows):
            device_name = self.table.item(r, 0).text()
            device_id = self.table.item(r, 1).text()
            baud_rate = self.table.item(r, 2).text()

            # Get checkbox inside the container widget
            container = self.table.cellWidget(r, 3)
            checkbox = container.findChild(QCheckBox) if container else None
            enabled = checkbox.isChecked() if checkbox else False

            row_data = {
                "Device Name": device_name,
                "Device ID": int(device_id) if device_id.isdigit() else device_id,
                "Baud Rate": baud_rate,
                "Enable/Disable": enabled
            }
            self.configured_devices.append(row_data)

        QMessageBox.information(self, "Saved", "Device settings saved successfully!")
        self.accept()
