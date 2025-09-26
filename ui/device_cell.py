from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

class DeviceCell(QFrame):
    """A single device cell showing name, id, baud, and temperature."""

    def __init__(self, device_row):
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
        self.setLineWidth(1)

        # ✅ Keep dynamic resizing
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(6)

        # 🔹 Header row: Centered Device Name + Dot
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(6)
        header_layout.setAlignment(Qt.AlignCenter)

        self.title = QLabel(f"{self.device_name}")
        self.title.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet("color: green; font-size: 14px;")

        header_layout.addWidget(self.title)
        header_layout.addWidget(self.status_dot)

        # 🔹 Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        # 🔹 Info row: ID and Baud rate
        self.id_label = QLabel(f"ID: {self.device_id}")
        self.id_label.setStyleSheet("font-size: 11px; color: #333;")
        self.baud_label = QLabel(f"Baud rate: {self.baud_rate}")
        self.baud_label.setStyleSheet("font-size: 11px; color: #333;")

        # 🔹 Temperature title
        self.temp_title = QLabel("Temp")
        self.temp_title.setAlignment(Qt.AlignCenter)
        self.temp_title.setStyleSheet("font-size: 12px; font-weight: bold;")

        # 🔹 Big temperature value
        self.temp_label = QLabel("25 °C")
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setStyleSheet("font-size: 28px; font-weight: bold;")

        # Add to layout
        main_layout.addWidget(header_widget)
        main_layout.addWidget(separator)
        main_layout.addWidget(self.id_label)
        main_layout.addWidget(self.baud_label)
        main_layout.addStretch(1)
        main_layout.addWidget(self.temp_title)
        main_layout.addWidget(self.temp_label)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def update_temp(self, value, status="OK"):
        """Update temperature dynamically."""
        self.temp_label.setText(f"{value:.1f} °C")
        if status == "OK":
            self.status_dot.setStyleSheet("color: green; font-size: 14px;")
        else:
            self.status_dot.setStyleSheet("color: red; font-size: 14px;")
