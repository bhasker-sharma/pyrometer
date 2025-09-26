from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap, QPainter, QFont


class DeviceCell(QFrame):
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
        self.setMinimumSize(100, 140)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(4)  # tighter spacing

        # ---------- Row 1: Bordered container for Name + Status Dot ----------
        top_frame = QFrame()
        top_frame.setFrameShape(QFrame.Box)
        top_frame.setLineWidth(1)
        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(5, 3, 5, 3)
        top_layout.setSpacing(8)
        top_layout.setAlignment(Qt.AlignCenter)

        self.title = QLabel(self.device_name)
        self.title.setFont(QFont("Arial", 10, QFont.Bold))

        self.status_dot = QLabel()
        self.status_dot.setFixedSize(14, 14)
        self.set_status_color("green")  # default

        top_layout.addWidget(self.title)
        top_layout.addStretch(1)  # spacer
        top_layout.addWidget(self.status_dot)

        # ---------- Row 2: Device ID + Port ----------
        mid_row = QHBoxLayout()
        mid_row.setSpacing(10)
        mid_row.setAlignment(Qt.AlignCenter)

        self.id_label = QLabel(f"ID: {self.device_id}")
        self.id_label.setFont(QFont("Arial", 9, QFont.Bold))

        self.port_label = QLabel(f"{self.com_port} | {self.baud_rate}")
        self.port_label.setFont(QFont("Arial", 9, QFont.Bold))

        mid_row.addWidget(self.id_label)
        # mid_row.addStretch(1)  # spacer
        mid_row.addWidget(self.port_label)
        
        # ---------- Row 3: Temperature label (smaller, compact) ----------
        self.temp_label = QLabel("Temp")
        self.temp_label.setFont(QFont("Arial", 9, QFont.Bold))
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setStyleSheet("font-size: 28px; font-weight: bold;")

        # ---------- Row 4: Big Bold Temperature Value (takes max space) ----------
        self.temp_value = QLabel("-- °C")
        self.temp_value.setAlignment(Qt.AlignCenter)
        self.temp_value.setFont(QFont("Arial", 22, QFont.Bold))  # bigger
        self.temp_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add everything to main layout
        main_layout.addWidget(top_frame)
        main_layout.addLayout(mid_row)
        main_layout.addWidget(self.temp_label)
        main_layout.addWidget(self.temp_value, stretch=1)  # ⬅️ takes extra space

        self.setLayout(main_layout)
        
    def set_status_color(self, color: str):
        """Set circular status dot color."""
        size = 14
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size-1, size-1)
        painter.end()

        self.status_dot.setPixmap(pixmap)

    def update_temp(self, value, status="OK"):
        self.temp_value.setText(f"{value:.1f} °C")
