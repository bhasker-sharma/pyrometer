from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class DeviceCell(QFrame):
    """A single device cell showing temp, id, status."""
    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        self.init_ui()

    def init_ui(self):
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(2)
        self.setFixedSize(150, 100)

        layout = QVBoxLayout()

        self.title = QLabel(f"Device {self.device_id}")
        self.title.setAlignment(Qt.AlignCenter)
        self.temp_label = QLabel("Temp: -- °C")
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.status_label = QLabel("Status: --")
        self.status_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title)
        layout.addWidget(self.temp_label)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def update_temp(self, value, status="OK"):
        """Update temperature & status on the cell."""
        self.temp_label.setText(f"Temp: {value:.1f} °C")
        self.status_label.setText(f"Status: {status}")
