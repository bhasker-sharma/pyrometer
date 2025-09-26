from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt


class GraphSection(QWidget):
    """Graph section divided vertically into 30% (logs) and 70% (graph)."""

    def __init__(self, parent=None):
        super().__init__(parent)

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
        left_layout.addWidget(QLabel("📋 Logs / Controls"))

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
