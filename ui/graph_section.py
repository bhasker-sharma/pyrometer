from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QCheckBox, QAbstractItemView, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor, QIcon
from db.database import DeviceConfigDB


def make_color_dot(color: str, size: int = 14) -> QPixmap:
    """Create a circular dot pixmap of given color."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QColor(color))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, size - 1, size - 1)
    painter.end()

    return pixmap


class GraphSection(QWidget):
    """Graph section divided vertically into 30% (logs/table) and 70% (graph)."""

    def __init__(self, parent=None, config_db: DeviceConfigDB = None):
        super().__init__(parent)
        self.config_db = config_db if config_db else DeviceConfigDB()

        # Main horizontal layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 🔹 Left panel (30%)
        self.left_panel = QWidget()
        self.left_panel.setStyleSheet("border: 1px solid #ccc; background-color: #f9f9f9;")
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(8, 8, 8, 8)
        left_layout.setSpacing(6)
        left_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Title
        left_layout.addWidget(QLabel("📋 Device Table"))

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Device", "Check", "Colour"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # prevent direct typing
        left_layout.addWidget(self.table)

        # 🔹 Divider line
        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("color: darkgrey;")

        # 🔹 Right panel (70%)
        self.right_panel = QWidget()
        self.right_panel.setStyleSheet("border: 1px solid #ccc;")
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(8, 8, 8, 8)
        right_layout.setSpacing(6)
        right_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        right_layout.addWidget(QLabel("📈 Graph Display"))

        # Add to layout with stretch factors
        main_layout.addWidget(self.left_panel, stretch=3)   # 30%
        main_layout.addWidget(divider)
        main_layout.addWidget(self.right_panel, stretch=7)  # 70%

        self.setLayout(main_layout)

        # Load data into the table
        self.load_enabled_devices()

    def load_enabled_devices(self):
        """Load only enabled devices from DB into the table."""
        configs = self.config_db.get_all()
        enabled_configs = [row for row in configs if row[5]]  # row[5] = enabled column

        self.table.setRowCount(0)  # clear existing

        # Predefined colors (cycle if > available)
        colors = ["red", "blue", "green", "orange", "purple", "brown", "pink", "cyan"]

        for i, row in enumerate(enabled_configs):
            _, name, device_id, baud_rate, com_port, enabled = row
            self.table.insertRow(i)

            # Device name
            item_device = QTableWidgetItem(name)
            self.table.setItem(i, 0, item_device)

            # Checkbox for "Check"
            checkbox = QCheckBox()
            checkbox.setChecked(False)
            self.table.setCellWidget(i, 1, checkbox)

            # Colour column (dot + label)
            color = colors[i % len(colors)]
            dot_item = QTableWidgetItem(color.capitalize())
            dot_item.setIcon(QIcon(make_color_dot(color)))  # ✅ fixed: wrap pixmap in QIcon
            self.table.setItem(i, 2, dot_item)
