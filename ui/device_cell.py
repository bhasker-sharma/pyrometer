from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel,QSizePolicy
from PyQt5.QtCore import Qt

class DeviceCell(QFrame):
    """A single device cell showing name, id, and temperature placeholder."""
    def __init__(self, device_row):
        """
        device_row = (id, device_name, device_id, baud_rate, com_port, enabled)
        """
        super().__init__()
        (
            self.db_id,
            self.device_name,
            self.device_id,
            self.baud_rate,
            self.com_port,
            self.enabled
        ) = device_row

        self.init_ui()

    def init_ui(self):
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(2)
        self.setMinimumSize(150, 100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout()

        # Show Device Name (from DB)
        self.title = QLabel(self.device_name)
        self.title.setAlignment(Qt.AlignCenter)

        # Show Device ID (from DB)
        self.id_label = QLabel(f"ID: {self.device_id}")
        self.id_label.setAlignment(Qt.AlignCenter)

        # Show COM port & Baud (optional, useful for debugging)
        self.port_label = QLabel(f"{self.com_port} | {self.baud_rate}")
        self.port_label.setAlignment(Qt.AlignCenter)

        # Temperature placeholder (later updated from readings DB)
        self.temp_label = QLabel("Temp: -- °C")
        self.temp_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title)
        layout.addWidget(self.id_label)
        layout.addWidget(self.port_label)
        layout.addWidget(self.temp_label)

        self.setLayout(layout)

    def update_temp(self, value, status="OK"):
        """Update temperature (later with real readings)."""
        self.temp_label.setText(f"Temp: {value:.1f} °C")